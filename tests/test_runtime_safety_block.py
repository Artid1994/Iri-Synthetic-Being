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


class TestRuntimeSafetyBlock(unittest.TestCase):
    def test_blocked_command_is_not_sent_to_robot_and_is_remembered(self):
        from runtime.runtime import TranscendingRuntime

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        hardware = TrackingHardware()

        runtime.robot_adapter = RobotAdapter(
            hardware
        )

        runtime.autonomous_controller.enable()

        blocked_command = BodyCommand(
            action="move",
            value=(2.0, 0.0),
        )

        result = runtime.act(blocked_command)

        self.assertIsNone(result)

        self.assertEqual(
            hardware.calls,
            [],
        )

        events = runtime.memory.state.safety_events

        self.assertEqual(
            len(events),
            1,
        )

        event = events[0]

        self.assertEqual(
            event.action,
            "move",
        )

        self.assertEqual(
            event.value,
            (2.0, 0.0),
        )

        self.assertEqual(
            event.reason,
            "move_limit_exceeded",
        )


if __name__ == "__main__":
    unittest.main()
