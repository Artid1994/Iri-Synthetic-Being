"""
Main workflow orchestrator.
Coordinates all agent roles and enforces workflow discipline.

v1.1: Real execution, context compaction, enhanced review loop.
"""

from typing import List, Optional, Dict
from pathlib import Path
import json

from .state import WorkflowState, WorkflowStatus, IterationRecord, FindingSeverity
from .budget import BudgetGovernor, ContextGovernor, ContextStatus
from .agents import PromptTokenAuditor, HermesBuilder, IndependentReviewer, FinalGate
from .compaction import StateCompactor


class WorkflowOrchestrator:
    """
    Controls the multi-agent development workflow.
    
    Enforces:
    - Token budget limits
    - Context limits
    - Iteration limits
    - State machine discipline
    - Evidence-based completion
    """
    
    def __init__(
        self,
        task_id: str,
        goal: str,
        acceptance_criteria: List[str],
        total_token_budget: int = 50000,
        context_limit: int = 100000,
        max_iterations: int = 5,
        max_fix_iterations: int = 3,
        workspace_root: str = ".",
    ):
        # Initialize state
        self.state = WorkflowState(
            task_id=task_id,
            goal=goal,
            acceptance_criteria=acceptance_criteria,
            total_token_budget=total_token_budget,
            context_limit=context_limit,
            max_iterations=max_iterations,
            max_fix_iterations=max_fix_iterations,
        )
        
        # Initialize governors
        self.budget_governor = BudgetGovernor(total_budget=total_token_budget)
        self.context_governor = ContextGovernor(context_limit=context_limit)
        
        # Initialize agents
        self.auditor = PromptTokenAuditor(budget_governor=self.budget_governor)
        self.builder = HermesBuilder(workspace_root=workspace_root)
        self.reviewer = IndependentReviewer(workspace_root=workspace_root)
        self.final_gate = FinalGate()
        
        # Initialize compactor
        self.compactor = StateCompactor()
    
    def run(self) -> WorkflowState:
        """
        Execute the complete workflow.
        
        Returns:
            Final workflow state
        """
        self.state.status = WorkflowStatus.PLANNING
        self.state.update_timestamp()
        
        while self.state.status not in (
            WorkflowStatus.DONE,
            WorkflowStatus.BUDGET_STOP,
            WorkflowStatus.CONTEXT_STOP,
            WorkflowStatus.ITERATION_STOP,
            WorkflowStatus.FAILED,
        ):
            # Check hard stops
            if not self._check_can_continue():
                break
            
            # Execute iteration
            self._execute_iteration()
        
        return self.state
    
    def _check_can_continue(self) -> bool:
        """Check if workflow can continue."""
        # Check iteration limit
        if self.state.iteration >= self.state.max_iterations:
            self.state.status = WorkflowStatus.ITERATION_STOP
            return False
        
        # Check fix iteration limit
        if self.state.fix_iteration >= self.state.max_fix_iterations:
            self.state.status = WorkflowStatus.ITERATION_STOP
            return False
        
        # Check budget
        if self.budget_governor.remaining <= 0:
            self.state.status = WorkflowStatus.BUDGET_STOP
            return False
        
        # Check context
        context_status = self.context_governor.get_status()
        if context_status == ContextStatus.HARD_STOP:
            self.state.status = WorkflowStatus.CONTEXT_STOP
            return False
        
        return True
    
    def _execute_iteration(self):
        """Execute a single workflow iteration."""
        self.state.iteration += 1
        iteration_record = IterationRecord(
            iteration=self.state.iteration,
            stage='start',
        )
        
        # Stage 1: Prompt audit
        self.state.status = WorkflowStatus.PROMPT_AUDIT
        prompt = self._build_prompt()
        
        approved, audit_msg, estimated_tokens, optimized_prompt = self.auditor.audit_prompt(
            prompt=prompt,
            expected_output_size=2000,
        )
        
        iteration_record.stage = 'prompt_audit'
        iteration_record.estimated_tokens = estimated_tokens
        iteration_record.prompt_hash = self.auditor.compute_prompt_hash(optimized_prompt or prompt)
        
        if not approved:
            self.state.status = WorkflowStatus.BUDGET_STOP
            self.state.iterations.append(iteration_record)
            return
        
        # Reserve budget
        success, reserve_msg = self.budget_governor.reserve(estimated_tokens)
        if not success:
            self.state.status = WorkflowStatus.BUDGET_STOP
            self.state.iterations.append(iteration_record)
            return
        
        self.state.tokens_reserved = self.budget_governor.reserved
        
        # Stage 2: Context check
        self.state.status = WorkflowStatus.CONTEXT_CHECK
        can_continue, ctx_status, ctx_msg = self.context_governor.can_continue(
            estimated_growth=estimated_tokens // 2  # Rough estimate of context growth
        )
        
        if not can_continue:
            if ctx_status == ContextStatus.HARD_STOP:
                self.state.status = WorkflowStatus.CONTEXT_STOP
            elif ctx_status == ContextStatus.COMPACTION_REQUIRED:
                # v1.1: Implement compaction
                compaction_result = self._compact_context()
                if compaction_result['success']:
                    # Continue after successful compaction
                    pass
                else:
                    # Compaction failed, must stop
                    self.state.status = WorkflowStatus.CONTEXT_STOP
                    self.state.iterations.append(iteration_record)
                    return
            else:
                self.state.status = WorkflowStatus.CONTEXT_STOP
                self.state.iterations.append(iteration_record)
                return
        
        # Stage 3: Execute
        self.state.status = WorkflowStatus.EXECUTING
        result = self.builder.execute_task(
            goal=self.state.goal,
            context=optimized_prompt or prompt,
            state=self.state,
        )
        
        actual_tokens = result.get('actual_tokens', estimated_tokens)
        iteration_record.actual_tokens = actual_tokens
        
        # Commit budget
        self.budget_governor.commit(estimated_tokens, actual_tokens)
        self.state.tokens_used = self.budget_governor.used
        self.state.tokens_reserved = self.budget_governor.reserved
        
        # Update context (rough estimate)
        self.context_governor.update(self.context_governor.context_used + actual_tokens // 2)
        self.state.context_used = self.context_governor.context_used
        self.state.context_utilization = self.context_governor.utilization
        
        # Stage 4: Review
        self.state.status = WorkflowStatus.REVIEWING
        passed, findings, summary = self.reviewer.review(
            goal=self.state.goal,
            acceptance_criteria=self.state.acceptance_criteria,
            changed_files=result.get('files_changed', []),
            git_diff=result.get('git_diff', ''),
            test_results=result.get('tests_run', ''),
            state=self.state,
        )
        
        iteration_record.reviewer_result = 'PASS' if passed else 'FAIL'
        iteration_record.findings = findings
        iteration_record.git_commit = result.get('git_commit')
        
        # Update state
        self.state.changed_files = result.get('files_changed', [])
        self.state.latest_commit = result.get('git_commit')
        
        if passed:
            # Stage 5: Final gate
            self.state.status = WorkflowStatus.FINAL_GATE
            gate_passed, gate_msg = self.final_gate.verify(
                state=self.state,
                reviewer_passed=passed,
                reviewer_findings=findings,
            )
            
            if gate_passed:
                self.state.status = WorkflowStatus.DONE
            else:
                # Gate failed despite reviewer pass
                # Record and potentially fix
                self.state.status = WorkflowStatus.FIX_REQUIRED
                self.state.fix_iteration += 1
        else:
            # Review failed - need fixes
            self.state.status = WorkflowStatus.FIX_REQUIRED
            self.state.fix_iteration += 1
            self.state.unresolved_findings = [
                f for f in findings
                if f.severity in (FindingSeverity.CRITICAL, FindingSeverity.HIGH)
            ]
        
        self.state.iterations.append(iteration_record)
        self.state.update_timestamp()
    
    def _build_prompt(self) -> str:
        """Build prompt for current iteration."""
        if self.state.iteration == 1:
            # Initial prompt
            prompt = f"""Goal: {self.state.goal}

Acceptance Criteria:
"""
            for i, criterion in enumerate(self.state.acceptance_criteria, 1):
                prompt += f"{i}. {criterion}\n"
            
            prompt += "\nImplement this task following the project's architecture and testing standards."
            return prompt
        else:
            # Fix iteration prompt
            prompt = f"""Previous implementation had issues. Fix the following:

Goal: {self.state.goal}

Unresolved Findings:
"""
            for finding in self.state.unresolved_findings:
                prompt += f"[{finding.severity.value.upper()}] {finding.description}\n"
                if finding.evidence:
                    prompt += f"  Evidence: {finding.evidence}\n"
            
            prompt += "\nProvide minimal targeted fixes for these issues only."
            return prompt
    
    def _compact_context(self) -> Dict:
        """
        Compact workflow context to free space.
        
        Returns:
            {
                'success': bool,
                'context_saved': int,
                'message': str,
            }
        """
        try:
            # Perform compaction
            compaction_result = self.compactor.compact(self.state)
            context_saved = compaction_result['context_saved']
            
            # Update context governor
            new_context = max(0, self.context_governor.context_used - context_saved)
            freed = self.context_governor.compact(new_context)
            
            # Update state
            self.state.context_used = new_context
            self.state.context_utilization = self.context_governor.utilization
            self.state.compaction_count = self.context_governor.compaction_count
            
            return {
                'success': True,
                'context_saved': freed,
                'message': f'Compacted: freed {freed} context tokens',
            }
        except Exception as e:
            return {
                'success': False,
                'context_saved': 0,
                'message': f'Compaction failed: {str(e)}',
            }
    
    def save_state(self, path: Path):
        """Persist workflow state."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(self.state.to_json())
    
    def get_summary(self) -> str:
        """Generate workflow summary."""
        summary = f"""
WORKFLOW SUMMARY
================

Task: {self.state.task_id}
Goal: {self.state.goal}

Status: {self.state.status.value}
Iterations: {self.state.iteration}/{self.state.max_iterations}
Fix Iterations: {self.state.fix_iteration}/{self.state.max_fix_iterations}

Budget:
  Total: {self.state.total_token_budget}
  Used: {self.state.tokens_used}
  Reserved: {self.state.tokens_reserved}
  Remaining: {self.state.tokens_remaining}
  Utilization: {self.state.tokens_used/self.state.total_token_budget*100:.1f}%

Context:
  Limit: {self.state.context_limit}
  Used: {self.state.context_used}
  Remaining: {self.state.context_remaining}
  Utilization: {self.state.context_utilization*100:.1f}%
  Compactions: {self.state.compaction_count}

Changed Files: {len(self.state.changed_files)}
Latest Commit: {self.state.latest_commit or 'None'}

Unresolved Findings: {len(self.state.unresolved_findings)}
"""
        return summary
