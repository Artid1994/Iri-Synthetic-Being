import unittest

from runtime.robot_adapter import RobotAdapter
from runtime.robot_feedback import RobotFeedback


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class FakeHardware:
    def execute(self, action, value):
        return True


class TestRuntimeAutonomousStep(unittest.TestCase):
    def test_autonomous_step_completes_one_closed_cycle(self):
        from runtime.runtime import TranscendingRuntime

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.robot_adapter = RobotAdapter(
            FakeHardware()
        )

        runtime.autonomous_controller.enable()

        result = runtime.autonomous_step(
            "person A sees tree"
        )

        self.assertIsNotNone(result)
        self.assertEqual(
            result["reasoning"],
            "tree is near the house",
        )
        self.assertIsNotNone(result["command"])
        self.assertIsInstance(
            result["feedback"],
            RobotFeedback,
        )
        self.assertTrue(
            result["feedback"].success
        )
        self.assertIsNotNone(
            result["evaluation"]
        )
        self.assertTrue(
            result["evaluation"].correct
        )
        self.assertTrue(
            result["learning"].accepted
        )


if __name__ == "__main__":
    unittest.main()
