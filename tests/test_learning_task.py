import unittest

from runtime.learning_task import LearningTask


class TestLearningTask(unittest.TestCase):
    def test_learning_task_requires_topic(self):
        with self.assertRaises(ValueError):
            LearningTask("")

    def test_learning_task_starts_pending(self):
        task = LearningTask("Python programming")

        self.assertEqual(task.topic, "Python programming")
        self.assertEqual(task.status, "PENDING")

    def test_learning_task_can_start(self):
        task = LearningTask("Python programming")

        task.start()

        self.assertEqual(task.status, "ACTIVE")

    def test_learning_task_can_complete(self):
        task = LearningTask("Python programming")

        task.start()
        task.complete()

        self.assertEqual(task.status, "COMPLETED")


if __name__ == "__main__":
    unittest.main()
