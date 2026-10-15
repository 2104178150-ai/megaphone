#!/usr/bin/env python3
"""Star history, traffic and launch attribution for a GitHub repo.

Standard library only, Python 3.8+ (IANA zone names such as Asia/Shanghai need 3.9+).

    python3 stars.py OWNER/REPO [--tz Asia/Shanghai] [--days 30] [--log .megaphone/log.csv]
                     [--snapshot] [--snapshot-dir .megaphone/snapshots] [--out report.md]

Run it from the root of the repo being reviewed: --log, --snapshot-dir and --out are
relative to the current directory. Pass --tz as the timezone the log's times were written
in; days in the report are counted in that zone too.

Needs a token in GITHUB_TOKEN or GH_TOKEN: GitHub only lists stargazers to authenticated
requests and is limiting that list to the repo's admins and collaborators (announced
June 2026), so use the maintainer's token (e.g. `export GITHUB_TOKEN=$(gh auth token)`).
Traffic data (views, clones, referrers, popular paths) needs push access to the repo.
"""

import argparse
import csv
import io
import json
import math
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter, OrderedDict
from datetime import datetime, time as dtime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # Python 3.9+
except ImportError:  # Python 3.8: --tz accepts offsets only
    ZoneInfo = None
    ZoneInfoNotFoundError = KeyError

API = "https://api.github.com"
PER_PAGE = 100
MAX_PAGES = 400  # the stargazers endpoint is commonly reported to stop paginating around 40k stars
WINDOW_HOURS = 48
OFFSET_RE = re.compile(r"^(?:UTC|GMT)?\s*([+-])?(\d{1,2})(?::?(\d{2}))?$", re.IGNORECASE)
TZ_EXAMPLES = "an IANA name like Asia/Shanghai or America/New_York, or an offset like +08:00 or -05:30"
STARGAZER_ACCESS = (
    "\nGitHub is limiting the stargazer list to the repo's admins and collaborators "
    "(announced June 2026), so use a token from an account with that access, "
    "usually the maintainer's."
)


class ApiError(Exception):
    def __init__(self, status, message, rate_limited=False):
        super().__init__(message)
        self.status = status
        self.rate_limited = rate_limited


def describe(err):
    return ("%s %s" % (err.status, err)) if err.status else str(err)


def _headers(headers):
    try:
        return {str(k).lower(): str(v).strip() for k, v in (headers or {}).items()}
    except AttributeError:
        return {}


def is_rate_limited(status, headers, message):
    h = _headers(headers)
    return status in (403, 429) and (
        h.get("x-ratelimit-remaining") == "0"
        or "retry-after" in h
        or "rate limit" in (message or "").lower()
    )


def rate_limit_hint(headers, now=None):
    """What to tell the user when GitHub says to slow down (a token is already in use)."""
    h = _headers(headers)
    retry = h.get("retry-after", "")
    if retry.isdigit():
        return "GitHub asks to wait %s seconds before retrying." % retry
    reset = h.get("x-ratelimit-reset", "")
    if reset.isdigit():
        at = datetime.fromtimestamp(int(reset), timezone.utc)
        now = now or datetime.now(timezone.utc)
        minutes = max(1, int(math.ceil((at - now).total_seconds() / 60)))
        return "The rate limit resets at %s UTC (in about %d min); wait and retry." % (
            at.strftime("%H:%M"), minutes)
    return "Wait a few minutes and retry."


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
        limited = is_rate_limited(e.code, e.headers, message)
        if limited:
            message = (message + ". " if message else "Rate limit reached. ") + rate_limit_hint(e.headers)
        raise ApiError(e.code, message or e.reason, rate_limited=limited)
    except (urllib.error.URLError, OSError) as e:
        raise ApiError(0, "network error: %s" % getattr(e, "reason", e))


def parse_time(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


# --- timezones -------------------------------------------------------------------------
# A zone is a tzinfo (ZoneInfo or a fixed offset) or None, meaning this machine's zone.
# ZoneInfo and the machine zone apply the UTC offset in force on each date (DST-aware).

def parse_offset(s):
    """'+08:00', '-05:30', '+8', '0800', 'UTC+8' -> fixed-offset tzinfo; None if not an offset."""
    m = OFFSET_RE.match(s.strip())
    if not m:
        return None
    sign, hours, minutes = m.group(1), int(m.group(2)), int(m.group(3) or 0)
    if hours > 14 or minutes > 59:
        raise argparse.ArgumentTypeError(
            "offset %r is out of range; real offsets run from -12:00 to +14:00" % s)
    delta = timedelta(hours=hours, minutes=minutes)
    return timezone(-delta if sign == "-" else delta)


def parse_tz(s):
    """argparse type for --tz: an IANA zone name or a UTC offset."""
    text = (s or "").strip()
    if text.upper() in ("UTC", "Z", "GMT"):
        return timezone.utc
    fixed = parse_offset(text)
    if fixed is not None:
        return fixed
    if ZoneInfo is None:
        raise argparse.ArgumentTypeError(
            "%r looks like a zone name, and zone names need Python 3.9+ (this is %d.%d). "
            "Use the UTC offset in force on your post dates instead, e.g. --tz +08:00."
            % (s, sys.version_info[0], sys.version_info[1]))
    try:
        return ZoneInfo(text)
    except (ZoneInfoNotFoundError, ValueError, OSError):
        raise argparse.ArgumentTypeError(
            "unknown timezone %r. Use %s. If this system has no zone database "
            "(some Windows installs), use an offset." % (s, TZ_EXAMPLES))


def join_tz_value(argv):
    """Let `--tz -05:30` work: argparse would read '-05:30' as an option, not a value."""
    out, i = [], 0
    while i < len(argv):
        if argv[i] == "--tz" and i + 1 < len(argv) and argv[i + 1].startswith("-") \
                and OFFSET_RE.match(argv[i + 1]):
            out.append("--tz=" + argv[i + 1])
            i += 2
        else:
            out.append(argv[i])
            i += 1
    return out


def tz_label(tz):
    if tz is None:
        return "this machine's local time (%s)" % datetime.now().astimezone().strftime("%Z, UTC%z")
    return getattr(tz, "key", None) or tz.tzname(None)


def to_utc(naive, tz):
    """A wall-clock time in `tz` as an aware UTC datetime."""
    if tz is None:
        return naive.astimezone(timezone.utc)  # naive = this machine's local time
    return naive.replace(tzinfo=tz).astimezone(timezone.utc)


def to_local(moment, tz):
    return moment.astimezone(tz)  # tz None = this machine's zone


# --- data ------------------------------------------------------------------------------

def stargazer_page(repo, page, token):
    return api_get(
        "/repos/%s/stargazers?per_page=%d&page=%d" % (repo, PER_PAGE, page),
        token, accept="application/vnd.github.star+json",
    )


def recent_stars(repo, total, since, token, notes):
    """Walk the stargazer list from the newest page backwards until we pass `since`."""
    pages = math.ceil(total / PER_PAGE)
    if pages > MAX_PAGES:
        notes.append(
            "This repo has more stars than the stargazers API is commonly reported to list "
            "(~40k), so the newest stars may lack timestamps. Daily numbers below may be "
            "incomplete."
        )
        pages = MAX_PAGES
    if not pages:
        return []
    # stargazers_count can run ahead of the list (a star removed since the /repos call, or
    # accounts GitHub counts but doesn't list) or behind it (a star added since), so the page
    # it points at may be empty, or may not be the newest one.
    page, batch = pages, stargazer_page(repo, pages, token)
    if not batch and page > 1 and stargazer_page(repo, 1, token):
        while not batch and page > 1:  # the list exists: step back to its real last page
            page -= 1
            batch = stargazer_page(repo, page, token)
    if not batch:
        notes.append(
            "GitHub returned an empty stargazer list although the repo has %d stars, so "
            "star numbers below are missing.%s" % (total, STARGAZER_ACCESS.replace("\n", " "))
        )
        return []
    while page >= pages and len(batch) == PER_PAGE and page < MAX_PAGES:
        newer = stargazer_page(repo, page + 1, token)  # stars added after the /repos call
        if not newer:
            break
        page, batch = page + 1, newer
    times = []
    while True:
        stamps = [parse_time(s["starred_at"]) for s in batch if s.get("starred_at")]
        times.extend(t for t in stamps if t >= since)
        if not stamps or min(stamps) < since or page == 1:
            break
        page -= 1
        batch = stargazer_page(repo, page, token)
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


def snapshot_name(repo, stamp):
    return "%s-%s.json" % (stamp, repo.replace("/", "__"))


def save_snapshot(directory, traffic, repo):
    os.makedirs(directory, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = os.path.join(directory, snapshot_name(repo, stamp))
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"repo": repo, "taken_at": stamp, **traffic}, f, ensure_ascii=False, indent=2)
    return path


def ignored_by_git(path):
    """True/False if git can tell whether `path` is ignored; None if git can't tell here."""
    try:
        r = subprocess.run(["git", "check-ignore", "-q", path], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return {0: True, 1: False}.get(r.returncode)


def load_snapshots(directory, repo=None, notes=None):
    """Snapshots for `repo`. Older snapshots without a repo name are included with a note;
    snapshots of other repos are skipped."""
    snaps, legacy, other = [], 0, 0
    if not os.path.isdir(directory):
        return snaps
    for name in sorted(os.listdir(directory)):
        if name.endswith(".json"):
            try:
                with open(os.path.join(directory, name), encoding="utf-8") as f:
                    snap = json.load(f)
            except (OSError, ValueError):
                continue
            if not isinstance(snap, dict):
                continue
            owner = snap.get("repo")
            if repo and owner and owner.lower() != repo.lower():
                other += 1
                continue
            if repo and not owner:
                legacy += 1
            snap.setdefault("taken_at", name[:10])
            snaps.append(snap)
    if notes is not None and other:
        notes.append("Ignored %d snapshot(s) in %s that belong to another repo." % (other, directory))
    if notes is not None and legacy:
        notes.append("%d older snapshot(s) in %s don't record which repo they're for; they were "
                     "counted as %s's." % (legacy, directory, repo))
    snaps.sort(key=lambda x: x.get("taken_at", ""))
    return snaps


def daily_traffic(snapshots, kind):
    """Merge per-day counts ('views' or 'clones') from every snapshot; later snapshots win.

    GitHub reports these per UTC day."""
    days = {}
    for snap in snapshots:
        for v in (snap.get(kind) or {}).get(kind) or []:
            days[v["timestamp"][:10]] = (v.get("count", 0), v.get("uniques", 0))
    return days


def read_log(path, tz, notes=None):
    """Parse the launch log. Returns (entries, skipped); skipped rows are reported in Notes,
    and anything else worth saying about the file is appended to `notes`.

    `date` is YYYY-MM-DD and `time` 24-hour HH:MM, both in `tz`. An empty time counts
    from the start of that day and is marked as not logged."""
    entries, skipped = [], []
    if not path or not os.path.exists(path):
        return entries, skipped
    with open(path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            # Excel on Chinese Windows saves "CSV" as GBK; GB18030 is a superset.
            text = raw.decode("gb18030")
            if notes is not None:
                notes.append("%s isn't UTF-8, so it was read as GB18030/GBK (how Excel on Chinese "
                             "Windows saves CSV). To be safe, save it as \"CSV UTF-8\"." % path)
        except UnicodeDecodeError:
            skipped.append("%s is neither UTF-8 nor GBK, so no row could be read (save it as "
                           "\"CSV UTF-8\")" % path)
            return entries, skipped
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames:
        reader.fieldnames = [(n or "").strip().lower() for n in reader.fieldnames]
    if "date" not in (reader.fieldnames or []):
        skipped.append("%s has no `date` column, so no row could be read. Its first line "
                       "must be the header date,time,channel,url,notes" % path)
        return entries, skipped
    for row in reader:
        def field(name):
            value = row.get(name)
            return value.strip() if isinstance(value, str) else ""

        date, clock = field("date"), field("time")
        channel = field("channel") or "?"
        where = "line %d (%s)" % (reader.line_num, channel)
        if not date:
            if any(isinstance(v, str) and v.strip() for v in row.values()):
                skipped.append("%s: no date" % where)
            continue
        try:
            local = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            skipped.append("%s: date %r isn't YYYY-MM-DD" % (where, date))
            continue
        if clock:
            parsed = None
            for fmt in ("%H:%M", "%H:%M:%S"):
                try:
                    parsed = datetime.strptime(clock, fmt)
                    break
                except ValueError:
                    pass
            if parsed is None:
                skipped.append("%s: time %r isn't 24-hour HH:MM" % (where, clock))
                continue
            local = local.replace(hour=parsed.hour, minute=parsed.minute)
        entries.append({
            "local": local,
            "when": to_utc(local, tz),
            "time_logged": bool(clock),
            "channel": channel,
            "url": field("url"),
            "notes": field("notes"),
        })
    return sorted(entries, key=lambda e: e["when"]), skipped


# --- report ----------------------------------------------------------------------------

def bar(n, top, width=36):
    if top <= 0 or n <= 0:
        return ""
    return "█" * max(1, round(n / top * width))


def describe_gap(gap):
    minutes = int(round(abs(gap.total_seconds()) / 60))
    if minutes == 0:
        return "same time"
    amount = ("%d min" % minutes) if minutes < 60 else ("%dh" % round(minutes / 60))
    return amount + (" later" if gap > timedelta(0) else " earlier")


def build_report(args, repo_info, stars, since, log, traffic, snapshots, notes, now=None):
    now = now or datetime.now(timezone.utc)
    tz = args.tz
    label = tz_label(tz)
    today_local = to_local(now, tz).date()
    lines = []
    total = repo_info.get("stargazers_count", 0)
    lines.append("# Launch review — %s" % args.repo)
    lines.append("")
    lines.append("Generated %s UTC · window: last %d days · total stars now: %d"
                 % (now.strftime("%Y-%m-%d %H:%M"), args.days, total))
    lines.append("")
    lines.append("Days and post times are in %s, the zone of the launch log. "
                 "GitHub's traffic numbers (views, clones) use UTC days." % label)
    lines.append("")

    per_day = Counter(to_local(t, tz).date().isoformat() for t in stars)
    days = OrderedDict()
    d = to_local(since, tz).date()
    while d <= today_local:
        days[d.isoformat()] = per_day.get(d.isoformat(), 0)
        d += timedelta(days=1)

    latest, latest_date = None, None
    if traffic:
        latest, latest_date = traffic, now.strftime("%Y-%m-%d")
    elif snapshots:
        latest, latest_date = snapshots[-1], snapshots[-1].get("taken_at", "?")

    gained = len(stars)
    best_day, best = max(days.items(), key=lambda kv: kv[1]) if days else ("-", 0)
    lines.append("## Summary")
    lines.append("")
    lines.append("- Stars gained in window: **%d**" % gained)
    if best:
        posted = [e["channel"] for e in log if e["local"].date().isoformat() == best_day]
        lines.append("- Best day (%s): **%s** with **%d** stars%s" % (
            label, best_day, best, (" (posted: %s)" % ", ".join(posted)) if posted else ""))
    if latest and (latest.get("views") or latest.get("clones")):
        v, c = latest.get("views") or {}, latest.get("clones") or {}
        lines.append("- Traffic in GitHub's last 14 days (as of %s): **%d** views (%d unique), "
                     "**%d** clones (%d unique)" % (latest_date, v.get("count", 0),
                                                    v.get("uniques", 0), c.get("count", 0),
                                                    c.get("uniques", 0)))
    lines.append("")

    lines.append("## Stars per day (%s)" % label)
    lines.append("")
    lines.append("```")
    marks = {}
    for e in log:
        marks.setdefault(e["local"].date().isoformat(), []).append(e["channel"])
    for day, n in days.items():
        tag = ("  ← " + ", ".join(marks[day])) if day in marks else ""
        lines.append("%s │%-36s %4d%s" % (day, bar(n, best), n, tag))
    lines.append("```")
    lines.append("")

    if log:
        window = timedelta(hours=WINDOW_HOURS)
        lines.append("## Per post (stars in the %d hours after posting)" % WINDOW_HOURS)
        lines.append("")
        lines.append("Posts less than %d hours apart share these stars; the Overlaps column "
                     "lists them in both directions." % WINDOW_HOURS)
        lines.append("")
        lines.append("| Posted (%s) | Channel | Stars in %dh | Overlaps | Link |"
                     % (label, WINDOW_HOURS))
        lines.append("|---|---|---|---|---|")
        for e in log:
            end = e["when"] + window
            n = sum(1 for t in stars if e["when"] <= t < end)
            if e["when"] < since:
                needed = (today_local - e["local"].date()).days + 1
                cell = "n/a (before the window; rerun with --days %d)" % needed
            elif e["when"] > now:
                cell = "— (future date)"
            elif end > now:
                cell = "%d so far" % n
            else:
                cell = "%d" % n
            overlaps = ["%s (%s)" % (o["channel"], describe_gap(o["when"] - e["when"]))
                        for o in log if o is not e and abs(o["when"] - e["when"]) < window]
            if e["time_logged"]:
                posted = e["local"].strftime("%Y-%m-%d %H:%M")
            else:
                posted = e["local"].strftime("%Y-%m-%d") + " (time not logged)"
            lines.append("| %s | %s | %s | %s | %s |" % (
                posted, e["channel"], cell, "; ".join(overlaps) or "—", e["url"] or "—"))
        lines.append("")

    sources = snapshots + ([traffic] if traffic else [])
    views, clones = daily_traffic(sources, "views"), daily_traffic(sources, "clones")
    first_day = since.strftime("%Y-%m-%d")
    shown = [day for day in sorted(set(views) | set(clones)) if day >= first_day]
    if shown:
        lines.append("## Views and clones per day (UTC days, merged from all snapshots)")
        lines.append("")
        lines.append("| Day (UTC) | Views | Unique visitors | Clones | Unique cloners |")
        lines.append("|---|---|---|---|---|")
        for day in shown:
            v, c = views.get(day), clones.get(day)
            lines.append("| %s | %s | %s | %s | %s |" % (
                day, v[0] if v else "—", v[1] if v else "—",
                c[0] if c else "—", c[1] if c else "—"))
        lines.append("")

    if latest and latest.get("referrers"):
        lines.append("## Top referrers, latest (%s: GitHub's top 10 for the 14 days before)"
                     % latest_date)
        lines.append("")
        lines.append("| Referrer | Views | Unique |")
        lines.append("|---|---|---|")
        for r in latest["referrers"]:
            lines.append("| %s | %d | %d |" % (r["referrer"], r["count"], r["uniques"]))
        lines.append("")
    if latest and latest.get("paths"):
        lines.append("## Popular pages, latest (%s)" % latest_date)
        lines.append("")
        for p in latest["paths"][:5]:
            lines.append("- %s — %d views (%d unique)" % (p["path"], p["count"], p.get("uniques", 0)))
        lines.append("")

    history = OrderedDict()
    for snap in snapshots:
        history[snap.get("taken_at", "?")] = snap
    if traffic:
        history[now.strftime("%Y-%m-%d")] = traffic
    if len(history) >= 2:
        lines.append("## Referrers by snapshot (each row is GitHub's 14-day top 10 on that date)")
        lines.append("")
        lines.append("Older rows keep early-launch referrers that have since left GitHub's "
                     "window. Rows overlap in time, so don't add them up.")
        lines.append("")
        lines.append("| Snapshot (UTC) | Referrers (views / unique) |")
        lines.append("|---|---|")
        for date, snap in history.items():
            refs = ", ".join("%s %d/%d" % (r["referrer"], r["count"], r["uniques"])
                             for r in snap.get("referrers") or []) or "—"
            lines.append("| %s | %s |" % (date, refs))
        lines.append("")
        lines.append("## Popular pages by snapshot (top 5 of each)")
        lines.append("")
        lines.append("| Snapshot (UTC) | Pages (views) |")
        lines.append("|---|---|")
        for date, snap in history.items():
            pages = ", ".join("%s %d" % (p["path"], p["count"])
                              for p in (snap.get("paths") or [])[:5]) or "—"
            lines.append("| %s | %s |" % (date, pages))
        lines.append("")

    if notes:
        lines.append("## Notes")
        lines.append("")
        lines.extend("- " + n for n in notes)
        lines.append("")
    return "\n".join(lines)


def utf8_output():
    """Print UTF-8 even where the console or pipe defaults to cp1252 or GBK (Windows)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def main(argv=None):
    utf8_output()
    argv = list(sys.argv[1:] if argv is None else argv)
    p = argparse.ArgumentParser(description="Star history, traffic and launch attribution for a GitHub repo.")
    p.add_argument("repo", help="OWNER/REPO")
    p.add_argument("--days", type=int, default=30, help="how many days back to look (default 30)")
    p.add_argument("--log", default=".megaphone/log.csv",
                   help="launch log CSV: date (YYYY-MM-DD),time (HH:MM, 24h),channel,url,notes")
    p.add_argument("--tz", type=parse_tz, metavar="ZONE",
                   help="timezone the log's times were written in, also used for days in the "
                        "report: an IANA name like Asia/Shanghai (Python 3.9+, DST-aware) or an "
                        "offset like +08:00 or -05:30 (default: this machine's zone)")
    p.add_argument("--snapshot", action="store_true",
                   help="save today's traffic data (needs a token with push access)")
    p.add_argument("--snapshot-dir", default=".megaphone/snapshots",
                   help="where snapshots are saved and read (default .megaphone/snapshots)")
    p.add_argument("--out", help="also write the report to this file")
    args = p.parse_args(join_tz_value(argv))

    if args.repo.count("/") != 1:
        p.error("repo must look like OWNER/REPO")
    if args.days < 1:
        p.error("--days must be 1 or more")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit(
            "GitHub requires authentication to list stargazers, so set a token first:\n"
            "  export GITHUB_TOKEN=$(gh auth token)      # if you use the GitHub CLI\n"
            "or create one at https://github.com/settings/personal-access-tokens/new\n"
            "(use the maintainer's account: GitHub is limiting the stargazer list to admins and\n"
            "collaborators; traffic needs push access)."
        )
    tz = args.tz
    notes = []
    now = datetime.now(timezone.utc)

    try:
        repo_info = api_get("/repos/" + args.repo, token)
    except ApiError as e:
        sys.exit("Couldn't read %s: %s" % (args.repo, describe(e)))

    first_day = to_local(now, tz).date() - timedelta(days=args.days - 1)
    since = to_utc(datetime.combine(first_day, dtime()), tz)
    try:
        stars = recent_stars(args.repo, repo_info.get("stargazers_count", 0), since, token, notes)
    except ApiError as e:
        hint = STARGAZER_ACCESS if e.status == 403 and not e.rate_limited else ""
        sys.exit("Couldn't read stargazers: %s%s" % (describe(e), hint))

    traffic = None
    try:
        traffic = fetch_traffic(args.repo, token)
    except ApiError as e:
        if e.rate_limited or e.status == 0:
            notes.append("Traffic data unavailable (%s)." % describe(e))
        else:
            notes.append("Traffic data unavailable (%s): it needs a token with push access to the "
                         "repo (for a fine-grained token, the Administration repository "
                         "permission, read)." % e.status)
    if args.snapshot:
        if traffic:
            path = save_snapshot(args.snapshot_dir, traffic, args.repo)
            notes.append("Saved traffic snapshot: %s" % path)
            if ignored_by_git(path) is False:
                notes.append("Warning: %s is not ignored by git. Snapshots hold traffic data that "
                             "GitHub shows only to people with push access; add `.megaphone/` to "
                             ".gitignore before committing." % path)
        else:
            notes.append("--snapshot was requested but there was no traffic data to save.")

    log, skipped = read_log(args.log, tz, notes)
    if not log and not skipped:
        notes.append("No launch log found at %s, so posts aren't marked on the chart." % args.log)
    for s in skipped:
        notes.append("Skipped log row, not attributed: %s." % s)
    if skipped:
        notes.append("Fix the skipped rows in %s (date YYYY-MM-DD, time HH:MM 24-hour) and rerun."
                     % args.log)
    if log and tz is None:
        notes.append("Log times were read as %s because --tz wasn't given. If they were written "
                     "in another zone, rerun with --tz (%s)." % (tz_label(None), TZ_EXAMPLES))

    report = build_report(args, repo_info, stars, since, log, traffic,
                          load_snapshots(args.snapshot_dir, args.repo, notes), notes, now=now)
    if args.out:  # write the file first, so a console that can't print the report doesn't lose it
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report + "\n")
    print(report)


if __name__ == "__main__":
    main()
