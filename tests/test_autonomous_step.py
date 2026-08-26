import unittest
from unittest.mock import Mock

from runtime.autonomous_step import AutonomousStep
from runtime.goal import Goal


class FakeResult:
    def __init__(
        self,
        memory_updated=True,
        reason="CONFIDENCE_THRESHOLD_MET",
    ):
        self.memory_updated = memory_updated
        self.reason = reason


class FakeAutonomousLearning:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def learn(self, task):
        self.calls.append(task)
        return self.result


class FakeGoalLearning:
    def __init__(self, autonomous_learning):
        self.autonomous_learning = autonomous_learning


class TestAutonomousStep(unittest.TestCase):
    def test_success_cycle(self):
        autonomous_learning = FakeAutonomousLearning(
            FakeResult()
        )
        goal_learning = FakeGoalLearning(
            autonomous_learning
        )

        step = AutonomousStep(goal_learning)
        goal = Goal("Learn Python")

        result = step.run(goal)

        result.learning_task.status = "COMPLETED"

        self.assertEqual(
            result.reflection.outcome,
            "SUCCESS",
        )
        self.assertIsNone(result.next_task)
        self.assertEqual(
            result.learning_task.status,
            "COMPLETED",
        )
        self.assertEqual(
            len(autonomous_learning.calls),
            1,
        )

    def test_missing_knowledge_creates_next_task(self):
        autonomous_learning = FakeAutonomousLearning(
            FakeResult(
                memory_updated=False,
                reason="EMPTY_RESEARCH_CONTENT",
            )
        )
        goal_learning = FakeGoalLearning(
            autonomous_learning
        )

        step = AutonomousStep(goal_learning)
        result = step.run(Goal("Learn ESP32 BLE"))

        self.assertEqual(
            result.reflection.outcome,
            "MISSING_KNOWLEDGE",
        )
        self.assertIsNotNone(result.next_task)
        self.assertEqual(
            result.next_task.status,
            "PENDING",
        )
        self.assertIn(
            "ESP32 BLE",
            result.next_task.topic,
        )

    def test_invalid_goal_is_rejected(self):
        step = AutonomousStep(
            Mock()
        )

        with self.assertRaises(TypeError):
            step.run("Learn Python")


if __name__ == "__main__":
    unittest.main()
