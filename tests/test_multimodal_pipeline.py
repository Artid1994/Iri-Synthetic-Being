import unittest

from runtime.experience import Experience
from runtime.memory import Memory
from runtime.perception import PerceptionModule
from runtime.sensor_source import MockSensor


class TestMultimodalPipeline(unittest.TestCase):
    def test_camera_creates_visual_experience(self):
        sensor = MockSensor("camera", "person A sees tree")
        reading = sensor.read(1.0)

        perception = PerceptionModule().process(str(reading.value))

        experience = Experience(
            source=reading.sensor,
            content=perception.normalized_input,
            timestamp=reading.timestamp,
            modality="vision",
        )

        self.assertEqual(experience.source, "camera")
        self.assertEqual(experience.modality, "vision")

    def test_microphone_creates_audio_experience(self):
        sensor = MockSensor("microphone", "person A hears a voice")
        reading = sensor.read(2.0)

        perception = PerceptionModule().process(str(reading.value))

        experience = Experience(
            source=reading.sensor,
            content=perception.normalized_input,
            timestamp=reading.timestamp,
            modality="audio",
        )

        self.assertEqual(experience.source, "microphone")
        self.assertEqual(experience.modality, "audio")

    def test_multimodal_experiences_share_memory(self):
        memory = Memory()

        for source, content, modality in (
            ("camera", "person A sees tree", "vision"),
            ("microphone", "person A hears a voice", "audio"),
        ):
            reading = MockSensor(source, content).read(1.0)
            perception = PerceptionModule().process(str(reading.value))

            experience = Experience(
                source=reading.sensor,
                content=perception.normalized_input,
                timestamp=reading.timestamp,
                modality=modality,
            )

            memory.add_experience(experience.content)

        self.assertEqual(len(memory.state.episodic), 2)
        self.assertEqual(
            memory.recall("person A sees tree"),
            "person A sees tree",
        )
        self.assertEqual(
            memory.recall("person A hears a voice"),
            "person A hears a voice",
        )


if __name__ == "__main__":
    unittest.main()
