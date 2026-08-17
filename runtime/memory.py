from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MemoryState:
    working: list = field(default_factory=list)
    episodic: list = field(default_factory=list)
    semantic: list = field(default_factory=list)


class Memory:
    def __init__(self) -> None:
        self.state = MemoryState()

    def snapshot(self) -> MemoryState:
        return MemoryState(
            working=list(self.state.working),
            episodic=list(self.state.episodic),
            semantic=list(self.state.semantic),
        )

    def add_experience(self, experience: str) -> None:
        experience = experience.strip()

        if not experience:
            return

        self.state.episodic.append(experience)

    def import_structured(self, structured_memory) -> None:
        for experience in structured_memory.episodic:
            if experience not in self.state.episodic:
                self.state.episodic.append(experience)

        for knowledge in structured_memory.semantic:
            if knowledge not in self.state.semantic:
                self.state.semantic.append(knowledge)

    def is_empty(self) -> bool:
        return not (
            self.state.working
            or self.state.episodic
            or self.state.semantic
        )
