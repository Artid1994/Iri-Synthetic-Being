import unittest

from runtime.learning import Learning
from runtime.memory import Memory
from runtime.prediction import PredictionEvaluation


class TestPredictionLearningFeedback(unittest.TestCase):
    def test_correct_prediction_creates_learning_feedback(self):
        learning = Learning(Memory())

        result = learning.learn_from_prediction(
            "tree is near the house",
            PredictionEvaluation(
                correct=True,
                reason="PREDICTION_MATCHED_OUTCOME",
            ),
        )

        self.assertTrue(result.accepted)
        self.assertEqual(
            result.reason,
            "PREDICTION_CONFIRMED",
        )

    def test_incorrect_prediction_creates_learning_feedback(self):
        learning = Learning(Memory())

        result = learning.learn_from_prediction(
            "tree is near the house",
            PredictionEvaluation(
                correct=False,
                reason="PREDICTION_DID_NOT_MATCH_OUTCOME",
            ),
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.reason,
            "PREDICTION_CORRECTION_REQUIRED",
        )

    def test_unknown_prediction_is_not_learned(self):
        learning = Learning(Memory())

        result = learning.learn_from_prediction(
            "tree is near the house",
            PredictionEvaluation(
                correct=None,
                reason="NO_PREDICTION",
            ),
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.reason,
            "PREDICTION_OUTCOME_UNKNOWN",
        )


if __name__ == "__main__":
    unittest.main()
