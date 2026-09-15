"""
Education System: Mastery Tracker
Tracks learning progress and mastery across lessons
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
import time


@dataclass
class MasteryRecord:
    """Record of mastery for a single lesson."""
    lesson_id: str
    mastery_score: float = 0.0  # 0.0 to 1.0
    attempts: int = 0
    last_attempt: Optional[float] = None
    mastered: bool = False
    
    def __post_init__(self) -> None:
        if not (0.0 <= self.mastery_score <= 1.0):
            raise ValueError("Mastery score must be between 0.0 and 1.0")
        if self.attempts < 0:
            raise ValueError("Attempts cannot be negative")


class MasteryTracker:
    """Tracks mastery across all lessons."""
    
    MASTERY_THRESHOLD = 0.8
    
    def __init__(self) -> None:
        self.records: Dict[str, MasteryRecord] = {}
        self._persistence = None  # Will be set externally
    
    def set_persistence(self, persistence) -> None:
        """Set persistence handler for auto-saving."""
        self._persistence = persistence
    
    def record_attempt(
        self,
        lesson_id: str,
        score: float,
    ) -> MasteryRecord:
        """
        Record an attempt at a lesson.
        
        Args:
            lesson_id: ID of the lesson
            score: Score achieved (0.0 to 1.0)
            
        Returns:
            Updated MasteryRecord
        """
        if not (0.0 <= score <= 1.0):
            raise ValueError("Score must be between 0.0 and 1.0")
        
        if lesson_id not in self.records:
            self.records[lesson_id] = MasteryRecord(lesson_id=lesson_id)
        
        record = self.records[lesson_id]
        
        # Update with new score (weighted average: 70% new, 30% old)
        if record.attempts > 0:
            new_score = (0.7 * score) + (0.3 * record.mastery_score)
        else:
            new_score = score
        
        record.mastery_score = new_score
        record.attempts += 1
        record.last_attempt = time.time()
        record.mastered = new_score >= self.MASTERY_THRESHOLD
        
        # Auto-save if persistence is configured
        if self._persistence:
            self._persistence.save_mastery_records(self.records)
        
        return record
    
    def is_mastered(self, lesson_id: str) -> bool:
        """Check if a lesson has been mastered."""
        if lesson_id not in self.records:
            return False
        return self.records[lesson_id].mastered
    
    def get_progress(self, lesson_id: str) -> Optional[MasteryRecord]:
        """Get progress record for a lesson."""
        return self.records.get(lesson_id)
    
    def prerequisites_met(
        self,
        prerequisites: list[str],
    ) -> bool:
        """Check if all prerequisites have been mastered."""
        if not prerequisites:
            return True
        return all(self.is_mastered(prereq) for prereq in prerequisites)
    
    def load_records(self, records: Dict[str, MasteryRecord]) -> None:
        """Load mastery records from persistence."""
        self.records = records
