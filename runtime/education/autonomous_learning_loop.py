"""
Autonomous Learning Loop Orchestrator
Closes the loop for self-directed learning cycles.
"""
from __future__ import annotations

from typing import Optional, List, Dict
from dataclasses import dataclass
from enum import Enum

from runtime.education.self_directed_controller import (
    SelfDirectedLearningController,
    LearningTarget,
)
from runtime.education.learning_session import LearningSession
from runtime.education.lesson import Lesson
from runtime.education.knowledge_state import KnowledgeState
from runtime.learning_exercise import LearningExercise


class CycleStatus(Enum):
    """Status of a learning cycle."""
    COMPLETED = "completed"
    NO_TARGET = "no_target"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class LearningCycleResult:
    """Result of one complete learning cycle."""
    status: CycleStatus
    target_concept: Optional[str]
    score: Optional[float]
    mastered: bool
    gaps_remaining: int
    next_action: str
    details: Dict


class AutonomousLearningLoop:
    """
    Orchestrates autonomous learning cycles.
    
    State-driven: uses current learning state to determine next action.
    """
    
    def __init__(
        self,
        controller: SelfDirectedLearningController,
        learning_session: LearningSession,
        available_lessons: List[Lesson],
        exercise_generators: Optional[Dict[str, callable]] = None,
    ):
        self.controller = controller
        self.learning_session = learning_session
        self.available_lessons = available_lessons
        self.exercise_generators = exercise_generators or {}
        self.cycle_count = 0
    
    def run_cycle(self) -> LearningCycleResult:
        """
        Execute one complete learning cycle.
        
        State-driven: current state → select target → practice → update state → determine next
        """
        self.cycle_count += 1
        
        # Step 1: Select target based on CURRENT state
        target = self.controller.select_next_target(self.available_lessons)
        
        if target is None:
            gaps = self.controller.detect_gaps()
            return LearningCycleResult(
                status=CycleStatus.NO_TARGET,
                target_concept=None,
                score=None,
                mastered=False,
                gaps_remaining=len(gaps),
                next_action='complete' if len(gaps) == 0 else 'blocked',
                details={'message': 'No valid learning target available'},
            )
        
        # Step 2: Get lesson
        lesson = self._get_lesson(target.lesson_id)
        if lesson is None:
            return LearningCycleResult(
                status=CycleStatus.BLOCKED,
                target_concept=target.gap.concept_id,
                score=None,
                mastered=False,
                gaps_remaining=len(self.controller.detect_gaps()),
                next_action='wait',
                details={'message': f'Lesson {target.lesson_id} not found'},
            )
        
        # Step 3: Get exercises
        exercises = self._get_exercises(lesson)
        if not exercises:
            return LearningCycleResult(
                status=CycleStatus.BLOCKED,
                target_concept=lesson.id,
                score=None,
                mastered=False,
                gaps_remaining=len(self.controller.detect_gaps()),
                next_action='wait',
                details={'message': f'No exercises for {lesson.id}'},
            )
        
        # Step 4: Execute practice
        try:
            # Auto-practice: use expected answers (for testing/autonomous mode)
            answers = [ex.expected_answer for ex in exercises]
            
            session_result = self.learning_session.conduct_session(
                lesson=lesson,
                exercises=exercises,
                answers=answers,
            )
            
            # Step 5: Update controller state
            self.controller.update_from_mastery(
                lesson_id=lesson.id,
                mastered=session_result.mastered,
                score=session_result.assessment_result.score,
            )
            
            # Step 6: Determine next action from UPDATED state
            next_target = self.controller.select_next_target(self.available_lessons)
            next_action = 'continue' if next_target is not None else 'complete'
            
            return LearningCycleResult(
                status=CycleStatus.COMPLETED,
                target_concept=lesson.id,
                score=session_result.assessment_result.score,
                mastered=session_result.mastered,
                gaps_remaining=len(self.controller.detect_gaps()),
                next_action=next_action,
                details={'lesson_title': lesson.title},
            )
            
        except Exception as e:
            return LearningCycleResult(
                status=CycleStatus.FAILED,
                target_concept=lesson.id,
                score=None,
                mastered=False,
                gaps_remaining=len(self.controller.detect_gaps()),
                next_action='wait',
                details={'error': str(e)},
            )
    
    def run_until_complete(self, max_cycles: int = 100) -> List[LearningCycleResult]:
        """Run learning cycles until completion or max cycles."""
        results = []
        
        for i in range(max_cycles):
            result = self.run_cycle()
            results.append(result)
            
            if result.next_action in ['complete', 'wait']:
                break
            
            if result.status in [CycleStatus.FAILED, CycleStatus.BLOCKED]:
                break
        
        return results
    
    def _get_lesson(self, lesson_id: Optional[str]) -> Optional[Lesson]:
        """Find lesson by ID."""
        if lesson_id is None:
            return None
        
        for lesson in self.available_lessons:
            if lesson.id == lesson_id:
                return lesson
        
        return None
    
    def _get_exercises(self, lesson: Lesson) -> List[LearningExercise]:
        """Get exercises for lesson from registered generators."""
        generator = self.exercise_generators.get(lesson.id)
        if generator:
            return generator()
        return []
    
    def get_status(self) -> Dict:
        """Get current loop status."""
        gaps = self.controller.detect_gaps()
        next_target = self.controller.select_next_target(self.available_lessons)
        
        return {
            'cycles_completed': self.cycle_count,
            'gaps_detected': len(gaps),
            'has_next_target': next_target is not None,
            'next_target_id': next_target.lesson_id if next_target else None,
        }
