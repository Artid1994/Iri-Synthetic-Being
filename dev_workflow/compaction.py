"""
Context compaction for workflow state.

Preserves authoritative information, discards redundant context.
"""

from typing import Dict
from .state import WorkflowState, ReviewerFinding, FindingSeverity


class StateCompactor:
    """
    Compacts workflow state to reduce context usage.
    
    Preserves:
    - Goal and acceptance criteria
    - Current iteration state
    - Unresolved findings
    - Budget/context state
    - Critical file paths
    - Latest commit
    
    Discards:
    - Redundant iteration history
    - Duplicate logs
    - Obsolete attempts
    """
    
    def __init__(self):
        self.compaction_history = []
    
    def compact(self, state: WorkflowState) -> Dict:
        """
        Compact workflow state.
        
        Returns:
            {
                'compacted_state': dict,
                'context_saved': int,
                'preserved_items': list,
            }
        """
        # Calculate current state size (rough estimate)
        original_size = self._estimate_state_size(state)
        
        # Build compact representation
        compact_state = {
            # Essential task definition
            'task_id': state.task_id,
            'goal': state.goal,
            'acceptance_criteria': state.acceptance_criteria,
            
            # Current progress
            'status': state.status.value,
            'iteration': state.iteration,
            'fix_iteration': state.fix_iteration,
            
            # Budget state
            'total_token_budget': state.total_token_budget,
            'tokens_used': state.tokens_used,
            'tokens_reserved': state.tokens_reserved,
            'tokens_remaining': state.tokens_remaining,
            
            # Context state
            'context_limit': state.context_limit,
            'context_used': state.context_used,
            'context_utilization': state.context_utilization,
            'compaction_count': state.compaction_count + 1,
            
            # Limits
            'max_iterations': state.max_iterations,
            'max_fix_iterations': state.max_fix_iterations,
            
            # Critical findings only (CRITICAL/HIGH)
            'unresolved_findings': [
                {
                    'severity': f.severity.value,
                    'description': f.description,
                    'affected_files': f.affected_files,
                    'evidence': f.evidence[:200] if f.evidence else '',  # Truncate evidence
                }
                for f in state.unresolved_findings
                if f.severity in (FindingSeverity.CRITICAL, FindingSeverity.HIGH)
            ],
            
            # Recent iterations only (last 2)
            'recent_iterations': [
                {
                    'iteration': rec.iteration,
                    'stage': rec.stage,
                    'estimated_tokens': rec.estimated_tokens,
                    'actual_tokens': rec.actual_tokens,
                    'reviewer_result': rec.reviewer_result,
                    'finding_count': len(rec.findings),
                }
                for rec in state.iterations[-2:]
            ],
            
            # File state
            'changed_files': state.changed_files,
            'latest_commit': state.latest_commit,
            
            # Metadata
            'created_at': state.created_at,
            'updated_at': state.updated_at,
        }
        
        # Calculate compacted size
        compacted_size = self._estimate_dict_size(compact_state)
        context_saved = original_size - compacted_size
        
        preserved_items = [
            'goal', 'acceptance_criteria', 'current_iteration',
            'unresolved_findings', 'budget_state', 'changed_files'
        ]
        
        self.compaction_history.append({
            'original_size': original_size,
            'compacted_size': compacted_size,
            'saved': context_saved,
            'iteration': state.iteration,
        })
        
        return {
            'compacted_state': compact_state,
            'context_saved': context_saved,
            'preserved_items': preserved_items,
        }
    
    def _estimate_state_size(self, state: WorkflowState) -> int:
        """Estimate state size in tokens."""
        # Rough estimate: serialize and count
        state_dict = state.to_dict()
        return self._estimate_dict_size(state_dict)
    
    def _estimate_dict_size(self, data: Dict) -> int:
        """Estimate dictionary size in tokens."""
        # Convert to string and estimate tokens
        import json
        json_str = json.dumps(data)
        return len(json_str) // 4  # ~4 chars per token
