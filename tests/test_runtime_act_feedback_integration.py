import unittest

from runtime.body_command import BodyCommand
from runtime.robot_feedback import RobotFeedback


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class FakeHardware:
    def execute(self, action, value):
        return True


class TestRuntimeActFeedbackIntegration(unittest.TestCase):
    def test_runtime_can_act_and_return_feedback(self):
        from runtime.runtime import TranscendingRuntime
        from runtime.robot_adapter import RobotAdapter

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.robot_adapter = RobotAdapter(
            FakeHardware()
        )

        cycle = runtime.cognitive_loop.process(
            "person A sees tree"
        )

        command = runtime.autonomous_controller.decide(
            cycle
        )

        self.assertIsInstance(command, BodyCommand)

        runtime.autonomous_controller.enable()

        self.assertTrue(
            runtime.autonomous_controller.allowed(command)
        )

        result = runtime.robot_adapter.execute(
            command
        )

        feedback = RobotFeedback(
            success=result.success,
            action=result.action,
            value=result.value,
            error=result.error,
        )

        self.assertTrue(feedback.success)
        self.assertEqual(
            feedback.action,
            command.action,
        )


if __name__ == "__main__":
    unittest.main()
