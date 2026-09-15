#!/usr/bin/env python3
"""Test autonomous learning cycle: PERCEIVE → COGNIZE → LEARN → PERSIST → RECALL."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, '.')

from runtime.runtime import TranscendingRuntime


class TestAutonomousLearningCycle(unittest.TestCase):
    """Test complete autonomous learning path."""

    def setUp(self):
        """Clean state for each test."""
        self.state_file = Path("03_Hippocampus/test_autonomous_cycle.json")
        if self.state_file.exists():
            self.state_file.unlink()

    def tearDown(self):
        """Cleanup test state."""
        if self.state_file.exists():
            self.state_file.unlink()

    def test_perceive_cognize_learn_path(self):
        """Test: PERCEIVE → COGNIZE → LEARN updates memory."""
        runtime = TranscendingRuntime()
        
        mem_before = len(runtime.memory.snapshot().episodic)
        
        # Perception
        observation = "Thai consonant ก makes /k/ sound"
        result = runtime.cognitive_loop.process(observation)
        
        # Verify cognition happened
        self.assertEqual(result.decision, "RESPOND")
        self.assertTrue(result.attention_required)
        
        # Verify learning happened
        self.assertTrue(result.experience_recorded)
        
        # Verify memory updated
        mem_after = len(runtime.memory.snapshot().episodic)
        self.assertGreater(mem_after, mem_before)

    def test_persistent_state_survives_restart(self):
        """Test: Knowledge persists across process restarts."""
        # Cycle 1: Learn
        runtime1 = TranscendingRuntime()
        runtime1.cognitive_loop.process("Thai consonant ก = /k/")
        runtime1.save_memory_brain_snapshot(self.state_file)
        
        # Cycle 2: Recall (new process)
        runtime2 = TranscendingRuntime()
        runtime2.load_memory_brain_snapshot(self.state_file)
        
        memories = runtime2.memory.snapshot().episodic
        all_content = " ".join(memories)
        
        self.assertIn("ก", all_content)
        self.assertIn("/k/", all_content)

    def test_later_cycles_use_prior_knowledge(self):
        """Test: Later cycles can access earlier learned knowledge."""
        runtime = TranscendingRuntime()
        
        # Learn
        runtime.cognitive_loop.process("Thai consonant ก = /k/")
        runtime.save_memory_brain_snapshot(self.state_file)
        
        # Load and verify knowledge available
        runtime2 = TranscendingRuntime()
        runtime2.load_memory_brain_snapshot(self.state_file)
        
        mem = runtime2.memory.snapshot()
        self.assertGreater(len(mem.episodic), 0)
        
        # New cycle can access prior memories
        result = runtime2.cognitive_loop.process("What is ก?")
        self.assertEqual(result.decision, "RESPOND")

    def test_knowledge_accumulates_across_cycles(self):
        """Test: Multiple learning cycles accumulate knowledge."""
        runtime = TranscendingRuntime()
        
        observations = [
            "Thai consonant ก = /k/",
            "Thai consonant ข = /kh/",
            "Thai consonant ค = /kh/",
        ]
        
        for obs in observations:
            runtime.cognitive_loop.process(obs)
        
        mem = runtime.memory.snapshot()
        self.assertEqual(len(mem.episodic), len(observations))

    def test_autonomous_step_integrates_with_cognitive_loop(self):
        """Test: autonomous_step() triggers cognitive_loop and learning."""
        runtime = TranscendingRuntime()
        
        mem_before = len(runtime.memory.snapshot().episodic)
        
        result = runtime.autonomous_step("Learn: Thai consonant ง = /ng/")
        
        # Verify autonomous_step executed
        self.assertIn("observation", result)
        self.assertIn("reasoning", result)
        self.assertIn("decision", result)
        
        # Verify memory was updated (cognitive_loop was called)
        mem_after = len(runtime.memory.snapshot().episodic)
        self.assertGreater(mem_after, mem_before)

    def test_empty_input_filtered_correctly(self):
        """Test: Empty/invalid input doesn't create spurious learning."""
        runtime = TranscendingRuntime()
        
        result = runtime.cognitive_loop.process("")
        
        # Empty input should not trigger attention
        self.assertEqual(result.decision, "NO_ACTION")
        self.assertFalse(result.experience_recorded)

    def test_multi_cycle_autonomous_operation(self):
        """Test: Multiple cycles work without external prompts."""
        runtime = TranscendingRuntime()
        
        observations = [
            "Concept A",
            "Concept B", 
            "Concept C",
        ]
        
        learned_count = 0
        for obs in observations:
            result = runtime.cognitive_loop.process(obs)
            if result.experience_recorded:
                learned_count += 1
        
        self.assertEqual(learned_count, len(observations))
        
        mem = runtime.memory.snapshot()
        self.assertEqual(len(mem.episodic), len(observations))


if __name__ == "__main__":
    unittest.main()
