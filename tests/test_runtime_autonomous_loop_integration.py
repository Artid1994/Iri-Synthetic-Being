import unittest

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class TestRuntimeAutonomousLoopIntegration(unittest.TestCase):

    def test_block_when_autonomous_disabled(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        result = runtime.run_autonomous_step(
            "observe tree"
        )

        self.assertEqual(
            result["status"],
            "BLOCKED",
        )

    def test_run_when_autonomous_enabled(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.enable_autonomous_mode()

        result = runtime.run_autonomous_step(
            "observe tree",
            0.5,
        )

        self.assertEqual(
            result["status"],
            "RUNNING",
        )


if __name__ == "__main__":
    unittest.main()
