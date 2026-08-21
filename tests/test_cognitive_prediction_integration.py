import unittest

from runtime.cognitive_loop import CognitiveLoop
from runtime.prediction import Prediction


class FakeLearning:
    def create_candidate(self, experience, category, confidence):
        return None

    def evaluate(self, candidate):
        return type(
            "Evaluation",
            (),
            {
                "accepted": False,
                "reason": "NO_CANDIDATE",
            },
        )()


class FakePersonality:
    pass


class FakeSelfModel:
    pass


class FakeDevelopment:
    pass


class TestCognitivePredictionIntegration(unittest.TestCase):
    def test_cognitive_reasoning_is_recorded_as_prediction(self):
        prediction = Prediction()

        class Cognitive:
            def process(self, user_input, record_experience=True):
                return "predicted: tree is near the house"

        loop = CognitiveLoop(
            cognitive=Cognitive(),
            learning=FakeLearning(),
            personality=FakePersonality(),
            self_model=FakeSelfModel(),
            development=FakeDevelopment(),
            prediction=prediction,
        )

        cycle = loop.process("person A sees tree")

        self.assertEqual(
            cycle.reasoning,
            "predicted: tree is near the house",
        )

        self.assertEqual(
            prediction.state.prediction_count,
            1,
        )

        self.assertEqual(
            prediction.state.last_prediction,
            "predicted: tree is near the house",
        )


if __name__ == "__main__":
    unittest.main()
