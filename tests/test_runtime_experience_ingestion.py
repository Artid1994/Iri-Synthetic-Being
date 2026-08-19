import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive
from runtime.experience import Experience


class TestRuntimeExperienceIngestion(unittest.TestCase):
    def test_camera_input_creates_experience(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.process_sensor(
            sensor="camera",
            value="person A sees tree",
            timestamp=10.5,
            modality="vision",
        )

        experience = runtime.last_experience

        self.assertIsInstance(experience, Experience)
        self.assertEqual(experience.source, "camera")
        self.assertEqual(experience.content, "person A sees tree")
        self.assertEqual(experience.timestamp, 10.5)
        self.assertEqual(experience.modality, "vision")

    def test_microphone_input_creates_experience(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.process_sensor(
            sensor="microphone",
            value="person A hears a voice",
            timestamp=20.5,
            modality="audio",
        )

        experience = runtime.last_experience

        self.assertIsInstance(experience, Experience)
        self.assertEqual(experience.source, "microphone")
        self.assertEqual(experience.content, "person A hears a voice")
        self.assertEqual(experience.timestamp, 20.5)
        self.assertEqual(experience.modality, "audio")


if __name__ == "__main__":
    unittest.main()
