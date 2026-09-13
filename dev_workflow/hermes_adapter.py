"""
Hermes execution adapter for v1.4.

Provides explicit boundary between orchestrator and Hermes execution capability.
Never imports execute_code directly - receives it from active Hermes context.
"""

from typing import Dict, Callable, Optional
from dataclasses import dataclass


@dataclass
class HermesContextStatus:
    """Status of Hermes execution context."""
    available: bool
    reason: str


class HermesExecutionAdapter:
    """
    Adapter between orchestrator and Hermes execution capability.
    
    v1.4: Explicit context bridge.
    
    Does NOT import execute_code as a module.
    Receives execution capability from active Hermes context.
    Returns BLOCKED when capability unavailable.
    """
    
    def __init__(self, execute_code_fn: Optional[Callable] = None):
        """
        Initialize adapter with optional Hermes execution capability.
        
        Args:
            execute_code_fn: Hermes execute_code function from active context.
                            If None, adapter will BLOCK execution attempts.
        """
        self._execute_code_fn = execute_code_fn
        self._execution_history = []
    
    def check_context(self) -> HermesContextStatus:
        """
        Check if Hermes execution context is available.
        
        Returns:
            HermesContextStatus indicating availability
        """
        if self._execute_code_fn is not None:
            return HermesContextStatus(
                available=True,
                reason="Hermes execution capability injected"
            )
        else:
            return HermesContextStatus(
                available=False,
                reason="Hermes execution capability unavailable (standalone context)"
            )
    
    def execute_script(self, script: str) -> Dict:
        """
        Execute script using Hermes capability if available.
        
        Args:
            script: Python script to execute
        
        Returns:
            Execution result dict or BLOCKED dict
        """
        context_status = self.check_context()
        
        if not context_status.available:
            return {
                'success': False,
                'message': f'BLOCKED: {context_status.reason}',
                'files_changed': [],
                'tests_run': '',
                'test_exit_code': None,
                'git_diff': '',
                'commands_executed': [],
                'blocked': True,
            }
        
        try:
            # Execute using injected Hermes capability
            result = self._execute_code_fn(code=script)
            
            # Parse output
            import json
            output = result.get('output', '{}')
            parsed = json.loads(output.strip())
            
            self._execution_history.append({
                'script_length': len(script),
                'success': parsed.get('success', False),
            })
            
            return parsed
            
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'message': f'JSON parse error: {str(e)}',
                'files_changed': [],
                'tests_run': '',
                'test_exit_code': None,
                'git_diff': '',
                'commands_executed': [],
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Execution error: {str(e)}',
                'files_changed': [],
                'tests_run': '',
                'test_exit_code': None,
                'git_diff': '',
                'commands_executed': [],
            }


def create_hermes_adapter_from_context() -> HermesExecutionAdapter:
    """
    Create adapter by detecting active Hermes context.
    
    This is called FROM WITHIN Hermes where execute_code is available
    as a callable in the global scope (not a module import).
    
    Returns:
        HermesExecutionAdapter with execute_code if available,
        or None-initialized adapter if not in Hermes context.
    """
    # Try to get execute_code from the calling context
    # It's a function provided by Hermes, not a module
    try:
        import sys
        frame = sys._getframe(1)  # Caller's frame
        execute_code_fn = frame.f_globals.get('execute_code')
        
        if execute_code_fn and callable(execute_code_fn):
            return HermesExecutionAdapter(execute_code_fn)
        else:
            return HermesExecutionAdapter(None)
    except:
        # If we can't access caller's frame, return unavailable adapter
        return HermesExecutionAdapter(None)
