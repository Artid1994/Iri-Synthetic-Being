import unittest

from runtime.identity import Identity
from runtime.identity_continuity import IdentityContinuity
from runtime.identity_representation import IdentityRepresentation
from runtime.self_model import SelfModel
from runtime.memory import Memory
from runtime.development import Development, DevelopmentPolicy


class TestIdentityFoundation(unittest.TestCase):
    def test_identity_accumulates_experience_and_maintains_stage(self):
        identity = Identity()
        self.assertEqual(identity.state.stage, "NEWBORN")
        self.assertEqual(identity.state.experience, 0)

        identity.add_experience(5)
        self.assertEqual(identity.state.experience, 5)
        self.assertEqual(identity.state.stage, "NEWBORN")

        identity.transition_to("INFANT")
        self.assertEqual(identity.state.stage, "INFANT")
        self.assertEqual(identity.state.experience, 5)

    def test_identity_continuity_tracks_snapshots_independently(self):
        identity = Identity()
        continuity = IdentityContinuity()

        identity.add_experience(2)
        continuity.record(identity)
        snap1 = continuity.snapshot()
        self.assertEqual(snap1.snapshot_count, 1)
        self.assertEqual(snap1.last_stage, "NEWBORN")
        self.assertEqual(snap1.last_experience, 2)

        identity.transition_to("INFANT")
        identity.add_experience(3)
        continuity.record(identity)
        snap2 = continuity.snapshot()
        self.assertEqual(snap2.snapshot_count, 2)
        self.assertEqual(snap2.last_stage, "INFANT")
        self.assertEqual(snap2.last_experience, 5)
        # Verify previous snapshot is unchanged (immutable frozen dataclass)
        self.assertEqual(snap1.snapshot_count, 1)

    def test_identity_representation_from_memory_is_immutable_and_isolated(self):
        memory = Memory()
        memory.add_experience("first experience")
        memory.add_experience("second experience")
        memory.add_semantic("known rule")

        structured_memory = memory.snapshot()
        rep = IdentityRepresentation.from_structured_memory(structured_memory)

        self.assertEqual(rep.episodic, ("first experience", "second experience"))
        self.assertEqual(rep.semantic, ("known rule",))

        # Modifying memory afterwards does not change existing representation
        memory.add_experience("third experience")
        self.assertEqual(rep.episodic, ("first experience", "second experience"))

    def test_self_model_state_updates_and_clamps(self):
        self_model = SelfModel()
        self.assertEqual(self_model.state.self_awareness, 0.0)
        self.assertEqual(self_model.state.self_knowledge, 0.0)

        self_model.update(
            self_awareness_delta=0.5,
            self_knowledge_delta=0.3,
            history_entry="Observed visual feedback",
        )
        self.assertAlmostEqual(self_model.state.self_awareness, 0.5)
        self.assertAlmostEqual(self_model.state.self_knowledge, 0.3)
        self.assertEqual(self_model.state.self_history, ["Observed visual feedback"])

        # Clamping check: exceeding 1.0 or dropping below 0.0
        self_model.update(self_awareness_delta=0.8, self_knowledge_delta=-0.5)
        self.assertAlmostEqual(self_model.state.self_awareness, 1.0)
        self.assertAlmostEqual(self_model.state.self_knowledge, 0.0)

    def test_development_lifecycle_flow(self):
        class DummyLearning:
            def __init__(self):
                self.last_candidate: str | None = None
                self.last_evaluation: DummyEvaluation | None = None

        class DummyEvaluation:
            accepted = True

        class DummyPersonality:
            def snapshot(self):
                return {}

        class DummyPredictionState:
            prediction_count = 0

        class DummyPrediction:
            state = DummyPredictionState()

        identity = Identity()
        memory = Memory()
        learning = DummyLearning()
        personality = DummyPersonality()
        self_model = SelfModel()
        prediction = DummyPrediction()
        continuity = IdentityContinuity()

        development = Development(
            identity=identity,
            memory=memory,
            learning=learning,
            personality=personality,
            self_model=self_model,
            prediction=prediction,
            identity_continuity=continuity,
        )

        # Initial assessment
        assessment = development.assess()
        self.assertEqual(assessment.stage, "NEWBORN")
        self.assertEqual(assessment.experience, 0)
        self.assertEqual(assessment.episodic_memory_count, 0)

        # Ingest experience into memory and accept learning
        memory.add_experience("learned item")
        learning.last_candidate = "learned item"
        learning.last_evaluation = DummyEvaluation()

        evidence = development.sync()
        self.assertEqual(evidence.experience, 1)
        self.assertEqual(identity.state.experience, 1)
        self.assertEqual(continuity.snapshot().snapshot_count, 1)

        # Evaluate stage transition with policy
        policy = DevelopmentPolicy(
            criteria={
                "INFANT": {
                    "experience": 1,
                    "episodic_memory_count": 1,
                    "learning_available": True,
                }
            }
        )
        next_stage = development.evaluate_stage(policy)
        self.assertEqual(next_stage, "INFANT")
        identity.transition_to(next_stage)
        self.assertEqual(identity.state.stage, "INFANT")


if __name__ == "__main__":
    unittest.main()
