"""
Tests for v1.1 features: compaction, real execution integration.
"""

import unittest
from dev_workflow.compaction import StateCompactor
from dev_workflow.state import WorkflowState, FindingSeverity, ReviewerFinding
from dev_workflow.orchestrator import WorkflowOrchestrator


class TestStateCompaction(unittest.TestCase):
    """Test state compaction."""
    
    def test_compaction_reduces_size(self):
        """Compaction reduces state size."""
        compactor = StateCompactor()
        state = WorkflowState(
            task_id="test",
            goal="Test goal",
            acceptance_criteria=["Criterion 1", "Criterion 2"],
        )
        
        # Add some iteration history
        from dev_workflow.state import IterationRecord
        for i in range(10):
            state.iterations.append(IterationRecord(
                iteration=i,
                stage='test',
                estimated_tokens=1000,
                actual_tokens=900,
            ))
        
        result = compactor.compact(state)
        
        self.assertTrue(result['context_saved'] > 0)
        self.assertIn('goal', result['preserved_items'])
        self.assertIn('acceptance_criteria', result['preserved_items'])
        
        # Should keep only last 2 iterations
        compact_state = result['compacted_state']
        self.assertEqual(len(compact_state['recent_iterations']), 2)
    
    def test_compaction_preserves_critical_findings(self):
        """Compaction preserves critical findings."""
        compactor = StateCompactor()
        state = WorkflowState(
            task_id="test",
            goal="Test goal",
            acceptance_criteria=["Criterion 1"],
        )
        
        # Add findings of various severities
        state.unresolved_findings = [
            ReviewerFinding(
                severity=FindingSeverity.CRITICAL,
                description="Critical issue",
            ),
            ReviewerFinding(
                severity=FindingSeverity.HIGH,
                description="High issue",
            ),
            ReviewerFinding(
                severity=FindingSeverity.LOW,
                description="Low issue",
            ),
        ]
        
        result = compactor.compact(state)
        compact_state = result['compacted_state']
        
        # Should keep CRITICAL and HIGH, discard LOW
        self.assertEqual(len(compact_state['unresolved_findings']), 2)
    
    def test_compaction_preserves_budget_state(self):
        """Compaction preserves budget and context state."""
        compactor = StateCompactor()
        state = WorkflowState(
            task_id="test",
            goal="Test goal",
            acceptance_criteria=["Criterion 1"],
            total_token_budget=10000,
        )
        state.tokens_used = 5000
        state.context_used = 30000
        
        result = compactor.compact(state)
        compact_state = result['compacted_state']
        
        self.assertEqual(compact_state['tokens_used'], 5000)
        self.assertEqual(compact_state['context_used'], 30000)
        self.assertIn('budget_state', result['preserved_items'])


class TestContextCompaction(unittest.TestCase):
    """Test context compaction in orchestrator."""
    
    def test_orchestrator_compacts_on_threshold(self):
        """Orchestrator compacts when context threshold reached."""
        orch = WorkflowOrchestrator(
            task_id="test-compact",
            goal="Test compaction",
            acceptance_criteria=["Criterion 1"],
            context_limit=10000,
            max_iterations=3,
        )
        
        # Simulate high context usage
        orch.context_governor.update(8500)  # 85% - requires compaction
        
        # Test compaction
        result = orch._compact_context()
        
        self.assertTrue(result['success'])
        self.assertGreater(result['context_saved'], 0)
    
    def test_compaction_updates_state(self):
        """Compaction updates state correctly."""
        orch = WorkflowOrchestrator(
            task_id="test-compact-state",
            goal="Test compaction state",
            acceptance_criteria=["Criterion 1"],
            context_limit=10000,
        )
        
        # Add some context
        orch.context_governor.update(8000)
        orch.state.context_used = 8000
        
        old_compaction_count = orch.state.compaction_count
        
        # Compact
        result = orch._compact_context()
        
        # Should update state
        self.assertEqual(orch.state.compaction_count, old_compaction_count + 1)
        self.assertLess(orch.state.context_used, 8000)


class TestHermesBuilder(unittest.TestCase):
    """Test v1.1 HermesBuilder."""
    
    def test_builder_executes(self):
        """Builder executes and returns structured result."""
        from dev_workflow.agents import HermesBuilder
        builder = HermesBuilder()
        
        state = WorkflowState(
            task_id="test",
            goal="Test goal",
            acceptance_criteria=["Criterion 1"],
        )
        state.iteration = 1
        
        result = builder.execute_task(
            goal="Test task",
            context="Test context",
            state=state,
        )
        
        self.assertIn('success', result)
        self.assertIn('message', result)
        self.assertIn('files_changed', result)
        self.assertIn('actual_tokens', result)
        self.assertIn('git_diff', result)
    
    def test_builder_tracks_history(self):
        """Builder tracks execution history."""
        from dev_workflow.agents import HermesBuilder
        builder = HermesBuilder()
        
        state = WorkflowState(
            task_id="test",
            goal="Test goal",
            acceptance_criteria=["Criterion 1"],
        )
        
        builder.execute_task("Task 1", "Context 1", state)
        builder.execute_task("Task 2", "Context 2", state)
        
        self.assertEqual(len(builder.execution_history), 2)


class TestWorkflowIntegration(unittest.TestCase):
    """Test v1.1 workflow integration."""
    
    def test_workflow_handles_compaction(self):
        """Workflow handles context compaction correctly."""
        orch = WorkflowOrchestrator(
            task_id="test-integration",
            goal="Test integration",
            acceptance_criteria=["Criterion 1"],
            context_limit=5000,
            max_iterations=2,
        )
        
        # Should be able to compact if needed
        orch.context_governor.update(4500)
        result = orch._compact_context()
        
        self.assertTrue(result['success'])


if __name__ == "__main__":
    unittest.main()
