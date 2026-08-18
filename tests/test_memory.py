import unittest
from runtime.memory import Memory


class TestMemory(unittest.TestCase):
    def test_memory_starts_empty(self):
        memory = Memory()
        self.assertTrue(memory.is_empty())

    def test_add_experience(self):
        memory = Memory()
        memory.add_experience("first experience")
        self.assertEqual(memory.state.episodic, ["first experience"])
        self.assertFalse(memory.is_empty())

    def test_blank_experience_is_ignored(self):
        memory = Memory()
        memory.add_experience("   ")
        self.assertTrue(memory.is_empty())

    def test_snapshot_is_independent(self):
        memory = Memory()
        memory.add_experience("experience")

        snapshot = memory.snapshot()
        snapshot.episodic.append("external change")

        self.assertEqual(memory.state.episodic, ["experience"])


if __name__ == "__main__":
    unittest.main()
