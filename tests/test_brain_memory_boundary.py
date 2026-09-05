import unittest

import numpy as np

from brain.brain import Brain
from brain.plasticity import Plasticity
from brain.population import NeuronPopulation
from brain.synapse import Synapse
from config.anatomy_settings import NeuronParameters, RegionParameters
from runtime.brain_memory_bridge import BrainMemoryBridge
from runtime.memory import Memory


def population(name, threshold=1.0):
    return NeuronPopulation(
        RegionParameters(
            name=name,
            neuron_count=4,
            chunk_size=4,
            neuron=NeuronParameters(threshold=threshold),
        )
    )


def projection(target_threshold=1.0):
    source = population("source")
    target = population("target", target_threshold)
    synapse = Synapse(source, 0, target, 0, [0], [0], [1.0])
    return source, target, synapse


class TestBrainMemoryBoundary(unittest.TestCase):
    def test_memory_operations_do_not_change_brain_or_synapse(self):
        brain = Brain()
        memory = Memory()
        source, target, synapse = projection()
        brain.run_neural_projection_cycle(
            synapse, np.zeros(4, dtype=np.float32), Plasticity()
        )
        membranes = (source.allocate_chunk(0).membrane.copy(), target.allocate_chunk(0).membrane.copy())
        weights = synapse.weights.copy()

        memory.add_experience("experience")
        memory.associate("experience", "meaning")

        np.testing.assert_array_equal(source.allocate_chunk(0).membrane, membranes[0])
        np.testing.assert_array_equal(target.allocate_chunk(0).membrane, membranes[1])
        np.testing.assert_array_equal(synapse.weights, weights)

    def test_neural_cycle_does_not_change_memory_graph(self):
        brain = Brain()
        memory = Memory()
        memory.associate("experience", "meaning")
        nodes = set(memory.memory_graph.nodes)
        edges = {key: edge.weight for key, edge in memory.memory_graph.edges.items()}
        _, _, synapse = projection(target_threshold=0.1)

        brain.run_neural_projection_cycle(
            synapse, np.array([1, 0, 0, 0], dtype=np.float32), Plasticity()
        )

        self.assertEqual(set(memory.memory_graph.nodes), nodes)
        self.assertEqual(
            {key: edge.weight for key, edge in memory.memory_graph.edges.items()},
            edges,
        )

    def test_bridge_exports_isolated_snapshots(self):
        brain = Brain()
        memory = Memory()
        bridge = BrainMemoryBridge(brain, memory)
        _, _, synapse = projection(target_threshold=0.1)
        brain.run_neural_projection_cycle(
            synapse, np.array([1, 0, 0, 0], dtype=np.float32), Plasticity()
        )
        memory.associate("experience", "meaning")

        neural = bridge.neural_state_snapshot()
        events = bridge.memory_activity_snapshot()
        self.assertIsNot(neural, brain.neural_state)
        self.assertIsNot(events, memory.memory_activity_snapshot())
        neural["source_membrane"][0] = 99
        events["nodes"].clear()
        self.assertNotEqual(brain.neural_state.source_membrane[0], 99)
        self.assertTrue(bridge.memory_activity_snapshot()["nodes"])

    def test_empty_and_repeated_operations_are_deterministic(self):
        bridge = BrainMemoryBridge(Brain(), Memory())
        self.assertIsNone(bridge.neural_state_snapshot())
        self.assertEqual(bridge.memory_activity_snapshot(), {"nodes": [], "edges": []})
        self.assertEqual(bridge.memory_activity_snapshot(), {"nodes": [], "edges": []})

    def test_invalid_bridge_inputs_fail(self):
        with self.assertRaises(TypeError):
            BrainMemoryBridge(object(), Memory())
        with self.assertRaises(TypeError):
            BrainMemoryBridge(Brain(), object())

    def test_existing_memory_methods_remain_compatible(self):
        brain = Brain()
        memory = Memory()
        self.assertTrue(brain.store_memory("memory"))
        memory.add_experience("one")
        memory.add_experience("two")
        self.assertEqual(brain.sync_memory(memory), 2)
        self.assertEqual(brain.sync_memory(memory), 0)
        self.assertTrue(brain.has_memory("one"))


if __name__ == "__main__":
    unittest.main()
