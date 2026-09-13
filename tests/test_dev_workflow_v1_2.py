"""
Tests for v1.2 real execution capabilities.
"""

import unittest
import tempfile
import os
from pathlib import Path
from dev_workflow.orchestrator import WorkflowOrchestrator
from dev_workflow.agents import HermesBuilder
from dev_workflow.state import WorkflowState
from dev_workflow.execution import ExecutionEngine


class TestRealExecution(unittest.TestCase):
    """Test v1.2 real execution."""
    
    def test_execution_engine_path_validation(self):
        """Execution engine validates paths within workspace."""
        engine = ExecutionEngine(workspace_root=".")
        
        # Valid paths
        self.assertTrue(engine.validate_path("dev_workflow/test.py"))
        self.assertTrue(engine.validate_path("./dev_workflow/test.py"))
        
        # Path traversal attempts should fail
        self.assertFalse(engine.validate_path("../../../etc/passwd"))
        self.assertFalse(engine.validate_path("/etc/passwd"))
    
    def test_builder_generates_execution_script(self):
        """Builder generates valid execution script."""
        builder = HermesBuilder()
        state = WorkflowState(
            task_id="test",
            goal="Test goal",
            acceptance_criteria=["Criterion 1"],
        )
        state.iteration = 1
        
        script = builder._build_execution_script(
            goal="Test task",
            context="Test context",
            state=state,
        )
        
        # Script should be valid Python
        self.assertIn("import json", script)
        self.assertIn("result =", script)
        self.assertIn("git status", script)
        self.assertIn("pytest", script)
    
    def test_builder_execution_returns_structure(self):
        """Builder execution returns expected structure."""
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
        
        # Check structure
        self.assertIn('success', result)
        self.assertIn('message', result)
        self.assertIn('files_changed', result)
        self.assertIn('tests_run', result)
        self.assertIn('git_diff', result)
        self.assertIn('test_exit_code', result)
        self.assertIn('commands_executed', result)


class TestExecutionSafety(unittest.TestCase):
    """Test execution safety boundaries."""
    
    def test_workspace_isolation(self):
        """Execution respects workspace boundaries."""
        engine = ExecutionEngine(workspace_root="/home/artid1994/Projects/THE_TRANSCENDING_FORM")
        
        # Within workspace
        self.assertTrue(engine.validate_path("dev_workflow/test.py"))
        
        # Outside workspace
        self.assertFalse(engine.validate_path("../../other_project/file.py"))
    
    def test_execution_script_contains_safety_checks(self):
        """Execution script includes safety boundaries."""
        builder = HermesBuilder(workspace_root="/home/artid1994/Projects/THE_TRANSCENDING_FORM")
        state = WorkflowState(
            task_id="test",
            goal="Test",
            acceptance_criteria=["Test"],
        )
        state.iteration = 1
        
        script = builder._build_execution_script("Test", "Context", state)
        
        # Should reference workspace
        self.assertIn("workspace", script.lower())


class TestWorkflowIntegrationV12(unittest.TestCase):
    """Test v1.2 workflow integration."""
    
    def test_orchestrator_can_execute(self):
        """Orchestrator can execute with v1.2 builder."""
        orch = WorkflowOrchestrator(
            task_id="test-v1.2",
            goal="Test v1.2 execution",
            acceptance_criteria=["Execution completes"],
            max_iterations=1,
            workspace_root=".",
        )
        
        # Orchestrator should have v1.2 builder
        self.assertIsNotNone(orch.builder)
        self.assertTrue(hasattr(orch.builder, 'workspace_root'))


if __name__ == "__main__":
    unittest.main()
