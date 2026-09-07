import unittest
from unittest.mock import Mock

from runtime.autonomous_learning import AutonomousLearningResult
from runtime.autonomous_runner import AutonomousRunner
from runtime.goal import Goal
from runtime.runtime import TranscendingRuntime


class TestAutonomousGoalDispatcher(unittest.TestCase):
    def setUp(self):
        self.runtime = TranscendingRuntime(cognitive=Mock())
        self.runtime.enable_autonomous_mode()

    def test_empty_queue_returns_none_or_empty(self):
        # Empty queue should safely return None for single dispatch and [] for all
        self.assertIsNone(self.runtime.dispatch_next_goal())
        results = self.runtime.dispatch_all_goals()
        self.assertEqual(results, [])

    def test_mode_disabled_blocks_dispatch(self):
        self.runtime.disable_autonomous_mode()
        results = self.runtime.dispatch_all_goals()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "BLOCKED")
        self.assertEqual(results[0]["reason"], "AUTONOMOUS_MODE_DISABLED")

    def test_priority_ordering_and_deterministic_tiebreak(self):
        low_goal = Goal("Low Priority Task", priority=1)
        high_goal = Goal("High Priority Task", priority=10)
        equal_goal_1 = Goal("Equal Priority First", priority=5)
        equal_goal_2 = Goal("Equal Priority Second", priority=5)

        self.runtime.add_goal(low_goal)
        self.runtime.add_goal(equal_goal_1)
        self.runtime.add_goal(equal_goal_2)
        self.runtime.add_goal(high_goal)

        # Mock successful learning
        self.runtime.autonomous_learning.learn = Mock(
            side_effect=lambda task: AutonomousLearningResult(
                topic=task.topic,
                status="COMPLETED",
                reason="CONFIDENCE_THRESHOLD_MET",
                memory_updated=True,
            )
        )

        # First dispatch should pick high_goal (priority 10)
        res1 = self.runtime.dispatch_next_goal()
        self.assertEqual(res1.goal.description, "High Priority Task")
        self.assertEqual(high_goal.status, "COMPLETED")

        # Second dispatch should pick equal_goal_1 (priority 5, first in list)
        res2 = self.runtime.dispatch_next_goal()
        self.assertEqual(res2.goal.description, "Equal Priority First")
        self.assertEqual(equal_goal_1.status, "COMPLETED")

        # Third dispatch should pick equal_goal_2 (priority 5, second in list)
        res3 = self.runtime.dispatch_next_goal()
        self.assertEqual(res3.goal.description, "Equal Priority Second")
        self.assertEqual(equal_goal_2.status, "COMPLETED")

        # Fourth dispatch should pick low_goal (priority 1)
        res4 = self.runtime.dispatch_next_goal()
        self.assertEqual(res4.goal.description, "Low Priority Task")
        self.assertEqual(low_goal.status, "COMPLETED")

        # Queue should now be drained of ACTIVE goals
        self.assertIsNone(self.runtime.dispatch_next_goal())

    def test_goal_chaining_and_queue_draining_via_runner(self):
        """
        Integration test:
        Goal A -> execute -> missing knowledge -> Goal B enqueued
               -> Goal B executed -> completed -> Goal A resumed and re-evaluated.
        """
        goal_a = Goal("Initial Goal A", priority=1)
        self.runtime.add_goal(goal_a)

        call_count = {"Goal A": 0}

        def mock_learn(task):
            if "Initial Goal A" in task.topic and "missing knowledge" not in task.topic:
                call_count["Goal A"] += 1
                if call_count["Goal A"] == 1:
                    return AutonomousLearningResult(
                        topic=task.topic,
                        status="INCOMPLETE",
                        reason="CONFIDENCE_TOO_LOW",
                        memory_updated=False,
                    )
                else:
                    return AutonomousLearningResult(
                        topic=task.topic,
                        status="COMPLETED",
                        reason="CONFIDENCE_THRESHOLD_MET",
                        memory_updated=True,
                    )
            else:
                return AutonomousLearningResult(
                    topic=task.topic,
                    status="COMPLETED",
                    reason="CONFIDENCE_THRESHOLD_MET",
                    memory_updated=True,
                )

        self.runtime.autonomous_learning.learn = Mock(side_effect=mock_learn)

        runner = AutonomousRunner(loop_controller=Mock(), interval=0.0)
        results = runner.run_goals(self.runtime, max_cycles=10)

        # Should execute Goal A (chaining Goal B), execute Goal B (completing & resuming A), execute Goal A (completing)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].goal.description, "Initial Goal A")
        self.assertEqual(results[1].goal.description, "Research missing knowledge for: Initial Goal A")
        self.assertEqual(results[1].goal.status, "COMPLETED")
        self.assertEqual(results[2].goal.description, "Initial Goal A")
        self.assertEqual(results[2].goal.status, "COMPLETED")

        # Active goals in runtime should now be empty
        active_remaining = [g for g in self.runtime.goals if g.status == "ACTIVE"]
        self.assertEqual(len(active_remaining), 0)


    def test_circuit_breaker_and_duplicate_prevention(self):
        stuck_goal = Goal("Unsolvable Task", priority=5)
        self.runtime.add_goal(stuck_goal)

        # Fails with persistent error that does not produce next_task
        self.runtime.autonomous_learning.learn = Mock(
            return_value=AutonomousLearningResult(
                topic=stuck_goal.description,
                status="FAILED",
                reason="FATAL_ERROR",
                memory_updated=False,
            )
        )

        runner = AutonomousRunner(loop_controller=Mock(), interval=0.0, failure_limit=3)
        results = runner.run_goals(self.runtime, max_cycles=10)

        # Should attempt 3 times, fail, and pause the goal
        self.assertEqual(len(results), 4)
        self.assertEqual(results[-1]["status"], "TASK_PAUSED")
        self.assertEqual(results[-1]["reason"], "CIRCUIT_BREAKER")
        self.assertEqual(stuck_goal.status, "PAUSED")

    def test_safety_stop_callback(self):
        goal_1 = Goal("Task 1", priority=1)
        goal_2 = Goal("Task 2", priority=1)
        self.runtime.add_goal(goal_1)
        self.runtime.add_goal(goal_2)

        self.runtime.autonomous_learning.learn = Mock(
            return_value=AutonomousLearningResult(
                topic="Task",
                status="COMPLETED",
                reason="OK",
                memory_updated=True,
            )
        )

        stop_signal = [False]

        def stop_check():
            return stop_signal[0]

        # First cycle runs, then stop signal trips
        def side_effect(task):
            stop_signal[0] = True
            return AutonomousLearningResult(
                topic=task.topic,
                status="COMPLETED",
                reason="OK",
                memory_updated=True,
            )

        self.runtime.autonomous_learning.learn = Mock(side_effect=side_effect)

        runner = AutonomousRunner(loop_controller=Mock(), interval=0.0)
        results = runner.run_goals(self.runtime, max_cycles=10, safety_stop_callback=stop_check)

        # Stopped after 1 goal despite remaining active goals
        self.assertEqual(len(results), 1)
        self.assertTrue(any(g.status == "ACTIVE" for g in self.runtime.goals))


if __name__ == "__main__":
    unittest.main()
