import unittest

from brain.brain import Brain


class TestBrainMemoryBridge(unittest.TestCase):
    def test_store_memory_also_activates_hippocampus(self):
        brain = Brain()

        before = brain.hippocampus.population.stats

        result = brain.store_memory("Python")

        after = brain.hippocampus.population.stats

        self.assertTrue(result)
        self.assertEqual(
            brain.hippocampus.memory_count,
            1,
        )
        self.assertGreater(
            after.allocated_neurons,
            before.allocated_neurons,
        )

    def test_duplicate_memory_does_not_create_new_memory(self):
        brain = Brain()

        self.assertTrue(
            brain.store_memory("ESP32 BLE")
        )

        allocated_before = (
            brain.hippocampus.population.stats.allocated_neurons
        )

        self.assertFalse(
            brain.store_memory("ESP32 BLE")
        )

        self.assertEqual(
            brain.hippocampus.memory_count,
            1,
        )
        self.assertEqual(
            brain.hippocampus.population.stats.allocated_neurons,
            allocated_before,
        )


if __name__ == "__main__":
    unittest.main()
