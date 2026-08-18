import unittest

from runtime.experience import Experience
from runtime.memory import Memory


class TestExperienceMemory(unittest.TestCase):
    def test_experience_can_be_stored_in_memory(self):
        memory = Memory()

        experience = Experience(
            source="camera",
            content="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        memory.add_experience(experience.content)

        self.assertEqual(
            memory.state.episodic,
            ["person A sees tree"],
        )

    def test_memory_preserves_experience_content(self):
        memory = Memory()

        experience = Experience(
            source="microphone",
            content="hello",
            timestamp=2.0,
            modality="audio",
        )

        memory.add_experience(experience.content)

        self.assertEqual(
            memory.recall("hello"),
            "hello",
        )


if __name__ == "__main__":
    unittest.main()
