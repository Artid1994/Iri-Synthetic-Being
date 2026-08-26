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
    def think(self, text, context=""):
        return "RESPOND"


class TestCognitiveMemoryConsolidation(unittest.TestCase):
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

        loop = CognitiveLoop(
            cognitive=FakeCognitive(),
            learning=Learning(memory),
            personality=Personality(),
            self_model=SelfModel(),
            development=development,
            prediction=Prediction(),
        )

        return loop, memory

    def test_accepted_learning_consolidates_to_episodic_memory(self):
        loop, memory = self._create_loop()

        loop.process("tree detected")

        self.assertEqual(
            memory.state.episodic,
            ["tree detected"],
        )

    def test_rejected_learning_does_not_consolidate(self):
        loop, memory = self._create_loop()

        loop.learning.evaluate = Mock(
            return_value=Mock(accepted=False)
        )

        loop.process("tree detected")

        self.assertEqual(
            memory.state.episodic,
            [],
        )


    def test_accepted_learning_records_one_episodic_event_per_cycle(self):
        loop, memory = self._create_loop()

        loop.process("tree detected")

        self.assertEqual(
            memory.state.episodic.count("tree detected"),
            1,
        )


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
