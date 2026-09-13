"""
Hermes-native execution engine for v1.3+.

v1.4: Uses HermesExecutionAdapter instead of direct import.
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
import json

from .safety import ExecutionPolicy
from .hermes_adapter import HermesExecutionAdapter


@dataclass
class ExecutionPlan:
    """
    Validated execution plan.
    
    Defines exactly what operations will be performed.
    """
    goal: str
    reads: List[str]  # Paths to read
    writes: List[str]  # Paths to write (must be in allowed_paths)
    commands: List[str]  # Terminal commands to execute
    allowed_paths: List[str]  # Paths this task can modify
    timeout: int = 30
    
    def to_dict(self) -> Dict:
        """Serialize to dict."""
        return {
            'goal': self.goal,
            'reads': self.reads,
            'writes': self.writes,
            'commands': self.commands,
            'allowed_paths': self.allowed_paths,
            'timeout': self.timeout,
        }


@dataclass
class ExecutionResult:
    """
    Structured execution result.
    
    Distinguishes KNOWN from UNKNOWN.
    """
    success: bool
    message: str
    files_changed: List[str]
    tests_run: str
    test_exit_code: Optional[int]
    git_diff: str
    commands_executed: List[str]
    actual_tokens: int  # Estimated, not measured
    git_commit: Optional[str] = None
    
    # Verification flags
    unauthorized_changes: bool = False
    policy_violations: List[str] = None
    
    def __post_init__(self):
        if self.policy_violations is None:
            self.policy_violations = []
    
    def to_dict(self) -> Dict:
        """Serialize to dict."""
        return {
            'success': self.success,
            'message': self.message,
            'files_changed': self.files_changed,
            'tests_run': self.tests_run,
            'test_exit_code': self.test_exit_code,
            'git_diff': self.git_diff,
            'commands_executed': self.commands_executed,
            'actual_tokens': self.actual_tokens,
            'git_commit': self.git_commit,
            'unauthorized_changes': self.unauthorized_changes,
            'policy_violations': self.policy_violations,
        }


class HermesNativeExecutor:
    """
    Hermes-native execution engine for v1.3+.
    
    v1.4: Uses HermesExecutionAdapter for proper context handling.
    """
    
    def __init__(self, workspace_root: str = ".", hermes_adapter: Optional[HermesExecutionAdapter] = None):
        self.workspace_root = Path(workspace_root).resolve()
        self.execution_history = []
        self.hermes_adapter = hermes_adapter or HermesExecutionAdapter(None)
    
    def execute_plan(
        self,
        plan: ExecutionPlan,
        policy: ExecutionPolicy,
    ) -> ExecutionResult:
        """
        Execute a validated plan using Hermes execute_code.
        
        Args:
            plan: Validated execution plan
            policy: Enforcement policy
        
        Returns:
            ExecutionResult with actual results
        """
        # Validate plan against policy
        valid, errors = policy.validate_execution_plan(
            reads=plan.reads,
            writes=plan.writes,
            commands=plan.commands,
        )
        
        if not valid:
            return ExecutionResult(
                success=False,
                message=f"Policy validation failed: {'; '.join(errors)}",
                files_changed=[],
                tests_run='',
                test_exit_code=None,
                git_diff='',
                commands_executed=[],
                actual_tokens=0,
                policy_violations=errors,
            )
        
        # Record pre-execution state
        pre_state = self._capture_state()
        
        # Build and execute script using execute_code
        script = self._build_safe_script(plan)
        
        try:
            # Use execute_code tool (available in Hermes environment)
            result = self._execute_via_hermes(script)
            
            # Capture post-execution state
            post_state = self._capture_state()
            
            # Verify execution
            verification = self._verify_execution(
                plan=plan,
                result=result,
                pre_state=pre_state,
                post_state=post_state,
                policy=policy,
            )
            
            # Build execution result
            exec_result = ExecutionResult(
                success=result.get('success', False) and verification['valid'],
                message=result.get('message', ''),
                files_changed=verification['files_changed'],
                tests_run=result.get('tests_run', ''),
                test_exit_code=result.get('test_exit_code'),
                git_diff=result.get('git_diff', ''),
                commands_executed=result.get('commands_executed', []),
                actual_tokens=self._estimate_tokens(script, result),
                unauthorized_changes=verification['unauthorized_changes'],
                policy_violations=verification['policy_violations'],
            )
            
            self.execution_history.append({
                'plan': plan.to_dict(),
                'result': exec_result.to_dict(),
            })
            
            return exec_result
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                message=f'Execution failed: {str(e)}',
                files_changed=[],
                tests_run='',
                test_exit_code=None,
                git_diff='',
                commands_executed=[],
                actual_tokens=0,
            )
    
    def _build_safe_script(self, plan: ExecutionPlan) -> str:
        """
        Build safe script for execute_code.
        
        Note: Script runs in Hermes execute_code environment where
        tools are available as importable functions.
        """
        # Build command list as JSON for safety
        commands_json = json.dumps(plan.commands)
        
        script = f'''
# Hermes-native execution v1.3
# Goal: {plan.goal}

from terminal import terminal
import json

result = {{
    'success': False,
    'message': '',
    'files_changed': [],
    'tests_run': '',
    'test_exit_code': None,
    'git_diff': '',
    'commands_executed': [],
}}

try:
    # Pre-execution git status
    git_status_before = terminal("git status --short", timeout=10)
    
    # Execute allowed commands
    commands = {commands_json}
    
    for cmd in commands:
        cmd_result = terminal(cmd, timeout={plan.timeout})
        result['commands_executed'].append(cmd)
        
        # Track test results
        if 'pytest' in cmd:
            result['test_exit_code'] = cmd_result.get('exit_code')
            result['tests_run'] = cmd_result.get('output', '')[:200]
    
    # Post-execution git status
    git_status_after = terminal("git status --short", timeout=10)
    git_diff = terminal("git diff --stat", timeout=10)
    
    result['git_diff'] = git_diff.get('output', '')
    
    # Parse changed files
    if git_status_after.get('exit_code') == 0:
        lines = git_status_after['output'].strip().split('\\n')
        changed = [line.split()[-1] for line in lines if line.strip()]
        result['files_changed'] = changed
    
    result['success'] = True
    result['message'] = 'Execution completed'
    
except Exception as e:
    result['message'] = f'Error: {{str(e)}}'
    result['success'] = False

print(json.dumps(result))
'''
        return script
    
    def _execute_via_hermes(self, script: str) -> Dict:
        """
        Execute script via Hermes adapter.
        
        v1.4: Uses injected adapter instead of direct import.
        """
        return self.hermes_adapter.execute_script(script)
    
    def _capture_state(self) -> Dict:
        """Capture current workspace state for verification."""
        try:
            from terminal import terminal
            
            git_status = terminal("git status --short", timeout=5)
            git_branch = terminal("git branch --show-current", timeout=5)
            
            return {
                'git_status': git_status.get('output', ''),
                'git_branch': git_branch.get('output', '').strip(),
            }
        except:
            return {
                'git_status': 'UNKNOWN',
                'git_branch': 'UNKNOWN',
            }
    
    def _verify_execution(
        self,
        plan: ExecutionPlan,
        result: Dict,
        pre_state: Dict,
        post_state: Dict,
        policy: ExecutionPolicy,
    ) -> Dict:
        """
        Verify execution results against plan and policy.
        
        Returns:
            {
                'valid': bool,
                'files_changed': List[str],
                'unauthorized_changes': bool,
                'policy_violations': List[str],
            }
        """
        violations = []
        files_changed = result.get('files_changed', [])
        
        # Check if any changed files are outside allowed_paths
        unauthorized = []
        for file in files_changed:
            if file not in plan.allowed_paths:
                unauthorized.append(file)
                violations.append(f"Unauthorized file change: {file}")
        
        # Verify git branch didn't change
        if pre_state.get('git_branch') != post_state.get('git_branch'):
            violations.append("Git branch changed unexpectedly")
        
        return {
            'valid': len(violations) == 0,
            'files_changed': files_changed,
            'unauthorized_changes': len(unauthorized) > 0,
            'policy_violations': violations,
        }
    
    def _estimate_tokens(self, script: str, result: Dict) -> int:
        """
        Estimate tokens used.
        
        Note: Actual token usage is UNKNOWN - this is heuristic.
        """
        script_tokens = len(script) // 4
        result_tokens = len(str(result)) // 4
        return script_tokens + result_tokens
