import unittest
from unittest.mock import Mock

from runtime.autonomous_learning import AutonomousLearningResult
from runtime.learning_task import LearningTask
from runtime.runtime import TranscendingRuntime


class TestRuntimeSelfDirectedLearning(unittest.TestCase):
    def test_runtime_can_run_next_self_directed_task(self):
        runtime = TranscendingRuntime(
            cognitive=Mock()
        )

        runtime.self_directed_learning.create_task(
            "ESP32 BLE"
        )

        runtime.autonomous_learning.learn = Mock(
            return_value=AutonomousLearningResult(
                topic="ESP32 BLE",
                status="COMPLETED",
                reason="CONFIDENCE_THRESHOLD_MET",
                memory_updated=True,
            )
        )

        result = runtime.run_next_self_directed_task()

        self.assertIsNotNone(result)
        self.assertIsInstance(
            result.task,
            LearningTask,
        )
        self.assertEqual(
            result.task.topic,
            "ESP32 BLE",
        )
        self.assertEqual(
            result.learning_result.status,
            "COMPLETED",
        )

        runtime.autonomous_learning.learn.assert_called_once()

    def test_runtime_without_pending_task_returns_none(self):
        runtime = TranscendingRuntime(
            cognitive=Mock()
        )

        result = runtime.run_next_self_directed_task()

        self.assertIsNone(result)

    def test_active_task_is_not_consumed_twice(self):
        runtime = TranscendingRuntime(
            cognitive=Mock()
        )

        runtime.self_directed_learning.create_task(
            "Python"
        )

        runtime.autonomous_learning.learn = Mock(
            return_value=AutonomousLearningResult(
                topic="Python",
                status="COMPLETED",
                reason="CONFIDENCE_THRESHOLD_MET",
                memory_updated=True,
            )
        )

        first = runtime.run_next_self_directed_task()
        second = runtime.run_next_self_directed_task()

        self.assertIsNotNone(first)
        self.assertIsNone(second)

        self.assertEqual(
            runtime.autonomous_learning.learn.call_count,
            1,
        )


if __name__ == "__main__":
    unittest.main()
