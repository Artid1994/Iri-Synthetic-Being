import unittest

from runtime.runtime import TranscendingRuntime


class TestModalityExperience(unittest.TestCase):
    def test_camera_creates_vision_experience(self):
        runtime = TranscendingRuntime()

        runtime.process_sensor(
            sensor="camera",
            value="person A sees a tree",
            timestamp=1.0,
            modality="vision",
        )

        experience = runtime.last_experience

        self.assertIsNotNone(experience)
        self.assertEqual(experience.modality, "vision")
        self.assertEqual(experience.source, "camera")

    def test_microphone_creates_audio_experience(self):
        runtime = TranscendingRuntime()

        runtime.process_sensor(
            sensor="microphone",
            value="person A hears a voice",
            timestamp=2.0,
            modality="audio",
        )

        experience = runtime.last_experience

        self.assertIsNotNone(experience)
        self.assertEqual(experience.modality, "audio")
        self.assertEqual(experience.source, "microphone")


if __name__ == "__main__":
    unittest.main()
