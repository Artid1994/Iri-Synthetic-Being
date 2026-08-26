from __future__ import annotations

from dataclasses import dataclass

from runtime.learning import Learning, LearningCandidate
from runtime.web_research import ResearchResult


@dataclass(frozen=True)
class ResearchLearningResult:
    candidate: LearningCandidate | None
    accepted: bool
    reason: str


class ResearchLearning:
    def __init__(self, learning: Learning) -> None:
        self.learning = learning

    def create_candidate(
        self,
        result: ResearchResult,
        confidence: float = 0.5,
    ) -> LearningCandidate | None:
        if not isinstance(result, ResearchResult):
            raise TypeError("result must be a ResearchResult")

        content = result.content.strip()

        if not content:
            return None

        return self.learning.create_candidate(
            content,
            category="WEB_RESEARCH",
            confidence=confidence,
        )

    def evaluate(
        self,
        result: ResearchResult,
        confidence: float = 0.5,
    ) -> ResearchLearningResult:
        candidate = self.create_candidate(
            result,
            confidence=confidence,
        )

        evaluation = self.learning.evaluate(candidate)

        return ResearchLearningResult(
            candidate=candidate,
            accepted=evaluation.accepted,
            reason=evaluation.reason,
        )
