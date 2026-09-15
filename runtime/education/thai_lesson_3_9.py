"""
Thai Week 3 Lesson 3.9: Reading Fluency Practice
Develop automatic word recognition and fluency
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_3_9() -> Lesson:
    """Create Lesson 3.9: Reading Fluency Practice."""
    lesson = Lesson(
        subject_id="thai_language",
        level=3,
        title="การอ่านคล่อง (Reading Fluency)",
        objectives=[
            "Develop automatic word recognition",
            "Read vocabulary without conscious decoding",
            "Increase reading speed and confidence",
            "Consolidate Week 3 vocabulary knowledge",
        ],
        content="Practice rapid recognition of learned vocabulary. "
                "Build fluency through repeated exposure and automatic retrieval.",
        prerequisites=[],  # Requires lessons 3.1-3.8
    )
    return lesson


def load_fluency_vocabulary() -> List[Dict]:
    """Load all Week 3 vocabulary for fluency practice."""
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    vocab_file = data_dir / "vocabulary.json"
    
    vocab_data = json.loads(vocab_file.read_text(encoding='utf-8'))
    
    # Get all vocabulary items
    all_vocab = vocab_data['vocabulary']
    
    return all_vocab


def generate_lesson_3_9_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 3.9.
    
    Exercise types:
    1. Rapid word → meaning
    2. Mixed vocabulary recall
    """
    words = load_fluency_vocabulary()
    exercises = []
    
    # Type 1: Rapid recognition (all words)
    for word in words:
        exercise = LearningExercise(
            question=f"Meaning: {word['word']}",
            expected_answer=word['meaning'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_3_9_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 3.9.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'recognition_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            error_patterns['recognition_errors'].append((question, answer, exercise.expected_answer))
    
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
    if len(error_patterns['recognition_errors']) > 3:
        knowledge_gaps.append("automatic vocabulary recognition")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_3_9(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 3.9 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_3_9(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 3.9 assessment.
    
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
