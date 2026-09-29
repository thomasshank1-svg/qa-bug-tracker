import sqlite3
import unittest

import domain


class BugDomainTest(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        domain.init(self.db)

    def test_create_bug(self):
        domain.handle("POST", "/api/bugs", {"title": "Button broken", "area": "UI", "severity": "High", "steps": "Click it"}, self.db)
        self.assertGreaterEqual(len(domain.bugs(self.db)), 4)

    def test_bad_severity_rejected(self):
        with self.assertRaises(ValueError):
            domain.handle("POST", "/api/bugs", {"title": "Broken", "severity": "Emergency"}, self.db)


if __name__ == "__main__":
    unittest.main()
