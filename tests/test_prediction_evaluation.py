import unittest

from runtime.prediction import Prediction


class TestPredictionEvaluation(unittest.TestCase):
    def test_prediction_can_be_evaluated_as_correct(self):
        prediction = Prediction()

        prediction.record("tree is near the house")

        result = prediction.evaluate(
            "tree is near the house"
        )

        self.assertTrue(result.correct)
        self.assertEqual(
            result.reason,
            "PREDICTION_MATCHED_OUTCOME",
        )

    def test_prediction_can_be_evaluated_as_incorrect(self):
        prediction = Prediction()

        prediction.record("tree is near the house")

        result = prediction.evaluate(
            "tree is far from the house"
        )

        self.assertFalse(result.correct)
        self.assertEqual(
            result.reason,
            "PREDICTION_DID_NOT_MATCH_OUTCOME",
        )

    def test_prediction_without_recorded_prediction_is_unknown(self):
        prediction = Prediction()

        result = prediction.evaluate(
            "tree is near the house"
        )

        self.assertIsNone(result.correct)
        self.assertEqual(
            result.reason,
            "NO_PREDICTION",
        )


if __name__ == "__main__":
    unittest.main()
