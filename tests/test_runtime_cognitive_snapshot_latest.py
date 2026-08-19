import unittest

from runtime.runtime import TranscendingRuntime


class TestRuntimeCognitiveSnapshotLatest(unittest.TestCase):
    def test_runtime_snapshot_contains_latest_cognitive_cycle(self):
        runtime = TranscendingRuntime()

        runtime.cognitive_loop.process(
            "person A sees a large tree near the house"
        )
        runtime.cognitive_loop.process(
            "person A hears a voice inside the house"
        )

        snapshot = runtime.snapshot()
        cycle = snapshot["cognitive_loop"]

        self.assertIsNotNone(cycle)
        self.assertEqual(
            cycle.input_text,
            "person A hears a voice inside the house",
        )


if __name__ == "__main__":
    unittest.main()
