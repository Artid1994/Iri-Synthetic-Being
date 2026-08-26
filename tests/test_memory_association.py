import unittest

from runtime.memory import Memory


class TestMemoryAssociation(unittest.TestCase):
    def test_memory_can_store_association(self):
        memory = Memory()

        memory.associate("tree detected", "tree")

        self.assertEqual(
            memory.associations("tree detected"),
            ["tree"],
        )

    def test_memory_preserves_multiple_associations(self):
        memory = Memory()

        memory.associate("tree detected", "tree")
        memory.associate("tree detected", "vision")

        self.assertEqual(
            memory.associations("tree detected"),
            ["tree", "vision"],
        )

    def test_memory_ignores_duplicate_association(self):
        memory = Memory()

        memory.associate("tree detected", "tree")
        memory.associate("tree detected", "tree")

        self.assertEqual(
            memory.associations("tree detected"),
            ["tree"],
        )

    def test_missing_association_returns_empty(self):
        memory = Memory()

        self.assertEqual(
            memory.associations("unknown"),
            [],
        )

    def test_associations_result_is_independent(self):
        memory = Memory()

        memory.associate("tree detected", "tree")

        result = memory.associations("tree detected")
        result.append("vision")

        self.assertEqual(
            memory.associations("tree detected"),
            ["tree"],
        )


if __name__ == "__main__":
    unittest.main()
