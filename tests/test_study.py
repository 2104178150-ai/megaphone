import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import study  # noqa: E402


class StudyTest(unittest.TestCase):
    def test_readme_language(self):
        self.assertEqual(study.readme_language("# Tool\n\nA small tool that turns notes into cards."), "latin")
        self.assertEqual(study.readme_language("# 工具\n\n把笔记变成卡片的小工具，支持 Markdown 和 PDF。"), "zh")
        self.assertEqual(study.readme_language("# Tool\n\n" + "Turns your notes into flashcards. " * 5 + "[简体中文](README.zh-CN.md)"), "latin")
        self.assertEqual(study.readme_language("```\n代码 code\n```"), "none")
        self.assertEqual(study.readme_language("# ツール\n\nメモをカードに変える小さなツールです。漢字も使います。ダウンロードしてください。"), "ja")
        both = "Turns your notes into flashcards and quizzes you on them. " * 4 + "把笔记变成卡片，按顺序复习，适合准备考试的学生使用。" * 2
        self.assertEqual(study.readme_language(both), "mixed")

    def test_skipped(self):
        self.assertTrue(study.skipped({"name": "awesome-agents", "description": ""}))
        self.assertTrue(study.skipped({"name": "cs101", "description": "Homework for the course"}))
        self.assertFalse(study.skipped({"name": "discourse-plugin", "description": "A resource finder"}))

    def test_fisher(self):
        self.assertAlmostEqual(study.fisher(3, 1, 1, 3), 0.4857, places=3)

    def test_looks_inflated(self):
        self.assertTrue(study.looks_inflated({"stargazers_count": 56, "forks_count": 0}))
        self.assertFalse(study.looks_inflated({"stargazers_count": 56, "forks_count": 3}))
        self.assertFalse(study.looks_inflated({"stargazers_count": 12, "forks_count": 0}))


if __name__ == "__main__":
    unittest.main()
