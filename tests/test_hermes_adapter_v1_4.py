"""
Tests for v1.4 Hermes Context Bridge.
"""

import unittest
from dev_workflow.hermes_adapter import HermesExecutionAdapter, HermesContextStatus
from dev_workflow.hermes_executor import HermesNativeExecutor, ExecutionPlan
from dev_workflow.safety import ExecutionPolicy


class TestHermesExecutionAdapter(unittest.TestCase):
    """Test Hermes execution adapter."""
    
    def test_adapter_without_capability_blocks(self):
        """Adapter without execute_code capability blocks execution."""
        adapter = HermesExecutionAdapter(None)
        
        status = adapter.check_context()
        self.assertFalse(status.available)
        self.assertIn("unavailable", status.reason.lower())
    
    def test_adapter_with_capability_available(self):
        """Adapter with execute_code reports available."""
        # Mock execute_code function
        def mock_execute_code(code):
            return {'output': '{"success": true}'}
        
        adapter = HermesExecutionAdapter(mock_execute_code)
        
        status = adapter.check_context()
        self.assertTrue(status.available)
        self.assertIn("injected", status.reason.lower())
    
    def test_adapter_blocks_execution_when_unavailable(self):
        """Adapter returns BLOCKED when capability unavailable."""
        adapter = HermesExecutionAdapter(None)
        
        result = adapter.execute_script("print('test')")
        
        self.assertFalse(result['success'])
        self.assertIn('BLOCKED', result['message'])
        self.assertTrue(result.get('blocked', False))
    
    def test_adapter_executes_with_capability(self):
        """Adapter executes when capability provided."""
        def mock_execute_code(code):
            return {
                'output': '{"success": true, "message": "OK", '
                         '"files_changed": [], "tests_run": "", '
                         '"test_exit_code": 0, "git_diff": "", '
                         '"commands_executed": []}'
            }
        
        adapter = HermesExecutionAdapter(mock_execute_code)
        result = adapter.execute_script("print('test')")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'OK')


class TestHermesNativeExecutorWithAdapter(unittest.TestCase):
    """Test executor with adapter."""
    
    def test_executor_blocks_without_adapter(self):
        """Executor blocks when no adapter provided."""
        executor = HermesNativeExecutor(".")
        policy = ExecutionPolicy(".", [])
        
        plan = ExecutionPlan(
            goal="Test",
            reads=[],
            writes=[],
            commands=["git status"],
            allowed_paths=[],
        )
        
        result = executor.execute_plan(plan, policy)
        
        self.assertFalse(result.success)
        self.assertIn("BLOCKED", result.message)
    
    def test_executor_uses_injected_adapter(self):
        """Executor uses injected adapter."""
        def mock_execute_code(code):
            return {
                'output': '{"success": true, "message": "OK", '
                         '"files_changed": [], "tests_run": "", '
                         '"test_exit_code": 0, "git_diff": "", '
                         '"commands_executed": ["git status"]}'
            }
        
        adapter = HermesExecutionAdapter(mock_execute_code)
        executor = HermesNativeExecutor(".", adapter)
        policy = ExecutionPolicy(".", [])
        
        plan = ExecutionPlan(
            goal="Test",
            reads=[],
            writes=[],
            commands=["git status"],
            allowed_paths=[],
        )
        
        result = executor.execute_plan(plan, policy)
        
        self.assertTrue(result.success)


class TestStandaloneBehavior(unittest.TestCase):
    """Test standalone (non-Hermes) behavior."""
    
    def test_standalone_python_blocks(self):
        """Running as standalone Python blocks execution."""
        # This is what happens when run outside Hermes
        adapter = HermesExecutionAdapter(None)
        executor = HermesNativeExecutor(".", adapter)
        policy = ExecutionPolicy(".", [])
        
        plan = ExecutionPlan(
            goal="Test",
            reads=[],
            writes=[],
            commands=["git status"],
            allowed_paths=[],
        )
        
        result = executor.execute_plan(plan, policy)
        
        # Must block, not execute
        self.assertFalse(result.success)
        self.assertIn("BLOCKED", result.message)
        self.assertIn("unavailable", result.message.lower())


class TestNoImportBypass(unittest.TestCase):
    """Test that adapter doesn't bypass security."""
    
    def test_no_exec_calls(self):
        """Adapter doesn't use exec()."""
        with open("dev_workflow/hermes_adapter.py") as f:
            content = f.read()
        
        import re
        exec_calls = re.findall(r'^\s*exec\s*\(', content, re.MULTILINE)
        self.assertEqual(len(exec_calls), 0, "Adapter must not use exec()")
    
    def test_no_hermes_tools_import(self):
        """Adapter doesn't import fake hermes_tools."""
        with open("dev_workflow/hermes_adapter.py") as f:
            content = f.read()
        
        self.assertNotIn("from hermes_tools import", content)
        self.assertNotIn("import hermes_tools", content)
    
    def test_no_execute_code_module_import(self):
        """Adapter doesn't import execute_code as module."""
        with open("dev_workflow/hermes_adapter.py") as f:
            content = f.read()
        
        # Check for actual import statements (not in comments/docstrings)
        import re
        # Match import statements at start of line (not in strings)
        imports = re.findall(r'^\s*(from\s+execute_code\s+import|import\s+execute_code)', 
                            content, re.MULTILINE)
        self.assertEqual(len(imports), 0, 
                        "Adapter must not import execute_code as module")


class TestPolicyIntegration(unittest.TestCase):
    """Test adapter respects all policies."""
    
    def test_adapter_cannot_bypass_execution_policy(self):
        """Adapter respects ExecutionPolicy validation."""
        def mock_execute_code(code):
            return {'output': '{"success": true}'}
        
        adapter = HermesExecutionAdapter(mock_execute_code)
        executor = HermesNativeExecutor(".", adapter)
        policy = ExecutionPolicy(".", [])  # No allowed paths
        
        # Try to write outside allowed paths
        plan = ExecutionPlan(
            goal="Test",
            reads=[],
            writes=["unauthorized.txt"],  # Not in allowed_paths
            commands=[],
            allowed_paths=[],
        )
        
        result = executor.execute_plan(plan, policy)
        
        # Policy should block before adapter runs
        self.assertFalse(result.success)
        self.assertGreater(len(result.policy_violations), 0)


if __name__ == "__main__":
    unittest.main()
