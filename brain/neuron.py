"""
Leaky Integrate-and-Fire (LIF) neuron model.
Vectorized implementation for computational efficiency.
"""
import numpy as np
from config.anatomy_settings import NeuronParameters


class LIFNeuronVector:
    """
    Vectorized LIF neuron population.

    Membrane potential integrates input current, leaks toward rest,
    and generates spike when threshold is exceeded.
    """

    def __init__(self, size: int, params: NeuronParameters = None):
        if size <= 0:
            raise ValueError("size must be positive")

        self.size = size
        self.params = params or NeuronParameters()

        # State: membrane potential (float32 for memory efficiency)
        self.membrane = np.zeros(size, dtype=np.float32)

    def step(self, current: np.ndarray, dt: float = 1.0) -> np.ndarray:
        """
        Single timestep update.

        Args:
            current: Input current for each neuron
            dt: Time step

        Returns:
            Boolean spike array
        """
        if current.shape != (self.size,):
            raise ValueError(f"current shape {current.shape} != expected {(self.size,)}")

        # Integrate current (before leak for immediate spike capability)
        self.membrane += current

        # Detect spikes
        spikes = self.membrane >= self.params.threshold

        # Reset spiked neurons
        self.membrane[spikes] = self.params.reset

        # Apply leak to non-spiked neurons
        self.membrane[~spikes] *= (1.0 - self.params.leak)

        return spikes

    def reset(self):
        """Reset all membrane potentials to rest."""
        self.membrane.fill(0.0)
