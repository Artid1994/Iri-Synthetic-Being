"""
Thai Week 3 Lesson 3.10: Integrated Vocabulary & Reading
Comprehensive integration of Week 3 vocabulary learning
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_3_10() -> Lesson:
    """Create Lesson 3.10: Integrated Vocabulary & Reading."""
    lesson = Lesson(
        subject_id="thai_language",
        level=3,
        title="การอ่านแบบบูรณาการ (Integrated Vocabulary Reading)",
        objectives=[
            "Demonstrate mastery of Week 3 vocabulary",
            "Apply phonology + vocabulary together",
            "Read and comprehend words and phrases",
            "Integrate pronunciation, meaning, and context",
        ],
        content="Final integration: apply Week 2 phonology + Week 3 vocabulary. "
                "Read real Thai words with accurate pronunciation and meaning.",
        prerequisites=[],  # Requires ALL lessons 3.1-3.9
    )
    return lesson


def load_integrated_vocabulary() -> List[Dict]:
    """Load comprehensive vocabulary for integration testing."""
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    vocab_file = data_dir / "vocabulary.json"
    
    vocab_data = json.loads(vocab_file.read_text(encoding='utf-8'))
    
    return vocab_data['vocabulary']


def generate_lesson_3_10_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 3.10.
    
    Exercise types:
    1. Word → meaning (comprehensive)
    2. Word → IPA (phonology integration)
    3. Word → category (linguistic analysis)
    4. Contextual comprehension
    """
    words = load_integrated_vocabulary()
    exercises = []
    
    # Type 1: Word → meaning (all vocabulary)
    for word in words:
        exercise = LearningExercise(
            question=f"Meaning: {word['word']}",
            expected_answer=word['meaning'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Word → IPA (phonology check)
    for word in words[:15]:  # Subset
        exercise = LearningExercise(
            question=f"IPA: {word['word']}",
            expected_answer=word['ipa'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Word → category
    for word in words:
        exercise = LearningExercise(
            question=f"Category: {word['word']}",
            expected_answer=word['category'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_3_10_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 3.10.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'meaning_errors': [],
        'ipa_errors': [],
        'category_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Meaning' in question:
                error_patterns['meaning_errors'].append((question, answer, exercise.expected_answer))
            elif 'IPA' in question:
                error_patterns['ipa_errors'].append((question, answer, exercise.expected_answer))
            elif 'Category' in question:
                error_patterns['category_errors'].append((question, answer, exercise.expected_answer))
    
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
    if len(error_patterns['meaning_errors']) > 3:
        knowledge_gaps.append("vocabulary recognition")
    if len(error_patterns['ipa_errors']) > 2:
        knowledge_gaps.append("phonology application")
    if len(error_patterns['category_errors']) > 2:
        knowledge_gaps.append("word classification")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_3_10(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 3.10 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_3_10(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 3.10 assessment.
    
    Consistent 90% threshold with all Week 3 lessons.
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
