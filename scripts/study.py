#!/usr/bin/env python3
"""Score a sample of new public GitHub repos with Megaphone's rubric and summarise the results.

Standard library only, Python 3.8+. Needs GITHUB_TOKEN or GH_TOKEN: about 5 API calls per repo,
so roughly 1,000 for a 200-repo sample.

    python3 scripts/study.py sample --created 2026-08-01..2026-09-30 --out .megaphone/research/study.jsonl
    python3 scripts/study.py report .megaphone/research/study.jsonl

`sample` searches repos created in the window, in four star bands, takes a seeded random
sample from each band and scores every repo with skills/launch-audit/scripts/audit.py. It
leaves out templates, lists and coursework, and repos with 20+ stars but no forks, and writes
how many it left out to `<out>.meta.json`. `report` prints the tables, including the 100+ vs
5–99 star comparison with Fisher exact p-values. Neither prints repo names: the point is the
pattern, not a public list of other people's projects. Keep the .jsonl out of git.
"""

import argparse
import json
import math
import os
import random
import re
import statistics
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "skills", "launch-audit", "scripts"))
import audit  # noqa: E402

BANDS = [("5–19", "5..19"), ("20–99", "20..99"), ("100–499", "100..499"), ("500+", ">=500")]
HIGH = ("100–499", "500+")
# Lists, notes and coursework aren't projects someone launches.
SKIP_NAME = re.compile(r"^awesome", re.I)
SKIP_WORDS = re.compile(r"\b(dotfiles|homework|leetcode|courses?|interview|cheat-?sheets?|tutorials?|study-notes)\b", re.I)
SCRIPTS = {"latin": r"[A-Za-z]", "han": r"[\u4e00-\u9fff]", "kana": r"[\u3040-\u30ff]",
           "hangul": r"[\uac00-\ud7af]", "cyrillic": r"[\u0400-\u04ff]"}


def readme_language(md):
    """Main script of the README's prose: latin, zh, mixed (a real Chinese part next to a
    Latin-script one), ja, ko, cyrillic or none."""
    text = re.sub(r"```.*?```|`[^`]*`|<[^>]+>|\]\([^)]*\)|https?://\S+", " ", md or "", flags=re.S)[:4000]
    n = {k: len(re.findall(v, text)) for k, v in SCRIPTS.items()}
    if n["kana"] >= 20:
        return "ja"
    if n["hangul"] >= 20:
        return "ko"
    if n["cyrillic"] >= 20 and n["cyrillic"] > n["latin"]:
        return "cyrillic"
    if not n["latin"] and not n["han"]:
        return "none"
    if n["han"] >= n["latin"] * 0.5:  # one Chinese character carries about as much as a short word
        return "zh"
    if n["han"] >= 30 and n["han"] >= n["latin"] * 0.1:
        return "mixed"
    return "latin"


def skipped(r):
    return (r.get("is_template") or SKIP_NAME.search(r["name"])
            or SKIP_WORDS.search(r["name"] + " " + (r.get("description") or "")))


def search(q, token, pages=3):
    items = []
    for page in range(1, pages + 1):
        path = "/search/repositories?" + urllib.parse.urlencode({"q": q, "sort": "updated", "per_page": 100, "page": page})
        batch = audit._api(path, token)["items"]
        items += batch
        if len(batch) < 100:
            break
    return items


def looks_inflated(r):
    """20+ stars and not one fork. Most such repos in our 2026-10 sample were look-alike
    'trainer' / 'mod' / 'vault' repos, which looks like star farming; we can't see who starred
    them, so this is a pattern, not proof."""
    return r["stargazers_count"] >= 20 and r["forks_count"] == 0


def score(name, band, stars, forks, created, token):
    data = audit.fetch_repo_data(name, token)
    a = audit.analyze(data)
    return {
        "repo": name, "band": band, "stars": stars, "forks": forks, "created": created, "score": a["score"],
        "lang": readme_language(data["readme"]), "readme_chars": len(data["readme"] or ""),
        "checks": {c["id"]: c["pass"] for c in a["checks"]},
        "titles": {c["id"]: c["title"] for c in a["checks"]},
    }


def sample(args, token):
    rng = random.Random(args.seed)
    done = []
    if os.path.exists(args.out):  # resume: keep what's scored, top each band up to --per-stratum
        with open(args.out, encoding="utf-8") as f:
            done = [json.loads(line) for line in f if line.strip()]
    seen = {r["repo"] for r in done}
    meta = {"created": args.created, "seed": args.seed, "per_stratum": args.per_stratum, "bands": {}}
    out = open(args.out, "a", encoding="utf-8")
    for band, stars in BANDS:
        q = "created:%s stars:%s fork:false archived:false is:public" % (args.created, stars)
        found = search(q, token)
        kept = [r for r in found if not skipped(r)]
        items = [r for r in kept if not looks_inflated(r)]
        meta["bands"][band] = {"search_results": len(found), "lists_or_coursework": len(found) - len(kept),
                               "stars_no_forks": len(kept) - len(items), "candidates": len(items)}
        rng.shuffle(items)
        need = args.per_stratum - sum(1 for r in done if r["band"] == band and r["readme_chars"] > 0)
        todo = [r for r in items if r["full_name"] not in seen]
        print("%s stars: %d candidates (%d left out with stars but no forks), %d to score"
              % (band, len(items), len(kept) - len(items), max(need, 0)), file=sys.stderr)
        with ThreadPoolExecutor(max_workers=8) as pool:
            while need > 0 and todo:
                batch, todo = todo[:need], todo[need:]
                futures = [pool.submit(score, r["full_name"], band, r["stargazers_count"], r["forks_count"],
                                       r["created_at"][:10], token)
                           for r in batch]
                for r, fut in zip(batch, futures):
                    try:
                        row = fut.result()
                    except audit.RateLimited:
                        sys.exit("rate limited; rerun later to continue")
                    except audit.FetchError as e:
                        print("skip %s: %s" % (r["full_name"], e), file=sys.stderr)
                        continue
                    out.write(json.dumps(row, ensure_ascii=False) + "\n")
                    out.flush()
                    seen.add(row["repo"])
                    if row["readme_chars"] > 0:  # a repo with no README doesn't fill a slot
                        need -= 1
    out.close()
    with open(args.out + ".meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)


def pct(xs):
    return "%d%%" % round(100.0 * sum(xs) / len(xs)) if xs else "—"


def fisher(a, b, c, d):
    """Two-sided Fisher exact test for the 2x2 table [[a, b], [c, d]]."""
    n, r1, c1 = a + b + c + d, a + b, a + c

    def p(x):
        return math.comb(r1, x) * math.comb(n - r1, c1 - x) / math.comb(n, c1)
    p0 = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, c1 - (n - r1)), min(r1, c1) + 1) if p(x) <= p0 * (1 + 1e-9)))


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda k: v[k])
        r, i = [0.0] * len(v), 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0
            i = j + 1
        return r
    x, y = ranks(xs), ranks(ys)
    mx, my = sum(x) / len(x), sum(y) / len(y)
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return cov / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))


def fmt_p(p):
    return "<0.001" if p < 0.001 else "%.3f" % p


def report(path):
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    with_readme = [r for r in rows if r["readme_chars"] > 0]
    titles = rows[0]["titles"]
    ids = list(titles)
    bands = [b for b, _ in BANDS]
    by = {b: [r for r in with_readme if r["band"] == b] for b in bands}
    high = [r for r in with_readme if r["band"] in HIGH]
    low = [r for r in with_readme if r["band"] not in HIGH]

    print("Repos scored: %d (%d with no README, left out below)" % (len(rows), len(rows) - len(with_readme)))
    if os.path.exists(path + ".meta.json"):
        meta = json.load(open(path + ".meta.json", encoding="utf-8"))
        print("Left out before sampling: " + "; ".join(
            "%s: %d lists or coursework, %d with stars but no forks, of %d results"
            % (b, m["lists_or_coursework"], m["stars_no_forks"], m["search_results"]) for b, m in meta["bands"].items()))
    rho = spearman([r["stars"] for r in with_readme], [r["score"] for r in with_readme])
    print("Spearman rho, score vs stars: %.2f (n = %d)\n" % (rho, len(with_readme)))

    print("| Stars | Repos | Median score | Share 80+ |")
    print("|---|---|---|---|")
    for b in bands + ["all"]:
        s = [r["score"] for r in (with_readme if b == "all" else by[b])]
        print("| %s | %d | %s | %s |" % (b, len(s), "%g" % statistics.median(s) if s else "—", pct([x >= 80 for x in s])))

    print("\n| Check | 100+ stars (%d) | 5–99 stars (%d) | p |" % (len(high), len(low)))
    print("|---|---|---|---|")
    rows_p = []
    for i in ids:
        a, c = sum(r["checks"][i] for r in high), sum(r["checks"][i] for r in low)
        rows_p.append((fisher(a, len(high) - a, c, len(low) - c), i))
    for p, i in sorted(rows_p):
        print("| %s %s | %s | %s | %s |" % (i, titles[i], pct([r["checks"][i] for r in high]),
                                          pct([r["checks"][i] for r in low]), fmt_p(p)))

    print("\n| Check | " + " | ".join(bands) + " |")
    print("|---|" + "---|" * len(bands))
    for i in sorted(ids):
        print("| %s %s | %s |" % (i, titles[i], " | ".join(pct([r["checks"][i] for r in by[b]]) for b in bands)))

    twin = next((i for i in ids if "language" in titles[i].lower()), None)
    print("\n| README language | Repos | Median score | Passes the two-languages check |")
    print("|---|---|---|---|")
    for lang in ("latin", "zh", "mixed", "ja", "ko", "cyrillic", "none"):
        g = [r for r in with_readme if r["lang"] == lang]
        if g:
            print("| %s | %d | %g | %s |" % (lang, len(g), statistics.median([r["score"] for r in g]),
                                            pct([r["checks"][twin] for r in g]) if twin else "—"))


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample")
    s.add_argument("--created", required=True, help="date range, e.g. 2026-08-01..2026-09-30")
    s.add_argument("--per-stratum", type=int, default=50)
    s.add_argument("--seed", type=int, default=1024)
    s.add_argument("--out", required=True)
    r = sub.add_parser("report")
    r.add_argument("path")
    args = p.parse_args()
    audit.utf8_output()
    if args.cmd == "report":
        report(args.path)
        return
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("Set GITHUB_TOKEN or GH_TOKEN: a 200-repo sample needs about 1,000 API calls.")
    sample(args, token)


if __name__ == "__main__":
    main()
