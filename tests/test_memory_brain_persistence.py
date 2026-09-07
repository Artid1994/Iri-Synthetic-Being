import unittest
import tempfile
import json
from pathlib import Path

from runtime.runtime import TranscendingRuntime
from runtime.memory import Memory
from runtime.experience import Experience
from runtime.safety_event import SafetyEvent
from brain.brain import Brain
from runtime.memory_brain_persistence import (
    MemoryBrainPersistence,
    PersistenceSchemaError,
)


class FakeCognitive:
    def process(self, user_input, record_experience=True):
        return "tree is near the house"

    def snapshot(self):
        return {}


class TestMemoryBrainPersistence(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.snapshot_file = Path(self.temp_dir.name) / "memory_brain_snapshot.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_memory_survives_runtime_restart(self):
        runtime1 = TranscendingRuntime(cognitive=FakeCognitive())
        runtime1.memory.add_working("Active idea")
        runtime1.memory.add_experience("First episodic event")
        runtime1.memory.add_semantic("Robots need energy")
        runtime1.memory.add_experience_object(
            Experience(
                source="sensor",
                content="Lidar point cloud",
                timestamp=12345.67,
                modality="spatial",
                salience=0.8,
            )
        )
        runtime1.memory.add_safety_event(
            SafetyEvent(
                action="halt",
                value=None,
                reason="proximity_breach",
            )
        )
        runtime1.save_memory_brain_snapshot(self.snapshot_file)

        # Restart runtime
        runtime2 = TranscendingRuntime(cognitive=FakeCognitive())
        self.assertTrue(runtime2.memory.is_empty())

        runtime2.load_memory_brain_snapshot(self.snapshot_file)

        # Assert memory reconstructed exactly
        self.assertEqual(runtime2.memory.working_memory(), ["Active idea"])
        self.assertEqual(runtime2.memory.state.episodic, ["First episodic event"])
        self.assertEqual(runtime2.memory.state.semantic, ["Robots need energy"])
        self.assertEqual(len(runtime2.memory.state.experiences), 1)
        self.assertEqual(runtime2.memory.state.experiences[0].content, "Lidar point cloud")
        self.assertEqual(runtime2.memory.state.experiences[0].salience, 0.8)
        self.assertEqual(len(runtime2.memory.state.safety_events), 1)
        self.assertEqual(runtime2.memory.state.safety_events[0].reason, "proximity_breach")

    def test_memory_graph_nodes_and_edges_survive_restart(self):
        runtime1 = TranscendingRuntime(cognitive=FakeCognitive())
        runtime1.memory.associate("rain", "wet ground")
        self.assertIn("EPISODIC:rain", runtime1.memory.memory_graph.nodes)
        self.assertIn("SEMANTIC:wet ground", runtime1.memory.memory_graph.nodes)
        self.assertIn(
            ("EPISODIC:rain", "SEMANTIC:wet ground"),
            runtime1.memory.memory_graph.edges,
        )
        runtime1.save_memory_brain_snapshot(self.snapshot_file)

        # Restart runtime
        runtime2 = TranscendingRuntime(cognitive=FakeCognitive())
        runtime2.load_memory_brain_snapshot(self.snapshot_file)

        graph = runtime2.memory.memory_graph
        self.assertIn("EPISODIC:rain", graph.nodes)
        self.assertIn("SEMANTIC:wet ground", graph.nodes)
        self.assertIn(("EPISODIC:rain", "SEMANTIC:wet ground"), graph.edges)
        edge = graph.edges[("EPISODIC:rain", "SEMANTIC:wet ground")]
        self.assertGreaterEqual(edge.weight, 1.0)
        self.assertEqual(runtime2.memory.associations("rain"), ["wet ground"])

    def test_brain_hippocampus_state_survives_restart(self):
        runtime1 = TranscendingRuntime(cognitive=FakeCognitive())
        runtime1.memory.add_experience("Observation 1")
        runtime1.memory.add_experience("Observation 2")
        synced = runtime1.sync_brain_memory()
        self.assertEqual(synced, 2)
        self.assertTrue(runtime1.brain.hippocampus.has_memory("Observation 1"))
        self.assertTrue(runtime1.brain.hippocampus.has_memory("Observation 2"))

        runtime1.save_memory_brain_snapshot(self.snapshot_file)

        # Restart runtime
        runtime2 = TranscendingRuntime(cognitive=FakeCognitive())
        self.assertFalse(runtime2.brain.hippocampus.has_memory("Observation 1"))

        runtime2.load_memory_brain_snapshot(self.snapshot_file)

        self.assertTrue(runtime2.brain.hippocampus.has_memory("Observation 1"))
        self.assertTrue(runtime2.brain.hippocampus.has_memory("Observation 2"))
        self.assertEqual(runtime2.brain.hippocampus.memory_count, 2)

    def test_learned_research_knowledge_can_be_recalled_after_restart(self):
        runtime1 = TranscendingRuntime(cognitive=FakeCognitive())
        runtime1.memory.add_semantic("Quantum entanglement exhibits non-local correlation")
        runtime1.memory.add_experience("Verified paper on Bell inequalities")
        runtime1.save_memory_brain_snapshot(self.snapshot_file)

        runtime2 = TranscendingRuntime(cognitive=FakeCognitive())
        runtime2.load_memory_brain_snapshot(self.snapshot_file)

        # Test recall and semantic search
        self.assertTrue(runtime2.memory.semantic_contains("Quantum entanglement exhibits non-local correlation"))
        recalled = runtime2.memory.recall("Verified paper on Bell inequalities")
        self.assertEqual(recalled, "Verified paper on Bell inequalities")

    def test_empty_persistence_initializes_safely(self):
        memory = Memory()
        brain = Brain()
        MemoryBrainPersistence.save(memory, brain, self.snapshot_file)

        restored_mem, restored_brain = MemoryBrainPersistence.load(self.snapshot_file)
        self.assertTrue(restored_mem.is_empty())
        self.assertEqual(restored_brain.hippocampus.memory_count, 0)

    def test_corrupted_and_incompatible_persistence_rejected_safely(self):
        # Incompatible version
        with open(self.snapshot_file, "w") as f:
            json.dump({"version": "999.0.0", "type": "ae01m_memory_brain_snapshot"}, f)

        with self.assertRaises(PersistenceSchemaError):
            MemoryBrainPersistence.load(self.snapshot_file)

        # Corrupted JSON
        with open(self.snapshot_file, "w") as f:
            f.write("NOT_A_VALID_JSON{:::}")

        with self.assertRaises(PersistenceSchemaError):
            MemoryBrainPersistence.load(self.snapshot_file)

        # Invalid snapshot type
        with open(self.snapshot_file, "w") as f:
            json.dump({"version": "1.0.0", "type": "wrong_type"}, f)

        with self.assertRaises(PersistenceSchemaError):
            MemoryBrainPersistence.load(self.snapshot_file)

    def test_snapshot_restore_dict_integration_in_runtime(self):
        runtime1 = TranscendingRuntime(cognitive=FakeCognitive())
        runtime1.memory.add_semantic("Integrated Knowledge")
        runtime1.brain.store_memory("Bio Memory")
        snap = runtime1.snapshot()

        runtime2 = TranscendingRuntime(cognitive=FakeCognitive())
        runtime2.restore(snap)

        self.assertTrue(runtime2.memory.semantic_contains("Integrated Knowledge"))
        self.assertTrue(runtime2.brain.has_memory("Bio Memory"))


if __name__ == "__main__":
    unittest.main()
