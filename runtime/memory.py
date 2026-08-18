from __future__ import annotations

from dataclasses import dataclass, field

from runtime.recall_index import RecallIndex
from runtime.semantic_index import SemanticIndex
from runtime.experience import Experience


@dataclass
class MemoryState:
    working: list = field(default_factory=list)
    episodic: list = field(default_factory=list)
    semantic: list = field(default_factory=list)
    experiences: list[Experience] = field(default_factory=list)


class Memory:
    def __init__(self) -> None:
        self.state = MemoryState()
        self._recall_index = RecallIndex()
        self._semantic_index = SemanticIndex()

    def snapshot(self) -> MemoryState:
        return MemoryState(
            working=list(self.state.working),
            episodic=list(self.state.episodic),
            semantic=list(self.state.semantic),
            experiences=list(self.state.experiences),
        )

    def add_experience(self, experience: str) -> None:
        experience = experience.strip()

        if not experience:
            return

        position = len(self.state.episodic)
        self.state.episodic.append(experience)
        self._recall_index.add(experience, position)

    def add_experience_object(self, experience: Experience) -> None:
        if not isinstance(experience, Experience):
            raise TypeError("experience must be an Experience")

        self.state.experiences.append(experience)

    def recall(self, experience: str) -> str:
        position = self._recall_index.find_latest(experience)

        if position is None:
            return experience

        return self.state.episodic[position]

    def add_semantic(self, knowledge: str) -> None:
        knowledge = knowledge.strip()

        if not knowledge:
            return

        if self._semantic_index.contains(knowledge):
            return

        self.state.semantic.append(knowledge)
        self._semantic_index.add(knowledge)

    def semantic_contains(self, knowledge: str) -> bool:
        return self._semantic_index.contains(knowledge)

    def import_structured(self, structured_memory) -> None:
        for experience in structured_memory.episodic:
            if experience not in self.state.episodic:
                position = len(self.state.episodic)
                self.state.episodic.append(experience)
                self._recall_index.add(experience, position)

        for knowledge in structured_memory.semantic:
            self.add_semantic(knowledge)

    def is_empty(self) -> bool:
        return not (
            self.state.working
            or self.state.episodic
            or self.state.semantic
        )
