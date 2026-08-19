import unittest

from runtime.runtime import TranscendingRuntime


class TestRuntimeCognitiveSnapshotLatestState(unittest.TestCase):
    def test_latest_snapshot_preserves_attention_and_salience(self):
        runtime = TranscendingRuntime()

        runtime.cognitive_loop.process("tree")
        runtime.cognitive_loop.process(
            "person A sees a large tree near the house"
        )

        snapshot = runtime.snapshot()
        cycle = snapshot["cognitive_loop"]

        self.assertIsNotNone(cycle)
        self.assertEqual(
            cycle.input_text,
            "person A sees a large tree near the house",
        )
        self.assertTrue(cycle.attention_required)
        self.assertGreater(cycle.salience, 0.0)
        self.assertLessEqual(cycle.salience, 1.0)


if __name__ == "__main__":
    unittest.main()
