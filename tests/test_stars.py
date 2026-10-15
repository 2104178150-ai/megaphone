"""Offline tests for skills/launch-review/scripts/stars.py (no network, no token needed).

Run from the repo root:  python3 -m unittest discover -s tests
"""

import argparse
import contextlib
import email.message
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
import unittest
import urllib.error
from datetime import datetime, timedelta, timezone
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "skills", "launch-review", "scripts", "stars.py")

spec = importlib.util.spec_from_file_location("stars", SCRIPT)
stars = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stars)

NOW = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)


def zone_db_available():
    if stars.ZoneInfo is None:
        return False
    try:
        stars.ZoneInfo("America/New_York")
        return True
    except Exception:
        return False


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def fake_github(star_times, traffic_status=200):
    """Return an api_get replacement that serves a repo with the given star times."""
    star_times = sorted(star_times)

    def api_get(path, token, accept=None):
        if path.startswith("/repos/acme/rocket/stargazers"):
            query = dict(p.split("=") for p in path.split("?")[1].split("&"))
            page, per = int(query["page"]), int(query["per_page"])
            chunk = star_times[(page - 1) * per: page * per]
            return [{"starred_at": iso(t), "user": {"login": "u"}} for t in chunk]
        if path == "/repos/acme/rocket":
            return {"stargazers_count": len(star_times)}
        if "/traffic/" in path:
            if traffic_status != 200:
                raise stars.ApiError(traffic_status, "Must have push access")
            day = (NOW - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
            if path.endswith("/views"):
                return {"count": 120, "uniques": 80, "views": [{"timestamp": day, "count": 120, "uniques": 80}]}
            if path.endswith("/clones"):
                return {"count": 3, "uniques": 2, "clones": [{"timestamp": day, "count": 3, "uniques": 2}]}
            if path.endswith("/referrers"):
                return [{"referrer": "news.ycombinator.com", "count": 90, "uniques": 70}]
            if path.endswith("/paths"):
                return [{"path": "/acme/rocket", "title": "rocket", "count": 100, "uniques": 75}]
        raise AssertionError("unexpected request " + path)

    return api_get


def run_main(argv, api_get, env=None):
    out = io.StringIO()
    environ = {"GITHUB_TOKEN": "test-token"} if env is None else env
    with mock.patch.object(stars, "api_get", api_get), \
            mock.patch.object(sys, "argv", ["stars.py"] + argv), \
            mock.patch.dict(os.environ, environ, clear=True), \
            contextlib.redirect_stdout(out):
        stars.main()
    return out.getvalue()


def run_main_expecting_exit(argv, api_get):
    """Run main() and return (exit code, stderr) for a run that should stop early."""
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            run_main(argv, api_get)
        except SystemExit as e:
            return e.code, err.getvalue()
    raise AssertionError("main() didn't exit")


def section(report, heading):
    """The text of one '## heading' section."""
    return report.split("## " + heading, 1)[1].split("\n## ", 1)[0]


class StarsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.snaps = os.path.join(self.tmp.name, "snaps")
        self.post_time = NOW - timedelta(days=3)
        # 250 old stars, a burst of 40 right after the post, and 5 a week earlier
        self.times = (
            [NOW - timedelta(days=400, minutes=i) for i in range(250)]
            + [self.post_time + timedelta(hours=1, minutes=i) for i in range(40)]
            + [NOW - timedelta(days=10, minutes=i) for i in range(5)]
        )
        self.log = os.path.join(self.tmp.name, "log.csv")
        self.write_log("%s,%s,Show HN,https://news.ycombinator.com/item?id=1,"
                       % (self.post_time.strftime("%Y-%m-%d"), self.post_time.strftime("%H:%M")))

    def write_log(self, *rows):
        with open(self.log, "w", encoding="utf-8") as f:
            f.write("date,time,channel,url,notes\n")
            for row in rows:
                f.write(row + "\n")

    def test_counts_and_attribution(self):
        report = run_main(["acme/rocket", "--days", "14", "--log", self.log, "--tz", "+00:00",
                           "--snapshot-dir", self.snaps],
                          fake_github(self.times))
        self.assertIn("Stars gained in window: **45**", report)
        self.assertIn("| Show HN | 40 |", report)
        self.assertIn("← Show HN", report)
        self.assertIn("news.ycombinator.com", report)

    def test_log_timezone_shifts_attribution_window(self):
        # Logged as 08:00 at +08:00 = 00:00 UTC, i.e. before the burst: still inside 48h.
        self.write_log("%s,08:00,V2EX,," % self.post_time.strftime("%Y-%m-%d"))
        report = run_main(["acme/rocket", "--days", "14", "--log", self.log, "--tz", "+08:00",
                           "--snapshot-dir", self.snaps],
                          fake_github(self.times))
        self.assertIn("| V2EX | 40 |", report)

    def test_snapshot_is_saved_and_merged(self):
        run_main(["acme/rocket", "--log", self.log, "--snapshot", "--snapshot-dir", self.snaps],
                 fake_github(self.times))
        files = os.listdir(self.snaps)
        self.assertEqual(len(files), 1)
        with open(os.path.join(self.snaps, files[0]), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["referrers"][0]["referrer"], "news.ycombinator.com")
        report = run_main(["acme/rocket", "--log", self.log, "--snapshot-dir", self.snaps],
                          fake_github(self.times))
        self.assertIn("| 120 | 80 |", report)

    def test_traffic_without_push_access_is_a_note_not_a_crash(self):
        report = run_main(["acme/rocket", "--log", self.log, "--snapshot-dir", self.snaps],
                          fake_github(self.times, traffic_status=403))
        self.assertIn("Traffic data unavailable (403)", report)
        self.assertIn("Stars gained in window", report)

    def test_missing_token_exits_with_instructions(self):
        with self.assertRaises(SystemExit) as cm:
            run_main(["acme/rocket"], fake_github(self.times), env={})
        self.assertIn("GITHUB_TOKEN", str(cm.exception.code))

    def test_only_fetches_pages_it_needs(self):
        # 250 old + 160 recent = 410 stars = 5 pages. Pages 5 and 4 are all recent,
        # page 3 starts with old stars, so the walk stops there and never asks for 1–2.
        times = ([NOW - timedelta(days=400, minutes=i) for i in range(250)]
                 + [NOW - timedelta(days=2, minutes=i) for i in range(160)])
        calls = []
        inner = fake_github(times)

        def counting(path, token, accept=None):
            calls.append(path)
            return inner(path, token, accept)

        report = run_main(["acme/rocket", "--days", "14", "--log", self.log,
                           "--snapshot-dir", self.snaps], counting)
        pages = [c.split("page=")[-1] for c in calls if "stargazers" in c]
        self.assertEqual(pages, ["5", "4", "3"])
        self.assertIn("Stars gained in window: **160**", report)

    # --- timezones ---------------------------------------------------------------------

    def test_offsets_are_parsed(self):
        cases = {"+08:00": 8 * 60, "-05:30": -330, "+8": 8 * 60, "8": 8 * 60, "+0545": 345,
                 "UTC+8": 8 * 60, "UTC": 0, "Z": 0}
        for text, minutes in cases.items():
            with self.subTest(tz=text):
                tz = stars.parse_tz(text)
                self.assertEqual(tz.utcoffset(None), timedelta(minutes=minutes))

    @unittest.skipUnless(zone_db_available(), "needs Python 3.9+ zoneinfo with a zone database")
    def test_iana_zone_uses_the_offset_in_force_on_each_post_date(self):
        tz = stars.parse_tz("America/New_York")
        # EDT (UTC-4) in July, EST (UTC-5) in December; the US falls back on 2026-11-01.
        self.write_log("2026-07-01,12:00,Summer,,", "2026-12-01,12:00,Winter,,",
                       "2026-10-31,20:00,Before,,", "2026-11-01,20:00,After,,")
        entries, skipped = stars.read_log(self.log, tz)
        self.assertEqual(skipped, [])
        when = {e["channel"]: e["when"] for e in entries}
        self.assertEqual(when["Summer"], datetime(2026, 7, 1, 16, 0, tzinfo=timezone.utc))
        self.assertEqual(when["Winter"], datetime(2026, 12, 1, 17, 0, tzinfo=timezone.utc))
        self.assertEqual(when["After"] - when["Before"], timedelta(hours=25))
        self.assertEqual(stars.tz_label(tz), "America/New_York")

    @unittest.skipUnless(zone_db_available(), "needs Python 3.9+ zoneinfo with a zone database")
    def test_iana_zone_works_on_the_command_line(self):
        self.write_log("%s,08:00,V2EX,," % self.post_time.strftime("%Y-%m-%d"))
        report = run_main(["acme/rocket", "--days", "14", "--log", self.log,
                           "--tz", "Asia/Shanghai", "--snapshot-dir", self.snaps],
                          fake_github(self.times))
        self.assertIn("| V2EX | 40 |", report)
        self.assertIn("## Stars per day (Asia/Shanghai)", report)

    def test_invalid_tz_exits_cleanly(self):
        for bad in ("Mars/Olympus", "+25:00", "8pm"):
            with self.subTest(tz=bad):
                code, err = run_main_expecting_exit(
                    ["acme/rocket", "--log", self.log, "--tz", bad], fake_github(self.times))
                self.assertEqual(code, 2)
                self.assertIn("argument --tz", err)
                self.assertIn(bad, err)
                self.assertNotIn("Traceback", err)

    def test_zone_names_without_zoneinfo_ask_for_an_offset(self):
        with mock.patch.object(stars, "ZoneInfo", None):
            with self.assertRaises(argparse.ArgumentTypeError) as cm:
                stars.parse_tz("Asia/Shanghai")
            self.assertIn("Python 3.9", str(cm.exception))
            self.assertIn("--tz +08:00", str(cm.exception))
            self.assertEqual(stars.parse_tz("+08:00").utcoffset(None), timedelta(hours=8))

    def test_negative_offset_can_follow_a_space(self):
        report = run_main(["acme/rocket", "--days", "14", "--log", self.log, "--tz", "-05:30",
                           "--snapshot-dir", self.snaps], fake_github(self.times))
        self.assertIn("## Stars per day (UTC-05:30)", report)

    def test_days_are_bucketed_in_the_log_timezone(self):
        # One star at 20:00 UTC on day D is 04:00 on D+1 in UTC+08:00.
        day = (NOW - timedelta(days=3)).date()
        star = datetime(day.year, day.month, day.day, 20, 0, tzinfo=timezone.utc)
        times = [NOW - timedelta(days=400, minutes=i) for i in range(250)] + [star]
        no_log = os.path.join(self.tmp.name, "none.csv")
        for tz, label, expected in (("+08:00", "UTC+08:00", day + timedelta(days=1)),
                                    ("+00:00", "UTC", day)):
            with self.subTest(tz=tz):
                report = run_main(["acme/rocket", "--days", "14", "--log", no_log, "--tz", tz,
                                   "--snapshot-dir", self.snaps], fake_github(times))
                self.assertIn("- Best day (%s): **%s** with **1** stars" % (label, expected), report)
                self.assertIn("## Stars per day (%s)" % label, report)
                self.assertRegex(report, re.compile(r"^%s │█+\s+1$" % expected, re.M))

    # --- the launch log ----------------------------------------------------------------

    def test_skipped_rows_are_listed_in_notes(self):
        good = "%s,%s,Show HN,," % (self.post_time.strftime("%Y-%m-%d"),
                                     self.post_time.strftime("%H:%M"))
        self.write_log("2026/10/21,20:00,V2EX,,", "2026-10-21,8pm,Jike,,", good, ",,,,",
                       ",20:00,Lobsters,,")
        report = run_main(["acme/rocket", "--days", "14", "--log", self.log, "--tz", "+00:00",
                           "--snapshot-dir", self.snaps], fake_github(self.times))
        notes = section(report, "Notes")
        self.assertIn("line 2 (V2EX): date '2026/10/21' isn't YYYY-MM-DD", notes)
        self.assertIn("line 3 (Jike): time '8pm' isn't 24-hour HH:MM", notes)
        self.assertIn("line 6 (Lobsters): no date", notes)
        self.assertNotIn("line 5", notes)  # an empty row is not worth a note
        self.assertIn("Fix the skipped rows", notes)
        self.assertIn("| Show HN | 40 |", report)

    def test_overlaps_are_listed_in_both_directions(self):
        fmt = "%Y-%m-%d,%H:%M"
        self.write_log(
            "%s,Show HN,," % self.post_time.strftime(fmt),
            "%s,V2EX,," % (self.post_time + timedelta(hours=5)).strftime(fmt),
            "%s,Reddit,," % (self.post_time - timedelta(hours=60)).strftime(fmt),
        )
        report = run_main(["acme/rocket", "--days", "14", "--log", self.log, "--tz", "+00:00",
                           "--snapshot-dir", self.snaps], fake_github(self.times))
        self.assertIn("| Show HN | 40 | V2EX (5h later) |", report)
        self.assertIn("| V2EX | 0 | Show HN (5h earlier) |", report)
        self.assertIn("| Reddit | 0 | — |", report)

    def test_empty_time_counts_from_the_start_of_the_local_day(self):
        day = self.post_time.date()
        # 18:00 UTC the evening before is 02:00 on `day` in UTC+08:00: inside the window
        # only if the window starts at local midnight, not UTC midnight.
        early = datetime(day.year, day.month, day.day, tzinfo=timezone.utc) - timedelta(hours=6)
        times = [NOW - timedelta(days=400, minutes=i) for i in range(250)] + [early]
        self.write_log("%s,,Reddit,," % day.isoformat())
        report = run_main(["acme/rocket", "--days", "14", "--log", self.log, "--tz", "+08:00",
                           "--snapshot-dir", self.snaps], fake_github(times))
        self.assertIn("| %s (time not logged) | Reddit | 1 |" % day.isoformat(), report)
        self.assertRegex(report, re.compile(r"^%s │█+\s+1  ← Reddit$" % day.isoformat(), re.M))

    def test_machine_zone_default_is_flagged(self):
        report = run_main(["acme/rocket", "--days", "14", "--log", self.log,
                           "--snapshot-dir", self.snaps], fake_github(self.times))
        self.assertIn("because --tz wasn't given", section(report, "Notes"))

    # --- traffic -----------------------------------------------------------------------

    def test_clones_are_reported_with_views(self):
        report = run_main(["acme/rocket", "--log", self.log, "--tz", "+00:00",
                           "--snapshot-dir", self.snaps], fake_github(self.times))
        self.assertIn("**120** views (80 unique), **3** clones (2 unique)", report)
        self.assertIn("| 120 | 80 | 3 | 2 |", report)

    def test_referrer_history_keeps_older_snapshots(self):
        os.makedirs(self.snaps)
        old = (NOW - timedelta(days=12)).strftime("%Y-%m-%d")
        with open(os.path.join(self.snaps, old + ".json"), "w", encoding="utf-8") as f:
            json.dump({"taken_at": old,
                       "views": {"count": 900, "uniques": 700, "views": []},
                       "clones": {"count": 9, "uniques": 8, "clones": []},
                       "referrers": [{"referrer": "v2ex.com", "count": 50, "uniques": 40}],
                       "paths": [{"path": "/acme/rocket", "count": 400, "uniques": 300}]}, f)
        report = run_main(["acme/rocket", "--log", self.log, "--tz", "+00:00",
                           "--snapshot-dir", self.snaps], fake_github(self.times))
        latest = section(report, "Top referrers, latest")
        self.assertIn("news.ycombinator.com", latest)
        self.assertNotIn("v2ex.com", latest)
        history = section(report, "Referrers by snapshot")
        self.assertIn("| %s | v2ex.com 50/40 |" % old, history)
        self.assertIn("| %s | news.ycombinator.com 90/70 |" % NOW.strftime("%Y-%m-%d"), history)
        self.assertIn("/acme/rocket 400", section(report, "Popular pages by snapshot"))

    def test_snapshot_outside_gitignore_is_flagged(self):
        with mock.patch.object(stars, "ignored_by_git", return_value=False):
            report = run_main(["acme/rocket", "--log", self.log, "--tz", "+00:00", "--snapshot",
                               "--snapshot-dir", self.snaps], fake_github(self.times))
        self.assertIn("is not ignored by git", section(report, "Notes"))

    def test_empty_stargazer_list_is_explained(self):
        inner = fake_github(self.times)

        def hidden(path, token, accept=None):
            return [] if "/stargazers" in path else inner(path, token, accept)

        report = run_main(["acme/rocket", "--log", self.log, "--tz", "+00:00",
                           "--snapshot-dir", self.snaps], hidden)
        self.assertIn("empty stargazer list", section(report, "Notes"))
        self.assertIn("admins and collaborators", section(report, "Notes"))

    # --- rate limits -------------------------------------------------------------------

    def test_rate_limit_hint_says_when_to_retry(self):
        now = datetime(2026, 10, 14, 12, 0, tzinfo=timezone.utc)
        reset = str(int((now + timedelta(minutes=10)).timestamp()))
        self.assertEqual(stars.rate_limit_hint({"X-RateLimit-Reset": reset}, now=now),
                         "The rate limit resets at 12:10 UTC (in about 10 min); wait and retry.")
        self.assertIn("60 seconds", stars.rate_limit_hint({"Retry-After": "60"}))
        self.assertEqual(stars.rate_limit_hint({}), "Wait a few minutes and retry.")

    def test_rate_limited_request_does_not_suggest_setting_a_token(self):
        headers = email.message.Message()
        headers["X-RateLimit-Remaining"] = "0"
        headers["X-RateLimit-Reset"] = str(int((NOW + timedelta(hours=1)).timestamp()))
        body = io.BytesIO(json.dumps({"message": "API rate limit exceeded"}).encode())
        error = urllib.error.HTTPError("https://api.github.com/x", 403, "Forbidden", headers, body)
        with mock.patch.object(stars.urllib.request, "urlopen", side_effect=error):
            with self.assertRaises(stars.ApiError) as cm:
                stars.api_get("/repos/acme/rocket", "test-token")
        self.assertTrue(cm.exception.rate_limited)
        self.assertIn("resets at", str(cm.exception))
        self.assertNotIn("GITHUB_TOKEN", str(cm.exception))


def with_count(api_get, count):
    """Wrap a fake so /repos reports `count` stars regardless of how many are listed."""
    def wrapped(path, token, accept=None):
        if path == "/repos/acme/rocket":
            return {"stargazers_count": count}
        return api_get(path, token, accept)
    return wrapped


class EdgeCaseTest(unittest.TestCase):
    """Cases found in review: count/list races, GBK logs, snapshots of other repos."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.snaps = os.path.join(self.tmp.name, "snaps")
        self.log = os.path.join(self.tmp.name, "log.csv")
        # 150 old stars and 50 in the last three days: exactly two full pages
        self.times = ([NOW - timedelta(days=400, minutes=i) for i in range(150)]
                      + [NOW - timedelta(days=2, minutes=i) for i in range(50)])

    def run_with(self, api_get, *extra):
        return run_main(["acme/rocket", "--days", "14", "--tz", "+00:00", "--log", self.log,
                         "--snapshot-dir", self.snaps] + list(extra), api_get)

    def test_count_ahead_of_list_across_a_page_boundary(self):
        # Someone unstarred between the two calls (or GitHub counts hidden accounts).
        report = self.run_with(with_count(fake_github(self.times), 201))
        self.assertIn("Stars gained in window: **50**", report)
        self.assertNotIn("empty stargazer list", report)

    def test_count_far_ahead_of_list(self):
        report = self.run_with(with_count(fake_github(self.times), 350))
        self.assertIn("Stars gained in window: **50**", report)

    def test_count_behind_list_still_reads_the_newest_page(self):
        times = self.times + [NOW - timedelta(hours=1)]  # a star added after the /repos call
        report = self.run_with(with_count(fake_github(times), 200))
        self.assertIn("Stars gained in window: **51**", report)

    def test_gbk_log_from_excel_is_read(self):
        day = (NOW - timedelta(days=2)).strftime("%Y-%m-%d")
        with open(self.log, "wb") as f:
            f.write(("date,time,channel,url,notes\n%s,09:00,即刻,https://okjike.com/x,\n" % day).encode("gbk"))
        report = self.run_with(fake_github(self.times))
        self.assertIn("即刻", section(report, "Per post"))
        self.assertIn("read as GB18030/GBK", section(report, "Notes"))
        self.assertNotIn("Skipped log row", report)

    def test_snapshots_of_other_repos_are_ignored(self):
        os.makedirs(self.snaps)
        other = (NOW - timedelta(days=3)).strftime("%Y-%m-%d")
        with open(os.path.join(self.snaps, "%s-acme__other.json" % other), "w", encoding="utf-8") as f:
            json.dump({"repo": "acme/other", "taken_at": other,
                       "views": {"views": [{"timestamp": other + "T00:00:00Z", "count": 999, "uniques": 1}]},
                       "referrers": [{"referrer": "elsewhere.example", "count": 5, "uniques": 5}]}, f)
        report = self.run_with(fake_github(self.times), "--snapshot")
        self.assertNotIn("999", report)
        self.assertNotIn("elsewhere.example", report)
        self.assertIn("belong to another repo", section(report, "Notes"))
        saved = [n for n in os.listdir(self.snaps) if n.endswith("acme__rocket.json")]
        self.assertEqual(len(saved), 1)
        with open(os.path.join(self.snaps, saved[0]), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["repo"], "acme/rocket")

    def test_out_file_is_written(self):
        out = os.path.join(self.tmp.name, "nested", "report.md")
        report = self.run_with(fake_github(self.times), "--out", out)
        with open(out, encoding="utf-8") as f:
            self.assertEqual(f.read().strip(), report.strip())


if __name__ == "__main__":
    unittest.main()
