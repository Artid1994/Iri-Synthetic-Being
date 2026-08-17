from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentState:
    name: str = "empty"
    time: float = 0.0


class Environment:
    def __init__(self) -> None:
        self.state = EnvironmentState()

    def update(
        self,
        name: str | None = None,
        time: float | None = None,
    ) -> None:
        self.state = EnvironmentState(
            name=self.state.name if name is None else name,
            time=self.state.time if time is None else time,
        )

    def snapshot(self) -> EnvironmentState:
        return EnvironmentState(
            name=self.state.name,
            time=self.state.time,
        )
