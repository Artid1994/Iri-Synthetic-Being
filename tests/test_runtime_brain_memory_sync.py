import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestRuntimeBrainMemorySync(unittest.TestCase):
    def test_existing_episodic_memory_is_synced_to_brain(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.memory.add_experience("Python")
        runtime.memory.add_experience("ESP32 BLE")

        result = runtime.sync_brain_memory()

        self.assertEqual(result, 2)
        self.assertTrue(
            runtime.brain.hippocampus.has_memory("Python")
        )
        self.assertTrue(
            runtime.brain.hippocampus.has_memory("ESP32 BLE")
        )

    def test_repeated_sync_does_not_duplicate(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.memory.add_experience("Python")

        self.assertEqual(
            runtime.sync_brain_memory(),
            1,
        )

        self.assertEqual(
            runtime.sync_brain_memory(),
            0,
        )

        self.assertEqual(
            runtime.brain.hippocampus.memory_count,
            1,
        )


if __name__ == "__main__":
    unittest.main()
