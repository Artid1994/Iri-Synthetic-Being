import unittest

from runtime.teaching import Teaching


class TestTeachingContract(unittest.TestCase):
    def test_new_teaching_starts_pending(self):
        teaching = Teaching(content="identify a tree")

        self.assertTrue(teaching.id)
        self.assertEqual(teaching.content, "identify a tree")
        self.assertEqual(teaching.status, "PENDING")

    def test_teaching_rejects_empty_content(self):
        with self.assertRaises(ValueError):
            Teaching(content="")

    def test_teaching_can_accept(self):
        teaching = Teaching(content="identify a tree")

        teaching.accept()

        self.assertEqual(teaching.status, "ACCEPTED")

    def test_teaching_can_reject(self):
        teaching = Teaching(content="identify a tree")

        teaching.reject()

        self.assertEqual(teaching.status, "REJECTED")


if __name__ == "__main__":
    unittest.main()
