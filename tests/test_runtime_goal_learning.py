import unittest
from unittest.mock import Mock

from runtime.autonomous_learning import AutonomousLearningResult
from runtime.goal import Goal
from runtime.runtime import TranscendingRuntime


class TestRuntimeGoalLearning(unittest.TestCase):
    def test_runtime_exposes_goal_learning(self):
        cognitive = Mock()

        runtime = TranscendingRuntime(
            cognitive=cognitive
        )

        self.assertIsNotNone(
            runtime.goal_learning
        )

    def test_goal_learning_uses_runtime_development(self):
        cognitive = Mock()

        runtime = TranscendingRuntime(
            cognitive=cognitive
        )

        result = AutonomousLearningResult(
            topic="Python",
            status="COMPLETED",
            reason="CONFIDENCE_THRESHOLD_MET",
            memory_updated=True,
        )

        runtime.autonomous_learning.learn = Mock(
            return_value=result
        )

        runtime.development.sync = Mock()

        goal = Goal("Python")

        result = runtime.goal_learning.learn_goal(
            goal
        )

        self.assertTrue(result.memory_updated)

        runtime.autonomous_learning.learn.assert_called_once()

        runtime.development.sync.assert_called_once()


if __name__ == "__main__":
    unittest.main()
