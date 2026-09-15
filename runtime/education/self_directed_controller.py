"""
Self-Directed Learning Controller
Bridges Education System and Autonomous Learning for closed-loop learning.
"""
from __future__ import annotations

from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass

from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel
from runtime.education.mastery_tracker import MasteryTracker
from runtime.education.lesson import Lesson
from runtime.goal import Goal
from runtime.memory import Memory
from runtime.self_model import SelfModel


@dataclass
class LearningGap:
    """Identified knowledge gap requiring attention."""
    concept_id: str
    gap_type: str  # 'remediation', 'prerequisite', 'next_lesson'
    priority: int  # Higher = more urgent
    knowledge_state: Optional[KnowledgeState]
    error_patterns: List[str]
    
    def to_question(self) -> str:
        """Formulate a learning question from this gap."""
        if self.gap_type == 'remediation':
            return f"How to improve understanding of {self.concept_id}?"
        elif self.gap_type == 'prerequisite':
            return f"What are the prerequisites for {self.concept_id}?"
        elif self.gap_type == 'next_lesson':
            return f"What should I learn after {self.concept_id}?"
        else:
            return f"How to learn {self.concept_id}?"


@dataclass
class LearningTarget:
    """Selected learning target with action plan."""
    gap: LearningGap
    question: str
    action: str  # 'research', 'practice', 'review'
    lesson_id: Optional[str]


class SelfDirectedLearningController:
    """
    Integrates Education System with Autonomous Learning.
    
    Enables IRI to:
    1. Detect knowledge gaps
    2. Formulate learning questions
    3. Select learning targets
    4. Route to appropriate learning system
    5. Update memory and self-model
    
    Does NOT claim:
    - Consciousness
    - True autonomy
    - AGI capability
    
    Provides:
    - Closed-loop learning infrastructure
    - Gap-driven learning selection
    - Integration bridge between systems
    """
    
    def __init__(
        self,
        mastery_tracker: MasteryTracker,
        memory: Memory,
        self_model: SelfModel,
    ):
        self.mastery_tracker = mastery_tracker
        self.memory = memory
        self.self_model = self_model
        self.knowledge_states: Dict[str, KnowledgeState] = {}
    
    def register_knowledge_state(self, concept_id: str, state: KnowledgeState) -> None:
        """Register a knowledge state for gap detection."""
        self.knowledge_states[concept_id] = state
    
    def detect_gaps(self) -> List[LearningGap]:
        """
        Detect knowledge gaps across all registered concepts.
        
        Returns prioritized list of gaps requiring attention.
        """
        gaps = []
        
        # Check knowledge states for remediation needs
        for concept_id, state in self.knowledge_states.items():
            if state.needs_remediation():
                gaps.append(LearningGap(
                    concept_id=concept_id,
                    gap_type='remediation',
                    priority=3,  # High priority
                    knowledge_state=state,
                    error_patterns=[],  # To be filled by caller
                ))
        
        # Check mastery tracker for incomplete lessons
        # Note: MasteryTracker doesn't expose lesson list, so we rely on external enumeration
        
        # Sort by priority
        gaps.sort(key=lambda g: g.priority, reverse=True)
        
        return gaps
    
    def select_next_target(
        self,
        available_lessons: List[Lesson],
    ) -> Optional[LearningTarget]:
        """
        Select the next learning target based on:
        1. Detected gaps (highest priority)
        2. Prerequisites met
        3. Next unmasted lesson
        
        Returns None if no valid target exists.
        """
        # First: address any gaps
        gaps = self.detect_gaps()
        if gaps:
            top_gap = gaps[0]
            return LearningTarget(
                gap=top_gap,
                question=top_gap.to_question(),
                action='practice',  # Remediation = more practice
                lesson_id=top_gap.concept_id if top_gap.gap_type == 'remediation' else None,
            )
        
        # Second: find next lesson with prerequisites met
        for lesson in available_lessons:
            if not self.mastery_tracker.is_mastered(lesson.id):
                if self.mastery_tracker.prerequisites_met(lesson.prerequisites):
                    # This is the next valid lesson
                    return LearningTarget(
                        gap=LearningGap(
                            concept_id=lesson.id,
                            gap_type='next_lesson',
                            priority=1,
                            knowledge_state=None,
                            error_patterns=[],
                        ),
                        question=f"How to complete lesson: {lesson.title}?",
                        action='practice',
                        lesson_id=lesson.id,
                    )
        
        # No targets found
        return None
    
    def formulate_question(self, gap: LearningGap) -> str:
        """
        Formulate a specific learning question from a gap.
        
        Note: This creates general questions. Specific question generation
        would require deeper integration with lesson content.
        """
        return gap.to_question()
    
    def create_goal_from_gap(self, gap: LearningGap) -> Goal:
        """
        Create a Goal object from a learning gap.
        
        This bridges to the existing Goal-based learning system.
        """
        question = self.formulate_question(gap)
        
        goal = Goal(
            description=question,
            priority=gap.priority,
        )
        # Goal is created as ACTIVE by default
        
        return goal
    
    def update_from_mastery(
        self,
        lesson_id: str,
        mastered: bool,
        score: float,
    ) -> None:
        """
        Update memory and self-model from mastery result.
        
        This consolidates verified learning.
        """
        # Update self-model with learning progress
        if mastered:
            # Add to memory as mastered
            self.memory.add_experience(
                f"Mastered: {lesson_id} (score: {int(score * 100)}%)"
            )
            
            # Update self-model: capability gained
            self.self_model.update(
                self_knowledge_delta=0.01,  # Small increment per mastery
                history_entry=f"Mastered {lesson_id}"
            )
        else:
            # Record as in-progress
            self.memory.add_experience(
                f"Practicing: {lesson_id} (score: {int(score * 100)}%)"
            )
            
            # Update self-model: learning in progress
            self.self_model.update(
                self_awareness_delta=0.005,  # Awareness of learning process
                history_entry=f"Practicing {lesson_id}"
            )
    
    def verify_learning_result(
        self,
        concept: str,
        evidence: str,
        confidence: float,
    ) -> Tuple[bool, str]:
        """
        Verify learning result before accepting as knowledge.
        
        Returns: (accepted, reason)
        
        Verification criteria:
        - Confidence threshold
        - Consistency with existing knowledge
        - Source reliability (if applicable)
        
        Note: This is a placeholder. Real verification would need
        domain-specific logic.
        """
        if confidence < 0.7:
            return False, f"Low confidence: {confidence}"
        
        # Basic acceptance
        return True, "Accepted based on confidence threshold"
    
    def get_learning_status(self) -> Dict:
        """
        Get current learning status summary.
        
        Returns:
        - Total concepts tracked
        - Gaps detected
        - Lessons mastered
        - Next recommended target
        """
        gaps = self.detect_gaps()
        
        # Count mastered lessons from tracker
        # Note: MasteryTracker doesn't expose count directly
        
        return {
            'concepts_tracked': len(self.knowledge_states),
            'gaps_detected': len(gaps),
            'top_priority_gap': gaps[0].concept_id if gaps else None,
        }
