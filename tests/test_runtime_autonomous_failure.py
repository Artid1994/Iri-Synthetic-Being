import unittest

from runtime.robot_adapter import RobotAdapter
from runtime.robot_feedback import RobotFeedback


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return f"understood: {user_input}"


class FailingHardware:
    def __init__(self):
        self.calls = []

    def execute(self, action, value):
        self.calls.append((action, value))
        return False


class TestRuntimeAutonomousFailure(unittest.TestCase):
    def test_failed_action_requires_approval_then_produces_failed_feedback(self):
        from runtime.runtime import TranscendingRuntime

        hardware = FailingHardware()

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.robot_adapter = RobotAdapter(hardware)
        runtime.autonomous_controller.enable()

        result = runtime.autonomous_step(
            "person A sees tree"
        )

        self.assertIsNotNone(result["command"])
        self.assertIsNotNone(result["approval"])
        self.assertEqual(
            result["approval"].state.value,
            "VALIDATED",
        )

        self.assertIsNone(result["feedback"])
        self.assertEqual(hardware.calls, [])

        self.assertTrue(
            runtime.approve_pending_action()
        )

        completed = runtime.complete_approved_cycle()

        self.assertIsNotNone(completed)

        feedback, evaluation = completed

        self.assertIsInstance(
            feedback,
            RobotFeedback,
        )

        self.assertFalse(
            feedback.success
        )

        self.assertIsNotNone(
            evaluation
        )

        self.assertFalse(
            evaluation.correct
        )

        self.assertIsNotNone(
            runtime.learning.last_evaluation
        )

        self.assertFalse(
            runtime.learning.last_evaluation.accepted
        )

        self.assertEqual(
            runtime.learning.last_evaluation.reason,
            "PREDICTION_CORRECTION_REQUIRED",
        )

        self.assertEqual(
            hardware.calls,
            [("respond", None)],
        )


if __name__ == "__main__":
    unittest.main()
