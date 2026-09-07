import unittest
from unittest.mock import Mock

from runtime.autonomous_learning import AutonomousLearningResult
from runtime.goal import Goal
from runtime.runtime import TranscendingRuntime


class TestAutonomousGoalChaining(unittest.TestCase):
    def test_multi_cycle_goal_chaining_via_reflection(self):
        """
        Verifies deterministic multi-cycle goal chaining:
        Goal A -> cycle 1 -> reflection generates next_task
               -> automatically enqueued into runtime.goals as Goal B
               -> cycle 2 processes Goal B -> completes with no further task.
        """
        runtime = TranscendingRuntime(
            cognitive=Mock()
        )

        initial_goal = Goal("Initial Research Topic", priority=1)
        runtime.add_goal(initial_goal)
        self.assertEqual(len(runtime.goals), 1)

        # First cycle: learning misses knowledge -> reflection emits next_task
        runtime.autonomous_learning.learn = Mock(
            return_value=AutonomousLearningResult(
                topic="Initial Research Topic",
                status="INCOMPLETE",
                reason="CONFIDENCE_TOO_LOW",
                memory_updated=False,
            )
        )

        result_1 = runtime.run_goal_learning_step(initial_goal)

        # Reflection should generate missing knowledge task
        self.assertEqual(result_1.reflection.outcome, "MISSING_KNOWLEDGE")
        expected_chained_desc = "Research missing knowledge for: Initial Research Topic"
        self.assertEqual(result_1.reflection.next_task, expected_chained_desc)

        # Verify child goal was automatically enqueued into runtime.goals
        self.assertEqual(len(runtime.goals), 2)
        child_goal = runtime.goals[1]
        self.assertEqual(child_goal.description, expected_chained_desc)
        self.assertEqual(child_goal.status, "ACTIVE")
        self.assertEqual(child_goal.priority, initial_goal.priority)

        # Re-running on same goal should NOT duplicate existing active goal
        runtime.run_goal_learning_step(initial_goal)
        self.assertEqual(len(runtime.goals), 2)

        # Second cycle: execute the chained child goal successfully
        runtime.autonomous_learning.learn = Mock(
            return_value=AutonomousLearningResult(
                topic=child_goal.description,
                status="COMPLETED",
                reason="CONFIDENCE_THRESHOLD_MET",
                memory_updated=True,
            )
        )

        result_2 = runtime.run_goal_learning_step(child_goal)
        child_goal.complete()

        self.assertEqual(result_2.reflection.outcome, "SUCCESS")
        self.assertIsNone(result_2.reflection.next_task)
        self.assertIsNone(result_2.next_task)
        self.assertEqual(child_goal.status, "COMPLETED")
        # No extra goals added
        self.assertEqual(len(runtime.goals), 2)


if __name__ == "__main__":
    unittest.main()
