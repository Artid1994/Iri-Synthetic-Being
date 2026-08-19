import unittest

from runtime.runtime import TranscendingRuntime


class TestRuntimeCognitiveSnapshotEmpty(unittest.TestCase):
    def test_newborn_runtime_has_empty_cognitive_loop_snapshot(self):
        runtime = TranscendingRuntime()

        snapshot = runtime.snapshot()

        self.assertIsNone(snapshot["cognitive_loop"])


if __name__ == "__main__":
    unittest.main()
