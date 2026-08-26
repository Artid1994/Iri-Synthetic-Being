import unittest

from runtime.cognitive_loop import CognitiveLoop
from runtime.development import Development
from runtime.identity import Identity
from runtime.identity_continuity import IdentityContinuity
from runtime.learning import Learning
from runtime.memory import Memory
from runtime.personality import Personality
from runtime.prediction import Prediction
from runtime.reflection import Reflection
from runtime.self_model import SelfModel


class FakeCognitive:
    def think(self, text, context=""):
        return "RESPOND"


class TestCognitiveReflectionState(unittest.TestCase):
    def _create_loop(self):
        memory = Memory()
        learning = Learning(memory)

        development = Development(
            Identity(),
            memory,
            learning,
            Personality(),
            SelfModel(),
            Prediction(),
            IdentityContinuity(),
        )

        return CognitiveLoop(
            cognitive=FakeCognitive(),
            learning=learning,
            personality=Personality(),
            self_model=SelfModel(),
            development=development,
            prediction=Prediction(),
            reflection=Reflection(),
        )

    def test_reflection_starts_empty(self):
        loop = self._create_loop()

        self.assertIsNone(loop.last_reflection)

    def test_reflection_state_can_be_stored(self):
        loop = self._create_loop()

        result = loop.reflection.reflect(
            "SUCCESS",
            observation="tree detected",
            task_topic="tree detection",
        )

        loop.last_reflection = result

        self.assertIs(loop.last_reflection, result)
        self.assertEqual(
            loop.last_reflection.lesson,
            "tree detected",
        )


if __name__ == "__main__":
    unittest.main()
