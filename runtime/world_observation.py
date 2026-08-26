from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorldObservation:
    position: tuple[float, float] = (0.0, 0.0)
    objects: tuple[str, ...] = ()
    environment: str = "empty"

    def render(self) -> str:
        objects = (
            ", ".join(self.objects)
            if self.objects
            else "none"
        )

        return (
            f"POSITION: {self.position}\n"
            f"OBJECTS: {objects}\n"
            f"ENVIRONMENT: {self.environment}"
        )
