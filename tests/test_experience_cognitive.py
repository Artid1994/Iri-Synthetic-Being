import unittest

from runtime.experience import Experience
from runtime.runtime import TranscendingRuntime


class TestExperienceCognitive(unittest.TestCase):
    def test_experience_content_can_enter_cognitive_loop(self):
        runtime = TranscendingRuntime()

        experience = Experience(
            source="camera",
            content="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        cycle = runtime.cognitive_loop.process(
            experience.content
        )

        self.assertEqual(
            cycle.input_text,
            "person A sees tree",
        )
        self.assertTrue(cycle.experience_recorded)

    def test_audio_experience_can_enter_cognitive_loop(self):
        runtime = TranscendingRuntime()

        experience = Experience(
            source="microphone",
            content="person A hears a voice",
            timestamp=2.0,
            modality="audio",
        )

        cycle = runtime.cognitive_loop.process(
            experience.content
        )

        self.assertEqual(
            cycle.input_text,
            "person A hears a voice",
        )
        self.assertTrue(cycle.experience_recorded)


if __name__ == "__main__":
    unittest.main()
