from __future__ import annotations

from brain.population import NeuronPopulation
from config.anatomy_settings import HIPPOCAMPUS


class Hippocampus:
    def __init__(self) -> None:
        self.population = NeuronPopulation(HIPPOCAMPUS)
        self._memories: set[str] = set()

    @property
    def neuron_count(self) -> int:
        return self.population.logical_neurons

    @property
    def memory_count(self) -> int:
        return len(self._memories)

    def store_memory(self, memory: str) -> bool:
        memory = memory.strip()

        if not memory:
            return False

        if memory in self._memories:
            return False

        self._memories.add(memory)
        return True

    def has_memory(self, memory: str) -> bool:
        return memory.strip() in self._memories
