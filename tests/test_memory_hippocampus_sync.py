import unittest

from brain.brain import Brain
from runtime.memory import Memory


class TestMemoryHippocampusSync(unittest.TestCase):
    def test_episodic_memory_can_sync_to_hippocampus(self):
        memory = Memory()
        brain = Brain()

        memory.add_experience("Python")
        memory.add_experience("ESP32 BLE")

        result = brain.sync_memory(memory)

        self.assertEqual(
            result,
            2,
        )

        self.assertTrue(
            brain.hippocampus.has_memory("Python")
        )
        self.assertTrue(
            brain.hippocampus.has_memory("ESP32 BLE")
        )

    def test_duplicate_episodic_memory_is_not_duplicated_in_hippocampus(self):
        memory = Memory()
        brain = Brain()

        memory.add_experience("Python")
        memory.add_experience("Python")

        result = brain.sync_memory(memory)

        self.assertEqual(
            result,
            1,
        )

        self.assertEqual(
            brain.hippocampus.memory_count,
            1,
        )

    def test_empty_memory_sync_does_not_allocate_hippocampus(self):
        memory = Memory()
        brain = Brain()

        result = brain.sync_memory(memory)

        self.assertEqual(result, 0)
        self.assertEqual(
            brain.hippocampus.memory_count,
            0,
        )
        self.assertEqual(
            brain.hippocampus.population.stats.allocated_neurons,
            0,
        )


if __name__ == "__main__":
    unittest.main()
