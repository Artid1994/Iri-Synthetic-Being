import unittest

from runtime.autonomous_policy_gate import AutonomousPolicyGate
from runtime.body_command import BodyCommand


class TestAutonomousPolicyGate(unittest.TestCase):
    def test_disabled_blocks(self):
        gate = AutonomousPolicyGate()

        result = gate.evaluate(
            BodyCommand("respond")
        )

        self.assertFalse(result.allowed)

    def test_enabled_allows_valid_command(self):
        gate = AutonomousPolicyGate()
        gate.enable()

        result = gate.evaluate(
            BodyCommand("respond")
        )

        self.assertTrue(result.allowed)


if __name__ == "__main__":
    unittest.main()
