"""
Thai Week 3 Lesson 3.8: Contextual Reading
Reading words in context for comprehension
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_3_8() -> Lesson:
    """Create Lesson 3.8: Contextual Reading."""
    lesson = Lesson(
        subject_id="thai_language",
        level=3,
        title="การอ่านตามบริบท (Contextual Reading)",
        objectives=[
            "Read words in meaningful context",
            "Use context to support comprehension",
            "Understand word relationships in phrases",
            "Apply vocabulary knowledge contextually",
        ],
        content="Reading vocabulary in context: simple phrases and word combinations. "
                "Practice using context clues for meaning.",
        prerequisites=[],  # Requires lessons 3.1-3.7
    )
    return lesson


def load_contextual_examples() -> List[Dict]:
    """
    Generate contextual reading examples.
    
    Simple 2-3 word phrases demonstrating context.
    """
    examples = [
        {
            'phrase': 'คน ดี',
            'words': ['คน', 'ดี'],
            'meaning': 'good person',
            'pattern': 'noun + adjective',
        },
        {
            'phrase': 'มา บ้าน',
            'words': ['มา', 'บ้าน'],
            'meaning': 'come home',
            'pattern': 'verb + noun',
        },
        {
            'phrase': 'กิน น้ำ',
            'words': ['กิน', 'น้ำ'],
            'meaning': 'drink water',
            'pattern': 'verb + noun',
        },
        {
            'phrase': 'บ้าน ใหญ่',
            'words': ['บ้าน', 'ใหญ่'],
            'meaning': 'big house',
            'pattern': 'noun + adjective',
        },
    ]
    
    return examples


def generate_lesson_3_8_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 3.8.
    
    Exercise types:
    1. Phrase → meaning
    2. Word in context → meaning
    3. Pattern recognition
    """
    examples = load_contextual_examples()
    exercises = []
    
    # Type 1: Phrase → meaning
    for ex in examples:
        exercise = LearningExercise(
            question=f"Meaning: {ex['phrase']}",
            expected_answer=ex['meaning'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Pattern identification
    for ex in examples:
        exercise = LearningExercise(
            question=f"Pattern: {ex['phrase']}",
            expected_answer=ex['pattern'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_3_8_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 3.8.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'meaning_errors': [],
        'pattern_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Meaning' in question:
                error_patterns['meaning_errors'].append((question, answer, exercise.expected_answer))
            elif 'Pattern' in question:
                error_patterns['pattern_errors'].append((question, answer, exercise.expected_answer))
    
    # Determine mastery level (90% threshold)
    if accuracy >= 0.90:
        mastery_level = "mastered"
    elif accuracy >= 0.75:
        mastery_level = "proficient"
    elif accuracy >= 0.60:
        mastery_level = "developing"
    else:
        mastery_level = "novice"
    
    # Identify knowledge gaps
    knowledge_gaps = []
    if len(error_patterns['meaning_errors']) > 1:
        knowledge_gaps.append("contextual comprehension")
    if len(error_patterns['pattern_errors']) > 1:
        knowledge_gaps.append("phrase pattern recognition")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_3_8(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 3.8 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_3_8(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 3.8 assessment.
    
    Consistent 90% threshold.
    """
    record = mastery_tracker.record_attempt(
        lesson_id=lesson_id,
        score=assessment['accuracy']
    )
    
    # Override mastered flag (90% threshold)
    if assessment['mastery_level'] == 'mastered':
        record.mastered = True
    else:
        record.mastered = False
