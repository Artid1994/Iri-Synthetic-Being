import unittest

from runtime.robot_adapter import RobotAdapter


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class FakeHardware:
    def __init__(self):
        self.calls = []

    def execute(self, action, value):
        self.calls.append((action, value))
        return True


class TestRuntimeAutonomousStep(unittest.TestCase):
    def test_autonomous_step_stops_at_human_approval(self):
        from runtime.runtime import TranscendingRuntime

        hardware = FakeHardware()

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.robot_adapter = RobotAdapter(hardware)
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
        self.assertIsNotNone(result["approval"])
        self.assertEqual(
            result["approval"].state.value,
            "VALIDATED",
        )

        self.assertIsNone(result["feedback"])
        self.assertIsNone(result["evaluation"])
        self.assertIsNone(result["learning"])

        self.assertEqual(
            hardware.calls,
            [],
        )

        self.assertTrue(
            runtime.approve_pending_action()
        )

        completed = runtime.complete_approved_cycle()

        self.assertIsNotNone(completed)

        feedback, evaluation = completed

        self.assertTrue(feedback.success)
        self.assertIsNotNone(evaluation)

        self.assertEqual(
            hardware.calls,
            [("respond", None)],
        )


if __name__ == "__main__":
    unittest.main()
