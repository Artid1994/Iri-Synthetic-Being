from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorldState:
    position: tuple[float, float] = (0.0, 0.0)
    objects: tuple[str, ...] = ()
    environment: str = "empty"


class WorldModel:
    def __init__(self) -> None:
        self.state = WorldState()

    def update(
        self,
        position: tuple[float, float] | None = None,
        objects: tuple[str, ...] | None = None,
        environment: str | None = None,
    ) -> None:
        self.state = WorldState(
            position=(
                self.state.position
                if position is None
                else tuple(position)
            ),
            objects=(
                self.state.objects
                if objects is None
                else tuple(objects)
            ),
            environment=(
                self.state.environment
                if environment is None
                else environment
            ),
        )

    def snapshot(self) -> WorldState:
        return WorldState(
            position=self.state.position,
            objects=self.state.objects,
            environment=self.state.environment,
        )
