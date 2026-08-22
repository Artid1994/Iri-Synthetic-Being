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


class TestRuntimeAutonomousPolicyExecution(unittest.TestCase):

    def test_autonomous_policy_can_approve(self):
        from runtime.runtime import TranscendingRuntime

        hardware = FakeHardware()

        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.robot_adapter = RobotAdapter(hardware)
        runtime.enable_autonomous_mode()
        runtime.autonomous_controller.enable()

        result = runtime.autonomous_step(
            "person sees tree"
        )

        self.assertIsNotNone(
            result["approval"]
        )

        self.assertTrue(
            runtime.approve_pending_action()
        )

        completed = runtime.complete_approved_cycle()

        self.assertIsNotNone(
            completed
        )

        self.assertEqual(
            hardware.calls,
            [("respond", None)],
        )


if __name__ == "__main__":
    unittest.main()
