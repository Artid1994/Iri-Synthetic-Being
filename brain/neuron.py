from __future__ import annotations

import numpy as np

from config.anatomy_settings import NeuronParameters


class LIFNeuronVector:
    """Vectorized Leaky Integrate-and-Fire state."""

    def __init__(
        self,
        size: int,
        parameters: NeuronParameters | None = None,
    ) -> None:
        if size <= 0:
            raise ValueError("size must be positive")

        self.parameters = parameters or NeuronParameters()
        self.membrane = np.zeros(size, dtype=np.float32)

    def step(self, input_current) -> np.ndarray:
        current = np.asarray(
            input_current,
            dtype=np.float32,
        )

        if current.shape != self.membrane.shape:
            raise ValueError(
                "input_current shape must match neuron population"
            )

        self.membrane = (
            self.membrane * self.parameters.leak
            + current
        )

        spikes = (
            self.membrane
            >= self.parameters.threshold
        )

        self.membrane[spikes] = self.parameters.reset

        return spikes
