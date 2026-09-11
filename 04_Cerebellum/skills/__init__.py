"""
Cerebellum Skills Package
Autonomous skills for system inspection, text analysis, and task execution.
"""
from pathlib import Path

__version__ = "1.0.0"
__all__ = ["SystemInspector", "TextAnalyzer"]

# Lazy imports to avoid circular dependencies
def get_system_inspector():
    """Get SystemInspector instance."""
    from .system_inspector import SystemInspector
    return SystemInspector()

def get_text_analyzer():
    """Get TextAnalyzer instance."""
    from .text_analyzer import TextAnalyzer
    return TextAnalyzer()
