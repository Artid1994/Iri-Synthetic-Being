import unittest

from runtime.robot_adapter import RobotAdapter
from runtime.robot_feedback import RobotFeedback


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class FailingHardware:
    def __init__(self):
        self.calls = []

    def execute(self, action, value):
        self.calls.append((action, value))
        return False


class TestRuntimeApprovedAutonomousFailure(unittest.TestCase):
    def test_approved_hardware_failure_reaches_feedback_and_evaluation(self):
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

        self.assertIsNotNone(result["approval"])
        self.assertEqual(
            result["approval"].state.value,
            "VALIDATED",
        )
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
        self.assertFalse(feedback.success)
        self.assertEqual(
            feedback.error,
            "hardware execution failed",
        )

        self.assertIsNotNone(evaluation)
        self.assertFalse(evaluation.correct)

        self.assertEqual(
            hardware.calls,
            [("respond", None)],
        )

        self.assertIsNone(
            runtime.pending_approval
        )
        self.assertIsNone(
            runtime.pending_command
        )


if __name__ == "__main__":
    unittest.main()
