from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from config.anatomy_settings import (
    NeuronParameters,
    RegionParameters,
)
from brain.neuron import LIFNeuronVector


@dataclass(frozen=True)
class PopulationStats:
    logical_neurons: int
    allocated_neurons: int
    chunk_size: int


class NeuronPopulation:
    """
    Logical neuron population backed by lazily allocated NumPy chunks.

    logical_neurons can be tens of millions without allocating all
    neuron state in RAM.
    """

    def __init__(
        self,
        parameters: RegionParameters,
    ) -> None:
        if parameters.neuron_count <= 0:
            raise ValueError("neuron_count must be positive")

        if parameters.chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        self.parameters = parameters
        self.logical_neurons = parameters.neuron_count
        self.chunk_size = parameters.chunk_size

        self._chunks: dict[int, LIFNeuronVector] = {}

    @property
    def allocated_neurons(self) -> int:
        return sum(
            len(chunk.membrane)
            for chunk in self._chunks.values()
        )

    @property
    def stats(self) -> PopulationStats:
        return PopulationStats(
            logical_neurons=self.logical_neurons,
            allocated_neurons=self.allocated_neurons,
            chunk_size=self.chunk_size,
        )

    def _chunk_length(self, chunk_index: int) -> int:
        start = chunk_index * self.chunk_size

        if start >= self.logical_neurons:
            raise IndexError("chunk index out of range")

        return min(
            self.chunk_size,
            self.logical_neurons - start,
        )

    def allocate_chunk(self, chunk_index: int) -> LIFNeuronVector:
        if chunk_index not in self._chunks:
            self._chunks[chunk_index] = LIFNeuronVector(
                self._chunk_length(chunk_index),
                parameters=self.parameters.neuron,
            )

        return self._chunks[chunk_index]

    def step_chunk(
        self,
        chunk_index: int,
        input_current,
    ) -> np.ndarray:
        chunk = self.allocate_chunk(chunk_index)

        return chunk.step(input_current)

    def allocated_chunk_indices(self) -> tuple[int, ...]:
        return tuple(sorted(self._chunks))
