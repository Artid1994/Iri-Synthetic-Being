"""
Autonomous School Integration
Connects SchoolWorkflow with AutonomousLoop for continuous learning
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, Any
import time

from runtime.education.school_workflow import (
    SchoolWorkflow,
    TestItem,
    TestResult,
)
from runtime.education.curriculum import Curriculum


class AutonomousSchool:
    """
    Autonomous learning controller that uses SchoolWorkflow
    to manage IRI's continuous education without human prompts.
    
    Integration with autonomous_loop.py:
    - Tracks current lesson
    - Generates appropriate assessments
    - Makes mastery decisions
    - Advances to next lesson
    - Handles remediation
    """
    
    def __init__(
        self,
        workflow: SchoolWorkflow,
        curriculum: Curriculum,
    ):
        self.workflow = workflow
        self.curriculum = curriculum
        self.current_lesson_id: Optional[str] = None
        self.current_phase: str = "IDLE"  # IDLE, BASELINE, TEACHING, PRACTICE, POST_TEST, RETENTION, TRANSFER
        self.phase_data: Dict[str, Any] = {}
    
    def get_current_objective(self) -> Optional[str]:
        """
        Get current learning objective for autonomous_loop.
        Returns human-readable objective or None if no active learning.
        """
        if self.current_lesson_id is None:
            # Check if there's a next lesson
            next_lesson_id = self.workflow.get_next_lesson_for_autonomous(
                self.curriculum
            )
            if next_lesson_id:
                self.current_lesson_id = next_lesson_id
                self.current_phase = "BASELINE"
                lesson = self.curriculum.get_lesson_by_id(next_lesson_id)
                return f"Begin learning: {lesson.title if lesson else next_lesson_id}"
            return None
        
        lesson = self.curriculum.get_lesson_by_id(self.current_lesson_id)
        if not lesson:
            return None
        
        # Return phase-appropriate objective
        phase_objectives = {
            "BASELINE": f"Baseline assessment: {lesson.title}",
            "TEACHING": f"Learning: {lesson.title}",
            "PRACTICE": f"Practice: {lesson.title}",
            "POST_TEST": f"Post-test: {lesson.title}",
            "RETENTION": f"Retention check: {lesson.title}",
            "TRANSFER": f"Transfer assessment: {lesson.title}",
        }
        
        return phase_objectives.get(self.current_phase, f"Study: {lesson.title}")
    
    def advance_phase(self) -> str:
        """
        Advance to next phase of learning cycle.
        Returns: next phase name
        """
        phase_sequence = [
            "BASELINE",
            "TEACHING",
            "PRACTICE",
            "POST_TEST",
            "RETENTION",
            "TRANSFER",
            "DECISION",
        ]
        
        if self.current_phase not in phase_sequence:
            self.current_phase = "BASELINE"
            return self.current_phase
        
        current_idx = phase_sequence.index(self.current_phase)
        
        if current_idx < len(phase_sequence) - 1:
            self.current_phase = phase_sequence[current_idx + 1]
        else:
            # End of cycle, make mastery decision
            if self.current_lesson_id:
                decision = self.workflow.make_mastery_decision(
                    self.current_lesson_id
                )
                
                if decision.next_action == "RETEACH":
                    # Remediation needed
                    self.current_phase = "TEACHING"
                elif decision.next_action == "ADVANCE":
                    # Mastered, move to next lesson
                    self.current_lesson_id = None
                    self.current_phase = "IDLE"
                else:
                    # More practice needed
                    self.current_phase = "PRACTICE"
        
        return self.current_phase
    
    def should_conduct_assessment(self, phase: str) -> bool:
        """Check if current phase requires assessment."""
        return phase in ["BASELINE", "POST_TEST", "RETENTION", "TRANSFER"]
    
    def get_assessment_type(self, phase: str) -> str:
        """Map phase to assessment type."""
        mapping = {
            "BASELINE": "baseline",
            "POST_TEST": "immediate_recall",
            "RETENTION": "retention",
            "TRANSFER": "transfer",
        }
        return mapping.get(phase, "immediate_recall")
    
    def record_lesson_completion(
        self,
        lesson_id: str,
        test_results: list[TestResult],
        assessment_type: str,
    ) -> None:
        """Record assessment results after a lesson phase."""
        assessment_id = f"{assessment_type}_{lesson_id}_{int(time.time())}"
        
        self.workflow.record_assessment(
            assessment_id=assessment_id,
            assessment_type=assessment_type,
            lesson_id=lesson_id,
            test_results=test_results,
        )
        
        # Calculate learning gain if post-test
        if assessment_type == "immediate_recall":
            self.workflow.calculate_learning_gain(lesson_id)
    
    def needs_remediation(self) -> bool:
        """Check if current lesson needs remediation."""
        if not self.current_lesson_id:
            return False
        return self.workflow.needs_remediation(self.current_lesson_id)
    
    def is_lesson_mastered(self, lesson_id: str) -> bool:
        """Check if lesson is mastered."""
        return self.workflow.is_mastered(lesson_id)
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get summary of learning progress for all lessons."""
        summary = {
            "current_lesson": self.current_lesson_id,
            "current_phase": self.current_phase,
            "lessons_mastered": [],
            "lessons_in_progress": [],
            "lessons_need_remediation": [],
        }
        
        for lesson_id in self.curriculum.lessons.keys():
            status = self.workflow.lesson_status.get(lesson_id)
            
            if status == "MASTERED" or self.workflow.is_mastered(lesson_id):
                summary["lessons_mastered"].append(lesson_id)
            elif self.workflow.needs_remediation(lesson_id):
                summary["lessons_need_remediation"].append(lesson_id)
            elif status is not None:
                # Has some status, so in progress
                summary["lessons_in_progress"].append(lesson_id)
        
        return summary
    
    def create_transfer_test(
        self,
        lesson_id: str,
        original_items: list[TestItem],
    ) -> list[TestItem]:
        """
        Create transfer test for a lesson using novel item formats.
        Prevents answer leakage.
        """
        return self.workflow.generate_transfer_items(
            original_items,
            transform="rephrase"
        )
    
    def get_next_action(self) -> str:
        """
        Get next action for autonomous loop.
        Returns: action command ("ASSESS", "TEACH", "PRACTICE", "ADVANCE", "IDLE")
        """
        if not self.current_lesson_id:
            # Try to get next lesson
            next_id = self.workflow.get_next_lesson_for_autonomous(self.curriculum)
            if next_id:
                self.current_lesson_id = next_id
                self.current_phase = "BASELINE"
                return "ASSESS"
            return "IDLE"
        
        if self.current_phase in ["BASELINE", "POST_TEST", "RETENTION", "TRANSFER"]:
            return "ASSESS"
        elif self.current_phase == "TEACHING":
            return "TEACH"
        elif self.current_phase == "PRACTICE":
            return "PRACTICE"
        elif self.current_phase == "DECISION":
            # Make decision and determine next action
            decision = self.workflow.make_mastery_decision(self.current_lesson_id)
            if decision.next_action == "ADVANCE":
                self.current_lesson_id = None
                self.current_phase = "IDLE"
                return "ADVANCE"
            elif decision.next_action == "RETEACH":
                self.current_phase = "TEACHING"
                return "TEACH"
            else:
                self.current_phase = "PRACTICE"
                return "PRACTICE"
        
        return "IDLE"
    
    def reset_lesson(self, lesson_id: str) -> None:
        """Reset lesson for remediation (clears mastery decision but keeps assessment history)."""
        if lesson_id in self.workflow.lesson_status:
            del self.workflow.lesson_status[lesson_id]
        self.workflow.save_state()
