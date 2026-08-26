import unittest

from runtime.association_index import AssociationIndex


class TestAssociationIndex(unittest.TestCase):
    def test_empty_index_returns_empty(self):
        index = AssociationIndex()

        self.assertEqual(
            index.find("tree"),
            [],
        )

    def test_association_can_be_added(self):
        index = AssociationIndex()

        index.add("tree detected", "tree")

        self.assertEqual(
            index.find("tree detected"),
            ["tree"],
        )

    def test_multiple_associations_are_preserved(self):
        index = AssociationIndex()

        index.add("tree detected", "tree")
        index.add("tree detected", "vision")

        self.assertEqual(
            index.find("tree detected"),
            ["tree", "vision"],
        )

    def test_duplicate_association_is_ignored(self):
        index = AssociationIndex()

        index.add("tree detected", "tree")
        index.add("tree detected", "tree")

        self.assertEqual(
            index.find("tree detected"),
            ["tree"],
        )

    def test_different_sources_are_independent(self):
        index = AssociationIndex()

        index.add("tree detected", "tree")
        index.add("person detected", "person")

        self.assertEqual(
            index.find("tree detected"),
            ["tree"],
        )

        self.assertEqual(
            index.find("person detected"),
            ["person"],
        )

    def test_snapshot_is_independent(self):
        index = AssociationIndex()

        index.add("tree detected", "tree")

        snapshot = index.snapshot()
        snapshot["tree detected"].append("vision")

        self.assertEqual(
            index.find("tree detected"),
            ["tree"],
        )


if __name__ == "__main__":
    unittest.main()
