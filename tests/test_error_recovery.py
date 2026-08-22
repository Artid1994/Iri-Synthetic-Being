import unittest

from runtime.error_recovery import ErrorRecovery


class TestErrorRecovery(unittest.TestCase):

    def test_retry_until_limit(self):
        recovery = ErrorRecovery(
            max_attempts=5
        )

        for i in range(5):
            result = recovery.handle(
                "parse_error"
            )

            self.assertEqual(
                result.action,
                "RETRY",
            )

        result = recovery.handle(
            "parse_error"
        )

        self.assertEqual(
            result.action,
            "ESCALATE",
        )

    def test_reset(self):
        recovery = ErrorRecovery()

        recovery.handle(
            "error"
        )

        recovery.reset()

        self.assertEqual(
            recovery.attempt,
            0,
        )


if __name__ == "__main__":
    unittest.main()
