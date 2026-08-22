import unittest

from runtime.runtime import TranscendingRuntime
from runtime.robot_feedback import RobotFeedback


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"

    def snapshot(self):
        return {}


class TestRuntimePredictionFeedback(unittest.TestCase):
    def test_feedback_is_processed_by_runtime(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.prediction.record("tree is near the house")

        feedback = RobotFeedback(
            success=True,
            action="observe",
            value="tree is near the house",
        )

        result = runtime.process_feedback(feedback)

        self.assertTrue(result.correct)
        self.assertEqual(
            result.reason,
            "PREDICTION_MATCHED_OUTCOME",
        )

        learning = runtime.learning.snapshot()["last_evaluation"]

        self.assertTrue(learning.accepted)
        self.assertEqual(
            learning.reason,
            "PREDICTION_CONFIRMED",
        )


if __name__ == "__main__":
    unittest.main()
