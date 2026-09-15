"""
Education System: Knowledge State
Tracks understanding level for specific knowledge items
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import time


class KnowledgeLevel(Enum):
    """Levels of knowledge understanding."""
    UNKNOWN = "unknown"              # Never encountered or no recall
    LEARNING = "learning"            # Actively studying, inconsistent
    UNDERSTOOD = "understood"        # Can explain or recognize
    CAN_USE = "can_use"             # Can apply in practice
    MASTERED = "mastered"            # Consistent correct application


class ErrorType(Enum):
    """Types of learning errors."""
    UNKNOWN = "unknown"              # No knowledge of concept
    INCORRECT = "incorrect"          # Wrong answer, has partial knowledge
    PARTIAL = "partial"              # Partially correct, incomplete
    MISCONCEPTION = "misconception"  # Systematic misunderstanding


@dataclass
class KnowledgeState:
    """State of knowledge for a specific concept."""
    concept_id: str
    level: KnowledgeLevel = KnowledgeLevel.UNKNOWN
    correct_count: int = 0
    incorrect_count: int = 0
    last_error_type: Optional[ErrorType] = None
    last_practiced: Optional[float] = None
    
    def record_correct(self) -> None:
        """Record a correct response."""
        self.correct_count += 1
        self.last_practiced = time.time()
        self._update_level()
    
    def record_error(self, error_type: ErrorType) -> None:
        """Record an error."""
        self.incorrect_count += 1
        self.last_error_type = error_type
        self.last_practiced = time.time()
        self._update_level()
    
    def _update_level(self) -> None:
        """Update knowledge level based on performance."""
        total = self.correct_count + self.incorrect_count
        if total == 0:
            self.level = KnowledgeLevel.UNKNOWN
            return
        
        accuracy = self.correct_count / total
        
        if accuracy >= 0.95 and self.correct_count >= 5:
            self.level = KnowledgeLevel.MASTERED
        elif accuracy >= 0.85 and self.correct_count >= 3:
            self.level = KnowledgeLevel.CAN_USE
        elif accuracy >= 0.70 and self.correct_count >= 2:
            self.level = KnowledgeLevel.UNDERSTOOD
        elif self.correct_count >= 1:
            self.level = KnowledgeLevel.LEARNING
        else:
            self.level = KnowledgeLevel.UNKNOWN
    
    def needs_remediation(self) -> bool:
        """Check if remediation is needed."""
        if self.incorrect_count >= 3 and self.level in {
            KnowledgeLevel.UNKNOWN,
            KnowledgeLevel.LEARNING,
        }:
            return True
        return False
