import unittest

from runtime.experience import Experience
from runtime.memory import Memory


class TestExperienceMemorySnapshot(unittest.TestCase):
    def test_experience_snapshot_is_independent(self):
        memory = Memory()

        experience = Experience(
            source="camera",
            content="person A sees tree",
            timestamp=1.0,
            modality="vision",
        )

        memory.add_experience_object(experience)

        snapshot = memory.snapshot()
        snapshot.experiences.clear()

        self.assertEqual(
            len(memory.state.experiences),
            1,
        )

        self.assertEqual(
            memory.state.experiences[0],
            experience,
        )


if __name__ == "__main__":
    unittest.main()
