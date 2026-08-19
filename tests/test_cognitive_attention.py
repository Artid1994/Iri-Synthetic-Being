import unittest

from runtime.cognitive_loop import CognitiveLoop
from tests.cognitive_test_helper import FakeCognitive


class TestCognitiveAttention(unittest.TestCase):
    def _create_loop(self, cognitive):
        from runtime.development import Development
        from runtime.identity import Identity
        from runtime.memory import Memory
        from runtime.learning import Learning
        from runtime.personality import Personality
        from runtime.self_model import SelfModel
        from runtime.prediction import Prediction
        from runtime.identity_continuity import IdentityContinuity

        identity = Identity()
        memory = Memory()
        learning = Learning(memory)
        personality = Personality()
        self_model = SelfModel()

        development = Development(
            identity,
            memory,
            learning,
            personality,
            self_model,
            Prediction(),
            IdentityContinuity(),
        )

        return CognitiveLoop(
            cognitive,
            learning,
            personality,
            self_model,
            development,
        )

    def test_unchanged_input_has_no_attention(self):
        loop = self._create_loop(FakeCognitive())

        loop.process("person A sees tree")
        cycle = loop.process("person A sees tree")

        self.assertFalse(cycle.attention_required)


    def test_changed_input_requires_attention(self):
        loop = self._create_loop(FakeCognitive())

        loop.process("person A sees tree")
        cycle = loop.process("person A sees dog")

        self.assertTrue(cycle.attention_required)


if __name__ == "__main__":
    unittest.main()
