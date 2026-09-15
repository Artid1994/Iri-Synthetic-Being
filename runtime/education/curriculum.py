"""
Education System: Curriculum
Manages subjects, lessons, and learning paths
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from runtime.education.subject import Subject
from runtime.education.lesson import Lesson
from runtime.education.mastery_tracker import MasteryTracker


class Curriculum:
    """Manages the complete curriculum."""
    
    def __init__(self) -> None:
        self.subjects: Dict[str, Subject] = {}
        self.lessons: Dict[str, Lesson] = {}
        self.mastery_tracker = MasteryTracker()
    
    def add_subject(self, subject: Subject) -> None:
        """Add a subject to the curriculum."""
        if not isinstance(subject, Subject):
            raise TypeError("Must be a Subject instance")
        self.subjects[subject.id] = subject
    
    def add_lesson(self, lesson: Lesson) -> None:
        """Add a lesson to the curriculum."""
        if not isinstance(lesson, Lesson):
            raise TypeError("Must be a Lesson instance")
        
        # Verify subject exists
        if lesson.subject_id not in self.subjects:
            raise ValueError(f"Subject {lesson.subject_id} not found")
        
        self.lessons[lesson.id] = lesson
    
    def get_next_lesson(
        self,
        subject_id: str,
    ) -> Optional[Lesson]:
        """
        Get the next unmastered lesson for a subject.
        
        Args:
            subject_id: ID of the subject
            
        Returns:
            Next lesson to study, or None if all mastered
        """
        if subject_id not in self.subjects:
            return None
        
        # Get all lessons for this subject
        subject_lessons = [
            lesson for lesson in self.lessons.values()
            if lesson.subject_id == subject_id
        ]
        
        if not subject_lessons:
            return None
        
        # Sort by level, then by ID for consistency
        subject_lessons.sort(key=lambda l: (l.level, l.id))
        
        # Find first unmastered lesson with met prerequisites
        for lesson in subject_lessons:
            if self.mastery_tracker.is_mastered(lesson.id):
                continue
            
            if self.mastery_tracker.prerequisites_met(lesson.prerequisites):
                return lesson
        
        return None
    
    def get_lesson_by_id(self, lesson_id: str) -> Optional[Lesson]:
        """Get a lesson by ID."""
        return self.lessons.get(lesson_id)
    
    def get_subject_by_id(self, subject_id: str) -> Optional[Subject]:
        """Get a subject by ID."""
        return self.subjects.get(subject_id)
    
    def get_mastery_progress(self, lesson_id: str):
        """Get mastery progress for a lesson."""
        return self.mastery_tracker.get_progress(lesson_id)
