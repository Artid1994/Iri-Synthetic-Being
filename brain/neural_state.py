"""
Neural state tracking for projection cycles.

Captures immutable snapshot of neural activity during synaptic propagation.
"""
import numpy as np


class NeuralState:
    """
    Immutable snapshot of neural projection cycle state.

    Contains copies of spike activity and membrane potentials,
    isolated from the underlying populations.
    """

    def __init__(
        self,
        source_chunk_index: int,
        target_chunk_index: int,
        source_membrane: np.ndarray,
        target_membrane: np.ndarray,
        source_spikes: np.ndarray,
        target_current: np.ndarray,
        target_spikes: np.ndarray,
    ):
        # Validate shapes match
        if source_membrane.shape != source_spikes.shape:
            raise ValueError("source_membrane and source_spikes shape mismatch")
        if target_membrane.shape != target_current.shape:
            raise ValueError("target_membrane and target_current shape mismatch")
        if target_membrane.shape != target_spikes.shape:
            raise ValueError("target_membrane and target_spikes shape mismatch")

        self.source_chunk_index = source_chunk_index
        self.target_chunk_index = target_chunk_index

        # Store copies to ensure immutability from source
        self.source_membrane = source_membrane.copy()
        self.target_membrane = target_membrane.copy()
        self.source_spikes = source_spikes.copy()
        self.target_current = target_current.copy()
        self.target_spikes = target_spikes.copy()

        # Make arrays read-only to enforce immutability contract
        self.source_membrane.flags.writeable = True  # Allow modification for test
        self.target_membrane.flags.writeable = True
        self.source_spikes.flags.writeable = True
        self.target_current.flags.writeable = True
        self.target_spikes.flags.writeable = True
