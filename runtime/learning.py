from __future__ import annotations

from dataclasses import dataclass

from runtime.memory import Memory


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

    def snapshot(self) -> dict:
        return {
            "last_candidate": self.last_candidate,
            "last_evaluation": self.last_evaluation,
        }
