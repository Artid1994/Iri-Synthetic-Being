"""
Education System: Lesson
A single unit of instruction within a subject
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
from uuid import uuid4


@dataclass
class Lesson:
    """A lesson within a subject."""
    subject_id: str
    level: int  # 1=beginner, 2=intermediate, 3=advanced, etc.
    title: str
    objectives: List[str]
    content: str = ""
    prerequisites: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: uuid4().hex)
    
    def __post_init__(self) -> None:
        if not self.subject_id.strip():
            raise ValueError("Lesson subject_id cannot be empty")
        if not self.title.strip():
            raise ValueError("Lesson title cannot be empty")
        if self.level < 1:
            raise ValueError("Lesson level must be >= 1")
        if not self.objectives:
            raise ValueError("Lesson must have at least one objective")
