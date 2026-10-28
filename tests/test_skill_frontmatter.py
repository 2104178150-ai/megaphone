"""Every SKILL.md must have frontmatter that strict YAML parsers accept.

A plain (unquoted) YAML scalar breaks on ": " or " #", which skill descriptions often contain, so
descriptions are written as double-quoted strings. A JSON string is a valid YAML double-quoted scalar,
so json.loads is enough to check them without a YAML library.
"""
import glob
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SkillFrontmatterTest(unittest.TestCase):
    def test_frontmatter_is_strict_yaml(self):
        files = sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md")))
        self.assertTrue(files)
        for path in files:
            with self.subTest(skill=os.path.relpath(path, ROOT)):
                text = open(path, encoding="utf-8").read()
                m = re.match(r"---\n(.*?)\n---\n", text, re.S)
                self.assertIsNotNone(m, "missing frontmatter")
                fields = {}
                for line in m.group(1).split("\n"):
                    key, sep, value = line.partition(": ")
                    self.assertTrue(sep and re.fullmatch(r"[a-z][a-z0-9_-]*", key), "not a simple key: value line: " + line)
                    fields[key] = value
                self.assertEqual(set(fields), {"name", "description"})
                self.assertRegex(fields["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
                self.assertEqual(fields["name"], os.path.basename(os.path.dirname(path)))
                description = json.loads(fields["description"])  # must be a double-quoted string
                self.assertTrue(0 < len(description) <= 1024)


if __name__ == "__main__":
    unittest.main()
