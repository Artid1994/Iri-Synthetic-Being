import unittest

from brain.brain import Brain


class TestBrainMemory(unittest.TestCase):
    def test_hippocampus_can_store_memory_signal(self):
        brain = Brain()

        result = brain.store_memory("Python")

        self.assertTrue(result)
        self.assertEqual(
            brain.hippocampus.memory_count,
            1,
        )

    def test_empty_memory_is_rejected(self):
        brain = Brain()

        result = brain.store_memory("")

        self.assertFalse(result)
        self.assertEqual(
            brain.hippocampus.memory_count,
            0,
        )

    def test_memory_is_not_duplicated(self):
        brain = Brain()

        self.assertTrue(
            brain.store_memory("ESP32 BLE")
        )
        self.assertFalse(
            brain.store_memory("ESP32 BLE")
        )

        self.assertEqual(
            brain.hippocampus.memory_count,
            1,
        )


if __name__ == "__main__":
    unittest.main()
