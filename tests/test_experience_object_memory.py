import unittest

from runtime.experience import Experience
from runtime.memory import Memory


class TestExperienceObjectMemory(unittest.TestCase):
    def test_memory_can_store_experience_object(self):
        memory = Memory()

        experience = Experience(
            source="camera",
            content="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        memory.add_experience_object(experience)

        self.assertIn(
            experience,
            memory.state.experiences,
        )

    def test_memory_preserves_experience_metadata(self):
        memory = Memory()

        experience = Experience(
            source="microphone",
            content="person A hears a voice",
            timestamp=2.0,
            modality="audio",
        )

        memory.add_experience_object(experience)

        stored = memory.state.experiences[-1]

        self.assertEqual(stored.source, "microphone")
        self.assertEqual(stored.content, "person A hears a voice")
        self.assertEqual(stored.timestamp, 2.0)
        self.assertEqual(stored.modality, "audio")


if __name__ == "__main__":
    unittest.main()
