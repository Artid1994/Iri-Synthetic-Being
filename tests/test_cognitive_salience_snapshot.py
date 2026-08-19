import unittest

from runtime.runtime import TranscendingRuntime


class TestCognitiveSalienceSnapshot(unittest.TestCase):
    def test_snapshot_preserves_attention_and_salience(self):
        runtime = TranscendingRuntime()

        runtime.cognitive_loop.process(
            "person A sees a large tree near the house"
        )

        snapshot = runtime.cognitive_loop.snapshot()

        self.assertIsNotNone(snapshot)
        self.assertTrue(snapshot.attention_required)
        self.assertGreater(snapshot.salience, 0.0)
        self.assertLessEqual(snapshot.salience, 1.0)


if __name__ == "__main__":
    unittest.main()
