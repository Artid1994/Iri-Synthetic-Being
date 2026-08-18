import unittest

from runtime.recall_index import RecallIndex


class TestRecallIndex(unittest.TestCase):
    def test_empty_index_returns_none(self):
        index = RecallIndex()

        self.assertIsNone(
            index.find_latest("missing")
        )

    def test_add_and_find(self):
        index = RecallIndex()

        index.add("hello", 0)

        self.assertEqual(
            index.find_latest("hello"),
            0,
        )

    def test_latest_duplicate_replaces_previous_position(self):
        index = RecallIndex()

        index.add("hello", 0)
        index.add("other", 1)
        index.add("hello", 2)

        self.assertEqual(
            index.find_latest("hello"),
            2,
        )

    def test_different_experiences_are_independent(self):
        index = RecallIndex()

        index.add("a", 0)
        index.add("b", 1)

        self.assertEqual(index.find_latest("a"), 0)
        self.assertEqual(index.find_latest("b"), 1)

    def test_snapshot_is_independent(self):
        index = RecallIndex()
        index.add("hello", 0)

        snapshot = index.snapshot()
        snapshot["hello"] = 999

        self.assertEqual(
            index.find_latest("hello"),
            0,
        )

    def test_index_size_counts_unique_experiences(self):
        index = RecallIndex()

        index.add("a", 0)
        index.add("a", 1)
        index.add("b", 2)

        self.assertEqual(len(index), 2)


if __name__ == "__main__":
    unittest.main()
