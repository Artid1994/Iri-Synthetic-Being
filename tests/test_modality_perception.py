import unittest

from runtime.perception import PerceptionModule


class TestModalityPerception(unittest.TestCase):
    def test_vision_perception(self):
        perception = PerceptionModule().process(
            "person A sees a tree"
        )

        self.assertTrue(perception.has_input)
        self.assertEqual(
            perception.normalized_input,
            "person A sees a tree",
        )

    def test_audio_perception(self):
        perception = PerceptionModule().process(
            "person A hears a voice"
        )

        self.assertTrue(perception.has_input)
        self.assertEqual(
            perception.normalized_input,
            "person A hears a voice",
        )


if __name__ == "__main__":
    unittest.main()
