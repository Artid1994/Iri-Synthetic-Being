import unittest

from runtime.runtime import TranscendingRuntime


class FailingCognitive:
    def process(self, user_input, record_experience=True):
        raise RuntimeError("injected_failure")


class TestStressErrorInjection(unittest.TestCase):

    def test_error_retry_then_escalate(self):
        runtime = TranscendingRuntime(
            cognitive=FailingCognitive()
        )

        runtime.enable_autonomous_mode()

        for _ in range(5):
            result = runtime.start_safe_autonomous_runtime(
                "error test",
                max_cycles=1,
            )

            self.assertEqual(
                result[0]["status"],
                "RETRY",
            )

        result = runtime.start_safe_autonomous_runtime(
            "error test",
            max_cycles=1,
        )

        self.assertEqual(
            result[0]["status"],
            "ESCALATE",
        )


if __name__ == "__main__":
    unittest.main()
