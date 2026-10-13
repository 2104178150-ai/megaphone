#!/usr/bin/env python3
"""Check that the facts our channel playbooks rely on still appear on their sources.

Each entry pairs a playbook with a phrase from the platform's own page. If the phrase
disappears, the rule may have changed and the playbook needs a human (or agent) to
re-read the source. Standard library only.

    python3 scripts/check_sources.py            # human-readable
    python3 scripts/check_sources.py --json     # machine-readable

Exit code: 0 all found, 1 something missing or unreachable.
"""

import json
import sys
import urllib.error
import urllib.request

# (playbook, url, phrase that should still be on the page)
SOURCES = [
    ("hacker-news.md", "https://news.ycombinator.com/showhn.html", "ask friends to upvote"),
    ("lobsters.md", "https://lobste.rs/about", "less than a quarter"),
    ("product-hunt.md", "https://www.producthunt.com/launch", "12:01"),
    ("hellogithub.md", "https://raw.githubusercontent.com/521xueweihan/HelloGitHub/master/README.md", "每月 28 号"),
    ("ruanyf-weekly.md", "https://raw.githubusercontent.com/ruanyf/weekly/master/README.md", "周五发布"),
    ("ruanyf-weekly.md", "https://raw.githubusercontent.com/ruanyf/weekly/master/README.md", "提交 issue"),
    ("v2ex.md", "https://www.v2ex.com/go/create", "爱意满满的作品展示区"),
    ("v2ex.md", "https://www.v2ex.com/signup", "invite code"),
    ("newsletters.md", "https://raw.githubusercontent.com/rust-lang/this-week-in-rust/master/README.md", "drafts"),
    ("newsletters.md", "https://console.dev/selection-criteria", "hello@console.dev"),
    ("newsletters.md", "https://pycoders.com/submissions", "Submit Your Link"),
]

UA = "Mozilla/5.0 (Macintosh; megaphone source check)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main():
    as_json = "--json" in sys.argv
    pages = {}
    results = []
    for playbook, url, phrase in SOURCES:
        if url not in pages:
            try:
                pages[url] = fetch(url)
            except (urllib.error.URLError, OSError) as e:
                pages[url] = e
        page = pages[url]
        if isinstance(page, Exception):
            status = "unreachable"
            detail = str(page)
        else:
            status = "ok" if phrase in page else "missing"
            detail = ""
        results.append({"playbook": playbook, "url": url, "phrase": phrase, "status": status, "detail": detail})

    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            mark = {"ok": "✓", "missing": "✗", "unreachable": "?"}[r["status"]]
            print("%s %-18s %-26s %s %s" % (mark, r["playbook"], r["phrase"], r["url"], r["detail"]))
        bad = [r for r in results if r["status"] != "ok"]
        print("\n%d/%d sources still match." % (len(results) - len(bad), len(results)))
    sys.exit(0 if all(r["status"] == "ok" for r in results) else 1)


if __name__ == "__main__":
    main()
