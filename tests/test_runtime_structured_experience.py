import unittest

from runtime.experience import Experience
from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestRuntimeStructuredExperience(unittest.TestCase):
    def test_camera_sensor_stores_structured_experience(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.process_sensor(
            sensor="camera",
            value="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        self.assertEqual(len(runtime.memory.state.experiences), 1)

        experience = runtime.memory.state.experiences[0]

        self.assertIsInstance(experience, Experience)
        self.assertEqual(experience.source, "camera")
        self.assertEqual(experience.content, "person A sees tree")
        self.assertEqual(experience.timestamp, 1.0)
        self.assertEqual(experience.modality, "vision")

    def test_microphone_sensor_stores_structured_experience(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.process_sensor(
            sensor="microphone",
            value="person A hears a voice",
            timestamp=2.0,
            modality="audio",
        )

        self.assertEqual(len(runtime.memory.state.experiences), 1)

        experience = runtime.memory.state.experiences[0]

        self.assertIsInstance(experience, Experience)
        self.assertEqual(experience.source, "microphone")
        self.assertEqual(experience.content, "person A hears a voice")
        self.assertEqual(experience.timestamp, 2.0)
        self.assertEqual(experience.modality, "audio")


if __name__ == "__main__":
    unittest.main()
