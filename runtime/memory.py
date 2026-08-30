from __future__ import annotations

from dataclasses import dataclass, field

from runtime.recall_index import RecallIndex
from runtime.association_index import AssociationIndex
from runtime.semantic_index import SemanticIndex
from runtime.experience import Experience
from runtime.safety_event import SafetyEvent


@dataclass
class MemoryState:
    working: list = field(default_factory=list)
    episodic: list = field(default_factory=list)
    semantic: list = field(default_factory=list)
    experiences: list[Experience] = field(default_factory=list)
    safety_events: list[SafetyEvent] = field(default_factory=list)


class Memory:
    def __init__(self) -> None:
        self.state = MemoryState()
        self._recall_index = RecallIndex()
        self._semantic_index = SemanticIndex()
        self._association_index = AssociationIndex()

    def snapshot(self) -> MemoryState:
        return MemoryState(
            working=list(self.state.working),
            episodic=list(self.state.episodic),
            semantic=list(self.state.semantic),
            experiences=list(self.state.experiences),
            safety_events=list(self.state.safety_events),
        )

    def add_working(
        self,
        item: str,
        capacity: int = 7,
    ) -> None:
        item = item.strip()

        if not item:
            return

        if capacity <= 0:
            raise ValueError("Working memory capacity must be positive")

        self.state.working.append(item)

        if len(self.state.working) > capacity:
            del self.state.working[:-capacity]

    def working_memory(self) -> list:
        return list(self.state.working)

    def clear_working(self) -> None:
        self.state.working.clear()

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

    def associate(
        self,
        experience: str,
        association: str,
    ) -> None:
        experience = experience.strip()
        association = association.strip()

        if not experience or not association:
            return

        self._association_index.add(
            experience,
            association,
        )

    def associations(self, experience: str) -> list[str]:
        experience = experience.strip()

        if not experience:
            return []

        return self._association_index.find(experience)

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


    def add_safety_event(self, event: SafetyEvent) -> None:
        if not isinstance(event, SafetyEvent):
            raise TypeError("event must be a SafetyEvent")

        self.state.safety_events.append(event)

    def import_structured(self, structured_memory) -> None:
        for experience in structured_memory.episodic:
            if experience not in self.state.episodic:
                position = len(self.state.episodic)
                self.state.episodic.append(experience)
                self._recall_index.add(experience, position)

        for knowledge in structured_memory.semantic:
            self.add_semantic(knowledge)

    def prune(
        self,
        max_experiences: int = 256,
        max_safety_events: int = 256,
        max_episodic: int = 512,
    ) -> None:
        if max_experiences < 0:
            raise ValueError("max_experiences must be non-negative")

        if max_safety_events < 0:
            raise ValueError("max_safety_events must be non-negative")

        if max_episodic < 0:
            raise ValueError("max_episodic must be non-negative")

        if len(self.state.experiences) > max_experiences:
            del self.state.experiences[:-max_experiences]

        if len(self.state.episodic) > max_episodic:
            self.state.episodic = self.state.episodic[-max_episodic:]
            self._recall_index.rebuild(self.state.episodic)

        if len(self.state.safety_events) > max_safety_events:
            del self.state.safety_events[:-max_safety_events]

    def is_empty(self) -> bool:
        return not (
            self.state.working
            or self.state.episodic
            or self.state.semantic
        )
