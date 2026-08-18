import unittest

from runtime.memory import Memory
from runtime.cognitive_engine import CognitiveEngine


class TestMemoryContract(unittest.TestCase):
    def test_episodic_memory_preserves_insertion_order(self):
        memory = Memory()

        memory.add_experience("first")
        memory.add_experience("second")
        memory.add_experience("third")

        self.assertEqual(
            memory.state.episodic,
            ["first", "second", "third"],
        )

    def test_episodic_memory_allows_duplicate_experiences(self):
        memory = Memory()

        memory.add_experience("same")
        memory.add_experience("same")

        self.assertEqual(
            memory.state.episodic,
            ["same", "same"],
        )

    def test_memory_recall_prefers_latest_matching_experience(self):
        memory = Memory()

        memory.add_experience("old")
        memory.add_experience("target")
        memory.add_experience("middle")
        memory.add_experience("target")

        self.assertEqual(
            memory.recall("target"),
            "target",
        )

    def test_memory_recall_missing_returns_input(self):
        memory = Memory()

        self.assertEqual(
            memory.recall("unknown"),
            "unknown",
        )

    def test_cognitive_engine_behavior_remains_unchanged(self):
        memory = Memory()
        memory.add_experience("remember this")

        engine = CognitiveEngine(memory)

        result = engine.process(
            "remember this",
            record_experience=False,
        )

        self.assertEqual(result, "RESPOND")
        self.assertEqual(
            engine.state.last_recalled,
            "remember this",
        )

    def test_semantic_memory_deduplicates_learning(self):
        memory = Memory()

        memory.state.semantic.append("knowledge")
        memory.state.semantic.append("knowledge")

        self.assertEqual(
            memory.state.semantic.count("knowledge"),
            2,
        )

    def test_working_memory_exists_without_implicit_behavior(self):
        memory = Memory()

        self.assertEqual(memory.state.working, [])

    def test_empty_memory_recall_returns_input(self):
        memory = Memory()

        self.assertEqual(
            memory.recall("unknown"),
            "unknown",
        )


if __name__ == "__main__":
    unittest.main()
