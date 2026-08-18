from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DevelopmentPolicy:
    criteria: dict[str, object]

    def for_stage(self, stage: str) -> dict[str, object]:
        return dict(self.criteria.get(stage, {}))


@dataclass(frozen=True)
class DevelopmentAssessment:
    stage: str
    experience: int
    episodic_memory_count: int
    semantic_memory_count: int
    learning_candidate: object | None
    learning_evaluation: object | None
    personality: object
    self_model: object


@dataclass(frozen=True)
class DevelopmentCriteriaEvidence:
    experience: int
    episodic_memory_count: int
    semantic_memory_count: int
    learning_available: bool
    self_model_complexity: int
    prediction_available: bool
    identity_continuity_available: bool


class Development:
    def __init__(
        self,
        identity,
        memory,
        learning,
        personality,
        self_model,
        prediction,
        identity_continuity,
    ) -> None:
        self.identity = identity
        self.memory = memory
        self.learning = learning
        self.personality = personality
        self.self_model = self_model
        self.prediction = prediction
        self.identity_continuity = identity_continuity
        self.history: list[DevelopmentCriteriaEvidence] = []

    def sync(self) -> DevelopmentCriteriaEvidence:
        candidate = self.learning.last_candidate
        evaluation = self.learning.last_evaluation
        identity = self.identity.snapshot()
        episodic_count = len(self.memory.state.episodic)

        if (
            candidate is not None
            and evaluation is not None
            and evaluation.accepted
            and identity.experience < episodic_count
        ):
            self.identity.add_experience(
                episodic_count - identity.experience
            )

        if (
            candidate is not None
            and evaluation is not None
            and evaluation.accepted
        ):
            self.identity_continuity.record(self.identity)

        return self.criteria_evidence()

    def evaluate_stage(self, policy: DevelopmentPolicy) -> str:
        identity = self.identity.snapshot()
        evidence = self.criteria_evidence()
        stages = self.identity.VALID_STAGES
        current_index = stages.index(identity.stage)

        if current_index >= len(stages) - 1:
            return identity.stage

        next_stage = stages[current_index + 1]
        criteria = policy.for_stage(next_stage)

        if not criteria:
            return identity.stage

        for name, threshold in criteria.items():
            value = getattr(evidence, name)

            if isinstance(threshold, bool):
                if value is not threshold:
                    return identity.stage
            elif value < threshold:
                return identity.stage

        return next_stage

    def assess(self) -> DevelopmentAssessment:
        identity = self.identity.snapshot()
        memory = self.memory.snapshot()

        return DevelopmentAssessment(
            stage=identity.stage,
            experience=identity.experience,
            episodic_memory_count=len(memory.episodic),
            semantic_memory_count=len(memory.semantic),
            learning_candidate=self.learning.last_candidate,
            learning_evaluation=self.learning.last_evaluation,
            personality=self.personality.snapshot(),
            self_model=self.self_model.snapshot(),
        )

    def criteria_evidence(self) -> DevelopmentCriteriaEvidence:
        identity = self.identity.snapshot()
        memory_state = self.memory.state
        self_model_state = self.self_model.state

        evidence = DevelopmentCriteriaEvidence(
            experience=identity.experience,
            episodic_memory_count=len(memory_state.episodic),
            semantic_memory_count=len(memory_state.semantic),
            learning_available=(
                self.learning.last_candidate is not None
                and self.learning.last_evaluation is not None
            ),
            self_model_complexity=(
                len(self_model_state.goals)
                + len(self_model_state.beliefs)
                + len(self_model_state.self_history)
            ),
            prediction_available=(
                self.prediction.state.prediction_count > 0
            ),
            identity_continuity_available=(
                self.identity_continuity.state.snapshot_count > 0
            ),
        )

        self.history.append(evidence)
        return evidence

    def history_snapshot(self) -> list[DevelopmentCriteriaEvidence]:
        return list(self.history)
