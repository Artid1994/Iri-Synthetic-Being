"""
Hebbian plasticity for synaptic weight adaptation.

"Neurons that fire together, wire together."
Coactive connections are strengthened.
"""
import numpy as np
from brain.synapse import Synapse


class Plasticity:
    """
    Hebbian plasticity rule.

    Strengthens connections when pre- and post-synaptic
    neurons are coactive.
    """

    def __init__(
        self,
        learning_rate: float = 0.01,
        min_weight: float = 0.0,
        max_weight: float = 1.0,  # Default max = 1.0 for biological plausibility
    ):
        if learning_rate < 0 or learning_rate > 1:
            raise ValueError("learning_rate must be in [0, 1]")
        if not np.isfinite(learning_rate):
            raise ValueError("learning_rate must be finite")
        if min_weight > max_weight:
            raise ValueError("min_weight must be <= max_weight")

        self.learning_rate = learning_rate
        self.min_weight = min_weight
        self.max_weight = max_weight

    def adapt(
        self,
        synapse: Synapse,
        source_spikes: np.ndarray,
        target_spikes: np.ndarray,
    ) -> np.ndarray:
        """
        Adapt synapse weights based on spike coincidence.

        Args:
            synapse: Synapse to adapt
            source_spikes: Pre-synaptic spikes
            target_spikes: Post-synaptic spikes

        Returns:
            Updated weights
        """
        if source_spikes.shape[0] != synapse.source.chunk_size:
            raise ValueError("source_spikes shape mismatch")
        if target_spikes.shape[0] != synapse.target.chunk_size:
            raise ValueError("target_spikes shape mismatch")

        # Copy current weights
        new_weights = synapse.weights.copy()

        # For each connection, check coactivity
        for i in range(len(synapse.source_indices)):
            src_idx = synapse.source_indices[i]
            tgt_idx = synapse.target_indices[i]

            # Hebbian rule: strengthen if both active
            if source_spikes[src_idx] and target_spikes[tgt_idx]:
                new_weights[i] += self.learning_rate

        # Clamp weights to bounds
        new_weights = np.clip(new_weights, self.min_weight, self.max_weight)

        # Update synapse (mutate in place)
        synapse.weights = new_weights

        return new_weights
