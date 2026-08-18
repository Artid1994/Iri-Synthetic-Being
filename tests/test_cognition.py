import unittest
from runtime.cognitive_engine import CognitiveEngine
from runtime.memory import Memory


class TestCognition(unittest.TestCase):
    def test_empty_input_produces_no_action(self):
        memory = Memory()
        engine = CognitiveEngine(memory)

        result = engine.process("")

        self.assertEqual(result, "NO_ACTION")
        self.assertEqual(memory.state.episodic, [])

    def test_input_produces_response_decision(self):
        memory = Memory()
        engine = CognitiveEngine(memory)

        result = engine.process("hello")

        self.assertEqual(result, "RESPOND")
        self.assertEqual(memory.state.episodic, ["hello"])

    def test_recall_uses_existing_experience(self):
        memory = Memory()
        memory.add_experience("remember this")

        engine = CognitiveEngine(memory)
        result = engine.process(
            "remember this",
            record_experience=False,
        )

        self.assertEqual(result, "RESPOND")
        self.assertEqual(
            engine.state.last_recalled,
            "remember this",
        )
        self.assertEqual(
            memory.state.episodic,
            ["remember this"],
        )

    def test_processing_flags_reset_after_cycle(self):
        engine = CognitiveEngine(Memory())

        engine.process("test")

        self.assertFalse(engine.state.recall_active)
        self.assertFalse(engine.state.reasoning_active)
        self.assertFalse(engine.state.decision_active)


if __name__ == "__main__":
    unittest.main()
