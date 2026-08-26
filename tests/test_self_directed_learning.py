import unittest

from runtime.learning_task import LearningTask
from runtime.self_directed_learning import SelfDirectedLearning


class TestSelfDirectedLearning(unittest.TestCase):
    def test_empty_need_returns_none(self):
        selector = SelfDirectedLearning()

        self.assertIsNone(
            selector.create_task("")
        )

    def test_missing_knowledge_creates_learning_task(self):
        selector = SelfDirectedLearning()

        task = selector.create_task(
            "BLE API knowledge is insufficient"
        )

        self.assertIsInstance(task, LearningTask)
        self.assertIn(
            "BLE API knowledge is insufficient",
            task.topic,
        )
        self.assertEqual(task.status, "PENDING")

    def test_duplicate_pending_topic_is_not_created(self):
        selector = SelfDirectedLearning()

        first = selector.create_task(
            "Learn Python"
        )

        second = selector.create_task(
            "Learn Python"
        )

        self.assertIsNotNone(first)
        self.assertIsNone(second)

    def test_completed_topic_can_be_requested_again(self):
        selector = SelfDirectedLearning()

        task = selector.create_task(
            "Learn Python"
        )

        task.start()
        task.complete()

        next_task = selector.create_task(
            "Learn Python"
        )

        self.assertIsNotNone(next_task)
        self.assertEqual(
            next_task.status,
            "PENDING",
        )


if __name__ == "__main__":
    unittest.main()
