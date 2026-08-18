import unittest

from runtime.experience import Experience


class TestExperience(unittest.TestCase):
    def test_experience_stores_core_fields(self):
        experience = Experience(
            source="camera",
            content="person A sees tree",
            timestamp=1.25,
            modality="vision",
        )

        self.assertEqual(experience.source, "camera")
        self.assertEqual(experience.content, "person A sees tree")
        self.assertEqual(experience.timestamp, 1.25)
        self.assertEqual(experience.modality, "vision")

    def test_experience_is_immutable(self):
        experience = Experience(
            source="microphone",
            content="hello",
            timestamp=2.0,
            modality="audio",
        )

        with self.assertRaises((AttributeError, TypeError)):
            experience.content = "changed"


if __name__ == "__main__":
    unittest.main()
