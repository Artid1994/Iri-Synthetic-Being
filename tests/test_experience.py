import unittest

from runtime.perception import PerceptionModule


class TestExperience(unittest.TestCase):
    def test_perception_can_become_experience_input(self):
        perception = PerceptionModule().process("  person A sees tree  ")

        self.assertTrue(perception.has_input)
        self.assertEqual(
            perception.normalized_input,
            "person A sees tree",
        )

    def test_empty_perception_produces_no_experience_input(self):
        perception = PerceptionModule().process("   ")

        self.assertFalse(perception.has_input)
        self.assertEqual(perception.normalized_input, "")


if __name__ == "__main__":
    unittest.main()
