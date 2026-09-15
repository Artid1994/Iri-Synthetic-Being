"""
Anatomical configuration for brain substrate.
Defines neuron and region parameters with resource-efficient lazy allocation.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class NeuronParameters:
    """LIF neuron model parameters."""
    threshold: float = 1.0          # Spike threshold
    reset: float = 0.0              # Post-spike reset potential
    leak: float = 0.1               # Membrane leak rate
    tau: float = 20.0               # Time constant (ms)
    
    def __post_init__(self):
        if self.threshold <= 0:
            raise ValueError("threshold must be positive")
        if self.leak < 0 or self.leak > 1:
            raise ValueError("leak must be in [0, 1]")
        if self.tau <= 0:
            raise ValueError("tau must be positive")


@dataclass(frozen=True)
class RegionParameters:
    """Brain region configuration."""
    name: str
    neuron_count: int               # Logical neuron count
    chunk_size: int = 1024          # Allocation chunk size
    neuron: NeuronParameters = None # Neuron parameters
    
    def __post_init__(self):
        if self.neuron_count <= 0:
            raise ValueError("neuron_count must be positive")
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if self.chunk_size > self.neuron_count:
            object.__setattr__(self, "chunk_size", self.neuron_count)
        # Set default neuron params if not provided
        if self.neuron is None:
            object.__setattr__(self, "neuron", NeuronParameters())


# Biologically-inspired region scales (reduced for hardware constraints)
# Using 100M total neurons as documented in tests
HIPPOCAMPUS = RegionParameters(
    name="hippocampus",
    neuron_count=40_000_000,
    chunk_size=1024,
    neuron=NeuronParameters(threshold=1.0, leak=0.05),
)

MOTOR_CORTEX = RegionParameters(
    name="motor_cortex",
    neuron_count=60_000_000,
    chunk_size=2048,
    neuron=NeuronParameters(threshold=1.2, leak=0.08),
)

TOTAL_NEURONS = HIPPOCAMPUS.neuron_count + MOTOR_CORTEX.neuron_count
