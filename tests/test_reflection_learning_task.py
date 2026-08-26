import unittest

from runtime.learning_task import LearningTask
from runtime.reflection import Reflection


class TestReflectionLearningTask(unittest.TestCase):
    def test_failure_creates_learning_task(self):
        reflection = Reflection()

        result = reflection.reflect(
            "FAILURE",
            observation="ESP32 compilation failed",
            task_topic="ESP32 BLE",
        )

        self.assertIsNotNone(result.next_task)

        task = LearningTask(result.next_task)

        self.assertEqual(task.status, "PENDING")
        self.assertIn("ESP32 BLE", task.topic)

    def test_missing_knowledge_creates_learning_task(self):
        reflection = Reflection()

        result = reflection.reflect(
            "MISSING_KNOWLEDGE",
            observation="BLE API knowledge is insufficient",
            task_topic="ESP32 BLE",
        )

        task = LearningTask(result.next_task)

        self.assertEqual(task.status, "PENDING")
        self.assertIn("ESP32 BLE", task.topic)


if __name__ == "__main__":
    unittest.main()
