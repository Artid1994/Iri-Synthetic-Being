import unittest

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class TestRuntimeAutonomousRunner(unittest.TestCase):

    def test_runner_block_without_mode(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        result = runtime.start_autonomous_runner(
            "observe tree",
            max_cycles=2,
        )

        self.assertEqual(
            result["status"],
            "BLOCKED",
        )

    def test_runner_executes_cycles(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.enable_autonomous_mode()

        result = runtime.start_autonomous_runner(
            "observe tree",
            max_cycles=2,
        )

        self.assertEqual(
            len(result),
            2,
        )


if __name__ == "__main__":
    unittest.main()
