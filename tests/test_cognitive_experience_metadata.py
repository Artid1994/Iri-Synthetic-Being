import unittest

from runtime.experience import Experience
from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestCognitiveExperienceMetadata(unittest.TestCase):
    def test_cognitive_cycle_preserves_sensor_context(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.process_sensor(
            sensor="camera",
            value="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        experience = runtime.last_experience
        cycle = runtime.cognitive_loop.last_cycle

        self.assertIsNotNone(experience)
        self.assertIsNotNone(cycle)

        self.assertIsInstance(experience, Experience)
        self.assertEqual(experience.source, "camera")
        self.assertEqual(experience.modality, "vision")
        self.assertEqual(
            experience.content,
            cycle.input_text,
        )

    def test_audio_context_reaches_cognitive_cycle(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.process_sensor(
            sensor="microphone",
            value="person A hears a voice",
            timestamp=2.0,
            modality="audio",
        )

        experience = runtime.last_experience
        cycle = runtime.cognitive_loop.last_cycle

        self.assertIsNotNone(experience)
        self.assertIsNotNone(cycle)

        self.assertEqual(experience.source, "microphone")
        self.assertEqual(experience.modality, "audio")
        self.assertEqual(
            experience.content,
            cycle.input_text,
        )


if __name__ == "__main__":
    unittest.main()
