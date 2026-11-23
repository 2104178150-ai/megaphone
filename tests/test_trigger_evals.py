"""tests/trigger_evals.json stays usable: every case names a real skill (or "none"), every skill is
covered in English and Chinese, no duplicates, and route_check.py scores its own answer key as 100%."""
import contextlib
import glob
import io
import json
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import route_check  # noqa: E402

CJK = re.compile(r"[一-鿿]")


class TriggerEvalsTest(unittest.TestCase):
    def setUp(self):
        self.cases = json.load(open(os.path.join(ROOT, "tests", "trigger_evals.json"), encoding="utf-8"))["cases"]
        self.skills = {os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))}

    def test_expectations_name_real_skills(self):
        for c in self.cases:
            self.assertIn(c["expect"], self.skills | {"none"}, c["query"])

    def test_every_skill_covered_in_both_languages(self):
        for name in sorted(self.skills | {"none"}):
            queries = [c["query"] for c in self.cases if c["expect"] == name]
            with self.subTest(skill=name):
                self.assertTrue(any(CJK.search(q) for q in queries), "no Chinese request")
                self.assertTrue(any(not CJK.search(q) for q in queries), "no English request")

    def test_no_duplicate_queries(self):
        queries = [c["query"] for c in self.cases]
        self.assertEqual(len(queries), len(set(queries)))

    def test_prompt_is_blind_and_scorer_accepts_answer_key(self):
        prompt = route_check.prompt()
        self.assertNotIn('"expect"', prompt)
        for name in self.skills:
            self.assertIn("- %s: " % name, prompt)
        key = "\n".join("%d | %s | high | -" % (i, c["expect"]) for i, c in enumerate(self.cases, 1))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(route_check.score(key), 0)

    def test_scorer_reads_common_answer_formats(self):
        first = self.cases[0]["expect"]
        lines = ("1 | %s | high | -", "`1 | %s | high | -`", "1. | %s | low", "| 1 | `%s` | high |", "**1** | %s | high")
        for line in lines + ("1 | %s" % first.title(),):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                route_check.score(line % first if "%s" in line else line)
            self.assertTrue(out.getvalue().startswith("1 / "), line)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            route_check.score("1 | %s_extra | high" % first)  # a different name must not count
        self.assertTrue(out.getvalue().startswith("0 / "))


if __name__ == "__main__":
    unittest.main()
