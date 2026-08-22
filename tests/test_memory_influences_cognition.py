import unittest

from runtime.learning import Learning
from runtime.memory import Memory
from runtime.prediction import PredictionEvaluation


class TestMemoryInfluencesCognition(unittest.TestCase):
    def test_confirmed_prediction_is_recallable_for_future_cognition(self):
        memory = Memory()
        learning = Learning(memory)

        learning.learn_from_prediction(
            "tree is near the house",
            PredictionEvaluation(
                correct=True,
                reason="PREDICTION_MATCHED_OUTCOME",
            ),
        )

        recalled = memory.recall(
            "tree is near the house"
        )

        self.assertEqual(
            recalled,
            "tree is near the house",
        )


if __name__ == "__main__":
    unittest.main()
