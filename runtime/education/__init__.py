"""
Education System for IRI (AE01M)

Architecture:
    Curriculum → Subject → Lesson → Practice → Assessment → Mastery → Memory → Self-Model

Components:
    - Subject: Domain of study (Thai, English, etc.)
    - Lesson: Unit of instruction with objectives
    - Assessment: Evaluates understanding
    - MasteryTracker: Tracks progress across lessons
    - Curriculum: Orchestrates the complete education system
    - LearningSession: Integrates with Memory, SelfModel, Identity
    - KnowledgeState: Tracks understanding level per concept
    - Persistence: Saves/loads state to disk
"""

from runtime.education.subject import Subject, SubjectType
from runtime.education.lesson import Lesson
from runtime.education.assessment import Assessment, AssessmentResult
from runtime.education.mastery_tracker import MasteryTracker, MasteryRecord
from runtime.education.curriculum import Curriculum
from runtime.education.learning_session import LearningSession, LearningSessionResult
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel, ErrorType
from runtime.education.persistence import EducationPersistence

__all__ = [
    "Subject",
    "SubjectType",
    "Lesson",
    "Assessment",
    "AssessmentResult",
    "MasteryTracker",
    "MasteryRecord",
    "Curriculum",
    "LearningSession",
    "LearningSessionResult",
    "KnowledgeState",
    "KnowledgeLevel",
    "ErrorType",
    "EducationPersistence",
]
