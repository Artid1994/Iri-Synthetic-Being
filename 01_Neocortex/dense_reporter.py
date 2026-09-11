"""
Ultra-Dense Reporting Engine - Zero-fluff, maximum token efficiency
Enforces strict formatting and word limits for all status reports.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ReportStatus(Enum):
    """Report status codes."""
    COMPLETE = "COMPLETE"
    OPERATIONAL = "OPERATIONAL"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"


@dataclass
class CompactReport:
    """Compact status report structure (150-200 words max)."""
    status: ReportStatus
    metrics: Dict[str, Any]  # Max 3 key metrics
    changes: List[str]  # Max 5 changes
    action_required: str  # "NONE" or specific command
    
    def __str__(self) -> str:
        """Generate ultra-compact report (no fluff)."""
        lines = []
        
        # Status (1 line)
        lines.append(f"Status: {self.status.value}")
        
        # Key Metrics (3 lines max, table format)
        if self.metrics:
            lines.append("\nMetrics:")
            for k, v in list(self.metrics.items())[:3]:
                lines.append(f"  {k}: {v}")
        
        # Changes (5 lines max, bullets)
        if self.changes:
            lines.append("\nChanges:")
            for change in self.changes[:5]:
                lines.append(f"  • {change}")
        
        # Action Required (1 line)
        lines.append(f"\nAction: {self.action_required}")
        
        return '\n'.join(lines)


class DenseReporter:
    """Token-efficient reporting engine."""
    
    @staticmethod
    def format_status(status: str, metrics: Dict = None, 
                     changes: List[str] = None, 
                     action: str = "NONE") -> str:
        """
        Generate ultra-dense status report.
        Max 150-200 words, zero fluff.
        """
        report = CompactReport(
            status=ReportStatus[status],
            metrics=metrics or {},
            changes=changes or [],
            action_required=action
        )
        return str(report)
    
    @staticmethod
    def format_execution_summary(command: str, result: Dict) -> str:
        """Format execution result (compact)."""
        status = "COMPLETE" if result.get('success') else "FAILED"
        
        metrics = {
            "Duration": f"{result.get('duration', 0):.1f}s",
            "Exit": result.get('exit_code', 0),
            "Output": f"{len(result.get('output', ''))} chars"
        }
        
        changes = [f"Executed: {command[:50]}..."]
        
        return DenseReporter.format_status(status, metrics, changes)
    
    @staticmethod
    def format_research_summary(topic: str, facts_count: int, 
                               source: str, domain: str) -> str:
        """Format research completion (compact)."""
        metrics = {
            "Topic": topic[:30],
            "Facts": facts_count,
            "Source": source
        }
        
        changes = [f"Added {facts_count} facts to knowledge base"]
        
        return DenseReporter.format_status("COMPLETE", metrics, changes)
    
    @staticmethod
    def format_goal_summary(goal_id: str, subtasks: int, 
                           completed: int, status: str) -> str:
        """Format goal progress (compact)."""
        metrics = {
            "Goal": goal_id[:20],
            "Progress": f"{completed}/{subtasks}",
            "Status": status
        }
        
        changes = [f"{completed} of {subtasks} subtasks complete"]
        
        action = "NONE" if status == "COMPLETE" else "Continue execution"
        
        return DenseReporter.format_status(
            "COMPLETE" if status == "COMPLETE" else "IN_PROGRESS",
            metrics,
            changes,
            action
        )
    
    @staticmethod
    def truncate_text(text: str, max_chars: int = 100) -> str:
        """Truncate text for compact display."""
        if len(text) <= max_chars:
            return text
        return text[:max_chars-3] + "..."
    
    @staticmethod
    def format_table(data: Dict, max_rows: int = 3) -> str:
        """Format data as compact table."""
        lines = []
        for i, (k, v) in enumerate(list(data.items())[:max_rows]):
            lines.append(f"{k:12} | {v}")
        return '\n'.join(lines)


def create_compact_log_entry(event: str, details: Dict) -> str:
    """Create compact JSON log entry (no whitespace)."""
    import json
    entry = {
        "event": event,
        "details": details,
        "ts": int(__import__('time').time())
    }
    return json.dumps(entry, separators=(',', ':'))


# Reporting rules enforcement
REPORTING_RULES = """
ULTRA-DENSE REPORTING RULES:
1. NO greetings, transitions, or conversational text
2. Use tables or key-value pairs ONLY
3. Max 150-200 words per report
4. Omit redundant code/status duplications
5. 4-section format: Status/Metrics/Changes/Action
"""
