import unittest

from runtime.autonomous_runner import AutonomousRunner


class FakeLoop:

    def __init__(self):
        self.calls = 0

    def step(self, observation, memory_usage):
        self.calls += 1

        return {
            "cycle": self.calls
        }


class TestAutonomousRunner(unittest.TestCase):

    def test_run_multiple_cycles(self):
        loop = FakeLoop()

        runner = AutonomousRunner(
            loop,
        )

        result = runner.run(
            "observe",
            max_cycles=3,
        )

        self.assertEqual(
            len(result),
            3,
        )

        self.assertEqual(
            loop.calls,
            3,
        )

    def test_stop(self):
        loop = FakeLoop()

        runner = AutonomousRunner(
            loop,
        )

        runner.stop()

        self.assertFalse(
            runner.running
        )

    def test_run_1000_cycles_without_growth_in_runner_state(self):
        loop = FakeLoop()

        runner = AutonomousRunner(
            loop,
            interval=0.0,
        )

        result = runner.run(
            "observe",
            max_cycles=1000,
        )

        self.assertEqual(loop.calls, 1000)
        self.assertEqual(runner.cycle_count, 1000)
        self.assertEqual(len(result), 1000)

    def test_start_is_non_blocking(self):
        loop = FakeLoop()

        runner = AutonomousRunner(
            loop,
            interval=0.01,
        )

        runner.start(
            "observe",
            max_cycles=3,
        )

        runner.join(timeout=1.0)

        self.assertFalse(runner.running)
        self.assertEqual(loop.calls, 3)

    def test_circuit_breaker_pauses_task_after_three_failures(self):
        class FailingLoop:
            def step(self, observation, memory_usage):
                return {"status": "FAILED"}

        runner = AutonomousRunner(
            FailingLoop(),
            interval=0.0,
            failure_limit=3,
        )

        result = runner.run(
            "same-task",
            max_cycles=10,
        )

        self.assertEqual(len(result), 3)
        self.assertEqual(result[-1]["status"], "TASK_PAUSED")
        self.assertIn("same-task", runner.paused_tasks())


if __name__ == "__main__":
    unittest.main()
