import unittest
from unittest.mock import Mock

from runtime.autonomous_learning import AutonomousLearningResult
from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestCognitiveSelfDirectedCycle(unittest.TestCase):
    def test_reflection_task_enters_runtime_queue(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        result = runtime.create_self_directed_task(
            "ESP32 BLE"
        )

        self.assertIsNotNone(result)
        self.assertEqual(
            result.status,
            "PENDING",
        )

        queued = runtime.self_directed_learning.next_task()

        self.assertIs(queued, result)

    def test_completed_self_directed_task_can_generate_new_cycle(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        task = runtime.create_self_directed_task(
            "Python"
        )

        self.assertIsNotNone(task)

        runtime.autonomous_learning.learn = Mock(
            return_value=AutonomousLearningResult(
                topic="Python",
                status="COMPLETED",
                reason="CONFIDENCE_THRESHOLD_MET",
                memory_updated=True,
            )
        )

        result = runtime.run_next_self_directed_task()

        self.assertIsNotNone(result)
        self.assertEqual(
            result.task.topic,
            "Python",
        )

        self.assertEqual(
            result.learning_result.status,
            "COMPLETED",
        )

    def test_empty_self_directed_queue_is_safe(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        result = runtime.run_next_self_directed_task()

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
