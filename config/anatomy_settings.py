from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NeuronParameters:
    threshold: float = 1.0
    reset: float = 0.0
    leak: float = 0.95


@dataclass(frozen=True)
class RegionParameters:
    name: str
    neuron_count: int
    chunk_size: int = 8192
    neuron: NeuronParameters = NeuronParameters()


HIPPOCAMPUS = RegionParameters(
    name="hippocampus",
    neuron_count=40_000_000,
)

MOTOR_CORTEX = RegionParameters(
    name="motor_cortex",
    neuron_count=60_000_000,
)

TOTAL_NEURONS = (
    HIPPOCAMPUS.neuron_count
    + MOTOR_CORTEX.neuron_count
)
