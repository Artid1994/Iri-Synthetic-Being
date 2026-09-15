"""
Thai Week 3 Lesson 3.6: Common Phrases
High-frequency phrases and greetings
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_3_6() -> Lesson:
    """Create Lesson 3.6: Common Phrases."""
    lesson = Lesson(
        subject_id="thai_language",
        level=3,
        title="วลีที่ใช้บ่อย (Common Phrases)",
        objectives=[
            "Read and recognize common Thai phrases",
            "Understand phrase meaning and usage",
            "Learn greetings and polite expressions",
            "Apply phonology to multi-word phrases",
        ],
        content="Common Thai phrases: สวัสดี (hello), ขอบคุณ (thank you), and other essential expressions. "
                "Practice reading phrases as complete units.",
        prerequisites=[],  # Requires lessons 3.1-3.5
    )
    return lesson


def load_common_phrases() -> List[Dict]:
    """Load common phrases from vocabulary data."""
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    vocab_file = data_dir / "vocabulary.json"
    
    vocab_data = json.loads(vocab_file.read_text(encoding='utf-8'))
    
    # Filter phrase-type vocabulary
    phrases = [
        w for w in vocab_data['vocabulary']
        if w['category'] in ['greeting', 'phrase']
    ]
    
    return phrases


def generate_lesson_3_6_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 3.6.
    
    Exercise types:
    1. Phrase → meaning
    2. Phrase → usage context
    3. Meaning → phrase
    """
    phrases = load_common_phrases()
    exercises = []
    
    # Type 1: Phrase → meaning
    for phrase in phrases:
        exercise = LearningExercise(
            question=f"Meaning: {phrase['word']}",
            expected_answer=phrase['meaning'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Category/usage
    for phrase in phrases:
        exercise = LearningExercise(
            question=f"Category: {phrase['word']}",
            expected_answer=phrase['category'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_3_6_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 3.6.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'meaning_errors': [],
        'usage_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Meaning' in question:
                error_patterns['meaning_errors'].append((question, answer, exercise.expected_answer))
            elif 'Category' in question:
                error_patterns['usage_errors'].append((question, answer, exercise.expected_answer))
    
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
        knowledge_gaps.append("phrase recognition")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_3_6(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 3.6 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_3_6(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 3.6 assessment.
    
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
