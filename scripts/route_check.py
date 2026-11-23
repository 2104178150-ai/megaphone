#!/usr/bin/env python3
"""Check which skill each request in tests/trigger_evals.json would fire.

  python3 scripts/route_check.py > prompt.txt         # prompt for a fresh agent (no expected answers in it)
  python3 scripts/route_check.py --score answers.txt  # compare the agent's "n | skill | ..." lines

The prompt holds only the skills' names and descriptions, exactly as an agent sees them, so the
agent routes blind. Standard library only.
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVALS = os.path.join(ROOT, "tests", "trigger_evals.json")

INSTRUCTIONS = (
    "You are acting as a skill router. Below are the ONLY skills installed (name + description), exactly as an "
    "agent sees them. For each numbered user request, answer which ONE skill you would load first, or 'none' if "
    "no skill fits (the agent would just answer normally). Judge only from the descriptions. Output one line per "
    "request: `n | skill | high/low | runner-up or -`. Then list any wording in the descriptions that made you hesitate."
)


def skills():
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
        text = open(path, encoding="utf-8").read().replace("\r\n", "\n")
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not m:
            sys.exit("%s: no frontmatter between --- lines" % os.path.relpath(path, ROOT))
        fields = dict(line.partition(": ")[::2] for line in m.group(1).split("\n"))
        try:
            out.append((fields["name"], json.loads(fields["description"])))
        except (KeyError, ValueError):
            sys.exit("%s: needs name and a double-quoted description (see tests/test_skill_frontmatter.py)" % os.path.relpath(path, ROOT))
    return out


def cases():
    return json.load(open(EVALS, encoding="utf-8"))["cases"]


def prompt():
    lines = [INSTRUCTIONS, "", "SKILLS:"]
    lines += ["- %s: %s" % s for s in skills()]
    lines += ["", "REQUESTS:"]
    lines += ["%d. %s" % (i, c["query"]) for i, c in enumerate(cases(), 1)]
    return "\n".join(lines)


def score(text):
    picked = {}
    for line in text.splitlines():
        m = re.match(r"\s*[`*|]*\s*(\d+)\.?[`*]*\s*\|\s*[`*]*([A-Za-z_-]+)[`*]*\s*(?:\||$)", line)
        if m:
            picked.setdefault(int(m.group(1)), m.group(2).lower())
    misses = []
    all_cases = cases()
    for i, c in enumerate(all_cases, 1):
        got = picked.get(i, "(no answer)")
        if got != c["expect"]:
            misses.append("%d. %s\n   expected %s, got %s" % (i, c["query"], c["expect"], got))
    print("%d / %d routed as expected" % (len(all_cases) - len(misses), len(all_cases)))
    for m in misses:
        print(m)
    return 1 if misses else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--score", metavar="FILE", help="the agent's answers, one 'n | skill | ...' line per request")
    args = ap.parse_args()
    if args.score:
        sys.exit(score(open(args.score, encoding="utf-8").read()))
    print(prompt())


if __name__ == "__main__":
    main()
