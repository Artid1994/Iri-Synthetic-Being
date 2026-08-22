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
    def test_multiple_autonomous_steps_require_approval_before_execution(self):
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

        self.assertIsNotNone(first["command"])
        self.assertIsNotNone(first["approval"])
        self.assertEqual(
            first["approval"].state.value,
            "VALIDATED",
        )
        self.assertIsNone(first["feedback"])
        self.assertEqual(hardware.calls, [])

        self.assertTrue(
            runtime.approve_pending_action()
        )

        completed_first = runtime.complete_approved_cycle()

        self.assertIsNotNone(completed_first)

        first_feedback, first_evaluation = completed_first

        self.assertIsInstance(
            first_feedback,
            RobotFeedback,
        )
        self.assertTrue(first_feedback.success)
        self.assertIsNotNone(first_evaluation)

        second = runtime.autonomous_step(
            "person A sees house"
        )

        self.assertIsNotNone(second["command"])
        self.assertIsNotNone(second["approval"])
        self.assertEqual(
            second["approval"].state.value,
            "VALIDATED",
        )
        self.assertIsNone(second["feedback"])

        self.assertEqual(
            hardware.calls,
            [("respond", None)],
        )

        self.assertTrue(
            runtime.approve_pending_action()
        )

        completed_second = runtime.complete_approved_cycle()

        self.assertIsNotNone(completed_second)

        second_feedback, second_evaluation = completed_second

        self.assertIsInstance(
            second_feedback,
            RobotFeedback,
        )
        self.assertTrue(second_feedback.success)
        self.assertIsNotNone(second_evaluation)

        self.assertEqual(
            hardware.calls,
            [
                ("respond", None),
                ("respond", None),
            ],
        )

        self.assertIsNone(
            runtime.pending_approval
        )
        self.assertIsNone(
            runtime.pending_command
        )


if __name__ == "__main__":
    unittest.main()
