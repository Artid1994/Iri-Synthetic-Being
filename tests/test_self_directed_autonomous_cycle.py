import unittest

from runtime.autonomous_step import AutonomousStep
from runtime.goal import Goal
from runtime.self_directed_learning import SelfDirectedLearning


class FakeResult:
    def __init__(self, memory_updated=False):
        self.memory_updated = memory_updated
        self.reason = "EMPTY_RESEARCH_CONTENT"


class FakeAutonomousLearning:
    def __init__(self):
        self.calls = []

    def learn(self, task):
        self.calls.append(task)
        return FakeResult()


class FakeGoalLearning:
    def __init__(self, autonomous_learning):
        self.autonomous_learning = autonomous_learning


class TestSelfDirectedAutonomousCycle(unittest.TestCase):
    def test_reflection_task_enters_queue_and_can_be_consumed(self):
        autonomous_learning = FakeAutonomousLearning()
        goal_learning = FakeGoalLearning(
            autonomous_learning
        )

        selector = SelfDirectedLearning()
        step = AutonomousStep(goal_learning)

        result = step.run(
            Goal("Learn ESP32 BLE")
        )

        created = selector.from_reflection(
            result.reflection
        )

        self.assertIsNotNone(created)

        queued = selector.next_task()

        self.assertIs(
            queued,
            created,
        )

        self.assertEqual(
            queued.status,
            "ACTIVE",
        )

    def test_consumed_task_is_not_returned_again(self):
        selector = SelfDirectedLearning()

        task = selector.create_task(
            "Learn Python"
        )

        self.assertIs(
            selector.next_task(),
            task,
        )

        self.assertIsNone(
            selector.next_task()
        )


if __name__ == "__main__":
    unittest.main()
