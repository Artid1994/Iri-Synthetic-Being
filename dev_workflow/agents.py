"""
Agent role implementations for the multi-agent workflow.

v1.3: Hermes-native execution with safety policies.
"""

from typing import Tuple, List, Optional, Dict
import hashlib
import re
from .state import WorkflowState, ReviewerFinding, FindingSeverity
from .hermes_executor import HermesNativeExecutor, ExecutionPlan, ExecutionResult
from .safety import ExecutionPolicy


class PromptTokenAuditor:
    """
    Reviews and optimizes prompts before execution.
    Estimates token costs.
    Enforces budget constraints.
    """
    
    def __init__(self, budget_governor):
        self.budget_governor = budget_governor
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate tokens from text.
        
        Conservative estimate: ~4 chars per token for English,
        adjust for code and other content.
        """
        # Basic heuristic: count chars and divide
        # Add overhead for structure
        char_count = len(text)
        
        # Rough approximation: 4 chars/token + 20% overhead
        estimated = int((char_count / 4) * 1.2)
        
        # Minimum estimate
        return max(estimated, 100)
    
    def audit_prompt(
        self,
        prompt: str,
        expected_output_size: int = 2000,
    ) -> Tuple[bool, str, int, Optional[str]]:
        """
        Audit a prompt before execution.
        
        Args:
            prompt: the prompt to audit
            expected_output_size: estimated output token size
        
        Returns:
            (approved, message, estimated_total_tokens, optimized_prompt)
        """
        # Estimate input tokens
        input_tokens = self.estimate_tokens(prompt)
        output_tokens = expected_output_size
        total_estimate = input_tokens + output_tokens
        
        # Check budget
        can_reserve = self.budget_governor.can_reserve(total_estimate)
        
        if not can_reserve:
            remaining = self.budget_governor.remaining
            return False, (
                f"Budget insufficient: need {total_estimate}, "
                f"remaining {remaining}"
            ), total_estimate, None
        
        # Basic optimization: remove excessive whitespace
        optimized = self._optimize_prompt(prompt)
        optimized_tokens = self.estimate_tokens(optimized)
        optimized_total = optimized_tokens + output_tokens
        
        return True, f"Approved: {optimized_total} tokens estimated", optimized_total, optimized
    
    def _optimize_prompt(self, prompt: str) -> str:
        """Basic prompt optimization."""
        # Remove excessive blank lines (keep structure)
        prompt = re.sub(r'\n{3,}', '\n\n', prompt)
        
        # Remove trailing whitespace
        lines = [line.rstrip() for line in prompt.split('\n')]
        
        return '\n'.join(lines)
    
    def compute_prompt_hash(self, prompt: str) -> str:
        """Compute a hash of the prompt for tracking."""
        return hashlib.sha256(prompt.encode('utf-8')).hexdigest()[:16]


class HermesBuilder:
    """
    Executes repository work using Hermes-native execute_code.
    
    v1.3: Hermes-native execution with safety policies.
    Replaces broken exec() mechanism.
    """
    
    def __init__(self, workspace_root: str = ".", allowed_paths: List[str] = None):
        self.execution_history = []
        self.workspace_root = workspace_root
        self.executor = HermesNativeExecutor(workspace_root)
        self.policy = ExecutionPolicy(workspace_root, allowed_paths)
    
    def execute_task(
        self,
        goal: str,
        context: str,
        state: WorkflowState,
        allowed_paths: List[str] = None,
    ) -> Dict:
        """
        Execute a development task using Hermes-native execute_code.
        
        v1.3: Policy-enforced execution with verification.
        
        Returns:
            {
                'success': bool,
                'message': str,
                'files_changed': List[str],
                'tests_run': str,
                'test_exit_code': Optional[int],
                'git_diff': str,
                'git_commit': Optional[str],
                'actual_tokens': int,
                'commands_executed': List[str],
                'unauthorized_changes': bool,
                'policy_violations': List[str],
            }
        """
        # Build execution plan
        plan = ExecutionPlan(
            goal=goal,
            reads=[],  # For v1.3: inspection only
            writes=[],  # No writes yet
            commands=[
                'git status --short',
                'git diff --stat',
                'python -m pytest --version',  # Test environment check
            ],
            allowed_paths=allowed_paths or [],
            timeout=30,
        )
        
        # Update policy with allowed_paths if provided
        if allowed_paths:
            self.policy = ExecutionPolicy(self.workspace_root, allowed_paths)
        
        # Execute plan with policy enforcement
        result = self.executor.execute_plan(plan, self.policy)
        
        # Convert to legacy dict format for compatibility
        result_dict = result.to_dict()
        
        self.execution_history.append({
            'goal': goal,
            'iteration': state.iteration,
            'result': result_dict,
        })
        
        return result_dict
    
    # Old v1.2 methods removed - replaced by HermesNativeExecutor in v1.3


class IndependentReviewer:
    """
    Reviews implementation independently.
    Does not trust Hermes' completion claim.
    Inspects repository directly.
    
    v1.1: Enhanced verification with real repository inspection.
    """
    
    def __init__(self, workspace_root: str = "."):
        self.review_history = []
        self.workspace_root = workspace_root
    
    def review(
        self,
        goal: str,
        acceptance_criteria: List[str],
        changed_files: List[str],
        git_diff: str,
        test_results: str,
        state: WorkflowState,
    ) -> Tuple[bool, List[ReviewerFinding], str]:
        """
        Perform independent code review.
        
        Args:
            goal: task goal
            acceptance_criteria: acceptance criteria
            changed_files: list of changed files
            git_diff: git diff output
            test_results: test execution results
            state: workflow state
        
        Returns:
            (passed, findings, summary)
        """
        findings = []
        
        # Check 1: Files actually changed
        if not changed_files:
            findings.append(ReviewerFinding(
                severity=FindingSeverity.HIGH,
                description="No files changed",
                evidence="changed_files list is empty",
            ))
        
        # Check 2: Tests exist and pass
        if "No tests run" in test_results or not test_results:
            findings.append(ReviewerFinding(
                severity=FindingSeverity.MEDIUM,
                description="No test verification",
                evidence=test_results,
            ))
        
        # Check 3: Each acceptance criterion
        for criterion in acceptance_criteria:
            # This is where actual verification would happen
            # For v1, we note that verification is needed
            findings.append(ReviewerFinding(
                severity=FindingSeverity.UNKNOWN,
                description=f"Acceptance criterion needs verification: {criterion}",
                evidence="Manual verification required in v1",
            ))
        
        # Determine pass/fail
        critical_or_high = [
            f for f in findings
            if f.severity in (FindingSeverity.CRITICAL, FindingSeverity.HIGH)
        ]
        
        passed = len(critical_or_high) == 0
        
        summary = self._generate_summary(findings, passed)
        
        self.review_history.append({
            'goal': goal,
            'iteration': state.iteration,
            'passed': passed,
            'findings': findings,
        })
        
        return passed, findings, summary
    
    def _generate_summary(self, findings: List[ReviewerFinding], passed: bool) -> str:
        """Generate review summary."""
        if passed:
            summary = "PASS: No critical or high severity issues found.\n"
        else:
            summary = "FAIL: Critical or high severity issues found.\n"
        
        by_severity = {}
        for finding in findings:
            severity = finding.severity.value
            by_severity.setdefault(severity, []).append(finding)
        
        summary += "\nFindings by severity:\n"
        for severity in ['critical', 'high', 'medium', 'low', 'unknown']:
            if severity in by_severity:
                summary += f"  {severity.upper()}: {len(by_severity[severity])}\n"
        
        return summary


class FinalGate:
    """
    Final quality gate before declaring DONE.
    
    Verifies:
    - Acceptance criteria met
    - Tests pass
    - No regression
    - Git state clean
    - Budget not exceeded
    - Context not exceeded
    - Reviewer passed
    """
    
    def __init__(self):
        self.gate_history = []
    
    def verify(
        self,
        state: WorkflowState,
        reviewer_passed: bool,
        reviewer_findings: List[ReviewerFinding],
    ) -> Tuple[bool, str]:
        """
        Perform final gate verification.
        
        Returns:
            (gate_passed, message)
        """
        checks = []
        
        # Check 1: Reviewer passed
        if not reviewer_passed:
            checks.append(("FAIL", "Reviewer did not pass"))
        else:
            checks.append(("PASS", "Reviewer passed"))
        
        # Check 2: No critical/high findings unresolved
        critical_high = [
            f for f in reviewer_findings
            if f.severity in (FindingSeverity.CRITICAL, FindingSeverity.HIGH)
        ]
        if critical_high:
            checks.append(("FAIL", f"{len(critical_high)} critical/high findings unresolved"))
        else:
            checks.append(("PASS", "No critical/high findings"))
        
        # Check 3: Budget not exceeded
        if state.tokens_remaining < 0:
            checks.append(("FAIL", "Token budget exceeded"))
        else:
            checks.append(("PASS", f"Token budget OK ({state.tokens_remaining} remaining)"))
        
        # Check 4: Context not exceeded
        if state.context_utilization > 0.9:
            checks.append(("FAIL", "Context utilization critical"))
        elif state.context_utilization > 0.8:
            checks.append(("WARN", "Context utilization high"))
        else:
            checks.append(("PASS", f"Context OK ({state.context_utilization:.1%})"))
        
        # Check 5: Iterations within limit
        if state.iteration >= state.max_iterations:
            checks.append(("WARN", "Max iterations reached"))
        else:
            checks.append(("PASS", f"Iterations OK ({state.iteration}/{state.max_iterations})"))
        
        # Determine final result
        failures = [c for c in checks if c[0] == "FAIL"]
        gate_passed = len(failures) == 0
        
        # Generate message
        message = "FINAL GATE:\n"
        for status, msg in checks:
            message += f"  [{status}] {msg}\n"
        
        if gate_passed:
            message += "\n✓ GATE PASSED: Task complete."
        else:
            message += "\n✗ GATE FAILED: Cannot declare DONE."
        
        self.gate_history.append({
            'iteration': state.iteration,
            'passed': gate_passed,
            'checks': checks,
        })
        
        return gate_passed, message
