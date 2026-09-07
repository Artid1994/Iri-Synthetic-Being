import unittest

from runtime.cognitive_loop import CognitiveLoop
from tests.cognitive_test_helper import FakeCognitive


class TestCognitiveLoopTrigger(unittest.TestCase):
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

    def test_empty_input_does_not_trigger_cognition(self):
        calls = []

        class TrackingCognitive(FakeCognitive):
            def process(self, user_input, record_experience=False):
                calls.append(user_input)
                return super().process(
                    user_input,
                    record_experience,
                )

        loop = self._create_loop(TrackingCognitive())

        loop.process("")

        self.assertEqual(calls, [])


    def test_non_empty_input_triggers_cognition(self):
        calls = []

        class TrackingCognitive(FakeCognitive):
            def process(self, user_input, record_experience=False):
                calls.append(user_input)
                return super().process(
                    user_input,
                    record_experience,
                )

        loop = self._create_loop(TrackingCognitive())

        loop.process("person A sees tree")

        self.assertEqual(calls, ["person A sees tree"])


    def test_repeated_input_does_not_trigger_cognition_twice(self):
        calls = []

        class TrackingCognitive(FakeCognitive):
            def process(self, user_input, record_experience=False):
                calls.append(user_input)
                return super().process(
                    user_input,
                    record_experience,
                )

        loop = self._create_loop(TrackingCognitive())

        loop.process("person A sees tree")
        loop.process("person A sees tree")

        self.assertEqual(
            calls,
            ["person A sees tree"],
        )


    def test_changed_input_triggers_cognition_again(self):
        calls = []

        class TrackingCognitive(FakeCognitive):
            def process(self, user_input, record_experience=False):
                calls.append(user_input)
                return super().process(
                    user_input,
                    record_experience,
                )

        loop = self._create_loop(TrackingCognitive())

        loop.process("person A sees tree")
        loop.process("person A sees dog")

        self.assertEqual(
            calls,
            [
                "person A sees tree",
                "person A sees dog",
            ],
        )


    def test_associative_recall_flows_into_cognitive_context(self):
        class TrackingCognitive(FakeCognitive):
            def __init__(self):
                self.contexts = []

            def think(self, text, context=""):
                self.contexts.append(context)
                return "recalled response"

        cognitive = TrackingCognitive()
        loop = self._create_loop(cognitive)


        loop.development.memory.add_experience("ฉันชอบสีแดง")

        loop.process("สีโปรดของฉันคืออะไร")

        self.assertEqual(len(cognitive.contexts), 1)
        self.assertIn(
            "RECALLED_MEMORY:\n- ฉันชอบสีแดง",
            cognitive.contexts[0],
        )


if __name__ == "__main__":
    unittest.main()
