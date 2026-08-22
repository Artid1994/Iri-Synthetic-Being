import unittest

from runtime.runtime import TranscendingRuntime


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "safe autonomous response"


class TestSafeRuntimeIntegration(unittest.TestCase):

    def test_block_without_autonomous_mode(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        result = runtime.start_safe_autonomous_runtime(
            "observe",
            max_cycles=2,
        )

        self.assertEqual(
            result["status"],
            "BLOCKED",
        )

    def test_safe_runtime_executes(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.enable_autonomous_mode()

        result = runtime.start_safe_autonomous_runtime(
            "observe",
            max_cycles=2,
        )

        self.assertEqual(
            len(result),
            2,
        )


if __name__ == "__main__":
    unittest.main()
