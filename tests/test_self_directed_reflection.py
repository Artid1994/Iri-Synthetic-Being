import unittest

from runtime.reflection import Reflection
from runtime.learning_task import LearningTask
from runtime.self_directed_learning import SelfDirectedLearning


class TestSelfDirectedReflection(unittest.TestCase):
    def test_missing_knowledge_reflection_creates_task(self):
        selector = SelfDirectedLearning()

        reflection = Reflection().reflect(
            "MISSING_KNOWLEDGE",
            observation="BLE API knowledge is insufficient",
            task_topic="ESP32 BLE",
        )

        task = selector.from_reflection(reflection)

        self.assertIsInstance(task, LearningTask)
        self.assertIn(
            "ESP32 BLE",
            task.topic,
        )
        self.assertEqual(
            task.status,
            "PENDING",
        )

    def test_success_reflection_creates_no_task(self):
        selector = SelfDirectedLearning()

        reflection = Reflection().reflect(
            "SUCCESS",
            observation="Python syntax passed",
            task_topic="Python",
        )

        self.assertIsNone(
            selector.from_reflection(reflection)
        )

    def test_failure_reflection_creates_task(self):
        selector = SelfDirectedLearning()

        reflection = Reflection().reflect(
            "FAILURE",
            observation="ESP32 compilation failed",
            task_topic="ESP32 BLE",
        )

        task = selector.from_reflection(reflection)

        self.assertIsInstance(task, LearningTask)
        self.assertIn(
            "ESP32 BLE",
            task.topic,
        )


if __name__ == "__main__":
    unittest.main()
