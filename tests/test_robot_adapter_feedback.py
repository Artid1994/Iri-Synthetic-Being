import unittest

from runtime.body_command import BodyCommand
from runtime.execution_result import ExecutionResult
from runtime.robot_adapter import RobotAdapter
from runtime.robot_feedback import RobotFeedback


class FakeHardware:
    def execute(self, action, value):
        return True


class TestRobotAdapterFeedback(unittest.TestCase):
    def test_successful_execution_can_become_robot_feedback(self):
        adapter = RobotAdapter(FakeHardware())

        command = BodyCommand(
            action="respond",
            value=None,
        )

        result = adapter.execute(command)

        self.assertIsInstance(result, ExecutionResult)
        self.assertTrue(result.success)

        feedback = RobotFeedback(
            success=result.success,
            action=result.action,
            value=result.value,
            error=result.error,
        )

        self.assertTrue(feedback.success)
        self.assertEqual(feedback.action, "respond")


if __name__ == "__main__":
    unittest.main()
