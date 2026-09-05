from __future__ import annotations

import numpy as np

from brain.synapse import Synapse


class Plasticity:
    """Deterministic bounded co-activity rule for existing synapses."""

    def __init__(
        self,
        learning_rate: float = 0.1,
        min_weight: float = 0.0,
        max_weight: float = 1.0,
    ) -> None:
        values = (learning_rate, min_weight, max_weight)
        if not all(np.isfinite(value) for value in values):
            raise ValueError("plasticity configuration must be finite")
        if learning_rate < 0:
            raise ValueError("learning_rate must be non-negative")
        if min_weight > max_weight:
            raise ValueError("min_weight must not exceed max_weight")

        self.learning_rate = float(learning_rate)
        self.min_weight = float(min_weight)
        self.max_weight = float(max_weight)

    def adapt(
        self,
        synapse: Synapse,
        source_spikes,
        target_spikes,
    ) -> np.ndarray:
        if not isinstance(synapse, Synapse):
            raise TypeError("synapse must be a Synapse")

        source_spikes = np.asarray(source_spikes)
        target_spikes = np.asarray(target_spikes)
        source_length = synapse._chunk_length(
            synapse.source,
            synapse.source_chunk_index,
        )
        target_length = synapse._chunk_length(
            synapse.target,
            synapse.target_chunk_index,
        )

        if source_spikes.shape != (source_length,):
            raise ValueError("source_spikes shape must match source population chunk")
        if target_spikes.shape != (target_length,):
            raise ValueError("target_spikes shape must match target population chunk")

        coactive = (
            source_spikes[synapse.source_indices].astype(bool, copy=False)
            & target_spikes[synapse.target_indices].astype(bool, copy=False)
        )
        updated = np.asarray(synapse.weights, dtype=np.float32).copy()
        updated[coactive] += np.float32(self.learning_rate)
        updated = np.clip(
            updated,
            np.float32(self.min_weight),
            np.float32(self.max_weight),
        ).astype(np.float32, copy=False)

        synapse.weights = updated
        return updated
