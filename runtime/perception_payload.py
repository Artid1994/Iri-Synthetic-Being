from __future__ import annotations

from dataclasses import dataclass

from runtime.world_model import WorldState


@dataclass(frozen=True)
class PerceptionPayload:
    position: tuple[float, float]
    objects: tuple[str, ...]
    environment: str

    @classmethod
    def from_world_state(
        cls,
        world_state: WorldState,
    ) -> "PerceptionPayload":
        return cls(
            position=world_state.position,
            objects=world_state.objects,
            environment=world_state.environment,
        )
