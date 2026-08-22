import unittest

from runtime.robot_adapter import RobotAdapter
from runtime.robot_feedback import RobotFeedback


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class FakeHardware:
    def execute(self, action, value):
        return True


class TestRuntimeClosedAutonomousCycle(unittest.TestCase):
    def test_runtime_can_complete_closed_autonomous_cycle(self):
        from runtime.runtime import TranscendingRuntime

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

        self.assertIsNotNone(command)

        runtime.autonomous_controller.enable()

        feedback = runtime.act(command)

        self.assertIsInstance(
            feedback,
            RobotFeedback,
        )

        evaluation = runtime.process_feedback(
            feedback
        )

        self.assertIsNotNone(evaluation)


if __name__ == "__main__":
    unittest.main()
