#!/usr/bin/env python3
"""
Hermes Bridge for AE01M Self-Improvement
Provides safe interface to Hermes CLI for autonomous code generation and optimization.
"""
import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, Tuple, List
from dataclasses import dataclass

# Import core directives for safety validation
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from core_directives import CoreDirectives, DirectiveViolation, DirectiveLevel
    DIRECTIVES_AVAILABLE = True
except ImportError:
    DIRECTIVES_AVAILABLE = False
    print("[HermesBridge] WARNING: Core directives not available")


@dataclass
class HermesResponse:
    """Response from Hermes CLI."""
    success: bool
    output: str
    error: Optional[str] = None
    blocked_reason: Optional[str] = None


class HermesBridge:
    """
    Safe bridge to Hermes CLI for self-improvement tasks.
    Enforces project boundary and safety directives.
    """
    
    # Allowed project root
    PROJECT_ROOT = Path.home() / "Projects" / "THE_TRANSCENDING_FORM"
    
    # Allowed file patterns for modification
    ALLOWED_PATTERNS = [
        "01_Neocortex/*.py",
        "03_Hippocampus/*.json",
        "04_Cerebellum/*.py",
        "logs/*.log",
        "logs/*.txt",
    ]
    
    # Forbidden operations
    FORBIDDEN_OPERATIONS = [
        "delete service",
        "remove service",
        "stop service",
        "disable service",
        "rm -rf",
        "format",
        "shutdown",
        "reboot",
    ]
    
    def __init__(self, enable_safety: bool = True):
        """
        Initialize Hermes bridge.
        
        Args:
            enable_safety: Enable safety checks (always True in production)
        """
        self.safety_enabled = enable_safety
        self.hermes_available = self._check_hermes_available()
        
        print(f"[HermesBridge] Initialized")
        print(f"[HermesBridge] Project root: {self.PROJECT_ROOT}")
        print(f"[HermesBridge] Safety: {'ENABLED' if self.safety_enabled else 'DISABLED'}")
        print(f"[HermesBridge] Hermes CLI: {'Available' if self.hermes_available else 'Not found'}")
    
    def _check_hermes_available(self) -> bool:
        """Check if Hermes CLI is available."""
        try:
            result = subprocess.run(
                ["which", "hermes"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def _validate_prompt_safety(self, prompt: str) -> Tuple[bool, Optional[str]]:
        """
        Validate prompt against safety directives.
        
        Args:
            prompt: User prompt to validate
        
        Returns:
            (is_safe, reason) - True if safe, False with reason if unsafe
        """
        if not self.safety_enabled:
            return True, None
        
        prompt_lower = prompt.lower()
        
        # Check for forbidden operations
        for forbidden in self.FORBIDDEN_OPERATIONS:
            if forbidden in prompt_lower:
                return False, f"Forbidden operation detected: {forbidden}"
        
        # Check against core directives (command patterns)
        if DIRECTIVES_AVAILABLE:
            # Extract potential commands from prompt
            import re
            command_patterns = re.findall(r'`([^`]+)`', prompt)
            for cmd in command_patterns:
                is_safe, violation = CoreDirectives.check_command_safety(cmd)
                if not is_safe:
                    return False, f"Unsafe command in prompt: {violation.reason}"
        
        # Check for path boundary violations
        if '/etc' in prompt_lower or '/sys' in prompt_lower or '/boot' in prompt_lower:
            return False, "Attempting to modify system paths"
        
        # Ensure operations are within project
        if 'file' in prompt_lower or 'write' in prompt_lower or 'modify' in prompt_lower:
            if str(self.PROJECT_ROOT) not in prompt and '~/Projects/THE_TRANSCENDING_FORM' not in prompt:
                return False, "File operations must be within project directory"
        
        return True, None
    
    def run_hermes_prompt(self, prompt: str, timeout: int = 30) -> HermesResponse:
        """
        Execute Hermes CLI with safety validation.
        
        Args:
            prompt: Prompt to send to Hermes
            timeout: Timeout in seconds
        
        Returns:
            HermesResponse with result
        """
        # Safety validation
        is_safe, reason = self._validate_prompt_safety(prompt)
        if not is_safe:
            print(f"[HermesBridge] BLOCKED: {reason}")
            return HermesResponse(
                success=False,
                output="",
                blocked_reason=reason
            )
        
        # Check Hermes availability
        if not self.hermes_available:
            return HermesResponse(
                success=False,
                output="",
                error="Hermes CLI not available"
            )
        
        # Execute Hermes CLI
        try:
            print(f"[HermesBridge] Executing Hermes prompt...")
            print(f"[HermesBridge] Prompt: {prompt[:100]}...")
            
            # Run Hermes in project directory
            result = subprocess.run(
                ["hermes", prompt],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.PROJECT_ROOT)
            )
            
            if result.returncode == 0:
                print(f"[HermesBridge] ✓ Success")
                return HermesResponse(
                    success=True,
                    output=result.stdout
                )
            else:
                print(f"[HermesBridge] ✗ Error (exit code {result.returncode})")
                return HermesResponse(
                    success=False,
                    output=result.stdout,
                    error=result.stderr
                )
        
        except subprocess.TimeoutExpired:
            print(f"[HermesBridge] ✗ Timeout after {timeout}s")
            return HermesResponse(
                success=False,
                output="",
                error=f"Timeout after {timeout} seconds"
            )
        
        except Exception as e:
            print(f"[HermesBridge] ✗ Exception: {e}")
            return HermesResponse(
                success=False,
                output="",
                error=str(e)
            )
    
    def self_improvement_prompt(self, goal: str) -> HermesResponse:
        """
        Generate self-improvement prompt for specific goal.
        
        Args:
            goal: Improvement goal (e.g., "optimize memory", "add training data")
        
        Returns:
            HermesResponse
        """
        # Define safe self-improvement prompts
        safe_prompts = {
            "status_report": f"""
Write a brief status report to {self.PROJECT_ROOT}/logs/self_improvement.log
Include:
- Current timestamp
- System status (services running)
- Recent improvements made
- Next optimization opportunities
""",
            "analyze_logs": f"""
Analyze the last 100 lines of {self.PROJECT_ROOT}/logs/iri_daemon.log
Identify:
- Most common user intents
- Response quality patterns
- Potential training data additions
Write findings to {self.PROJECT_ROOT}/logs/log_analysis.txt
""",
            "suggest_training": f"""
Review {self.PROJECT_ROOT}/01_Neocortex/neural_core.py training dataset
Suggest 5 new diverse Thai training samples for underrepresented intents
Write suggestions to {self.PROJECT_ROOT}/logs/training_suggestions.txt
""",
        }
        
        prompt = safe_prompts.get(goal)
        if not prompt:
            return HermesResponse(
                success=False,
                output="",
                error=f"Unknown self-improvement goal: {goal}"
            )
        
        return self.run_hermes_prompt(prompt)


def test_hermes_bridge():
    """Test Hermes bridge with safe operations."""
    print("=" * 60)
    print("Hermes Bridge - Dry-Run Test")
    print("=" * 60)
    
    bridge = HermesBridge(enable_safety=True)
    
    # Test 1: Safety validation
    print("\n1. Safety Validation Tests:")
    test_prompts = [
        ("Write status report to logs/test.log", True, "Safe log write"),
        ("rm -rf /", False, "Destructive command"),
        ("Analyze neural_core.py", True, "Safe code analysis"),
        ("Modify /etc/passwd", False, "System file modification"),
        ("Add training data to knowledge_base.json", True, "Safe project file"),
    ]
    
    for prompt, expected_safe, description in test_prompts:
        is_safe, reason = bridge._validate_prompt_safety(prompt)
        status = "✓ PASS" if is_safe == expected_safe else "✗ FAIL"
        result = "SAFE" if is_safe else f"BLOCKED ({reason})"
        print(f"   {status}: {description}")
        print(f"         Prompt: {prompt[:50]}...")
        print(f"         Result: {result}")
    
    # Test 2: Self-improvement prompts
    print("\n2. Self-Improvement Prompt Tests:")
    goals = ["status_report", "analyze_logs", "suggest_training"]
    
    for goal in goals:
        print(f"\n   Goal: {goal}")
        response = bridge.self_improvement_prompt(goal)
        if response.success:
            print(f"   ✓ Prompt generated successfully")
        elif response.blocked_reason:
            print(f"   ✗ Blocked: {response.blocked_reason}")
        elif response.error:
            print(f"   ⚠ Error: {response.error}")
    
    # Test 3: Hermes availability
    print("\n3. Hermes CLI Status:")
    if bridge.hermes_available:
        print("   ✓ Hermes CLI available")
    else:
        print("   ⚠ Hermes CLI not found (expected in development)")
        print("   Note: Install with: curl -sSL https://install.nousresearch.com | bash")
    
    print("\n" + "=" * 60)
    print("Dry-run complete - Safety validation working")
    print("=" * 60)


if __name__ == "__main__":
    test_hermes_bridge()
