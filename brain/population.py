"""
Neuron population with lazy chunk allocation.

Supports biological-scale neuron counts (millions) without allocating
all memory upfront. Only requested chunks are allocated.
"""
import numpy as np
from dataclasses import dataclass
from typing import Dict

from brain.neuron import LIFNeuronVector
from config.anatomy_settings import RegionParameters


@dataclass(frozen=True)
class PopulationStats:
    """Statistics about population allocation."""
    logical_neurons: int
    allocated_neurons: int
    chunk_count: int
    chunk_size: int


class NeuronPopulation:
    """
    Lazy-allocated neuron population.

    Maintains logical count (e.g., 40M) but only allocates
    chunks as they are accessed.
    """

    def __init__(self, region: RegionParameters):
        self.region = region
        self.neuron_count = region.neuron_count
        self.chunk_size = region.chunk_size

        # Lazy allocation: chunks created on first access
        self._chunks: Dict[int, LIFNeuronVector] = {}

    @property
    def stats(self) -> PopulationStats:
        """Current allocation statistics."""
        return PopulationStats(
            logical_neurons=self.neuron_count,
            allocated_neurons=len(self._chunks) * self.chunk_size,
            chunk_count=len(self._chunks),
            chunk_size=self.chunk_size,
        )

    def _get_or_create_chunk(self, chunk_index: int) -> LIFNeuronVector:
        """Lazy chunk allocation."""
        if chunk_index < 0:
            raise IndexError(f"chunk_index {chunk_index} < 0")

        max_chunks = (self.neuron_count + self.chunk_size - 1) // self.chunk_size
        if chunk_index >= max_chunks:
            raise IndexError(
                f"chunk_index {chunk_index} >= max_chunks {max_chunks}"
            )

        if chunk_index not in self._chunks:
            # Allocate chunk on first access
            chunk_neuron_count = min(
                self.chunk_size,
                self.neuron_count - chunk_index * self.chunk_size
            )
            self._chunks[chunk_index] = LIFNeuronVector(
                chunk_neuron_count,
                self.region.neuron
            )

        return self._chunks[chunk_index]

    def step_chunk(self, chunk_index: int, current: np.ndarray) -> np.ndarray:
        """
        Step a single chunk.

        Args:
            chunk_index: Which chunk to step
            current: Input current array

        Returns:
            Boolean spike array for the chunk
        """
        chunk = self._get_or_create_chunk(chunk_index)
        return chunk.step(current)

    def reset_chunk(self, chunk_index: int):
        """Reset a chunk if it exists."""
        if chunk_index in self._chunks:
            self._chunks[chunk_index].reset()

    def reset_all(self):
        """Reset all allocated chunks."""
        for chunk in self._chunks.values():
            chunk.reset()

    def allocate_chunk(self, chunk_index: int) -> LIFNeuronVector:
        """Explicitly allocate and return a chunk."""
        return self._get_or_create_chunk(chunk_index)

    def allocated_chunk_indices(self) -> tuple:
        """Return tuple of allocated chunk indices."""
        return tuple(sorted(self._chunks.keys()))
