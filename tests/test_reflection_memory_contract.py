import unittest

from runtime.memory import Memory
from runtime.reflection import Reflection


class TestReflectionMemoryContract(unittest.TestCase):
    def test_success_reflection_can_be_stored_as_episodic_lesson(self):
        memory = Memory()
        reflection = Reflection()

        result = reflection.reflect(
            "SUCCESS",
            observation="Python syntax passed",
            task_topic="Python",
        )

        memory.add_experience(result.lesson)

        self.assertEqual(
            memory.state.episodic,
            ["Python syntax passed"],
        )

    def test_failure_reflection_can_be_stored_as_episodic_lesson(self):
        memory = Memory()
        reflection = Reflection()

        result = reflection.reflect(
            "FAILURE",
            observation="ESP32 compilation failed",
            task_topic="ESP32 BLE",
        )

        memory.add_experience(result.lesson)

        self.assertEqual(
            memory.state.episodic,
            ["ESP32 compilation failed"],
        )

    def test_missing_knowledge_reflection_can_be_stored_as_semantic_knowledge(self):
        memory = Memory()
        reflection = Reflection()

        result = reflection.reflect(
            "MISSING_KNOWLEDGE",
            observation="BLE API knowledge is insufficient",
            task_topic="ESP32 BLE",
        )

        memory.add_semantic(result.lesson)

        self.assertTrue(
            memory.semantic_contains(
                "BLE API knowledge is insufficient"
            )
        )


if __name__ == "__main__":
    unittest.main()
