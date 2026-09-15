"""
Education System: Assessment
Evaluates learning progress and mastery
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AssessmentResult:
    """Result of an assessment."""
    passed: bool
    score: float  # 0.0 to 1.0
    attempts: int
    feedback: str = ""
    
    def __post_init__(self) -> None:
        if not (0.0 <= self.score <= 1.0):
            raise ValueError("Score must be between 0.0 and 1.0")
        if self.attempts < 1:
            raise ValueError("Attempts must be >= 1")


class Assessment:
    """Assesses learning progress."""
    
    MASTERY_THRESHOLD = 0.8  # 80% to pass
    MAX_ATTEMPTS_BEFORE_REMEDIATION = 3
    
    def evaluate(
        self,
        correct_count: int,
        total_count: int,
        attempts: int = 1,
    ) -> AssessmentResult:
        """
        Evaluate assessment performance.
        
        Args:
            correct_count: Number of correct answers
            total_count: Total number of questions
            attempts: Number of attempts taken
            
        Returns:
            AssessmentResult with pass/fail and score
        """
        if total_count <= 0:
            raise ValueError("Total count must be > 0")
        if correct_count < 0 or correct_count > total_count:
            raise ValueError("Correct count must be between 0 and total_count")
        if attempts < 1:
            raise ValueError("Attempts must be >= 1")
        
        score = correct_count / total_count
        passed = score >= self.MASTERY_THRESHOLD
        
        if passed:
            feedback = f"MASTERED ({int(score * 100)}%)"
        elif attempts >= self.MAX_ATTEMPTS_BEFORE_REMEDIATION:
            feedback = f"REMEDIATION_REQUIRED (score: {int(score * 100)}%, attempts: {attempts})"
        else:
            feedback = f"NOT_YET_MASTERED ({int(score * 100)}%)"
        
        return AssessmentResult(
            passed=passed,
            score=score,
            attempts=attempts,
            feedback=feedback,
        )
