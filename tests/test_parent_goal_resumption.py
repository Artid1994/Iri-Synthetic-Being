import unittest
from unittest.mock import Mock

from runtime.autonomous_learning import AutonomousLearningResult
from runtime.autonomous_runner import AutonomousRunner
from runtime.goal import Goal
from runtime.runtime import TranscendingRuntime


class TestParentGoalResumption(unittest.TestCase):
    def setUp(self):
        self.runtime = TranscendingRuntime()
        self.runtime.autonomous_mode = True

    def test_parent_goal_resumption_end_to_end(self):
        """
        Deterministic integration test proving:
        Goal A
        -> missing knowledge
        -> Child Goal B (Goal A paused)
        -> B executes successfully (Goal B completed)
        -> A automatically resumes
        -> A executes and completes
        -> no active goals remain.
        """
        goal_a = Goal("Complex Engineering Objective", priority=1)
        self.runtime.add_goal(goal_a)

        call_count = {"Goal A": 0, "Child B": 0}

        def mock_learn(task):
            if "Complex Engineering Objective" in task.topic and "missing knowledge" not in task.topic:
                call_count["Goal A"] += 1
                if call_count["Goal A"] == 1:
                    # First attempt fails due to missing knowledge
                    return AutonomousLearningResult(
                        topic=task.topic,
                        status="INCOMPLETE",
                        reason="CONFIDENCE_TOO_LOW",
                        memory_updated=False,
                    )
                else:
                    # Second attempt (after Child B completed) succeeds
                    return AutonomousLearningResult(
                        topic=task.topic,
                        status="COMPLETED",
                        reason="CONFIDENCE_THRESHOLD_MET",
                        memory_updated=True,
                    )
            else:
                call_count["Child B"] += 1
                return AutonomousLearningResult(
                    topic=task.topic,
                    status="COMPLETED",
                    reason="CONFIDENCE_THRESHOLD_MET",
                    memory_updated=True,
                )

        self.runtime.autonomous_learning.learn = Mock(side_effect=mock_learn)

        runner = AutonomousRunner(loop_controller=Mock(), interval=0.0)
        results = runner.run_goals(self.runtime, max_cycles=10)

        # 3 cycles: Goal A (fails -> chains B, pauses A), Goal B (completes -> resumes A), Goal A (completes)
        self.assertEqual(len(results), 3)

        self.assertEqual(results[0].goal.description, "Complex Engineering Objective")
        self.assertEqual(results[0].reflection.outcome, "MISSING_KNOWLEDGE")

        self.assertEqual(results[1].goal.description, "Research missing knowledge for: Complex Engineering Objective")
        self.assertEqual(results[1].goal.status, "COMPLETED")

        self.assertEqual(results[2].goal.description, "Complex Engineering Objective")
        self.assertEqual(results[2].goal.status, "COMPLETED")

        # All goals completed
        active_remaining = [g for g in self.runtime.goals if g.status == "ACTIVE"]
        self.assertEqual(len(active_remaining), 0)

        completed_goals = [g for g in self.runtime.goals if g.status == "COMPLETED"]
        self.assertEqual(len(completed_goals), 2)

    def test_child_failure_does_not_resume_parent(self):
        """
        If child goal fails, parent goal remains PAUSED and is not incorrectly resumed.
        """
        goal_a = Goal("Main Task", priority=1)
        self.runtime.add_goal(goal_a)

        def mock_learn(task):
            if "Main Task" in task.topic and "missing knowledge" not in task.topic:
                return AutonomousLearningResult(
                    topic=task.topic,
                    status="INCOMPLETE",
                    reason="CONFIDENCE_TOO_LOW",
                    memory_updated=False,
                )
            else:
                # Child goal persistently fails
                return AutonomousLearningResult(
                    topic=task.topic,
                    status="FAILED",
                    reason="FATAL_ERROR",
                    memory_updated=False,
                )

        self.runtime.autonomous_learning.learn = Mock(side_effect=mock_learn)

        runner = AutonomousRunner(loop_controller=Mock(), interval=0.0, failure_limit=2)
        runner.run_goals(self.runtime, max_cycles=10)

        # Parent goal should still be PAUSED
        self.assertEqual(goal_a.status, "PAUSED")

    def test_duplicate_resumption_prevented(self):
        """
        Resumption does not trigger duplicate active instances.
        """
        goal_a = Goal("Main Task", priority=1)
        goal_a.pause()
        self.runtime.add_goal(goal_a)

        child_b = Goal("Child Task", priority=1)
        setattr(child_b, "parent_goal_id", goal_a.id)
        self.runtime.add_goal(child_b)

        # First resumption
        resumed = self.runtime._resume_parent_goal_if_any(child_b)
        self.assertEqual(resumed, goal_a)
        self.assertEqual(goal_a.status, "ACTIVE")

        # Second resumption attempt when parent is already ACTIVE returns None
        resumed_again = self.runtime._resume_parent_goal_if_any(child_b)
        self.assertIsNone(resumed_again)
        self.assertEqual(goal_a.status, "ACTIVE")

    def test_safety_stop_prevents_resumed_goal_execution(self):
        """
        When safety stop is signaled after child completes, resumed parent is not executed.
        """
        goal_a = Goal("Main Task", priority=1)
        self.runtime.add_goal(goal_a)

        stop_signal = [False]

        def stop_check():
            return stop_signal[0]

        def mock_learn(task):
            # If the task is the parent goal (initial run before stop)
            if "Main Task" in task.topic and "Research missing knowledge" not in task.topic and not stop_signal[0]:
                return AutonomousLearningResult(
                    topic=task.topic,
                    status="INCOMPLETE",
                    reason="CONFIDENCE_TOO_LOW",
                    memory_updated=False,
                )
            else:
                # Child goal execution: complete successfully and signal safety stop
                stop_signal[0] = True
                return AutonomousLearningResult(
                    topic=task.topic,
                    status="COMPLETED",
                    reason="CONFIDENCE_THRESHOLD_MET",
                    memory_updated=True,
                )

        self.runtime.autonomous_learning.learn = Mock(side_effect=mock_learn)

        runner = AutonomousRunner(loop_controller=Mock(), interval=0.0)
        results = runner.run_goals(self.runtime, max_cycles=10, safety_stop_callback=stop_check)

        # Executed Goal A (pause), Goal B (complete + stop signal), but NOT resumed Goal A
        self.assertEqual(len(results), 2)
        self.assertEqual(goal_a.status, "ACTIVE")  # Resumed, but not executed because runner stopped


if __name__ == "__main__":
    unittest.main()
