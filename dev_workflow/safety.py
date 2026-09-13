"""
Safety policies for Development Orchestrator v1.3.

Enforces:
- Path validation
- Task scope
- Command restrictions
- Git operation restrictions
- Execution boundaries
"""

from typing import List, Tuple, Optional
from pathlib import Path
import re


class PathPolicy:
    """
    Enforces path validation and workspace boundaries.
    
    All paths must be within workspace_root.
    Rejects traversal, absolute outside paths, symlink escapes.
    """
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root).resolve()
    
    def validate(self, path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate path is within workspace.
        
        Returns:
            (valid, error_message)
        """
        try:
            # Resolve to absolute path (follows symlinks)
            target = (self.workspace_root / path).resolve()
            
            # Check if within workspace
            if not target.is_relative_to(self.workspace_root):
                return False, f"Path {path} resolves outside workspace: {target}"
            
            return True, None
            
        except (ValueError, OSError) as e:
            return False, f"Path validation error: {str(e)}"
    
    def validate_multiple(self, paths: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate multiple paths.
        
        Returns:
            (all_valid, error_messages)
        """
        errors = []
        for path in paths:
            valid, error = self.validate(path)
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors


class TaskScopePolicy:
    """
    Enforces task scope - which files a task is allowed to modify.
    
    Separate from workspace boundary: task scope is narrower.
    """
    
    def __init__(self, allowed_paths: List[str], path_policy: PathPolicy):
        self.allowed_paths = set(allowed_paths)
        self.path_policy = path_policy
    
    def allows_write(self, path: str) -> Tuple[bool, Optional[str]]:
        """
        Check if task allows writing to this path.
        
        Returns:
            (allowed, error_message)
        """
        # First check workspace boundary
        valid, error = self.path_policy.validate(path)
        if not valid:
            return False, error
        
        # Then check task scope
        if path not in self.allowed_paths:
            return False, f"Path {path} not in task allowed_paths"
        
        return True, None
    
    def validate_writes(self, paths: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate multiple write paths against task scope.
        
        Returns:
            (all_allowed, error_messages)
        """
        errors = []
        for path in paths:
            allowed, error = self.allows_write(path)
            if not allowed:
                errors.append(error)
        
        return len(errors) == 0, errors


class CommandPolicy:
    """
    Enforces command restrictions for terminal operations.
    
    Deterministic whitelist approach.
    """
    
    # Allowed commands (strict whitelist)
    ALLOWED_COMMANDS = {
        # Test execution
        'pytest',
        'python -m pytest',
        
        # Git read-only
        'git status',
        'git status --short',
        'git diff',
        'git diff --stat',
        'git diff --cached',
        'git log',
        'git log --oneline',
        'git branch',
        'git branch --show-current',
        
        # Python verification
        'python --version',
        'python -m pytest --version',
    }
    
    # Blocked command patterns (high-risk)
    BLOCKED_PATTERNS = [
        r'\brm\b',
        r'\brm\s+-rf\b',
        r'\bdd\b',
        r'\bmkfs\b',
        r'\bshutdown\b',
        r'\breboot\b',
        r'git\s+reset',
        r'git\s+clean',
        r'git\s+push',
        r'git\s+push\s+--force',
        r'git\s+push\s+-f',
        r'git\s+rebase',
        r'git\s+checkout\s+(?!-b)',  # Allow branch creation but not switching
        r'git\s+restore',
        r'curl\b',
        r'wget\b',
        r'nc\b',
        r'netcat\b',
        r'ssh\b',
        r'scp\b',
        r'rsync\b',
    ]
    
    def validate(self, command: str) -> Tuple[bool, Optional[str]]:
        """
        Validate command against policy.
        
        Returns:
            (allowed, error_message)
        """
        command = command.strip()
        
        # Check if in whitelist
        if command in self.ALLOWED_COMMANDS:
            return True, None
        
        # Check for variations with paths (pytest tests/, etc.)
        base_cmd = command.split()[0] if command else ""
        
        if base_cmd == "pytest" or command.startswith("PYTHONPATH="):
            # Allow pytest with paths
            return True, None
        
        if command.startswith("git "):
            # Check git commands more carefully
            if any(cmd in command for cmd in ['status', 'diff', 'log', 'branch']):
                # Block dangerous flags even on safe commands
                if '--force' in command or '-f' in command.split():
                    return False, f"Force flag not allowed: {command}"
                return True, None
        
        # Check blocked patterns
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Command matches blocked pattern '{pattern}': {command}"
        
        # Unknown command - reject by default
        return False, f"Command not in whitelist: {command}"


class GitPolicy:
    """
    Enforces git operation restrictions.
    
    v1.3: Read-only git operations only.
    """
    
    ALLOWED_OPERATIONS = {
        'status',
        'diff',
        'log',
        'branch',
        'show',
    }
    
    BLOCKED_OPERATIONS = {
        'commit',
        'push',
        'reset',
        'clean',
        'restore',
        'rebase',
        'checkout',  # Can change worktree
        'switch',
        'merge',
        'cherry-pick',
        'revert',
    }
    
    def validate_git_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """
        Validate git command is read-only.
        
        Returns:
            (allowed, error_message)
        """
        if not command.startswith('git '):
            return False, "Not a git command"
        
        # Extract git operation
        parts = command.split()
        if len(parts) < 2:
            return False, "Invalid git command"
        
        operation = parts[1]
        
        # Check if blocked
        if operation in self.BLOCKED_OPERATIONS:
            return False, f"Git operation '{operation}' is blocked (mutating operation)"
        
        # Check if allowed
        if operation in self.ALLOWED_OPERATIONS:
            return True, None
        
        # Unknown operation - reject
        return False, f"Git operation '{operation}' not in allowed list"


class ExecutionPolicy:
    """
    Combined execution policy enforcement.
    
    Validates all aspects of execution safety.
    """
    
    def __init__(
        self,
        workspace_root: str,
        allowed_paths: Optional[List[str]] = None,
    ):
        self.path_policy = PathPolicy(workspace_root)
        self.command_policy = CommandPolicy()
        self.git_policy = GitPolicy()
        
        # Task scope policy (None = no write operations allowed)
        self.task_scope = TaskScopePolicy(
            allowed_paths or [],
            self.path_policy
        ) if allowed_paths else None
    
    def validate_read(self, path: str) -> Tuple[bool, Optional[str]]:
        """Validate read operation on path."""
        return self.path_policy.validate(path)
    
    def validate_write(self, path: str) -> Tuple[bool, Optional[str]]:
        """Validate write operation on path."""
        if self.task_scope is None:
            return False, "No task scope defined - writes not allowed"
        
        return self.task_scope.allows_write(path)
    
    def validate_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """Validate terminal command."""
        # First check general command policy
        allowed, error = self.command_policy.validate(command)
        if not allowed:
            return False, error
        
        # If it's a git command, apply git policy
        if command.strip().startswith('git '):
            return self.git_policy.validate_git_command(command)
        
        return True, None
    
    def validate_execution_plan(
        self,
        reads: List[str],
        writes: List[str],
        commands: List[str],
    ) -> Tuple[bool, List[str]]:
        """
        Validate complete execution plan.
        
        Returns:
            (valid, error_messages)
        """
        errors = []
        
        # Validate reads
        for path in reads:
            valid, error = self.validate_read(path)
            if not valid:
                errors.append(f"Read: {error}")
        
        # Validate writes
        for path in writes:
            valid, error = self.validate_write(path)
            if not valid:
                errors.append(f"Write: {error}")
        
        # Validate commands
        for cmd in commands:
            valid, error = self.validate_command(cmd)
            if not valid:
                errors.append(f"Command: {error}")
        
        return len(errors) == 0, errors
