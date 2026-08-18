import unittest

from runtime.experience import Experience
from runtime.memory import Memory
from runtime.perception import PerceptionModule
from runtime.sensor_source import MockSensor


class TestSensoryExperiencePipeline(unittest.TestCase):
    def test_mock_sensor_to_memory(self):
        sensor = MockSensor(
            name="camera",
            value="person A sees tree",
        )

        reading = sensor.read(timestamp=1.0)

        perception = PerceptionModule().process(
            str(reading.value)
        )

        self.assertTrue(perception.has_input)

        experience = Experience(
            source=reading.sensor,
            content=perception.normalized_input,
            timestamp=reading.timestamp,
            modality="vision",
        )

        memory = Memory()
        memory.add_experience(experience.content)

        self.assertEqual(
            memory.recall("person A sees tree"),
            "person A sees tree",
        )

        self.assertEqual(experience.source, "camera")
        self.assertEqual(experience.modality, "vision")


if __name__ == "__main__":
    unittest.main()
