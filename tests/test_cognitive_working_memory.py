import unittest
from unittest.mock import Mock

from runtime.cognitive_loop import CognitiveLoop
from runtime.learning import Learning
from runtime.memory import Memory
from runtime.personality import Personality
from runtime.self_model import SelfModel
from runtime.development import Development
from runtime.prediction import Prediction
from runtime.identity_continuity import IdentityContinuity


class FakeCognitive:
    def __init__(self):
        self.calls = []

    def think(self, text, context=""):
        self.calls.append((text, context))
        return "RESPOND"


class TestCognitiveWorkingMemory(unittest.TestCase):
    def _create_loop(self):
        memory = Memory()

        development = Development(
            Mock(),
            memory,
            Learning(memory),
            Personality(),
            SelfModel(),
            Prediction(),
            IdentityContinuity(),
        )

        cognitive = FakeCognitive()

        loop = CognitiveLoop(
            cognitive=cognitive,
            learning=Learning(memory),
            personality=Personality(),
            self_model=SelfModel(),
            development=development,
            prediction=Prediction(),
        )

        return loop, cognitive, memory

    def test_attention_input_enters_working_memory(self):
        loop, _, memory = self._create_loop()

        loop.process("tree detected")

        self.assertEqual(
            memory.working_memory(),
            ["tree detected"],
        )

    def test_working_memory_is_available_to_cognitive_context(self):
        loop, cognitive, memory = self._create_loop()

        memory.add_working("tree detected")

        loop.process("person detected")

        _, context = cognitive.calls[-1]

        self.assertIn(
            "tree detected",
            context,
        )

    def test_working_memory_does_not_replace_episodic_memory(self):
        loop, _, memory = self._create_loop()

        loop.process("tree detected")

        self.assertEqual(
            memory.state.episodic,
            ["tree detected"],
        )
        self.assertEqual(
            memory.working_memory(),
            ["tree detected"],
        )


if __name__ == "__main__":
    unittest.main()
