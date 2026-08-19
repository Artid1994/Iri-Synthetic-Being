import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestNewborn(unittest.TestCase):
    def test_person_a_starts_as_newborn(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        identity = runtime.identity.snapshot()
        memory = runtime.memory.snapshot()
        self_model = runtime.self_model.snapshot()
        development = runtime.development.history_snapshot()
        continuity = runtime.identity_continuity.snapshot()

        self.assertEqual(identity.stage, "NEWBORN")
        self.assertEqual(identity.experience, 0)
        self.assertEqual(identity.identity_level, "MINIMAL")

        self.assertEqual(memory.working, [])
        self.assertEqual(memory.episodic, [])
        self.assertEqual(memory.semantic, [])

        self.assertEqual(self_model.self_awareness, 0.0)
        self.assertEqual(self_model.self_knowledge, 0.0)
        self.assertEqual(self_model.self_history, [])

        self.assertEqual(development, [])
        self.assertEqual(continuity.snapshot_count, 0)


if __name__ == "__main__":
    unittest.main()
