import unittest

from runtime.body_command import BodyCommand
from runtime.robot_adapter import RobotAdapter
from runtime.runtime import TranscendingRuntime
from runtime.safety_event import SafetyEvent


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class TrackingHardware:
    def __init__(self):
        self.calls = []

    def execute(self, action, value):
        self.calls.append((action, value))
        return True


class TestRuntimeLearnedSafetyContract(unittest.TestCase):
    def test_learned_safety_blocks_future_command(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        hardware = TrackingHardware()
        runtime.robot_adapter = RobotAdapter(hardware)
        runtime.autonomous_controller.enable()

        runtime.memory.add_safety_event(
            SafetyEvent(
                action="move",
                value=(2.0, 0.0),
                reason="move_limit_exceeded",
            )
        )

        runtime._sync_safety_policy()

        command = BodyCommand(
            action="move",
            value=(1.0, 0.0),
        )

        self.assertTrue(
            runtime.embodiment.safety_check(command).allowed
        )

        self.assertTrue(
            runtime.safety_policy.evaluate(
                "move_limit_exceeded"
            ).blocked
        )

        result = runtime.act(command)

        self.assertIsNone(result)
        self.assertEqual(hardware.calls, [])


if __name__ == "__main__":
    unittest.main()
