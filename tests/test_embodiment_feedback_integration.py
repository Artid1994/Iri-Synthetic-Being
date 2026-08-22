import unittest

from runtime.body_command import BodyCommand
from runtime.embodiment import EmbodimentLoop
from runtime.robot_feedback import RobotFeedback
from runtime.virtual_body import VirtualBody


class TestEmbodimentFeedbackIntegration(unittest.TestCase):
    def test_command_can_produce_feedback(self):
        embodiment = EmbodimentLoop(VirtualBody())

        command = BodyCommand(
            action="move",
            value=(1.0, 0.0),
        )

        embodiment.autonomous_gate.enabled = True

        self.assertTrue(
            embodiment.autonomous_allowed(command)
        )

        result = embodiment.execute_command(command)

        self.assertIsNotNone(result)

        feedback = RobotFeedback(
            success=True,
            action=command.action,
            value=command.value,
        )

        received = embodiment.ingest_feedback(feedback)

        self.assertIs(received, feedback)
        self.assertTrue(received.success)
        self.assertEqual(received.action, "move")
        self.assertEqual(received.value, (1.0, 0.0))


if __name__ == "__main__":
    unittest.main()
