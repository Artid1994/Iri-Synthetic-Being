import unittest

from runtime.learning import Learning
from runtime.memory import Memory
from runtime.prediction import PredictionEvaluation


class TestPredictionLearningMemory(unittest.TestCase):
    def test_confirmed_prediction_is_stored_as_experience(self):
        memory = Memory()
        learning = Learning(memory)

        result = learning.learn_from_prediction(
            "tree is near the house",
            PredictionEvaluation(
                correct=True,
                reason="PREDICTION_MATCHED_OUTCOME",
            ),
        )

        self.assertTrue(result.accepted)
        self.assertEqual(
            len(memory.state.episodic),
            1,
        )
        self.assertEqual(
            memory.state.episodic[0],
            "tree is near the house",
        )

    def test_failed_prediction_is_not_stored_as_confirmed_experience(self):
        memory = Memory()
        learning = Learning(memory)

        result = learning.learn_from_prediction(
            "tree is near the house",
            PredictionEvaluation(
                correct=False,
                reason="PREDICTION_DID_NOT_MATCH_OUTCOME",
            ),
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            len(memory.state.episodic),
            0,
        )


if __name__ == "__main__":
    unittest.main()
