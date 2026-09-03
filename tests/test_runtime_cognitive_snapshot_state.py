import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestRuntimeCognitiveSnapshotState(unittest.TestCase):
    def test_runtime_snapshot_preserves_cognitive_attention_and_salience(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.cognitive_loop.process(
            "person A sees a large tree near the house"
        )

        snapshot = runtime.snapshot()

        self.assertIsNotNone(snapshot)
        self.assertTrue(snapshot["cognitive_loop"].attention_required)
        self.assertGreater(
            snapshot["cognitive_loop"].salience,
            0.0,
        )
        self.assertLessEqual(
            snapshot["cognitive_loop"].salience,
            1.0,
        )


if __name__ == "__main__":
    unittest.main()
