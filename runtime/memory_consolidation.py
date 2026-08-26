from __future__ import annotations

from dataclasses import dataclass

from runtime.memory import Memory


@dataclass(frozen=True)
class ConsolidationResult:
    item: str
    consolidated: bool
    semantic_promoted: bool = False


class MemoryConsolidation:
    def __init__(self, memory: Memory) -> None:
        if not isinstance(memory, Memory):
            raise TypeError("memory must be a Memory")

        self.memory = memory

    def consolidate(
        self,
        item: str,
        promote_semantic: bool = False,
    ) -> ConsolidationResult:
        item = item.strip()

        if not item:
            return ConsolidationResult(
                item=item,
                consolidated=False,
            )

        if item not in self.memory.working_memory():
            return ConsolidationResult(
                item=item,
                consolidated=False,
            )

        if item not in self.memory.state.episodic:
            self.memory.add_experience(item)

        semantic_promoted = False

        if promote_semantic:
            before = self.memory.semantic_contains(item)
            self.memory.add_semantic(item)
            semantic_promoted = not before

        return ConsolidationResult(
            item=item,
            consolidated=True,
            semantic_promoted=semantic_promoted,
        )
