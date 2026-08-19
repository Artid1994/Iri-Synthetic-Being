import unittest

from runtime.cognitive_loop import CognitiveLoop
from tests.cognitive_test_helper import FakeCognitive


class TestCognitiveSalience(unittest.TestCase):
    def _create_loop(self):
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
            FakeCognitive(),
            learning,
            personality,
            self_model,
            development,
        )

    def test_new_input_has_high_salience(self):
        loop = self._create_loop()

        cycle = loop.process("person A sees tree")

        self.assertGreater(cycle.salience, 0.0)
        self.assertLessEqual(cycle.salience, 1.0)


    def test_unchanged_input_has_zero_salience(self):
        loop = self._create_loop()

        loop.process("person A sees tree")
        cycle = loop.process("person A sees tree")

        self.assertEqual(cycle.salience, 0.0)


    def test_salience_threshold_allows_cognition(self):
        loop = self._create_loop()

        cycle = loop.process("person A sees a large tree near the house")

        self.assertGreaterEqual(cycle.salience, 0.5)
        self.assertTrue(cycle.attention_required)
        self.assertEqual(cycle.decision, "RESPOND")


    def test_longer_new_input_can_have_higher_salience(self):
        loop = self._create_loop()

        cycle = loop.process(
            "person A sees a large tree near the house"
        )

        self.assertGreater(cycle.salience, 0.0)
        self.assertLessEqual(cycle.salience, 1.0)


    def test_longer_input_has_higher_salience(self):
        loop = self._create_loop()

        short_cycle = loop.process("tree")
        long_cycle = loop.process(
            "person A sees a large tree near the house"
        )

        self.assertGreater(
            long_cycle.salience,
            short_cycle.salience,
        )


    def test_salience_is_bounded_to_one(self):
        loop = self._create_loop()

        cycle = loop.process("x" * 128)

        self.assertLessEqual(cycle.salience, 1.0)


if __name__ == "__main__":
    unittest.main()
