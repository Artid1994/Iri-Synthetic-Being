import unittest

from runtime.runtime import TranscendingRuntime
from tests.cognitive_test_helper import FakeCognitive


class TestBrainIntegration(unittest.TestCase):
    def test_newborn_runtime_starts_empty(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        self.assertEqual(runtime.identity.state.stage, "NEWBORN")
        self.assertEqual(runtime.identity.state.experience, 0)
        self.assertTrue(runtime.memory.is_empty())

    def test_cognitive_cycle_creates_experience(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        cycle = runtime.cognitive_loop.process("hello brain")

        self.assertEqual(cycle.input_text, "hello brain")
        self.assertEqual(cycle.decision, "RESPOND")
        self.assertTrue(cycle.experience_recorded)

        self.assertIn(
            "hello brain",
            runtime.memory.state.episodic,
        )
        self.assertIn(
            "hello brain",
            runtime.memory.state.semantic,
        )

    def test_experience_updates_identity(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.cognitive_loop.process("first experience")

        self.assertEqual(
            runtime.identity.state.experience,
            1,
        )

    def test_experience_updates_self_model(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.cognitive_loop.process("self model experience")

        self.assertGreater(
            len(runtime.self_model.state.self_history),
            0,
        )

    def test_experience_updates_personality(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        before = runtime.personality.snapshot()

        runtime.cognitive_loop.process("personality experience")

        after = runtime.personality.snapshot()

        self.assertGreaterEqual(
            after.openness,
            before.openness,
        )
        self.assertGreaterEqual(
            after.conscientiousness,
            before.conscientiousness,
        )

    def test_development_records_evidence(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.cognitive_loop.process("development experience")

        history = runtime.development.history_snapshot()

        self.assertGreater(len(history), 0)
        self.assertEqual(
            history[-1].experience,
            runtime.identity.state.experience,
        )

    def test_identity_continuity_records_experience(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.cognitive_loop.process("continuity experience")

        continuity = runtime.identity_continuity.snapshot()

        self.assertGreater(
            continuity.snapshot_count,
            0,
        )

    def test_runtime_snapshot_contains_brain_state(self):
        runtime = TranscendingRuntime(cognitive=FakeCognitive())

        runtime.cognitive_loop.process("snapshot experience")

        snapshot = runtime.snapshot()

        required = {
            "identity",
            "memory",
            "personality",
            "self_model",
            "cognitive",
            "cognitive_loop",
            "learning",
            "development",
            "identity_continuity",
        }

        self.assertTrue(required.issubset(snapshot.keys()))


    def test_runtime_uses_gemma_cognitive_engine(self):
        from runtime.gemma_cognitive_engine import GemmaCognitiveEngine

        runtime = TranscendingRuntime()

        self.assertIsInstance(runtime.cognitive, GemmaCognitiveEngine)


if __name__ == "__main__":
    unittest.main()
