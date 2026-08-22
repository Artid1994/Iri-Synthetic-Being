import unittest

from runtime.autonomous_policy_gate import AutonomousPolicyGate


class TestAutonomousPolicyMode(unittest.TestCase):

    def test_default_mode_disabled(self):
        gate = AutonomousPolicyGate()

        self.assertFalse(
            gate.enabled
        )

    def test_enable_autonomous_mode(self):
        gate = AutonomousPolicyGate()

        gate.enable()

        self.assertTrue(
            gate.enabled
        )


if __name__ == "__main__":
    unittest.main()
