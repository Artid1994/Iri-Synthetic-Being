import unittest

from runtime.runtime import TranscendingRuntime


class TestRuntimeAutonomousMode(unittest.TestCase):

    def test_default_mode_is_human(self):
        runtime = TranscendingRuntime(cognitive=None)

        self.assertFalse(
            runtime.autonomous_mode
        )

        self.assertFalse(
            runtime.autonomous_policy.enabled
        )

    def test_enable_and_disable_mode(self):
        runtime = TranscendingRuntime(cognitive=None)

        runtime.enable_autonomous_mode()

        self.assertTrue(
            runtime.autonomous_mode
        )

        self.assertTrue(
            runtime.autonomous_policy.enabled
        )

        runtime.disable_autonomous_mode()

        self.assertFalse(
            runtime.autonomous_mode
        )

        self.assertFalse(
            runtime.autonomous_policy.enabled
        )


if __name__ == "__main__":
    unittest.main()
