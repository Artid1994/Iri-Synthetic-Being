import unittest

from runtime.autonomous_step import AutonomousStep
from runtime.goal import Goal
from runtime.self_directed_learning import SelfDirectedLearning


class FakeResult:
    def __init__(
        self,
        memory_updated=False,
        reason="EMPTY_RESEARCH_CONTENT",
    ):
        self.memory_updated = memory_updated
        self.reason = reason


class FakeAutonomousLearning:
    def learn(self, task):
        return FakeResult()


class FakeGoalLearning:
    def __init__(self):
        self.autonomous_learning = FakeAutonomousLearning()


class TestAutonomousStepSelfDirected(unittest.TestCase):
    def test_reflection_task_can_enter_self_directed_queue(self):
        selector = SelfDirectedLearning()
        step = AutonomousStep(
            FakeGoalLearning()
        )

        result = step.run(
            Goal("Learn ESP32 BLE")
        )

        task = selector.from_reflection(
            result.reflection
        )

        self.assertIsNotNone(task)
        self.assertEqual(
            task.status,
            "PENDING",
        )
        self.assertIn(
            "ESP32 BLE",
            task.topic,
        )

    def test_success_does_not_create_self_directed_task(self):
        class SuccessfulLearning:
            def learn(self, task):
                return FakeResult(
                    memory_updated=True,
                    reason="CONFIDENCE_THRESHOLD_MET",
                )

        class SuccessfulGoalLearning:
            autonomous_learning = SuccessfulLearning()

        selector = SelfDirectedLearning()
        step = AutonomousStep(
            SuccessfulGoalLearning()
        )

        result = step.run(
            Goal("Learn Python")
        )

        task = selector.from_reflection(
            result.reflection
        )

        self.assertIsNone(task)


if __name__ == "__main__":
    unittest.main()
