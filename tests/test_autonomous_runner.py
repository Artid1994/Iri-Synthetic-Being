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


if __name__ == "__main__":
    unittest.main()
