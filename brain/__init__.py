# Brain substrate module

# Export brain components for test compatibility
from brain.brain import Brain
from brain.neuron import LIFNeuronVector
from brain.population import NeuronPopulation
from brain.synapse import Synapse
from brain.neural_state import NeuralState
from brain.plasticity import Plasticity

# Aliases for test compatibility
Neuron = LIFNeuronVector  # Tests expect "Neuron" class


# Node is referenced in tests but not part of neural substrate
# Create minimal Node for test compatibility
class Node:
    """Minimal node primitive for test compatibility."""
    def __init__(self, node_id: str, label: str = ""):
        self.node_id = node_id
        self.label = label
        self.active = False

        # Infer region from node_id prefix if present
        self.region = node_id.split("_")[0] if "_" in node_id else "default"

    def activate(self):
        """Mark node as active."""
        self.active = True

    def deactivate(self):
        """Mark node as inactive."""
        self.active = False


__all__ = [
    "Brain",
    "Node",
    "Neuron",
    "LIFNeuronVector",
    "NeuronPopulation",
    "Synapse",
    "NeuralState",
    "Plasticity",
]
