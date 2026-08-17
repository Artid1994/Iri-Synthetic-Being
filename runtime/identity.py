from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class IdentityState:
    stage: str = "NEWBORN"
    experience: int = 0
    identity_level: str = "MINIMAL"
    created_at: str = ""


class Identity:
    VALID_STAGES = (
        "NEWBORN",
        "INFANT",
        "LEARNING AGENT",
        "DEVELOPING PERSONA",
        "MATURE AGENT",
    )

    def __init__(self) -> None:
        self.state = IdentityState(
            created_at=datetime.now(timezone.utc).isoformat()
        )

    def set_stage(self, stage: str) -> None:
        if stage not in self.VALID_STAGES:
            raise ValueError(f"Invalid development stage: {stage}")

        self.state.stage = stage

    def transition_to(self, stage: str) -> None:
        if stage not in self.VALID_STAGES:
            raise ValueError(f"Invalid development stage: {stage}")

        current_index = self.VALID_STAGES.index(self.state.stage)
        target_index = self.VALID_STAGES.index(stage)

        if target_index != current_index + 1:
            raise ValueError(
                f"Invalid development transition: "
                f"{self.state.stage} -> {stage}"
            )

        self.state.stage = stage

    def add_experience(self, amount: int = 1) -> None:
        if amount < 0:
            raise ValueError("Experience amount cannot be negative")

        self.state.experience += amount

    def snapshot(self) -> IdentityState:
        return IdentityState(
            stage=self.state.stage,
            experience=self.state.experience,
            identity_level=self.state.identity_level,
            created_at=self.state.created_at,
        )
