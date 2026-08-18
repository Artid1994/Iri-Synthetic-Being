import unittest

from runtime.semantic_index import SemanticIndex


class TestSemanticIndex(unittest.TestCase):
    def test_empty_index_does_not_contain_value(self):
        index = SemanticIndex()

        self.assertFalse(index.contains("missing"))

    def test_add_and_contains(self):
        index = SemanticIndex()

        index.add("knowledge")

        self.assertTrue(index.contains("knowledge"))

    def test_duplicate_add_is_idempotent(self):
        index = SemanticIndex()

        index.add("knowledge")
        index.add("knowledge")

        self.assertEqual(len(index), 1)

    def test_different_values_are_independent(self):
        index = SemanticIndex()

        index.add("a")
        index.add("b")

        self.assertTrue(index.contains("a"))
        self.assertTrue(index.contains("b"))
        self.assertFalse(index.contains("c"))

    def test_contains_operator(self):
        index = SemanticIndex()
        index.add("knowledge")

        self.assertTrue("knowledge" in index)
        self.assertFalse("missing" in index)

    def test_snapshot_is_independent(self):
        index = SemanticIndex()
        index.add("knowledge")

        snapshot = index.snapshot()
        snapshot.add("external")

        self.assertTrue(index.contains("knowledge"))
        self.assertFalse(index.contains("external"))


if __name__ == "__main__":
    unittest.main()
