"""
Hippocampus region implementation.

Specialized for memory formation and storage.
"""
from brain.population import NeuronPopulation
from config.anatomy_settings import HIPPOCAMPUS
from typing import Set


class Hippocampus:
    """
    Hippocampus: memory formation and consolidation.

    Tracks stored memories and their neural representations.
    """

    def __init__(self):
        self.population = NeuronPopulation(HIPPOCAMPUS)
        self.region_name = HIPPOCAMPUS.name
        self.neuron_count = HIPPOCAMPUS.neuron_count

        # Track stored memories (content-addressed)
        self._memories: Set[str] = set()
        self._memory_to_chunk: dict = {}  # memory -> chunk_index mapping
        self._next_chunk = 0

    @property
    def memory_count(self) -> int:
        """Number of stored memories."""
        return len(self._memories)

    def has_memory(self, content: str) -> bool:
        """Check if memory is stored."""
        return content in self._memories

    def store(self, content: str) -> bool:
        """
        Store a memory.

        Args:
            content: Memory content

        Returns:
            True if new memory stored, False if duplicate or empty
        """
        # Reject empty content
        if not content or not content.strip():
            return False

        if content in self._memories:
            return False

        # Allocate chunk for this memory
        max_chunks = (self.neuron_count + HIPPOCAMPUS.chunk_size - 1) // HIPPOCAMPUS.chunk_size
        if self._next_chunk >= max_chunks:
            # Capacity reached, wrap around (simplified)
            self._next_chunk = 0

        chunk_index = self._next_chunk
        self._next_chunk += 1

        # Activate neurons for this memory (triggers allocation)
        import numpy as np
        activation = np.ones(HIPPOCAMPUS.chunk_size, dtype=np.float32) * 0.5
        self.population.step_chunk(chunk_index, activation)

        # Record memory
        self._memories.add(content)
        self._memory_to_chunk[content] = chunk_index

        return True

    def recall_chunk(self, content: str) -> int:
        """Get chunk index for memory content."""
        return self._memory_to_chunk.get(content, -1)
