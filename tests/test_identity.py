import unittest
from runtime.identity import Identity


class TestIdentity(unittest.TestCase):
    def test_newborn_identity(self):
        identity = Identity()
        self.assertEqual(identity.state.stage, "NEWBORN")
        self.assertEqual(identity.state.experience, 0)
        self.assertEqual(identity.state.identity_level, "MINIMAL")

    def test_add_experience(self):
        identity = Identity()
        identity.add_experience(3)
        self.assertEqual(identity.state.experience, 3)

    def test_negative_experience_rejected(self):
        identity = Identity()
        with self.assertRaises(ValueError):
            identity.add_experience(-1)

    def test_sequential_stage_transition(self):
        identity = Identity()
        identity.transition_to("INFANT")
        self.assertEqual(identity.state.stage, "INFANT")

    def test_invalid_stage_transition_rejected(self):
        identity = Identity()
        with self.assertRaises(ValueError):
            identity.transition_to("MATURE AGENT")

    def test_invalid_stage_rejected(self):
        identity = Identity()
        with self.assertRaises(ValueError):
            identity.set_stage("INVALID")


if __name__ == "__main__":
    unittest.main()
