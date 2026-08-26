import unittest
from unittest.mock import Mock

from runtime.autonomous_learning import AutonomousLearningResult
from runtime.goal import Goal
from runtime.goal_learning import GoalLearning


class TestGoalLearning(unittest.TestCase):
    def test_active_goal_creates_learning_cycle(self):
        autonomous = Mock()
        autonomous.learn.return_value = AutonomousLearningResult(
            topic="Python",
            status="COMPLETED",
            reason="CONFIDENCE_THRESHOLD_MET",
            memory_updated=True,
        )

        development = Mock()

        goal_learning = GoalLearning(
            autonomous_learning=autonomous,
            development=development,
        )

        goal = Goal("Python")

        result = goal_learning.learn_goal(goal)

        self.assertTrue(result.memory_updated)

        autonomous.learn.assert_called_once()

        task = autonomous.learn.call_args.args[0]

        self.assertEqual(task.topic, "Python")
        self.assertEqual(task.status, "PENDING")

        development.sync.assert_called_once()

    def test_completed_goal_does_not_learn(self):
        autonomous = Mock()
        development = Mock()

        goal_learning = GoalLearning(
            autonomous_learning=autonomous,
            development=development,
        )

        goal = Goal("Python")
        goal.complete()

        result = goal_learning.learn_goal(goal)

        self.assertEqual(
            result.reason,
            "GOAL_NOT_ACTIVE",
        )
        self.assertFalse(result.memory_updated)

        autonomous.learn.assert_not_called()
        development.sync.assert_not_called()

    def test_paused_goal_does_not_learn(self):
        autonomous = Mock()
        development = Mock()

        goal_learning = GoalLearning(
            autonomous_learning=autonomous,
            development=development,
        )

        goal = Goal("Python")
        goal.pause()

        result = goal_learning.learn_goal(goal)

        self.assertEqual(
            result.reason,
            "GOAL_NOT_ACTIVE",
        )

        autonomous.learn.assert_not_called()

    def test_invalid_goal_is_rejected(self):
        goal_learning = GoalLearning(Mock())

        with self.assertRaises(TypeError):
            goal_learning.learn_goal(object())


if __name__ == "__main__":
    unittest.main()
