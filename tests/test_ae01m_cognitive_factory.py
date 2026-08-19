import unittest

from runtime.ae01m_cognitive_factory import create_cognitive_engine
from runtime.gemma_cognitive_engine import GemmaCognitiveEngine


class TestAE01MCognitiveFactory(unittest.TestCase):
    def test_creates_gemma_cognitive_engine(self):
        engine = create_cognitive_engine(
            model_path="/models/gemma.gguf",
            executable="/bin/llama-completion",
        )

        self.assertIsInstance(engine, GemmaCognitiveEngine)


    def test_factory_engine_can_use_injected_backend(self):
        engine = create_cognitive_engine(
            model_path="/models/gemma.gguf",
            executable="/bin/llama-completion",
        )

        self.assertTrue(callable(engine._inference))


if __name__ == "__main__":
    unittest.main()
