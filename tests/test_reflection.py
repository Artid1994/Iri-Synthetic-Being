import unittest

from runtime.reflection import Reflection


class TestReflection(unittest.TestCase):
    def setUp(self):
        self.reflection = Reflection()

    def test_success_creates_lesson(self):
        result = self.reflection.reflect(
            "SUCCESS",
            observation="Python syntax passed",
            task_topic="Python",
        )

        self.assertEqual(result.outcome, "SUCCESS")
        self.assertEqual(result.lesson, "Python syntax passed")
        self.assertIsNone(result.next_task)

    def test_failure_creates_next_task(self):
        result = self.reflection.reflect(
            "FAILURE",
            observation="Compilation failed",
            task_topic="ESP32",
        )

        self.assertEqual(result.outcome, "FAILURE")
        self.assertEqual(result.lesson, "Compilation failed")
        self.assertIn("ESP32", result.next_task)

    def test_missing_knowledge_creates_research_task(self):
        result = self.reflection.reflect(
            "MISSING_KNOWLEDGE",
            task_topic="Flutter BLE",
        )

        self.assertEqual(
            result.outcome,
            "MISSING_KNOWLEDGE",
        )
        self.assertIn("Flutter BLE", result.next_task)


if __name__ == "__main__":
    unittest.main()
