"""
Education System: Subject/Domain
Represents a subject of study (e.g., Thai Language, English Language)
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SubjectType(Enum):
    """Types of subjects."""
    LANGUAGE = "language"
    SCIENCE = "science"
    MATHEMATICS = "mathematics"
    TECHNICAL = "technical"


@dataclass(frozen=True)
class Subject:
    """A subject of study."""
    id: str
    name: str
    subject_type: SubjectType
    description: str = ""
    
    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Subject ID cannot be empty")
        if not self.name.strip():
            raise ValueError("Subject name cannot be empty")
