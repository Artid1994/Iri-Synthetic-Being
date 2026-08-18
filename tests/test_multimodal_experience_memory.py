import unittest

from runtime.experience import Experience
from runtime.memory import Memory


class TestMultimodalExperienceMemory(unittest.TestCase):
    def test_memory_preserves_vision_and_audio_experiences(self):
        memory = Memory()

        vision = Experience(
            source="camera",
            content="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        audio = Experience(
            source="microphone",
            content="person A hears a voice",
            timestamp=2.0,
            modality="audio",
        )

        memory.add_experience(vision.content)
        memory.add_experience(audio.content)

        self.assertIn(
            "person A sees tree",
            memory.state.episodic,
        )
        self.assertIn(
            "person A hears a voice",
            memory.state.episodic,
        )

        self.assertEqual(
            len(memory.state.episodic),
            2,
        )


if __name__ == "__main__":
    unittest.main()
