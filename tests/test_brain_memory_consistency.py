import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestBrainMemoryConsistency(unittest.TestCase):
    def test_cognitive_learning_updates_both_memory_layers(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.cognitive_loop.process("Python")

        self.assertTrue(
            runtime.brain.hippocampus.has_memory("Python")
        )

        self.assertIn(
            "Python",
            runtime.memory.state.episodic,
        )

        self.assertIn(
            "Python",
            runtime.memory.state.semantic,
        )

    def test_repeated_cognitive_input_does_not_duplicate_brain_memory(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.cognitive_loop.process("ESP32 BLE")
        runtime.cognitive_loop.process("ESP32 BLE")

        self.assertEqual(
            runtime.brain.hippocampus.memory_count,
            1,
        )

        self.assertEqual(
            runtime.memory.state.episodic.count("ESP32 BLE"),
            1,
        )

        self.assertEqual(
            runtime.memory.state.semantic.count("ESP32 BLE"),
            1,
        )


if __name__ == "__main__":
    unittest.main()
