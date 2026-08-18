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


if __name__ == "__main__":
    unittest.main()
