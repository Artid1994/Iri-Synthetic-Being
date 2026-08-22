from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceDecision:
    level: str
    reason: str


class ResourceGuard:
    NORMAL = "NORMAL"
    COOLING = "COOLING"
    CRITICAL = "CRITICAL"

    def __init__(
        self,
        cooling_threshold: float = 0.80,
        critical_threshold: float = 0.95,
    ) -> None:
        self.cooling_threshold = cooling_threshold
        self.critical_threshold = critical_threshold

    def evaluate(
        self,
        memory_usage: float,
    ) -> ResourceDecision:

        if memory_usage >= self.critical_threshold:
            return ResourceDecision(
                self.CRITICAL,
                "MEMORY_CRITICAL",
            )

        if memory_usage >= self.cooling_threshold:
            return ResourceDecision(
                self.COOLING,
                "MEMORY_PRESSURE",
            )

        return ResourceDecision(
            self.NORMAL,
            "RESOURCE_OK",
        )
