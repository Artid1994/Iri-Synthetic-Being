import math
import unittest

from runtime.body_command import BodyCommand
from runtime.cognitive_safety_gate import CognitiveSafetyGate


class TestCognitiveSafetyGate(unittest.TestCase):
    def setUp(self):
        self.gate = CognitiveSafetyGate()

    def test_valid_move_is_allowed(self):
        result = self.gate.evaluate(
            BodyCommand(
                action="move",
                value=(1.0, 0.0),
            )
        )

        self.assertTrue(result.allowed)
        self.assertEqual(result.reason, "safe")

    def test_valid_respond_is_allowed(self):
        result = self.gate.evaluate(
            BodyCommand(
                action="respond",
                value=None,
            )
        )

        self.assertTrue(result.allowed)

    def test_unknown_action_is_blocked(self):
        result = self.gate.evaluate(
            BodyCommand(
                action="destroy",
            )
        )

        self.assertFalse(result.allowed)
        self.assertEqual(
            result.reason,
            "action_not_allowed",
        )

    def test_move_limit_is_enforced(self):
        result = self.gate.evaluate(
            BodyCommand(
                action="move",
                value=(1.1, 0.0),
            )
        )

        self.assertFalse(result.allowed)
        self.assertEqual(
            result.reason,
            "move_limit_exceeded",
        )

    def test_invalid_move_dimensions_are_blocked(self):
        result = self.gate.evaluate(
            BodyCommand(
                action="move",
                value=(1.0,),
            )
        )

        self.assertFalse(result.allowed)

    def test_non_finite_move_is_blocked(self):
        result = self.gate.evaluate(
            BodyCommand(
                action="move",
                value=(math.inf, 0.0),
            )
        )

        self.assertFalse(result.allowed)
        self.assertEqual(
            result.reason,
            "non_finite_move_value",
        )

    def test_invalid_respond_value_is_blocked(self):
        result = self.gate.evaluate(
            BodyCommand(
                action="respond",
                value="unexpected",
            )
        )

        self.assertFalse(result.allowed)

    def test_missing_command_is_blocked(self):
        result = self.gate.evaluate(None)

        self.assertFalse(result.allowed)
        self.assertEqual(
            result.reason,
            "missing_command",
        )


if __name__ == "__main__":
    unittest.main()
