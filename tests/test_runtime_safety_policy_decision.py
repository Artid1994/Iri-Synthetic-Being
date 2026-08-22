import unittest

from runtime.body_command import BodyCommand
from runtime.robot_adapter import RobotAdapter
from runtime.safety_event import SafetyEvent
from runtime.safety_policy import SafetyPolicy


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class TrackingHardware:
    def __init__(self):
        self.calls = []

    def execute(self, action, value):
        self.calls.append((action, value))
        return True


class TestRuntimeSafetyPolicyDecision(unittest.TestCase):
    def test_policy_blocks_matching_reason(self):
        policy = SafetyPolicy()

        policy.observe(
            SafetyEvent(
                action="move",
                value=(1.0, 0.0),
                reason="move_limit_exceeded",
            )
        )

        decision = policy.evaluate("move_limit_exceeded")

        self.assertTrue(decision.blocked)
        self.assertEqual(
            decision.reason,
            "POLICY_BLOCK",
        )

    def test_policy_does_not_override_hard_safety(self):
        from runtime.cognitive_safety_gate import CognitiveSafetyGate

        gate = CognitiveSafetyGate()
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

        hard_safety = gate.evaluate(command)
        policy_decision = policy.evaluate(
            hard_safety.reason
        )

        self.assertFalse(hard_safety.allowed)
        self.assertTrue(policy_decision.blocked)

    def test_runtime_policy_block_must_not_send_robot_command(self):
        from runtime.runtime import TranscendingRuntime

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        hardware = TrackingHardware()

        runtime.robot_adapter = RobotAdapter(
            hardware
        )

        runtime.autonomous_controller.enable()

        runtime.memory.add_safety_event(
            SafetyEvent(
                action="move",
                value=(1.0, 0.0),
                reason="move_limit_exceeded",
            )
        )

        runtime._sync_safety_policy()

        command = BodyCommand(
            action="move",
            value=(1.0, 0.0),
        )

        policy_decision = runtime.safety_policy.evaluate(
            "move_limit_exceeded"
        )

        self.assertTrue(policy_decision.blocked)

        self.assertTrue(
            runtime.autonomous_controller.allowed(command)
        )

        self.assertEqual(
            hardware.calls,
            [],
        )


if __name__ == "__main__":
    unittest.main()
