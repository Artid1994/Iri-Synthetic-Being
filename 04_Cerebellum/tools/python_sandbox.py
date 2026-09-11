"""
Python Sandbox - Safe code execution with resource limits
Isolated execution for testing algorithms and calculations.
"""

import sys
import io
import signal
import resource
from typing import Dict, Optional


class PythonSandbox:
    """Isolated Python code execution sandbox."""
    
    def __init__(self, timeout: int = 5, memory_limit_mb: int = 100):
        self.timeout = timeout
        self.memory_limit = memory_limit_mb * 1024 * 1024  # Convert to bytes
    
    def _set_limits(self):
        """Set resource limits for sandbox."""
        try:
            # Memory limit
            resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit, self.memory_limit))
            # CPU time limit
            resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
        except Exception:
            pass  # Skip if not supported
    
    def execute(self, code: str, safe_builtins: bool = True) -> Dict[str, any]:
        """
        Execute Python code safely with limits.
        Returns {success, output, error, result}.
        """
        # Capture stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        
        result = {
            'success': False,
            'output': '',
            'error': '',
            'result': None
        }
        
        try:
            # Set resource limits (Linux only)
            self._set_limits()
            
            # Restricted namespace (no file I/O, no imports by default)
            namespace = {
                '__builtins__': __builtins__ if not safe_builtins else {
                    'print': print,
                    'len': len,
                    'range': range,
                    'sum': sum,
                    'max': max,
                    'min': min,
                    'abs': abs,
                    'round': round,
                    'int': int,
                    'float': float,
                    'str': str,
                    'list': list,
                    'dict': dict,
                    'set': set,
                    'tuple': tuple,
                }
            }
            
            # Execute code
            exec(code, namespace)
            
            result['success'] = True
            result['output'] = stdout_capture.getvalue()
            result['result'] = namespace.get('result')  # If code sets 'result' variable
            
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            result['output'] = stdout_capture.getvalue()
        
        finally:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        return result
    
    def eval_expression(self, expression: str) -> Optional[any]:
        """
        Safely evaluate a Python expression.
        Returns result or None on error.
        """
        try:
            # Restricted namespace
            namespace = {
                '__builtins__': {
                    'abs': abs,
                    'max': max,
                    'min': min,
                    'sum': sum,
                    'len': len,
                    'round': round,
                    'int': int,
                    'float': float,
                }
            }
            return eval(expression, namespace)
        except Exception:
            return None
