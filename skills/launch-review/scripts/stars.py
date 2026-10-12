#!/usr/bin/env python3
"""Star history, traffic and launch attribution for a GitHub repo.

Standard library only, Python 3.8+.

    python3 stars.py OWNER/REPO [--days 30] [--log .megaphone/log.csv]
                     [--snapshot] [--snapshot-dir .megaphone/snapshots] [--out report.md]

Needs a token in GITHUB_TOKEN or GH_TOKEN: GitHub requires authentication to list
stargazers. Any token works for star history (e.g. `export GITHUB_TOKEN=$(gh auth token)`);
traffic data (views, referrers) additionally needs push access to the repo.
"""

import argparse
import csv
import json
import math
import os
import sys
import urllib.error
import urllib.request
from collections import Counter, OrderedDict
from datetime import datetime, timedelta, timezone

API = "https://api.github.com"
PER_PAGE = 100
MAX_PAGES = 400  # the stargazers endpoint stops paginating around 40k stars
WINDOW_HOURS = 48


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


def api_get(path, token, accept="application/vnd.github+json"):
    req = urllib.request.Request(API + path, headers={
        "Accept": accept,
        "User-Agent": "megaphone-launch-review",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            message = json.load(e).get("message", "")
        except Exception:
            message = ""
        if e.code == 403 and "rate limit" in message.lower():
            message += " (set GITHUB_TOKEN for a higher limit)"
        raise ApiError(e.code, message or e.reason)


def parse_time(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def recent_stars(repo, total, since, token, notes):
    """Walk the stargazer list from the newest page backwards until we pass `since`."""
    pages = math.ceil(total / PER_PAGE)
    if pages > MAX_PAGES:
        notes.append(
            "This repo has more stars than the stargazers API lists (~40k), so the newest "
            "stars can't be fetched with timestamps. Daily numbers below are incomplete."
        )
        pages = MAX_PAGES
    times = []
    for page in range(pages, 0, -1):
        batch = api_get(
            "/repos/%s/stargazers?per_page=%d&page=%d" % (repo, PER_PAGE, page),
            token, accept="application/vnd.github.star+json",
        )
        stamps = [parse_time(s["starred_at"]) for s in batch if s.get("starred_at")]
        times.extend(t for t in stamps if t >= since)
        if not stamps or min(stamps) < since:
            break
    return sorted(times)


def fetch_traffic(repo, token):
    out = {}
    for key, path in (
        ("views", "/traffic/views"),
        ("clones", "/traffic/clones"),
        ("referrers", "/traffic/popular/referrers"),
        ("paths", "/traffic/popular/paths"),
    ):
        out[key] = api_get("/repos/%s%s" % (repo, path), token)
    return out


def save_snapshot(directory, traffic):
    os.makedirs(directory, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = os.path.join(directory, stamp + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"taken_at": stamp, **traffic}, f, ensure_ascii=False, indent=2)
    return path


def load_snapshots(directory):
    snaps = []
    if not os.path.isdir(directory):
        return snaps
    for name in sorted(os.listdir(directory)):
        if name.endswith(".json"):
            try:
                with open(os.path.join(directory, name), encoding="utf-8") as f:
                    snaps.append(json.load(f))
            except (OSError, ValueError):
                pass
    return snaps


def daily_views(snapshots):
    """Merge per-day view counts from every snapshot (later snapshots win)."""
    days = {}
    for snap in snapshots:
        for v in (snap.get("views") or {}).get("views", []):
            days[v["timestamp"][:10]] = (v.get("count", 0), v.get("uniques", 0))
    return days


def read_log(path, local_tz):
    entries = []
    if not path or not os.path.exists(path):
        return entries
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            date = (row.get("date") or "").strip()
            if not date:
                continue
            clock = (row.get("time") or "").strip() or "00:00"
            try:
                local = datetime.strptime(date + " " + clock, "%Y-%m-%d %H:%M")
            except ValueError:
                print("skipping log row with unreadable date/time: %r" % row, file=sys.stderr)
                continue
            entries.append({
                "when": local.replace(tzinfo=local_tz).astimezone(timezone.utc),
                "channel": (row.get("channel") or "").strip() or "?",
                "url": (row.get("url") or "").strip(),
                "notes": (row.get("notes") or "").strip(),
            })
    return sorted(entries, key=lambda e: e["when"])


def parse_offset(s):
    sign = -1 if s.startswith("-") else 1
    h, _, m = s.lstrip("+-").partition(":")
    return timezone(sign * timedelta(hours=int(h), minutes=int(m or 0)))


def bar(n, top, width=36):
    if top <= 0 or n <= 0:
        return ""
    return "█" * max(1, round(n / top * width))


def build_report(args, repo_info, stars, since, log, traffic, snapshots, notes):
    lines = []
    total = repo_info.get("stargazers_count", 0)
    lines.append("# Launch review — %s" % args.repo)
    lines.append("")
    lines.append("Generated %s UTC · window: last %d days · total stars now: %d"
                 % (datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"), args.days, total))
    lines.append("")

    per_day = Counter(t.strftime("%Y-%m-%d") for t in stars)
    days = OrderedDict()
    d = since.date()
    today = datetime.now(timezone.utc).date()
    while d <= today:
        days[d.isoformat()] = per_day.get(d.isoformat(), 0)
        d += timedelta(days=1)

    gained = len(stars)
    best_day, best = max(days.items(), key=lambda kv: kv[1]) if days else ("-", 0)
    lines.append("## Summary")
    lines.append("")
    lines.append("- Stars gained in window: **%d**" % gained)
    if best:
        posted = [e["channel"] for e in log if e["when"].strftime("%Y-%m-%d") == best_day]
        lines.append("- Best day: **%s** with **%d** stars%s" % (
            best_day, best, (" (posted: %s)" % ", ".join(posted)) if posted else ""))
    lines.append("")

    lines.append("## Stars per day (UTC)")
    lines.append("")
    lines.append("```")
    marks = {}
    for e in log:
        marks.setdefault(e["when"].strftime("%Y-%m-%d"), []).append(e["channel"])
    for day, n in days.items():
        tag = ("  ← " + ", ".join(marks[day])) if day in marks else ""
        lines.append("%s │%-36s %4d%s" % (day, bar(n, best), n, tag))
    lines.append("```")
    lines.append("")

    if log:
        lines.append("## Per post (stars in the %d hours after posting)" % WINDOW_HOURS)
        lines.append("")
        lines.append("| Posted (UTC) | Channel | Stars in %dh | Link |" % WINDOW_HOURS)
        lines.append("|---|---|---|---|")
        for e in log:
            end = e["when"] + timedelta(hours=WINDOW_HOURS)
            n = sum(1 for t in stars if e["when"] <= t < end)
            overlap = [o["channel"] for o in log
                       if o is not e and e["when"] <= o["when"] < end]
            label = e["channel"] + (" (overlaps: %s)" % ", ".join(overlap) if overlap else "")
            lines.append("| %s | %s | %d | %s |" % (
                e["when"].strftime("%Y-%m-%d %H:%M"), label, n, e["url"] or "—"))
        lines.append("")

    views = daily_views(snapshots + ([{"views": traffic["views"]}] if traffic else []))
    if views:
        lines.append("## Views per day (from traffic snapshots)")
        lines.append("")
        lines.append("| Day | Views | Unique visitors |")
        lines.append("|---|---|---|")
        for day in sorted(views):
            if day >= since.strftime("%Y-%m-%d"):
                lines.append("| %s | %d | %d |" % (day, views[day][0], views[day][1]))
        lines.append("")

    latest = traffic or (snapshots[-1] if snapshots else None)
    if latest and latest.get("referrers"):
        lines.append("## Top referrers (GitHub keeps the last 14 days)")
        lines.append("")
        lines.append("| Referrer | Views | Unique |")
        lines.append("|---|---|---|")
        for r in latest["referrers"]:
            lines.append("| %s | %d | %d |" % (r["referrer"], r["count"], r["uniques"]))
        lines.append("")
    if latest and latest.get("paths"):
        lines.append("## Popular pages")
        lines.append("")
        for p in latest["paths"][:5]:
            lines.append("- %s — %d views" % (p["path"], p["count"]))
        lines.append("")

    if notes:
        lines.append("## Notes")
        lines.append("")
        lines.extend("- " + n for n in notes)
        lines.append("")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Star history, traffic and launch attribution for a GitHub repo.")
    p.add_argument("repo", help="OWNER/REPO")
    p.add_argument("--days", type=int, default=30, help="how many days back to look (default 30)")
    p.add_argument("--log", default=".megaphone/log.csv", help="launch log CSV: date,time,channel,url,notes")
    p.add_argument("--tz", help="timezone offset of the times in the log, e.g. +08:00 (default: this machine's)")
    p.add_argument("--snapshot", action="store_true", help="save today's traffic data (needs a token with push access)")
    p.add_argument("--snapshot-dir", default=".megaphone/snapshots")
    p.add_argument("--out", help="also write the report to this file")
    args = p.parse_args()

    if args.repo.count("/") != 1:
        p.error("repo must look like OWNER/REPO")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit(
            "GitHub requires authentication to list stargazers, so set a token first:\n"
            "  export GITHUB_TOKEN=$(gh auth token)      # if you use the GitHub CLI\n"
            "or create one at https://github.com/settings/personal-access-tokens\n"
            "(read-only public access is enough for stars; traffic needs push access)."
        )
    local_tz = parse_offset(args.tz) if args.tz else datetime.now().astimezone().tzinfo
    notes = []

    try:
        repo_info = api_get("/repos/" + args.repo, token)
    except ApiError as e:
        sys.exit("Couldn't read %s: %s %s" % (args.repo, e.status, e))

    since = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=args.days - 1)
    try:
        stars = recent_stars(args.repo, repo_info.get("stargazers_count", 0), since, token, notes)
    except ApiError as e:
        sys.exit("Couldn't read stargazers: %s %s" % (e.status, e))

    traffic = None
    try:
        traffic = fetch_traffic(args.repo, token)
    except ApiError as e:
        notes.append("Traffic data unavailable (%s): it needs a token with push access to the repo." % e.status)
    if args.snapshot:
        if traffic:
            notes.append("Saved traffic snapshot: %s" % save_snapshot(args.snapshot_dir, traffic))
        else:
            notes.append("--snapshot was requested but there was no traffic data to save.")

    log = read_log(args.log, local_tz)
    if not log:
        notes.append("No launch log found at %s, so posts aren't marked on the chart." % args.log)

    report = build_report(args, repo_info, stars, since, log, traffic,
                          load_snapshots(args.snapshot_dir), notes)
    print(report)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report + "\n")


if __name__ == "__main__":
    main()
