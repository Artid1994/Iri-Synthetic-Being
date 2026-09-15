"""
Synaptic connections between neuron populations.

Propagates spikes from source to target neurons with weighted connections.
"""
import numpy as np
from brain.population import NeuronPopulation


class Synapse:
    """
    Sparse synaptic connection between two populations.

    Maps specific source neurons to target neurons with weights.
    Lightweight representation for millions of potential connections.
    """

    def __init__(
        self,
        source: NeuronPopulation,
        source_chunk_index: int,
        target: NeuronPopulation,
        target_chunk_index: int,
        source_indices: list,
        target_indices: list,
        weights: list,
    ):
        # Validate same endpoints
        if (source is target and
            source_chunk_index == target_chunk_index):
            raise ValueError("Synapse cannot connect chunk to itself")

        # Validate mapping lengths
        if len(source_indices) != len(target_indices):
            raise ValueError("source_indices and target_indices must have same length")
        if len(source_indices) != len(weights):
            raise ValueError("indices and weights must have same length")

        self.source = source
        self.source_chunk_index = source_chunk_index
        self.target = target
        self.target_chunk_index = target_chunk_index

        # Convert to numpy arrays for efficient computation
        self.source_indices = np.array(source_indices, dtype=np.int32)
        self.target_indices = np.array(target_indices, dtype=np.int32)
        self.weights = np.array(weights, dtype=np.float32)

        # Validate indices are in range
        if len(self.source_indices) > 0:
            if np.max(self.source_indices) >= source.chunk_size:
                raise IndexError(
                    f"source_indices max {np.max(self.source_indices)} >= chunk_size {source.chunk_size}"
                )
            if np.max(self.target_indices) >= target.chunk_size:
                raise IndexError(
                    f"target_indices max {np.max(self.target_indices)} >= chunk_size {target.chunk_size}"
                )

    def propagate(self, source_spikes: np.ndarray) -> np.ndarray:
        """
        Propagate spikes through synapse.

        Args:
            source_spikes: Boolean array of source neuron spikes

        Returns:
            Float32 array of weighted currents to target neurons
        """
        if source_spikes.shape[0] != self.source.chunk_size:
            raise ValueError(
                f"source_spikes shape {source_spikes.shape} != chunk_size {self.source.chunk_size}"
            )

        # Initialize target current (zeros)
        target_current = np.zeros(self.target.chunk_size, dtype=np.float32)

        # For each connection, propagate weighted spike
        for i, src_idx in enumerate(self.source_indices):
            if source_spikes[src_idx]:
                tgt_idx = self.target_indices[i]
                target_current[tgt_idx] += self.weights[i]

        return target_current
