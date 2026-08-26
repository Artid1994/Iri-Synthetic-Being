import unittest

from runtime.cognitive_loop import CognitiveLoop
from runtime.learning import Learning
from runtime.memory import Memory
from runtime.prediction import Prediction
from runtime.robot_feedback import RobotFeedback


class FakeCognitive:
    def think(self, text, context=""):
        return "tree is near the house"


class FakePersonality:
    def adapt(self, **kwargs):
        pass


class FakeSelfModel:
    def snapshot(self):
        class State:
            self_awareness = 0.0
            self_knowledge = 0.0
            self_history = ()

        return State()

    def update(self, **kwargs):
        pass


class FakeDevelopment:
    def __init__(self, memory):
        self.memory = memory

        class Identity:
            def snapshot(self):
                class State:
                    stage = "NEWBORN"
                    experience = 0

                return State()

        self.identity = Identity()

    def sync(self):
        pass


class TestCognitiveClosedLoop(unittest.TestCase):
    def test_prediction_flows_from_cognition_to_feedback_learning(self):
        memory = Memory()
        learning = Learning(memory)
        prediction = Prediction()

        loop = CognitiveLoop(
            cognitive=FakeCognitive(),
            learning=learning,
            personality=FakePersonality(),
            self_model=FakeSelfModel(),
            development=FakeDevelopment(memory),
            prediction=prediction,
        )

        cycle = loop.process("observe the tree")

        self.assertEqual(
            cycle.reasoning,
            "tree is near the house",
        )

        self.assertEqual(
            prediction.state.last_prediction,
            "tree is near the house",
        )

        feedback = RobotFeedback(
            success=True,
            action="observe",
            value="tree is near the house",
        )

        evaluation = prediction.evaluate(
            str(feedback.value)
        )

        result = learning.learn_from_prediction(
            prediction.state.last_prediction,
            evaluation,
        )

        self.assertTrue(evaluation.correct)
        self.assertTrue(result.accepted)
        self.assertEqual(
            result.reason,
            "PREDICTION_CONFIRMED",
        )

        self.assertIn(
            "tree is near the house",
            memory.state.episodic,
        )


if __name__ == "__main__":
    unittest.main()
