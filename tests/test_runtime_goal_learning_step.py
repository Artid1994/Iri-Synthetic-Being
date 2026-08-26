import unittest
from unittest.mock import Mock

from runtime.autonomous_learning import AutonomousLearningResult
from runtime.goal import Goal
from runtime.runtime import TranscendingRuntime


class TestRuntimeGoalLearningStep(unittest.TestCase):
    def test_runtime_runs_one_goal_learning_step(self):
        runtime = TranscendingRuntime(
            cognitive=Mock()
        )

        runtime.autonomous_learning.learn = Mock(
            return_value=AutonomousLearningResult(
                topic="Python",
                status="COMPLETED",
                reason="CONFIDENCE_THRESHOLD_MET",
                memory_updated=True,
            )
        )

        goal = Goal("Python")

        result = runtime.run_goal_learning_step(goal)

        self.assertEqual(
            result.goal,
            goal,
        )
        self.assertEqual(
            result.learning_task.topic,
            "Python",
        )
        self.assertEqual(
            result.learning_task.status,
            "COMPLETED",
        )
        self.assertEqual(
            result.reflection.outcome,
            "SUCCESS",
        )
        self.assertIsNone(
            result.next_task,
        )

        runtime.autonomous_learning.learn.assert_called_once()


if __name__ == "__main__":
    unittest.main()
