"""Unscored Skill & plugin checks (SK1–SK3) in skills/launch-audit/scripts/audit.py.

The cases in tests/fixtures/skill-cases.json are shared so the web checker can match them later.
Run from the repo root:  python3 -m unittest discover -s tests
"""

import importlib.util
import json
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "audit", os.path.join(HERE, "..", "skills", "launch-audit", "scripts", "audit.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

with open(os.path.join(HERE, "fixtures", "skill-cases.json"), encoding="utf-8") as f:
    CASES = json.load(f)["cases"]


def with_skills(base, case):
    """A scored fixture repo plus one case's skills and plugin files (its README stays)."""
    data = dict(base)
    data.update({k: v for k, v in expand(case).items() if k != "readme"})
    return data


def expand(case):
    data = json.loads(json.dumps(case["data"]))
    if case.get("long_description"):
        for s in data["skills"]:
            s["text"] = s["text"].replace("LONG", "x" * case["long_description"])
    return data


class SkillChecksTest(unittest.TestCase):
    def test_shared_cases(self):
        for case in CASES:
            with self.subTest(case=case["name"]):
                out = audit.skill_checks(expand(case))
                if case["expected"] is None:
                    self.assertIsNone(out)
                else:
                    self.assertEqual({c["id"]: c["status"] for c in out}, case["expected"])

    def test_frontmatter_forms(self):
        fm = audit.skill_frontmatter
        self.assertIsNone(fm("# no frontmatter"))
        self.assertEqual(fm('---\nname: a\ndescription: "x: y # z"\n---\n')["description"], "x: y # z")
        self.assertEqual(fm("---\nname: a\ndescription: 'it''s'\n---\n")["description"], "it's")
        self.assertEqual(fm("---\nname: a # note\n---\n")["name"], "a")
        self.assertEqual(fm("---\ndescription: |\n  one\n  two\nname: b\n---\n"), {"description": "one\ntwo", "name": "b"})
        self.assertEqual(fm("﻿---\r\nname: c\r\n---\r\n")["name"], "c")

    def test_reviewer_edge_cases(self):
        fm = audit.skill_frontmatter
        wrapped = fm("---\nname: pdf\ndescription: Extract text from PDFs.\n  Use when the user mentions PDFs.\n---\n")
        self.assertEqual(wrapped["description"], "Extract text from PDFs. Use when the user mentions PDFs.")
        self.assertEqual(fm("---\ndescription: Does X. # note\n  Use when Y.\n---\n")["description"], "Does X. Use when Y.")
        when = audit.SKILL_WHEN_RE.search
        self.assertTrue(when("Activate when working with PDFs"))
        self.assertTrue(when("Invoke this skill when a deploy fails"))
        self.assertFalse(when("Generates DB triggers for Postgres"))
        # a SKILL.md we couldn't download is unknown, not broken
        out = audit.skill_checks({"readme": "npx skills add a/b", "skills": [{"path": "skills/x/SKILL.md", "text": None}]})
        self.assertEqual([c["status"] for c in out], ["unknown", "unknown", "pass"])
        # odd marketplace.json shapes never crash
        for market in ({"name": "m", "plugins": [{"name": ["x"]}]}, {"name": "m", "plugins": "x"}, ["m"]):
            out = audit.skill_checks({"readme": "/plugin marketplace add a/b\n/plugin install x@m", "marketplace": market, "pluginDir": True})
            self.assertEqual(out[-1]["id"], "SK3")
        out = audit.skill_checks({"readme": "", "skills": [{"path": "SKILL.md", "text": "---\nname: a\ndescription: Use when x\n---"}],
                                  "skillTotal": 30, "treeTruncated": True})
        self.assertIn("first 1 of 30", out[0]["evidence"])

    def test_description_says_what(self):
        # backlog K1d: Python-only until the web checker gets the same rule (K1d-web); then these move to skill-cases.json
        def sk2(*descs, names=None):
            names = names or ["s%d" % i for i in range(len(descs))]
            skills = [{"path": "skills/%s/SKILL.md" % n, "text": "---\nname: %s\ndescription: %s\n---\n" % (n, d)}
                      for n, d in zip(names, descs)]
            return audit.skill_checks({"readme": "npx skills add a/b", "skills": skills})[1]
        rule = "Use only when the user explicitly invokes {0} or asks for a {0} review by name. Never apply it on your own initiative."
        out = sk2(rule.format("comm-minto"), rule.format("cs-murphy"), names=["comm-minto", "cs-murphy"])
        self.assertEqual(out["status"], "fail")
        self.assertIn("2 skills (comm-minto, cs-murphy) say only when to call them", out["evidence"])
        self.assertIn("have the same description apart from the name", out["evidence"])
        out = sk2("Use only when invoked by name. Don\u2019t apply it on your own.")
        self.assertIn("s0 says only when to call it, not what it does", out["evidence"])
        same = "Review the {0} config. Use when the user says 检查配置."
        out = sk2(same.format("lint-a"), same.format("lint-b"), names=["lint-a", "lint-b"])
        self.assertIn("2 skills (lint-a, lint-b) have the same description apart from the name", out["evidence"])
        # what + when, and descriptions that differ in more than the name, pass
        for descs, names in (
                (("Deploy to Vercel. Use when the user says deploy to Vercel.",
                  "Deploy to Netlify. Use when the user says deploy to Netlify."), ["deploy-vercel", "deploy-netlify"]),
                (("Use when the user explicitly asks to deploy to Vercel.",), None),
                (("Use when the user invokes this skill to rename files in bulk.",), None),
                (("Write a Minto-style review of a draft. Use when the user asks for a Minto review by name.",), None),
                # reviewer cases: a "what" clause before a comma, "Only" that isn't a rule, a mirrored copy of one skill
                (("Use when the user invokes pdf-tools to merge or split PDF files.",), ["pdf-tools"]),
                (("Writes a Minto-style review, but use it only when the user asks for it by name.",), None),
                (("生成周报，仅在用户点名时使用。",), None),
                (("Only works on macOS; use when the user asks to clean Xcode caches.",), None),
                (("Only use this when the user asks to format Python code.",), None),
                (("Merge PDFs. Use when the user says merge PDFs.",) * 2, ["pdf", "pdf"])):
            with self.subTest(descs=descs):
                self.assertEqual(sk2(*descs, names=names)["status"], "pass")

    def test_score_is_unchanged(self):
        with open(os.path.join(HERE, "fixtures", "rubric-cases.json"), encoding="utf-8") as f:
            base = json.load(f)["cases"][0]["data"]
        plain = audit.analyze(base, 0)
        skilled = audit.analyze(with_skills(base, CASES[2]), 0)
        self.assertEqual(plain["score"], skilled["score"])
        self.assertIsNone(plain["skillChecks"])
        self.assertEqual(len(skilled["skillChecks"]), 3)

    def test_markdown_lists_the_section(self):
        with open(os.path.join(HERE, "fixtures", "rubric-cases.json"), encoding="utf-8") as f:
            base = json.load(f)["cases"][0]["data"]
        md = audit.to_markdown(audit.analyze(with_skills(base, CASES[3]), 0))
        self.assertIn("## Skill & plugin (not scored", md)
        self.assertIn("- n/a SK1 Valid frontmatter", md)
        self.assertIn("- [ ] SK3 Copy-paste install", md)


if __name__ == "__main__":
    unittest.main()
