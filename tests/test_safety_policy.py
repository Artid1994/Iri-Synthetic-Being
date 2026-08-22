import unittest

from runtime.body_command import BodyCommand
from runtime.safety_event import SafetyEvent
from runtime.safety_policy import SafetyPolicy


class TestSafetyPolicy(unittest.TestCase):
    def test_policy_starts_empty(self):
        policy = SafetyPolicy()

        self.assertEqual(
            policy.snapshot(),
            (),
        )

    def test_safety_event_creates_policy_observation(self):
        policy = SafetyPolicy()

        policy.observe(
            SafetyEvent(
                action="move",
                value=(2.0, 0.0),
                reason="move_limit_exceeded",
            )
        )

        self.assertEqual(
            policy.snapshot(),
            ("move_limit_exceeded",),
        )

    def test_matching_reason_is_blocked(self):
        policy = SafetyPolicy()

        policy.observe(
            SafetyEvent(
                action="move",
                value=(2.0, 0.0),
                reason="move_limit_exceeded",
            )
        )

        result = policy.evaluate(
            "move_limit_exceeded"
        )

        self.assertTrue(result.blocked)
        self.assertEqual(
            result.reason,
            "POLICY_BLOCK",
        )

    def test_unknown_reason_is_not_blocked(self):
        policy = SafetyPolicy()

        result = policy.evaluate(
            "unknown_reason"
        )

        self.assertFalse(result.blocked)
        self.assertEqual(
            result.reason,
            "NO_POLICY_MATCH",
        )

    def test_invalid_event_is_rejected(self):
        policy = SafetyPolicy()

        with self.assertRaises(TypeError):
            policy.observe(None)

    def test_matching_command_pattern_is_blocked(self):
        policy = SafetyPolicy()

        policy.observe(
            SafetyEvent(
                action="move",
                value=(2.0, 0.0),
                reason="move_limit_exceeded",
            )
        )

        command = BodyCommand(
            action="move",
            value=(2.0, 0.0),
        )

        result = policy.evaluate_command(command)

        self.assertTrue(result.blocked)
        self.assertEqual(
            result.reason,
            "POLICY_BLOCK",
        )

    def test_safe_move_is_not_blocked_by_previous_move_limit(self):
        policy = SafetyPolicy()

        policy.observe(
            SafetyEvent(
                action="move",
                value=(2.0, 0.0),
                reason="move_limit_exceeded",
            )
        )

        command = BodyCommand(
            action="move",
            value=(1.0, 0.0),
        )

        result = policy.evaluate_command(command)

        self.assertFalse(result.blocked)
        self.assertEqual(
            result.reason,
            "NO_POLICY_MATCH",
        )

    def test_unrelated_action_is_not_blocked(self):
        policy = SafetyPolicy()

        policy.observe(
            SafetyEvent(
                action="move",
                value=(2.0, 0.0),
                reason="move_limit_exceeded",
            )
        )

        command = BodyCommand(
            action="respond",
            value=None,
        )

        result = policy.evaluate_command(command)

        self.assertFalse(result.blocked)
        self.assertEqual(
            result.reason,
            "NO_POLICY_MATCH",
        )


if __name__ == "__main__":
    unittest.main()
