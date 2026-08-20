import unittest

from runtime.gemma_cognitive_engine import GemmaCognitiveEngine


class TestGemmaCognitiveEngine(unittest.TestCase):
    def test_engine_uses_injected_inference_backend(self):
        calls = []

        def fake_inference(text):
            calls.append(text)
            return "I see a tree."

        engine = GemmaCognitiveEngine(inference=fake_inference)

        result = engine.think("person A sees tree")

        self.assertEqual(result, "I see a tree.")
        self.assertEqual(calls, ["person A sees tree"])

    def test_engine_does_not_own_memory(self):
        engine = GemmaCognitiveEngine(
            inference=lambda text: "internal thought"
        )

        self.assertFalse(hasattr(engine, "memory"))


    def test_engine_passes_cognitive_context_to_inference(self):
        calls = []

        def fake_inference(prompt):
            calls.append(prompt)
            return "internal thought"

        engine = GemmaCognitiveEngine(inference=fake_inference)

        result = engine.think(
            "person A sees tree",
            context="person A previously saw a tree",
        )

        self.assertEqual(result, "internal thought")
        self.assertEqual(
            calls,
            ["person A previously saw a tree\nperson A sees tree"],
        )


    def test_engine_accepts_llama_inference_backend(self):
        inference = lambda prompt: "ต้นไม้เป็นสิ่งมีชีวิต"
        engine = GemmaCognitiveEngine(inference=inference)

        result = engine.think("เห็นต้นไม้")

        self.assertEqual(result, "ต้นไม้เป็นสิ่งมีชีวิต")


    def test_process_returns_respond_when_thought_is_generated(self):
        engine = GemmaCognitiveEngine(
            inference=lambda prompt: "ต้นไม้เป็นพืช",
        )

        result = engine.process("ต้นไม้คืออะไร")

        self.assertEqual(result, "RESPOND")


if __name__ == "__main__":
    unittest.main()

class TestGemmaThoughtState(unittest.TestCase):
    def test_process_preserves_generated_thought(self):
        engine = GemmaCognitiveEngine(
            inference=lambda prompt: "internal thought: tree detected",
        )

        engine.process("person A sees tree")

        self.assertEqual(
            engine.snapshot()["last_thought"],
            "internal thought: tree detected",
        )


if __name__ == "__main__":
    unittest.main()

class TestGemmaEmptyThought(unittest.TestCase):
    def test_empty_thought_is_preserved_as_empty(self):
        engine = GemmaCognitiveEngine(
            inference=lambda prompt: "",
        )

        result = engine.process("person A sees tree")

        self.assertEqual(result, "NO_ACTION")
        self.assertEqual(
            engine.snapshot()["last_thought"],
            "",
        )


if __name__ == "__main__":
    unittest.main()
