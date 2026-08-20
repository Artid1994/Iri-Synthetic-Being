import unittest

from runtime.cognitive_loop import CognitiveLoop


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


class FakeCognitive:
    def __init__(self):
        self.calls = []

    def process(self, user_input, record_experience=True):
        self.calls.append((user_input, record_experience))
        return "RESPOND"


class TestGemmaCognitiveLoopIntegration(unittest.TestCase):
    def test_cognitive_loop_calls_injected_cognitive_engine(self):
        cognitive = FakeCognitive()

        loop = CognitiveLoop(
            cognitive=cognitive,
            learning=FakeLearning(),
            personality=FakePersonality(),
            self_model=FakeSelfModel(),
            development=FakeDevelopment(),
        )

        cycle = loop.process("person A sees tree")

        self.assertEqual(cycle.decision, "RESPOND")
        self.assertEqual(
            cognitive.calls,
            [("person A sees tree", False)],
        )


if __name__ == "__main__":
    unittest.main()

class TestGemmaThoughtPropagation(unittest.TestCase):
    def test_cognitive_engine_output_becomes_cognitive_reasoning(self):
        class ThoughtCognitive:
            def process(self, user_input, record_experience=True):
                return "internal thought: tree detected"

        loop = CognitiveLoop(
            cognitive=ThoughtCognitive(),
            learning=FakeLearning(),
            personality=FakePersonality(),
            self_model=FakeSelfModel(),
            development=FakeDevelopment(),
        )

        cycle = loop.process("person A sees tree")

        self.assertEqual(
            cycle.reasoning,
            "internal thought: tree detected",
        )


if __name__ == "__main__":
    unittest.main()

class TestCognitiveReasoningContract(unittest.TestCase):
    def test_reasoning_preserves_cognitive_engine_output(self):
        class Cognitive:
            def process(self, user_input, record_experience=True):
                return "predicted: tree is near the house"

        loop = CognitiveLoop(
            cognitive=Cognitive(),
            learning=FakeLearning(),
            personality=FakePersonality(),
            self_model=FakeSelfModel(),
            development=FakeDevelopment(),
        )

        cycle = loop.process("person A sees tree")

        self.assertEqual(
            cycle.reasoning,
            "predicted: tree is near the house",
        )


if __name__ == "__main__":
    unittest.main()
