import unittest

from runtime.body_command import BodyCommand
from runtime.robot_feedback import RobotFeedback


class FakeHardware:
    def execute(self, action, value):
        return True


class TestRuntimeAct(unittest.TestCase):
    def test_runtime_act_returns_feedback(self):
        from runtime.runtime import TranscendingRuntime
        from runtime.robot_adapter import RobotAdapter

        runtime = TranscendingRuntime()
        runtime.robot_adapter = RobotAdapter(FakeHardware())
        runtime.autonomous_controller.enable()

        command = BodyCommand(
            action="respond",
            value=None,
        )

        feedback = runtime.act(command)

        self.assertIsInstance(
            feedback,
            RobotFeedback,
        )
        self.assertTrue(feedback.success)
        self.assertEqual(feedback.action, "respond")


if __name__ == "__main__":
    unittest.main()
