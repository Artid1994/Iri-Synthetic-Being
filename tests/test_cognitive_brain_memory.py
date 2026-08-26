import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestCognitiveBrainMemory(unittest.TestCase):
    def test_cognitive_experience_is_stored_in_hippocampus(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.cognitive_loop.process(
            "ESP32 BLE"
        )

        self.assertTrue(
            runtime.brain.hippocampus.has_memory(
                "ESP32 BLE"
            )
        )

    def test_duplicate_cognitive_experience_is_not_duplicated(self):
        runtime = TranscendingRuntime(
            cognitive=FakeCognitive()
        )

        runtime.cognitive_loop.process(
            "Python"
        )

        runtime.cognitive_loop.process(
            "Python"
        )

        self.assertEqual(
            runtime.brain.hippocampus.memory_count,
            1,
        )


if __name__ == "__main__":
    unittest.main()
