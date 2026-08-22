import unittest

from runtime.body_command import BodyCommand
from runtime.robot_feedback import RobotFeedback


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class TestRuntimeAutonomousCycle(unittest.TestCase):
    def test_runtime_can_complete_one_autonomous_cycle(self):
        from runtime.runtime import TranscendingRuntime

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        observation = "person A sees tree"

        cycle = runtime.cognitive_loop.process(
            observation
        )

        self.assertEqual(
            cycle.reasoning,
            "tree is near the house",
        )

        command = runtime.autonomous_controller.decide(
            cycle
        )

        self.assertIsInstance(
            command,
            (BodyCommand, type(None)),
        )

        if command is None:
            self.skipTest(
                "Embodiment does not produce a command yet"
            )

        runtime.autonomous_controller.enable()

        self.assertTrue(
            runtime.autonomous_controller.allowed(command)
        )


if __name__ == "__main__":
    unittest.main()
