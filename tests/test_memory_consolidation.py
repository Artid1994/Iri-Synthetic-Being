import unittest

from runtime.memory import Memory
from runtime.memory_consolidation import MemoryConsolidation


class TestMemoryConsolidation(unittest.TestCase):
    def test_consolidation_moves_working_item_to_episodic_memory(self):
        memory = Memory()
        memory.add_working("tree detected")

        consolidation = MemoryConsolidation(memory)

        result = consolidation.consolidate("tree detected")

        self.assertTrue(result.consolidated)
        self.assertEqual(
            memory.state.episodic,
            ["tree detected"],
        )

    def test_consolidation_does_not_remove_working_memory(self):
        memory = Memory()
        memory.add_working("tree detected")

        consolidation = MemoryConsolidation(memory)
        consolidation.consolidate("tree detected")

        self.assertEqual(
            memory.working_memory(),
            ["tree detected"],
        )

    def test_consolidation_can_promote_semantic_knowledge(self):
        memory = Memory()
        memory.add_working("trees need water")

        consolidation = MemoryConsolidation(memory)

        result = consolidation.consolidate(
            "trees need water",
            promote_semantic=True,
        )

        self.assertTrue(result.consolidated)
        self.assertTrue(
            memory.semantic_contains("trees need water")
        )

    def test_unknown_item_is_not_consolidated(self):
        memory = Memory()
        consolidation = MemoryConsolidation(memory)

        result = consolidation.consolidate(
            "unknown",
        )

        self.assertFalse(result.consolidated)
        self.assertEqual(
            memory.state.episodic,
            [],
        )

    def test_blank_item_is_rejected(self):
        memory = Memory()
        consolidation = MemoryConsolidation(memory)

        result = consolidation.consolidate("   ")

        self.assertFalse(result.consolidated)

    def test_prune_episodic_rebuilds_recall_index(self):
        memory = Memory()

        for i in range(5):
            memory.add_experience(f"experience {i}")

        memory.prune(max_episodic=3)

        self.assertEqual(
            memory.state.episodic,
            ["experience 2", "experience 3", "experience 4"],
        )
        self.assertEqual(
            memory.recall("experience 4"),
            "experience 4",
        )
        self.assertEqual(
            memory.recall("experience 1"),
            "experience 1",
        )


if __name__ == "__main__":
    unittest.main()


    def test_consolidation_preserves_all_distinct_episodic_memories(self):
        memory = Memory()

        memory.add_working("tree")
        MemoryConsolidation(memory).consolidate("tree")

        memory.add_working("person")
        MemoryConsolidation(memory).consolidate("person")

        memory.add_working("house")
        MemoryConsolidation(memory).consolidate("house")

        self.assertEqual(
            memory.state.episodic,
            ["tree", "person", "house"],
        )
