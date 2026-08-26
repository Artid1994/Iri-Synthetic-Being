from __future__ import annotations

from dataclasses import dataclass

from runtime.web_research import ResearchResult


@dataclass(frozen=True)
class ResearchSafetyResult:
    accepted: bool
    reason: str


class ResearchSafetyGate:
    BLOCKED_CATEGORIES = {
        "IDENTITY",
        "SAFETY",
        "CORE",
        "SYSTEM",
    }

    def evaluate(
        self,
        result: ResearchResult,
        category: str = "GENERAL",
    ) -> ResearchSafetyResult:
        if not isinstance(result, ResearchResult):
            return ResearchSafetyResult(
                accepted=False,
                reason="INVALID_RESEARCH_RESULT",
            )

        if not result.topic.strip():
            return ResearchSafetyResult(
                accepted=False,
                reason="EMPTY_TOPIC",
            )

        if not result.content.strip():
            return ResearchSafetyResult(
                accepted=False,
                reason="EMPTY_RESEARCH_CONTENT",
            )

        category = category.strip().upper()

        if category in self.BLOCKED_CATEGORIES:
            return ResearchSafetyResult(
                accepted=False,
                reason="PROTECTED_CATEGORY",
            )

        return ResearchSafetyResult(
            accepted=True,
            reason="RESEARCH_ACCEPTED",
        )
