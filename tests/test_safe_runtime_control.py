import unittest

from runtime.safe_runtime_control import SafeRuntimeControl


class FakeRunner:

    def __init__(self):
        self.calls = 0

    def run(
        self,
        observation,
        max_cycles,
        memory_usage,
    ):
        self.calls += 1

        return [
            {
                "status": "RUNNING"
            }
        ]


class TestSafeRuntimeControl(unittest.TestCase):

    def test_start_executes_runner(self):
        runner = FakeRunner()

        control = SafeRuntimeControl(
            runner
        )

        result = control.start(
            "observe",
            max_cycles=1,
        )

        self.assertEqual(
            len(result),
            1,
        )

        self.assertEqual(
            runner.calls,
            1,
        )

    def test_stop(self):
        runner = FakeRunner()

        control = SafeRuntimeControl(
            runner
        )

        control.stop()

        self.assertFalse(
            control.is_running()
        )


if __name__ == "__main__":
    unittest.main()
