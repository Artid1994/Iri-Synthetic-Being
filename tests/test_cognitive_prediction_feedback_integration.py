import unittest

from runtime.cognitive_loop import CognitiveLoop
from runtime.memory import Memory
from runtime.learning import Learning
from runtime.prediction import Prediction
from runtime.prediction import PredictionEvaluation


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"


class FakePersonality:
    def adapt(self, **kwargs):
        pass


class FakeSelfModel:
    def update(self, **kwargs):
        pass


class FakeDevelopment:
    def sync(self):
        pass


class TestCognitivePredictionFeedbackIntegration(unittest.TestCase):
    def test_prediction_outcome_can_flow_into_learning(self):
        prediction = Prediction()
        learning = Learning(Memory())

        loop = CognitiveLoop(
            cognitive=FakeCognitive(),
            learning=learning,
            personality=FakePersonality(),
            self_model=FakeSelfModel(),
            development=FakeDevelopment(),
            prediction=prediction,
        )

        cycle = loop.process("person A sees tree")

        self.assertEqual(
            cycle.reasoning,
            "tree is near the house",
        )

        evaluation = prediction.evaluate(
            "tree is near the house"
        )

        result = learning.learn_from_prediction(
            prediction.state.last_prediction,
            evaluation,
        )

        self.assertTrue(result.accepted)
        self.assertEqual(
            result.reason,
            "PREDICTION_CONFIRMED",
        )


if __name__ == "__main__":
    unittest.main()
