from __future__ import annotations

from dataclasses import dataclass

from runtime.memory import Memory
from runtime.prediction import PredictionEvaluation
from runtime.safety_event import SafetyEvent
from runtime.teaching import Teaching


@dataclass(frozen=True)
class LearningCandidate:
    experience: str
    category: str = "GENERAL"
    confidence: float = 0.0


@dataclass(frozen=True)
class LearningEvaluation:
    accepted: bool
    reason: str


class Learning:
    def __init__(self, memory: Memory) -> None:
        self.memory = memory
        self.last_candidate: LearningCandidate | None = None
        self.last_evaluation: LearningEvaluation | None = None

    def create_candidate(
        self,
        experience: str,
        category: str = "GENERAL",
        confidence: float = 0.0,
    ) -> LearningCandidate | None:
        experience = experience.strip()

        if not experience:
            return None

        confidence = max(0.0, min(1.0, confidence))

        candidate = LearningCandidate(
            experience=experience,
            category=category,
            confidence=confidence,
        )

        self.last_candidate = candidate
        return candidate

    def evaluate(
        self,
        candidate: LearningCandidate | None,
    ) -> LearningEvaluation:
        if candidate is None:
            evaluation = LearningEvaluation(
                accepted=False,
                reason="NO_CANDIDATE",
            )

        elif candidate.category == "SAFETY":
            evaluation = LearningEvaluation(
                accepted=False,
                reason="SAFETY_CANDIDATE_REQUIRES_SEPARATE_POLICY",
            )

        elif candidate.confidence >= 0.5:
            evaluation = LearningEvaluation(
                accepted=True,
                reason="CONFIDENCE_THRESHOLD_MET",
            )

        else:
            evaluation = LearningEvaluation(
                accepted=False,
                reason="CONFIDENCE_TOO_LOW",
            )

        self.last_evaluation = evaluation

        if evaluation.accepted and candidate is not None:
            self.memory.add_experience(candidate.experience)
            self.memory.add_semantic(candidate.experience)

        return evaluation

    def evaluate_teaching(
        self,
        teaching: Teaching,
    ) -> LearningEvaluation:
        if not isinstance(teaching, Teaching):
            return LearningEvaluation(
                accepted=False,
                reason="INVALID_TEACHING",
            )

        candidate = self.create_candidate(
            teaching.content,
            category="TEACHING",
            confidence=1.0,
        )

        evaluation = self.evaluate(candidate)

        if evaluation.accepted:
            teaching.accept()

        return evaluation

    def observe_safety_event(
        self,
        event: SafetyEvent,
    ) -> LearningEvaluation:
        if not isinstance(event, SafetyEvent):
            return LearningEvaluation(
                accepted=False,
                reason="INVALID_SAFETY_EVENT",
            )

        return LearningEvaluation(
            accepted=False,
            reason="SAFETY_EVENT_OBSERVED_ONLY",
        )

    def learn_from_prediction(
        self,
        prediction: str,
        evaluation: PredictionEvaluation,
    ) -> LearningEvaluation:
        prediction = prediction.strip()

        if evaluation.correct is None:
            return LearningEvaluation(
                accepted=False,
                reason="PREDICTION_OUTCOME_UNKNOWN",
            )

        if not prediction:
            return LearningEvaluation(
                accepted=False,
                reason="PREDICTION_OUTCOME_UNKNOWN",
            )

        if evaluation.correct:
            self.memory.add_experience(prediction)

            result = LearningEvaluation(
                accepted=True,
                reason="PREDICTION_CONFIRMED",
            )
        else:
            result = LearningEvaluation(
                accepted=False,
                reason="PREDICTION_CORRECTION_REQUIRED",
            )

        self.last_evaluation = result
        return result

    def snapshot(self) -> dict:
        return {
            "last_candidate": self.last_candidate,
            "last_evaluation": self.last_evaluation,
        }
