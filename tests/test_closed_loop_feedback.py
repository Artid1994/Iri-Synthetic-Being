import unittest

from runtime.learning import Learning
from runtime.memory import Memory
from runtime.prediction import Prediction
from runtime.robot_feedback import RobotFeedback


class TestClosedLoopFeedback(unittest.TestCase):
    def test_successful_feedback_confirms_prediction(self):
        prediction = Prediction()
        learning = Learning(Memory())

        prediction.record("tree is near the house")

        feedback = RobotFeedback(
            success=True,
            action="observe",
            value="tree is near the house",
        )

        evaluation = prediction.evaluate(str(feedback.value))
        result = learning.learn_from_prediction(
            "tree is near the house",
            evaluation,
        )

        self.assertTrue(evaluation.correct)
        self.assertTrue(result.accepted)
        self.assertEqual(
            result.reason,
            "PREDICTION_CONFIRMED",
        )

    def test_failed_feedback_requires_correction(self):
        prediction = Prediction()
        learning = Learning(Memory())

        prediction.record("tree is near the house")

        feedback = RobotFeedback(
            success=True,
            action="observe",
            value="tree is far from the house",
        )

        evaluation = prediction.evaluate(str(feedback.value))
        result = learning.learn_from_prediction(
            "tree is near the house",
            evaluation,
        )

        self.assertFalse(evaluation.correct)
        self.assertFalse(result.accepted)
        self.assertEqual(
            result.reason,
            "PREDICTION_CORRECTION_REQUIRED",
        )


if __name__ == "__main__":
    unittest.main()
