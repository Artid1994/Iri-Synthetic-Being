import unittest

from runtime.robot_adapter import RobotAdapter
from runtime.robot_feedback import RobotFeedback


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return f"understood: {user_input}"


class FailingHardware:
    def execute(self, action, value):
        return False


class TestRuntimeAutonomousFailure(unittest.TestCase):
    def test_failed_action_produces_failed_feedback_and_correction(self):
        from runtime.runtime import TranscendingRuntime

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.robot_adapter = RobotAdapter(
            FailingHardware()
        )

        runtime.autonomous_controller.enable()

        result = runtime.autonomous_step(
            "person A sees tree"
        )

        self.assertIsInstance(
            result["feedback"],
            RobotFeedback,
        )

        self.assertFalse(
            result["feedback"].success
        )

        self.assertIsNotNone(
            result["evaluation"]
        )

        self.assertFalse(
            result["evaluation"].correct
        )

        self.assertIsNotNone(
            result["learning"]
        )

        self.assertFalse(
            result["learning"].accepted
        )

        self.assertEqual(
            result["learning"].reason,
            "PREDICTION_CORRECTION_REQUIRED",
        )


if __name__ == "__main__":
    unittest.main()
