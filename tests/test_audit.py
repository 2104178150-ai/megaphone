"""Parity tests: skills/launch-audit/scripts/audit.py must score the shared cases exactly like
docs/checker.js (tests/checker.test.js checks the JS side against the same expectations).

Run from the repo root:  python3 -m unittest discover -s tests
"""

import importlib.util
import json
import os
import unittest
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "audit", os.path.join(HERE, "..", "skills", "launch-audit", "scripts", "audit.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

with open(os.path.join(HERE, "fixtures", "rubric-cases.json"), encoding="utf-8") as f:
    FIXTURES = json.load(f)
NOW_MS = datetime.strptime(FIXTURES["now"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp() * 1000


class ParityTest(unittest.TestCase):
    def test_rubric_adds_up(self):
        self.assertEqual(sum(r[2] for r in audit.RUBRIC), 100)
        for cid, mx, _ in audit.CATEGORIES:
            self.assertEqual(sum(r[2] for r in audit.RUBRIC if r[1] == cid), mx)

    def test_shared_cases_match_the_web_checker(self):
        for case in FIXTURES["cases"]:
            with self.subTest(case=case["name"]):
                a = audit.analyze(case["data"], NOW_MS)
                points = {c["id"]: c["points"] for c in a["checks"]}
                self.assertEqual(points, case["expected"]["points"])
                self.assertEqual(a["score"], case["expected"]["score"])

    def test_missing_licence_is_a_blocker_and_goes_first(self):
        case = json.loads(json.dumps(next(c for c in FIXTURES["cases"] if c["name"] == "good")))
        case["data"]["repo"]["license"] = None
        case["data"]["repo"]["homepage"] = ""
        case["data"]["repo"]["description"] = ""
        a = audit.analyze(case["data"], NOW_MS)
        self.assertEqual([f["id"] for f in a["fixes"]][:3], ["C1", "A1", "A6"])
        self.assertTrue(a["fixes"][0]["blocker"])
        self.assertFalse(a["fixes"][1].get("blocker"))
        self.assertIn("⚠️ Blocker: **License**", audit.to_markdown(a))

    def test_markdown_report_renders(self):
        a = audit.analyze(FIXTURES["cases"][0]["data"], NOW_MS)
        md = audit.to_markdown(a)
        self.assertIn("Score: 100/100", md)
        self.assertIn("- [x] A5", md)

    def test_logo_is_not_a_visual(self):
        f = audit.readme_facts('<img src="assets/brand.png" alt="Project logo" width="120">\n\n# X\n')
        self.assertIsNone(f["visual"])
        self.assertTrue(f["logo_only"])

class HumanCommitNoteTest(unittest.TestCase):
    """C2 evidence names the last non-bot commit; the score stays on pushed_at."""

    @staticmethod
    def commit(login, date, name="someone"):
        return {"author": {"login": login} if login else None,
                "commit": {"author": {"name": name, "date": date}, "committer": {"date": date}}}

    def test_skips_bots_and_keeps_the_score(self):
        case = json.loads(json.dumps(next(c for c in FIXTURES["cases"] if c["name"] == "good")))
        before = {c["id"]: c for c in audit.analyze(case["data"], NOW_MS)["checks"]}["C2"]
        case["data"]["commits"] = [
            self.commit("dependabot[bot]", "2026-05-02T10:00:00Z"),
            self.commit(None, "2026-05-01T09:00:00Z", name="renovate[bot]"),
            self.commit("alice", "2026-01-15T08:00:00Z"),
        ]
        after = {c["id"]: c for c in audit.analyze(case["data"], NOW_MS)["checks"]}["C2"]
        self.assertEqual(after["points"], before["points"])
        self.assertTrue(after["evidence"].endswith("(last human commit: 2026-01-15)"), after["evidence"])

    def test_only_bots(self):
        note = audit.human_commit_note([self.commit("dependabot[bot]", "2026-05-02T10:00:00Z")] * 30)
        self.assertEqual(note, " (no human commit in the last 30 commits)")

    def test_no_data_adds_nothing(self):
        self.assertEqual(audit.human_commit_note(None), "")
        self.assertEqual(audit.human_commit_note([]), "")
        self.assertEqual(audit.human_commit_note({"message": "Git Repository is empty."}), "")

    def test_odd_shapes_never_raise(self):
        odd = [{"author": "x", "commit": "y"}, {"author": {"login": 5}, "commit": {"author": {"name": None, "date": 7}}}, 3]
        self.assertEqual(audit.human_commit_note(odd), " (no human commit in the last 3 commits)")


if __name__ == "__main__":
    unittest.main()
