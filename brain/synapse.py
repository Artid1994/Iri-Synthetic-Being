from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from brain.population import NeuronPopulation


class Synapse:
    """Fixed weighted signal projection between population chunks."""

    def __init__(
        self,
        source: NeuronPopulation,
        source_chunk_index: int,
        target: NeuronPopulation,
        target_chunk_index: int,
        source_indices: Sequence[int],
        target_indices: Sequence[int],
        weights: Sequence[float],
    ) -> None:
        if not isinstance(source, NeuronPopulation):
            raise TypeError("source must be a NeuronPopulation")
        if not isinstance(target, NeuronPopulation):
            raise TypeError("target must be a NeuronPopulation")
        if source is target and source_chunk_index == target_chunk_index:
            raise ValueError("Synapse endpoints must be distinct")

        source_length = self._chunk_length(source, source_chunk_index)
        target_length = self._chunk_length(target, target_chunk_index)

        source_indices = np.asarray(source_indices)
        target_indices = np.asarray(target_indices)
        weights = np.asarray(weights, dtype=np.float32)

        if source_indices.ndim != 1 or target_indices.ndim != 1 or weights.ndim != 1:
            raise ValueError("synapse mappings must be one-dimensional")
        if not (len(source_indices) == len(target_indices) == len(weights)):
            raise ValueError("source indices, target indices, and weights must have equal length")
        if not np.issubdtype(source_indices.dtype, np.integer):
            raise ValueError("source indices must be integers")
        if not np.issubdtype(target_indices.dtype, np.integer):
            raise ValueError("target indices must be integers")
        if not np.isfinite(weights).all():
            raise ValueError("weights must be finite")
        if ((source_indices < 0) | (source_indices >= source_length)).any():
            raise IndexError("source index out of range")
        if ((target_indices < 0) | (target_indices >= target_length)).any():
            raise IndexError("target index out of range")

        self.source = source
        self.source_chunk_index = source_chunk_index
        self.target = target
        self.target_chunk_index = target_chunk_index
        self.source_indices = source_indices.astype(np.intp, copy=True)
        self.target_indices = target_indices.astype(np.intp, copy=True)
        self.weights = weights.copy()

    @staticmethod
    def _chunk_length(population: NeuronPopulation, chunk_index: int) -> int:
        if not isinstance(chunk_index, (int, np.integer)):
            raise TypeError("chunk index must be an integer")
        return population._chunk_length(int(chunk_index))

    def propagate(self, source_spikes) -> np.ndarray:
        source_spikes = np.asarray(source_spikes)
        source_length = self._chunk_length(self.source, self.source_chunk_index)

        if source_spikes.shape != (source_length,):
            raise ValueError("source_spikes shape must match source population chunk")

        target_length = self._chunk_length(self.target, self.target_chunk_index)
        target_current = np.zeros(target_length, dtype=np.float32)
        active = source_spikes[self.source_indices].astype(np.float32, copy=False)
        np.add.at(target_current, self.target_indices, active * self.weights)
        return target_current
