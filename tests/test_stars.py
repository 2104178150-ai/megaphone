"""Offline tests for skills/launch-review/scripts/stars.py (no network, no token needed).

Run from the repo root:  python3 -m unittest discover -s tests
"""

import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "skills", "launch-review", "scripts", "stars.py")

spec = importlib.util.spec_from_file_location("stars", SCRIPT)
stars = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stars)

NOW = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)


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
            if path.endswith("/views"):
                day = (NOW - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
                return {"count": 120, "uniques": 80, "views": [{"timestamp": day, "count": 120, "uniques": 80}]}
            if path.endswith("/clones"):
                return {"count": 3, "uniques": 2, "clones": []}
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


class StarsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.post_time = NOW - timedelta(days=3)
        # 250 old stars, a burst of 40 right after the post, and 5 a week earlier
        self.times = (
            [NOW - timedelta(days=400, minutes=i) for i in range(250)]
            + [self.post_time + timedelta(hours=1, minutes=i) for i in range(40)]
            + [NOW - timedelta(days=10, minutes=i) for i in range(5)]
        )
        self.log = os.path.join(self.tmp.name, "log.csv")
        with open(self.log, "w", encoding="utf-8") as f:
            f.write("date,time,channel,url,notes\n")
            f.write("%s,%s,Show HN,https://news.ycombinator.com/item?id=1,\n"
                    % (self.post_time.strftime("%Y-%m-%d"), self.post_time.strftime("%H:%M")))

    def test_counts_and_attribution(self):
        report = run_main(["acme/rocket", "--days", "14", "--log", self.log, "--tz", "+00:00",
                           "--snapshot-dir", os.path.join(self.tmp.name, "snaps")],
                          fake_github(self.times))
        self.assertIn("Stars gained in window: **45**", report)
        self.assertIn("| Show HN | 40 |", report)
        self.assertIn("← Show HN", report)
        self.assertIn("news.ycombinator.com", report)

    def test_log_timezone_shifts_attribution_window(self):
        # Logged as 08:00 at +08:00 = 00:00 UTC, i.e. before the burst: still inside 48h.
        with open(self.log, "w", encoding="utf-8") as f:
            f.write("date,time,channel,url,notes\n")
            f.write("%s,08:00,V2EX,,\n" % self.post_time.strftime("%Y-%m-%d"))
        report = run_main(["acme/rocket", "--days", "14", "--log", self.log, "--tz", "+08:00",
                           "--snapshot-dir", os.path.join(self.tmp.name, "snaps")],
                          fake_github(self.times))
        self.assertIn("| V2EX | 40 |", report)

    def test_snapshot_is_saved_and_merged(self):
        snaps = os.path.join(self.tmp.name, "snaps")
        run_main(["acme/rocket", "--log", self.log, "--snapshot", "--snapshot-dir", snaps],
                 fake_github(self.times))
        files = os.listdir(snaps)
        self.assertEqual(len(files), 1)
        with open(os.path.join(snaps, files[0]), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["referrers"][0]["referrer"], "news.ycombinator.com")
        report = run_main(["acme/rocket", "--log", self.log, "--snapshot-dir", snaps],
                          fake_github(self.times))
        self.assertIn("| 120 | 80 |", report)

    def test_traffic_without_push_access_is_a_note_not_a_crash(self):
        report = run_main(["acme/rocket", "--log", self.log,
                           "--snapshot-dir", os.path.join(self.tmp.name, "snaps")],
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
                           "--snapshot-dir", os.path.join(self.tmp.name, "snaps")], counting)
        pages = [c.split("page=")[-1] for c in calls if "stargazers" in c]
        self.assertEqual(pages, ["5", "4", "3"])
        self.assertIn("Stars gained in window: **160**", report)


if __name__ == "__main__":
    unittest.main()
