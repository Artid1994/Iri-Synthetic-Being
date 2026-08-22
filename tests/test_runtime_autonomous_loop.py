import unittest

from runtime.robot_adapter import RobotAdapter
from runtime.robot_feedback import RobotFeedback


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return f"understood: {user_input}"


class FakeHardware:
    def __init__(self):
        self.calls = []

    def execute(self, action, value):
        self.calls.append((action, value))
        return True


class TestRuntimeAutonomousLoop(unittest.TestCase):
    def test_multiple_autonomous_steps_process_new_observations(self):
        from runtime.runtime import TranscendingRuntime

        hardware = FakeHardware()

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )
        runtime.robot_adapter = RobotAdapter(hardware)
        runtime.autonomous_controller.enable()

        first = runtime.autonomous_step(
            "person A sees tree"
        )

        second = runtime.autonomous_step(
            "person A sees house"
        )

        self.assertIsInstance(
            first["feedback"],
            RobotFeedback,
        )
        self.assertTrue(
            first["feedback"].success
        )
        self.assertTrue(
            first["evaluation"].correct
        )
        self.assertTrue(
            first["learning"].accepted
        )

        self.assertIsInstance(
            second["feedback"],
            RobotFeedback,
        )
        self.assertTrue(
            second["feedback"].success
        )
        self.assertTrue(
            second["evaluation"].correct
        )
        self.assertTrue(
            second["learning"].accepted
        )

        self.assertEqual(
            len(hardware.calls),
            2,
        )


if __name__ == "__main__":
    unittest.main()
