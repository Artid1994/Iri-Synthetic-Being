from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IdentityRepresentation:
    episodic: tuple[str, ...] = ()
    semantic: tuple[str, ...] = ()

    @classmethod
    def from_structured_memory(cls, structured_memory) -> "IdentityRepresentation":
        return cls(
            episodic=tuple(structured_memory.episodic),
            semantic=tuple(structured_memory.semantic),
        )
