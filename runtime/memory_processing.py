from __future__ import annotations

from dataclasses import dataclass

from runtime.human_data import HumanData


@dataclass(frozen=True)
class StructuredMemory:
    episodic: tuple[str, ...] = ()
    semantic: tuple[str, ...] = ()


class MemoryProcessor:
    def process(self, data: HumanData) -> StructuredMemory:
        episodic: list[str] = []
        semantic: list[str] = []

        for source in (
            data.biography,
            data.conversation,
            data.experiences,
            data.memories,
        ):
            if source is None:
                continue

            values = source if isinstance(source, (list, tuple)) else [source]

            for value in values:
                if not isinstance(value, str):
                    continue

                value = value.strip()

                if value and value not in episodic:
                    episodic.append(value)

        for source in (
            data.values,
            data.beliefs,
            data.preferences,
            data.decision_patterns,
            data.emotional_associations,
        ):
            if source is None:
                continue

            values = source if isinstance(source, (list, tuple)) else [source]

            for value in values:
                if not isinstance(value, str):
                    continue

                value = value.strip()

                if value and value not in semantic:
                    semantic.append(value)

        return StructuredMemory(
            episodic=tuple(episodic),
            semantic=tuple(semantic),
        )
