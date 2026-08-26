import unittest

from runtime.learning_task import LearningTask
from runtime.self_directed_learning import SelfDirectedLearning


class TestSelfDirectedQueue(unittest.TestCase):
    def test_created_task_can_be_queued(self):
        selector = SelfDirectedLearning()

        task = selector.create_task("ESP32 BLE")

        self.assertIsNotNone(task)

        queued = selector.next_task()

        self.assertIs(queued, task)

    def test_queue_returns_tasks_in_order(self):
        selector = SelfDirectedLearning()

        first = selector.create_task("Python")
        second = selector.create_task("ESP32 BLE")

        self.assertIs(selector.next_task(), first)
        self.assertIs(selector.next_task(), second)

    def test_empty_queue_returns_none(self):
        selector = SelfDirectedLearning()

        self.assertIsNone(
            selector.next_task()
        )

    def test_completed_task_can_be_requested_again(self):
        selector = SelfDirectedLearning()

        first = selector.create_task("Python")
        first.complete = lambda: None
        first.status = "COMPLETED"

        second = selector.create_task("Python")

        self.assertIsNotNone(second)
        self.assertIsNot(first, second)


if __name__ == "__main__":
    unittest.main()
