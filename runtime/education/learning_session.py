"""
Education System: Learning Session
Orchestrates lesson practice, assessment, and integration
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict
import time

from runtime.education.lesson import Lesson
from runtime.education.assessment import Assessment, AssessmentResult
from runtime.education.mastery_tracker import MasteryTracker
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel, ErrorType
from runtime.learning_exercise import LearningExercise
from runtime.learning_verification import LearningVerification
from runtime.memory import Memory
from runtime.self_model import SelfModel
from runtime.identity import Identity


@dataclass(frozen=True)
class LearningSessionResult:
    """Result of a complete learning session."""
    lesson_id: str
    assessment_result: AssessmentResult
    mastered: bool
    exercises_attempted: int
    requires_remediation: bool
    knowledge_gaps: list[str]  # Concepts needing remediation


class LearningSession:
    """
    Orchestrates a complete learning session:
    Lesson → Practice → Assessment → Mastery → Memory → Self-Model
    """
    
    def __init__(
        self,
        mastery_tracker: MasteryTracker,
        memory: Memory,
        self_model: SelfModel,
        identity: Identity,
        persistence=None,
    ) -> None:
        self.mastery_tracker = mastery_tracker
        self.memory = memory
        self.self_model = self_model
        self.identity = identity
        self.assessment = Assessment()
        self.verification = LearningVerification()
        self.knowledge_states: Dict[str, KnowledgeState] = {}
        self._persistence = persistence
        
        # Load knowledge states if persistence configured
        if self._persistence:
            self.knowledge_states = self._persistence.load_knowledge_states()
    
    def conduct_session(
        self,
        lesson: Lesson,
        exercises: list[LearningExercise],
        answers: Optional[list[str]] = None,
    ) -> LearningSessionResult:
        """
        Conduct a complete learning session.
        
        Args:
            lesson: The lesson to study
            exercises: Practice exercises for the lesson
            answers: Optional answers to verify (for testing/practice)
            
        Returns:
            LearningSessionResult with assessment and mastery status
        """
        if not isinstance(lesson, Lesson):
            raise TypeError("lesson must be a Lesson instance")
        if not exercises:
            raise ValueError("exercises cannot be empty")
        
        # Practice phase with knowledge tracking
        correct_count = 0
        total_count = len(exercises)
        knowledge_gaps = []
        
        if answers:
            # Verify provided answers and track knowledge
            for exercise, answer in zip(exercises, answers):
                concept_id = f"{lesson.id}:{exercise.question[:50]}"
                
                result = self.verification.check(exercise, answer)
                
                if concept_id not in self.knowledge_states:
                    self.knowledge_states[concept_id] = KnowledgeState(concept_id=concept_id)
                
                knowledge_state = self.knowledge_states[concept_id]
                
                if result.passed:
                    correct_count += 1
                    knowledge_state.record_correct()
                else:
                    # Determine error type
                    if not answer or answer.strip() == "":
                        error_type = ErrorType.UNKNOWN
                    elif len(answer) > 0 and len(exercise.expected_answer) > 0:
                        # Simple heuristic: partial if some overlap
                        answer_lower = answer.lower()
                        expected_lower = exercise.expected_answer.lower()
                        if any(word in expected_lower for word in answer_lower.split()):
                            error_type = ErrorType.PARTIAL
                        else:
                            error_type = ErrorType.INCORRECT
                    else:
                        error_type = ErrorType.INCORRECT
                    
                    knowledge_state.record_error(error_type)
                    
                    if knowledge_state.needs_remediation():
                        knowledge_gaps.append(concept_id)
        else:
            # Simulate perfect practice (for testing without answers)
            correct_count = total_count
        
        # Get attempt count
        progress = self.mastery_tracker.get_progress(lesson.id)
        attempts = (progress.attempts + 1) if progress else 1
        
        # Assessment phase
        assessment_result = self.assessment.evaluate(
            correct_count=correct_count,
            total_count=total_count,
            attempts=attempts,
        )
        
        # Record attempt in mastery tracker
        mastery_record = self.mastery_tracker.record_attempt(
            lesson_id=lesson.id,
            score=assessment_result.score,
        )
        
        # Memory consolidation (if mastered)
        if mastery_record.mastered:
            self._consolidate_to_memory(lesson, assessment_result)
        
        # Self-model update
        self._update_self_model(lesson, assessment_result)
        
        # Identity experience
        self.identity.add_experience(amount=1)
        
        # Save learning event to history
        if self._persistence:
            self._persistence.append_learning_event({
                "timestamp": time.time(),
                "lesson_id": lesson.id,
                "lesson_title": lesson.title,
                "score": assessment_result.score,
                "attempts": attempts,
                "mastered": mastery_record.mastered,
                "knowledge_gaps": knowledge_gaps,
            })
            
            # Save knowledge states
            self._persistence.save_knowledge_states(self.knowledge_states)
        
        # Determine if remediation needed
        requires_remediation = (
            not assessment_result.passed and
            attempts >= Assessment.MAX_ATTEMPTS_BEFORE_REMEDIATION
        ) or len(knowledge_gaps) > 0
        
        return LearningSessionResult(
            lesson_id=lesson.id,
            assessment_result=assessment_result,
            mastered=mastery_record.mastered,
            exercises_attempted=total_count,
            requires_remediation=requires_remediation,
            knowledge_gaps=knowledge_gaps,
        )
    
    def get_knowledge_state(self, concept_id: str) -> Optional[KnowledgeState]:
        """Get knowledge state for a concept."""
        return self.knowledge_states.get(concept_id)
    
    def _consolidate_to_memory(
        self,
        lesson: Lesson,
        assessment_result: AssessmentResult,
    ) -> None:
        """Consolidate mastered lesson to memory."""
        memory_entry = (
            f"Mastered: {lesson.title} "
            f"(Level {lesson.level}, Score: {int(assessment_result.score * 100)}%)"
        )
        self.memory.add_experience(memory_entry)
        
        # Add semantic memory for each objective
        for objective in lesson.objectives:
            self.memory.add_semantic(
                f"{lesson.title}: {objective}"
            )
    
    def _update_self_model(
        self,
        lesson: Lesson,
        assessment_result: AssessmentResult,
    ) -> None:
        """Update self-model with learning progress."""
        if assessment_result.passed:
            # Increase self-knowledge for mastered content
            delta = 0.01  # Small incremental gain per lesson
            history_entry = f"Mastered {lesson.title}"
        else:
            # Small awareness gain even from failed attempts (learning from mistakes)
            delta = 0.005
            history_entry = f"Practiced {lesson.title} (score: {int(assessment_result.score * 100)}%)"
        
        self.self_model.update(
            self_knowledge_delta=delta,
            history_entry=history_entry,
        )

