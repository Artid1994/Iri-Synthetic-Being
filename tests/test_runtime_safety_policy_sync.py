import unittest

from runtime.body_command import BodyCommand
from runtime.robot_adapter import RobotAdapter


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class TrackingHardware:
    def __init__(self):
        self.calls = []

    def execute(self, action, value):
        self.calls.append((action, value))
        return True


class TestRuntimeSafetyPolicySync(unittest.TestCase):
    def test_blocked_command_updates_safety_policy(self):
        from runtime.runtime import TranscendingRuntime

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        hardware = TrackingHardware()

        runtime.robot_adapter = RobotAdapter(
            hardware
        )

        runtime.autonomous_controller.enable()

        command = BodyCommand(
            action="move",
            value=(2.0, 0.0),
        )

        result = runtime.act(command)

        self.assertIsNone(result)
        self.assertEqual(hardware.calls, [])

        self.assertEqual(
            runtime.memory.state.safety_events[0].reason,
            "move_limit_exceeded",
        )

        runtime._sync_safety_policy()

        self.assertEqual(
            runtime.safety_policy.snapshot(),
            ("move_limit_exceeded",),
        )

        self.assertEqual(
            runtime.safety_policy.snapshot(),
            ("move_limit_exceeded",),
        )

        policy_result = runtime.safety_policy.evaluate(
            "move_limit_exceeded"
        )

        self.assertTrue(policy_result.blocked)
        self.assertEqual(
            policy_result.reason,
            "POLICY_BLOCK",
        )


if __name__ == "__main__":
    unittest.main()
