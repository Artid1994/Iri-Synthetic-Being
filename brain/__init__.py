"""Neural Substrate Package for AE01M / The Transcending Form."""

from brain.neural_state import NeuralState
from brain.neuron import LIFNeuronVector, LIFNeuronVector as Neuron
from brain.plasticity import Plasticity
from brain.population import NeuronPopulation, PopulationStats
from brain.synapse import Synapse


class Node:
    """Represents an atomic structural neural unit or reference node in the substrate."""

    def __init__(self, node_id: str, label: str = "", region: str = "parietal") -> None:
        self.node_id = str(node_id)
        self.label = label or self.node_id
        self.region = region
        self.active: bool = False

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def __repr__(self) -> str:
        return f"<Node id={self.node_id!r} region={self.region!r} active={self.active}>"


__all__ = [
    "Node",
    "Neuron",
    "LIFNeuronVector",
    "Synapse",
    "NeuralState",
    "NeuronPopulation",
    "PopulationStats",
    "Plasticity",
]
