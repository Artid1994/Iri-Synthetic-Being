from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class NeuralState:
    """Inspectable snapshot of one neural projection cycle."""

    source_chunk_index: int
    target_chunk_index: int
    source_membrane: np.ndarray
    target_membrane: np.ndarray
    source_spikes: np.ndarray
    target_current: np.ndarray
    target_spikes: np.ndarray

    def __post_init__(self) -> None:
        if not isinstance(self.source_chunk_index, (int, np.integer)):
            raise TypeError("source_chunk_index must be an integer")
        if not isinstance(self.target_chunk_index, (int, np.integer)):
            raise TypeError("target_chunk_index must be an integer")

        arrays = (
            ("source_membrane", self.source_membrane, np.float32),
            ("target_membrane", self.target_membrane, np.float32),
            ("source_spikes", self.source_spikes, np.bool_),
            ("target_current", self.target_current, np.float32),
            ("target_spikes", self.target_spikes, np.bool_),
        )
        for name, value, dtype in arrays:
            array = np.asarray(value)
            if array.ndim != 1:
                raise ValueError(f"{name} must be one-dimensional")
            if array.dtype != np.dtype(dtype):
                raise ValueError(f"{name} must have dtype {np.dtype(dtype)}")
            object.__setattr__(self, name, array.copy())

        if self.source_membrane.shape != self.source_spikes.shape:
            raise ValueError("source membrane and spikes must have equal shape")
        if self.target_membrane.shape != self.target_spikes.shape:
            raise ValueError("target membrane and spikes must have equal shape")
        if self.target_current.shape != self.target_spikes.shape:
            raise ValueError("target current and spikes must have equal shape")
