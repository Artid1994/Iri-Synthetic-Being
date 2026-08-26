import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestCognitiveMemoryBrainPipeline(unittest.TestCase):
    def test_cognitive_learning_reaches_episodic_and_hippocampus(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        cycle = runtime.cognitive_loop.process(
            "ESP32 BLE"
        )

        self.assertEqual(
            cycle.decision,
            "RESPOND",
        )

        self.assertIn(
            "ESP32 BLE",
            runtime.memory.state.episodic,
        )

        self.assertTrue(
            runtime.brain.hippocampus.has_memory(
                "ESP32 BLE"
            )
        )

    def test_repeated_cognitive_input_does_not_duplicate_hippocampus(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.cognitive_loop.process("Python")
        allocated = (
            runtime.brain
            .hippocampus
            .population
            .stats
            .allocated_neurons
        )

        runtime.cognitive_loop.process("Python")

        self.assertEqual(
            runtime.brain.hippocampus.memory_count,
            1,
        )

        self.assertEqual(
            runtime.brain
            .hippocampus
            .population
            .stats
            .allocated_neurons,
            allocated,
        )


if __name__ == "__main__":
    unittest.main()
