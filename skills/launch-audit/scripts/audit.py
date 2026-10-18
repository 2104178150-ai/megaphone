#!/usr/bin/env python3
"""Megaphone launch-readiness score for a GitHub repo — the same rubric as the web checker.

Standard library only, Python 3.8+.

    python3 audit.py OWNER/REPO                 # fetch from GitHub, print a Markdown report
    python3 audit.py OWNER/REPO --readme README.md   # score a local README draft instead
    python3 audit.py OWNER/REPO --json

GITHUB_TOKEN / GH_TOKEN is optional (raises the API limit from 60 to 5,000 requests an hour).

This is a line-by-line port of docs/checker.js (readmeFacts + analyze). The shared cases in
tests/fixtures/rubric-cases.json keep the two implementations in agreement — change both.
"""

import argparse
import base64
import http.client
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"

# ---------------------------------------------------------------------------
# Rubric

CATEGORIES = [
    ("A", 35, "First impression"),
    ("B", 25, "Time to wow"),
    ("C", 20, "Trust"),
    ("D", 20, "Shareability"),
]

RUBRIC = [
    ("A1", "A", 8, "Description (20–160 chars)", "launch-positioning",
     "Write a one-line description in the About box: what it is and who it's for, 20–160 characters."),
    ("A2", "A", 5, "At least 3 topics", None,
     "Add specific topics (language, category, use case) so topic pages and search can find you."),
    ("A3", "A", 3, "Title at the top of the README", "launch-readme",
     "Start the README with the project name as a heading."),
    ("A4", "A", 4, "Tagline near the top", "launch-readme",
     "Put a plain one-sentence tagline directly under the title: the outcome, for whom."),
    ("A5", "A", 8, "Screenshot, GIF or video in the first screen", "launch-readme",
     "Add a screenshot or a short GIF of the aha moment near the top. A logo is not a visual."),
    ("A6", "A", 4, "Demo or website link", None,
     "Set the Website field to a live demo or docs page (not the repo URL itself)."),
    ("A7", "A", 3, "README has substance (150+ words)", "launch-readme",
     "Explain what it does, how to use it and why it exists."),
    ("B1", "B", 7, "Getting-started section", "launch-readme",
     "Add a Quick start / Install section with the shortest path to a first result."),
    ("B2", "B", 5, "Code block early in the README", "launch-readme",
     "Show the install or usage command in a code block near the top."),
    ("B3", "B", 8, "One step to try it (command or website)", "launch-readme",
     "Offer a single command to try it, or a hosted version that needs no sign-up."),
    ("B4", "B", 5, "Shows what it does (features / examples)", "launch-readme",
     "Add a Features or Examples section, or three benefit bullets near the top."),
    ("C1", "C", 6, "License", None,
     "Add a LICENSE file. Without one, people can't legally use the code."),
    ("C2", "C", 4, "Recently active", None,
     "Push something before you launch — a stale last commit looks abandoned."),
    ("C3", "C", 4, "At least one release", None,
     "Publish a release (v0.1.0 is fine) with short notes."),
    ("C4", "C", 3, "Contributing guide", None,
     "Add CONTRIBUTING.md so visitors who want to help know how."),
    ("C5", "C", 3, "Issue templates", None,
     "Add issue templates for bugs and ideas."),
    ("D1", "D", 5, "Two languages", "launch-readme",
     "Add a translated README (e.g. README.zh-CN.md) to unlock channels in that language."),
    ("D2", "D", 4, "\"Why\" or comparison section", "launch-readme",
     "Add a short Why section: what people use today and why this is better for them."),
    ("D3", "D", 5, "Community channel", None,
     "Turn on Discussions or link a chat (Discord, Telegram, 微信群…)."),
    ("D4", "D", 3, "Badges", "launch-readme",
     "Add a row of meaningful badges (version, license, CI)."),
    ("D5", "D", 3, "Code of conduct", None,
     "Add CODE_OF_CONDUCT.md."),
]

CATEGORY_WEIGHT = {"A": 1.2, "B": 1.2, "C": 1.0, "D": 0.8}

LEVELS = [
    (90, "📣", "great", "Ready to launch"),
    (75, "🔊", "good", "Almost there"),
    (55, "🔉", "ok", "Needs polish"),
    (35, "🔈", "low", "Whispering"),
    (0, "🔇", "mute", "Muted"),
]


def level_for(score):
    for lvl in LEVELS:
        if score >= lvl[0]:
            return lvl
    return LEVELS[-1]


# ---------------------------------------------------------------------------
# README facts (mirrors readmeFacts in docs/checker.js)

A = re.ASCII
# JavaScript's \s (ECMAScript WhiteSpace + LineTerminator). Patterns compiled with re.ASCII keep
# JS's ASCII-only \b and \w, but their \s/\S must still match full-width spaces from Chinese
# IMEs (U+3000), NBSP and friends, as they do in the browser.
JS_WS = "\t\n\x0b\x0c\r \xa0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"


def jsre(pattern, flags=0):
    """Compile `pattern` with \s and \S meaning what they mean in JavaScript."""
    out, i, in_class = [], 0, False
    while i < len(pattern):
        c = pattern[i]
        if c == "\\" and i + 1 < len(pattern):
            nxt = pattern[i + 1]
            if nxt == "s":
                out.append(JS_WS if in_class else "[" + JS_WS + "]")
            elif nxt == "S":
                if in_class:
                    raise ValueError("\\S inside a character class isn't supported: " + pattern)
                out.append("[^" + JS_WS + "]")
            else:
                out.append(c + nxt)
            i += 2
            continue
        if c == "[" and not in_class:
            in_class = True
        elif c == "]" and in_class:
            in_class = False
        out.append(c)
        i += 1
    return re.compile("".join(out), flags)


BADGE_RE = re.compile(r"shields\.io|badgen\.net|badge|codecov|travis-ci|circleci|/workflows/", re.I)
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(\s*<?([^)\s>]+)")
HTML_MEDIA_RE = jsre(r"<(img|source|video)\b[^>]*>", re.I | A)
LOGO_RE = re.compile(r"logo|icon|avatar|favicon", re.I)
SMALL_PX = 128
ATTACHMENT_RE = re.compile(r"^\s*https://(?:github\.com/user-attachments/assets/|user-images\.githubusercontent\.com/)\S+\s*$")
HEADING_RE = jsre(r"^\s{0,3}#{1,6}\s+\S|^\s*<h[1-6]\b", re.I | A)
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")
CJK_RE = re.compile("[㐀-鿿豈-﫿]")
LATIN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*")

INSTALL_RES = [jsre(p, A) for p in [
    r"\bnpm\s+(?:i|install)\s+(?:-g\s+|--global\s+)?[@\w]",
    r"\bnpx\s+[@\w]",
    r"\bpnpm\s+(?:add|dlx)\s+\S",
    r"\byarn\s+(?:add|dlx|global\s+add)\s+\S",
    r"\bbun\s+(?:add|install|i|x|create)\s+[@\w]",
    r"\bbunx\s+[@\w]",
    r"\bpip3?\s+install\s+(?!-r\b)\S",
    r"\bpipx\s+(?:install|run)\s+\S",
    r"\buv\s+(?:tool\s+(?:install|run)|pip\s+install|add|run)\s+\S",
    r"\buvx\s+[@\w]",
    r"\bbrew\s+install\s+\S",
    r"\bport\s+install\s+\S",
    r"\bcargo\s+(?:install|add|binstall)\s+\S",
    r"\bgo\s+(?:install|get)\s+\S",
    r"\bdocker\s+(?:run|pull)\s+\S",
    r"\bdocker[\s-]compose\s+up\b",
    r"\b(?:curl|wget)\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba|z)?sh\b",
    r"\biwr\b[^\n|]*\|\s*iex\b",
    r"\bgem\s+install\s+\S",
    r"\bcomposer\s+(?:global\s+)?require\s+\S",
    r"\bdotnet\s+tool\s+install\s+\S",
    r"\b(?:winget|scoop|choco)\s+install\s+\S",
    r"\bapt(?:-get)?\s+install\s+\S",
    r"\b(?:snap|flatpak)\s+install\s+\S",
    r"\bnix\s+(?:run|profile\s+install|shell)\s+\S",
    r"\bhelm\s+install\s+\S",
    r"\bclaude\s+plugin\s+(?:install|marketplace\s+add)\s+\S",
    r"/plugin\s+(?:install|marketplace\s+add)\s+\S",
]]

GETTING_STARTED_RE = re.compile(r"install|quick ?start|getting started|get started|setup|set up|usage|how to use|run|安装|快速开始|快速上手|上手|开始使用|使用")
SHOWCASE_RE = re.compile(r"feature|usage|example|demo|screenshot|how it works|what it does|tutorial|walkthrough|tour|showcase|gallery|功能|特性|示例|例子|演示|截图|效果|教程")
WHY_RE = jsre(r"\bwhy\b|motivation|comparison|compare|\bvs\.?\b|alternative|difference|为什么|对比|比较|动机|初衷", A)
TRANSLATION_FILE_RE = re.compile(r"README[._-]?(zh|cn|en|ja|ko|es|fr|de|ru|pt|tw|hk)[\w-]*\.md", re.I | A)
TRANSLATION_LINK_RE = re.compile(r"\[(简体中文|中文|English|繁體中文|日本語)\]\(")
COMMUNITY_RE = re.compile(r"discord\.(gg|com/invite)|t\.me/|slack\.com|gitter\.im|matrix\.to|微信群|qq群|QQ群|telegram", re.I)
COMPOSE_RE = re.compile(r"docker(\s|-)compose|compose\.ya?ml", re.I)


def js_len(s):
    """String length the way JavaScript counts it (UTF-16 code units)."""
    return len(s.encode("utf-16-le")) // 2


def strip_inline(line):
    line = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", line)
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"<[^>]+>", " ", line)
    line = re.sub(r"[*_`~]", "", line)
    line = re.sub(r"^\s*>\s?", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def prose_of(text):
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\]\([^)]*\)", "] ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    return text


def attr(tag, name):
    m = jsre(r"\b%s\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))" % name, re.I | A).search(tag)
    if not m:
        return ""
    return next((g for g in m.groups() if g is not None), "")


def count_words(text):
    latin = len(LATIN_WORD_RE.findall(text))
    cjk = len(CJK_RE.findall(text))
    return {"latin": latin, "cjk": cjk, "total": latin + cjk // 2}


def _px(s):
    """A pixel size from a width/height attribute; percentages (width="100%") aren't pixels."""
    m = re.match(r"\s*(\d+)\s*(px)?\s*$", s or "", re.I)
    return int(m.group(1)) if m else 0


def readme_facts(md):
    text = (md or "")
    if text.startswith("\ufeff"):
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    in_fence = []
    open_ = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence.append(True)
            open_ = not open_
            continue
        in_fence.append(open_)

    non_empty = [i for i, l in enumerate(lines) if l.strip()]

    def media_in(start, end):
        found = []
        for l in lines[start:min(end, len(lines))]:
            for m in IMAGE_RE.finditer(l):
                found.append({"src": m.group(2), "alt": m.group(1), "video": False, "small": False})
            for m in HTML_MEDIA_RE.finditer(l):
                tag = m.group(0)
                w, h = _px(attr(tag, "width")), _px(attr(tag, "height"))
                found.append({
                    "src": attr(tag, "src"),
                    "alt": attr(tag, "alt"),
                    "video": m.group(1).lower() != "img",
                    "small": (0 < w <= SMALL_PX) or (0 < h <= SMALL_PX),
                })
            if ATTACHMENT_RE.match(l):
                found.append({"src": l.strip(), "alt": "", "video": True, "small": False})
        return [x for x in found if x["src"]]

    def is_badge(x):
        return bool(BADGE_RE.search(x["src"]))

    def is_logo(x):
        return not x["video"] and (x["small"] or bool(LOGO_RE.search(x["src"])) or bool(LOGO_RE.search(x["alt"])))

    headings = [
        {"i": i, "text": strip_inline(re.sub(r"^\s*#+\s*", "", l)).lower()}
        for i, l in enumerate(lines) if not in_fence[i] and HEADING_RE.search(l)
    ]

    title_at_top = any(not in_fence[i] and HEADING_RE.search(lines[i]) for i in non_empty[:15])

    tagline = None
    for i in non_empty[:25]:
        raw = lines[i]
        if in_fence[i] or HEADING_RE.search(raw) or FENCE_RE.match(raw):
            continue
        if re.match(r"^\s*([-*+]|\d+\.)\s", raw) or re.match(r"^\s*\|", raw):
            continue
        t = strip_inline(raw)
        if js_len(t) < 10 or js_len(t) > 200:
            continue
        w = count_words(t)
        if w["latin"] < 3 and w["cjk"] < 8:
            continue
        if re.match(r"^(english|简体中文|中文|繁體中文|日本語)(?![a-z])", t, re.I) and "|" in t:
            continue
        tagline = t
        break

    first_screen = media_in(0, 60)
    visual_item = next((x for x in first_screen if not is_badge(x) and not is_logo(x)), None)
    visual = visual_item["src"] if visual_item else None
    logo_only = not visual and any(not is_badge(x) and is_logo(x) for x in first_screen)
    badges = [x for x in media_in(0, 30) if is_badge(x)]

    fence_start = next((i for i, l in enumerate(lines) if FENCE_RE.match(l)), -1)
    install_line = next((l for l in lines if any(r.search(l) for r in INSTALL_RES)), None)

    def find_heading(rx, within=math.inf):
        return next((h for h in headings if h["i"] < within and rx.search(h["text"])), None)

    getting_started = find_heading(GETTING_STARTED_RE)
    showcase = find_heading(SHOWCASE_RE, 120)
    why = find_heading(WHY_RE)

    bullets = 0
    for i in range(min(80, len(lines))):
        if not in_fence[i] and re.match(r"^\s*[-*+]\s+\S", lines[i]) and not BADGE_RE.search(lines[i]):
            bullets += 1

    words = count_words(prose_of("\n".join(l for i, l in enumerate(lines) if not in_fence[i])))
    translation_link = bool(TRANSLATION_FILE_RE.search(text)) or bool(TRANSLATION_LINK_RE.search("\n".join(lines[:40])))
    # Inline bilingual = real prose in both languages, each at least a quarter of the words.
    latin_share = words["latin"] / words["total"] if words["total"] else 0
    inline_bilingual = words["cjk"] >= 30 and words["latin"] >= 80 and 0.25 <= latin_share <= 0.75
    bilingual = inline_bilingual or translation_link

    return {
        "empty": not text.strip(),
        "words": words,
        "title_at_top": title_at_top,
        "tagline": tagline,
        "visual": visual,
        "logo_only": logo_only,
        "badges": len(badges),
        "fence_start": fence_start,
        "install_line": install_line.strip() if install_line else None,
        "getting_started": getting_started,
        "showcase": showcase,
        "why": why,
        "bullets": bullets,
        "bilingual": bilingual,
        "translation_link": translation_link,
        "community_link": bool(COMMUNITY_RE.search(text)),
        "has_chinese": words["cjk"] >= 30,
        "has_english": words["latin"] >= 80,
        "mentions_compose": bool(COMPOSE_RE.search(text)),
    }


# ---------------------------------------------------------------------------
# Scoring (mirrors analyze in docs/checker.js)

def external_homepage(repo):
    url = (repo.get("homepage") or "").strip()
    if not url:
        return None
    bare = re.sub(r"^www\.", "", re.sub(r"^https?://", "", url.rstrip("/").lower()))
    return None if bare == ("github.com/" + (repo.get("full_name") or "")).lower() else url


def present(v):
    """JavaScript truthiness for API values: any object (even {}) counts, None/""/0/False don't."""
    return v is not None and v is not False and v != "" and v != 0


def _parse_iso(s):
    return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)


def analyze(data, now_ms=None):
    repo = data["repo"]
    f = readme_facts(data.get("readme") or "")
    files = ((data.get("community") or {}).get("files")) or {}
    desc = (repo.get("description") or "").strip()
    topics = repo.get("topics") or []
    releases = data.get("releases") or []
    now = now_ms if now_ms is not None else datetime.now(timezone.utc).timestamp() * 1000

    pts, ev = {}, {}

    def s(cid, points, evidence):
        pts[cid] = points
        ev[cid] = evidence

    s("A1", (4 if desc else 0) + (4 if 20 <= js_len(desc) <= 160 else 0),
      '%d chars: "%s"' % (js_len(desc), desc) if desc else "No description")
    s("A2", 5 if len(topics) >= 3 else 2 if topics else 0,
      "%d topics: %s" % (len(topics), ", ".join(topics)) if topics else "No topics")
    s("A3", 3 if f["title_at_top"] else 0, "Heading found at the top" if f["title_at_top"] else "No heading in the first 15 lines")
    s("A4", 4 if f["tagline"] else 0, '"%s"' % f["tagline"] if f["tagline"] else "No plain sentence near the top")
    s("A5", 8 if f["visual"] else 0,
      "Found a screenshot, GIF or video near the top" if f["visual"]
      else "Only a logo near the top — a logo isn't a picture of the product" if f["logo_only"]
      else "Only badges (or nothing) in the first 60 lines")
    site = external_homepage(repo)
    s("A6", 4 if site else 0, site if site else
      "Website field points back to the repo itself" if repo.get("homepage") else "Website field is empty")
    s("A7", 3 if f["words"]["total"] >= 150 else 0, "≈ %d words" % f["words"]["total"])

    s("B1", 7 if f["getting_started"] else 0,
      'Section: "%s"' % f["getting_started"]["text"] if f["getting_started"] else "No install / quick start heading")
    early = 0 <= f["fence_start"] < 150
    s("B2", 5 if early else 0, "First code block at line %d" % (f["fence_start"] + 1) if early else "No code block in the first 150 lines")
    s("B3", 8 if (f["install_line"] or site) else 0,
      "`%s`" % f["install_line"][:90] if f["install_line"]
      else "Try it online: %s" % site if site
      else "No one-line install/run command and no website to try it")
    shows = bool(f["showcase"]) or f["bullets"] >= 3
    s("B4", 5 if shows else 0,
      'Section: "%s"' % f["showcase"]["text"] if f["showcase"]
      else "%d bullet points near the top" % f["bullets"] if shows else "No features / examples section")

    lic = repo.get("license")
    s("C1", 6 if present(lic) else 0, (lic.get("spdx_id") or lic.get("name") or "license") if present(lic) else "No license detected")
    pushed = repo.get("pushed_at")
    age = (now - _parse_iso(pushed).timestamp() * 1000) / 86400000 if pushed else math.inf
    s("C2", 4 if age <= 90 else 2 if age <= 365 else 0,
      "Last push %d days ago" % round(age) if age != math.inf else "Unknown last push")
    s("C3", 4 if releases else 0, "Latest: %s" % releases[0].get("tag_name") if releases else "No releases")
    contributing = present(files.get("contributing"))
    s("C4", 3 if contributing else 0, "CONTRIBUTING found" if contributing else "No CONTRIBUTING file")
    templates = present(files.get("issue_template")) or present(data.get("issueTemplates"))
    s("C5", 3 if templates else 0, "Issue templates found" if templates else "No issue templates")

    s("D1", 5 if f["bilingual"] else 0,
      ("Links to a translated README" if f["translation_link"] else "Two languages in one README") if f["bilingual"]
      else ("Chinese only" if f["has_chinese"] else "One language only"))
    s("D2", 4 if f["why"] else 0, 'Section: "%s"' % f["why"]["text"] if f["why"] else "No \"why\" or comparison section")
    community = present(repo.get("has_discussions")) or f["community_link"]
    s("D3", 5 if community else 0,
      "Discussions enabled" if repo.get("has_discussions") else "Chat link in README" if f["community_link"] else "No Discussions or chat link")
    s("D4", 3 if f["badges"] else 0, "%d badge(s) near the top" % f["badges"])
    coc = present(files.get("code_of_conduct")) or present(files.get("code_of_conduct_file"))
    s("D5", 3 if coc else 0, "Code of conduct found" if coc else "No code of conduct")

    checks = []
    for cid, cat, mx, title, skill, fix in RUBRIC:
        checks.append({"id": cid, "cat": cat, "max": mx, "points": pts[cid], "pass": pts[cid] == mx,
                       "title": title, "skill": skill, "fix": fix, "evidence": ev[cid]})
    cats = []
    for cid, mx, name in CATEGORIES:
        cats.append({"id": cid, "max": mx, "name": name, "score": sum(c["points"] for c in checks if c["cat"] == cid)})
    score = sum(c["score"] for c in cats)
    fixes = sorted([c for c in checks if not c["pass"]],
                   key=lambda c: (-(c["max"] - c["points"]) * CATEGORY_WEIGHT[c["cat"]], c["id"]))
    lvl = level_for(score)
    return {"repo": repo.get("full_name"), "score": score,
            "level": {"emoji": lvl[1], "color": lvl[2], "name": lvl[3]},
            "categories": cats, "checks": checks, "fixes": fixes, "archived": bool(repo.get("archived"))}


# ---------------------------------------------------------------------------
# Fetching (mirrors fetchRepoData)

class FetchError(Exception):
    pass


class RateLimited(FetchError):
    """The API budget ran out. Never swallowed: a partial fetch would quietly cost points."""


def _get(url, token=None, accept="application/vnd.github+json", timeout=30):
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "megaphone-audit"})
    if token and url.startswith(API):
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _api(path, token, optional=False):
    try:
        return json.loads(_get(API + path, token))
    except urllib.error.HTTPError as e:
        if optional and e.code == 404:
            return None
        if e.code == 404:
            raise FetchError("Repository not found (private or misspelled?)")
        if e.code == 429 or (e.code == 403 and e.headers.get("x-ratelimit-remaining") == "0"):
            raise RateLimited("GitHub API rate limit reached (%d). Set GITHUB_TOKEN or wait an hour, then retry." % e.code)
        if e.code == 403:
            raise FetchError("GitHub refused %s (403)." % path)
        raise FetchError("GitHub returned %d for %s" % (e.code, path))
    except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError) as e:
        # timeouts, dropped connections and truncated bodies — common on slow links
        raise FetchError("network problem while reading %s: %s" % (path, e))


def fetch_repo_data(full_name, token=None):
    repo = _api("/repos/" + full_name, token)
    name = repo["full_name"]
    try:
        readme = _get("%s/%s/HEAD/README.md" % (RAW, name), timeout=4).decode("utf-8", "replace")
    except (urllib.error.URLError, http.client.HTTPException, OSError):
        readme = None
    if readme is None:
        j = _api("/repos/%s/readme" % name, token, optional=True)
        readme = base64.b64decode(j["content"]).decode("utf-8", "replace") if j and j.get("content") else ""
    try:
        community = _api("/repos/%s/community/profile" % name, token, optional=True)
    except RateLimited:
        raise
    except FetchError:
        community = None
    releases = _api("/repos/%s/releases?per_page=1" % name, token, optional=True) or []
    templates = bool(community and present((community.get("files") or {}).get("issue_template")))
    if not templates:
        try:
            d = _api("/repos/%s/contents/.github/ISSUE_TEMPLATE" % name, token, optional=True)
            templates = isinstance(d, list) and len(d) > 0
        except RateLimited:
            raise
        except FetchError:
            templates = False
    return {"repo": repo, "readme": readme, "community": community, "releases": releases, "issueTemplates": templates}


# ---------------------------------------------------------------------------
# Output

def to_markdown(a):
    lines = ["# Launch audit — %s" % a["repo"], "",
             "**Score: %d/100 · %s %s** (rubric only — add the human review and blockers on top)" % (
                 a["score"], a["level"]["emoji"], a["level"]["name"]), ""]
    if a["archived"]:
        lines += ["> ⚠️ This repo is archived.", ""]
    lines += ["| Category | Score |", "|---|---|"]
    lines += ["| %s | %d/%d |" % (c["name"], c["score"], c["max"]) for c in a["categories"]]
    lines += ["", "## Fix first (rubric)", ""]
    for n, c in enumerate(a["fixes"][:5], 1):
        hint = " — `%s` skill" % c["skill"] if c["skill"] else ""
        lines.append("%d. **%s** (+%d) — %s%s" % (n, c["title"], c["max"] - c["points"], c["fix"], hint))
    lines += ["", "## Rubric detail", ""]
    for c in a["checks"]:
        mark = "x" if c["pass"] else " "
        lines.append("- [%s] %s %s (%d/%d) — %s" % (mark, c["id"], c["title"], c["points"], c["max"], c["evidence"]))
    return "\n".join(lines)


def utf8_output():
    """Print UTF-8 even where the console or pipe defaults to cp1252 or GBK (Windows)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def main():
    utf8_output()
    p = argparse.ArgumentParser(description="Megaphone launch-readiness score (same rubric as the web checker).")
    p.add_argument("repo", help="OWNER/REPO")
    p.add_argument("--readme", help="score this local README file instead of the one on GitHub")
    p.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    args = p.parse_args()
    if args.repo.count("/") != 1:
        p.error("repo must look like OWNER/REPO")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    try:
        data = fetch_repo_data(args.repo, token)
    except (FetchError, urllib.error.URLError) as e:
        sys.exit("Couldn't read %s: %s" % (args.repo, e))
    if args.readme:
        with open(args.readme, encoding="utf-8-sig") as fh:
            data["readme"] = fh.read()
    a = analyze(data)
    if args.json:
        print(json.dumps(a, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(a))


if __name__ == "__main__":
    main()
