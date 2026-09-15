"""
Thai Week 3 Lesson 3.3: Word Categories
Classify words by part of speech (noun/verb/adjective)
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_3_3() -> Lesson:
    """Create Lesson 3.3: Word Categories."""
    lesson = Lesson(
        subject_id="thai_language",
        level=3,
        title="ประเภทคำ (Word Categories)",
        objectives=[
            "Classify words as noun, verb, or adjective",
            "Understand basic Thai word categories",
            "Recognize category from meaning and usage",
            "Build categorical vocabulary knowledge",
        ],
        content="Thai word categories: nouns (person, thing, place), "
                "verbs (action, state), adjectives (description). "
                "Practice classifying vocabulary by category.",
        prerequisites=[],  # Requires lessons 3.1-3.2
    )
    return lesson


def load_categorized_vocabulary() -> List[Dict]:
    """Load vocabulary with category labels."""
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    vocab_file = data_dir / "vocabulary.json"
    
    vocab_data = json.loads(vocab_file.read_text(encoding='utf-8'))
    
    # Get all vocabulary with categories
    categorized_words = [
        {
            'word': w['word'],
            'meaning': w['meaning'],
            'category': w['category'],
            'syllables': len(w['syllables']),
        }
        for w in vocab_data['vocabulary']
    ]
    
    return categorized_words


def generate_lesson_3_3_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 3.3.
    
    Exercise types:
    1. Word → category
    2. Category → example words
    3. Meaning → category
    """
    words = load_categorized_vocabulary()
    exercises = []
    
    # Type 1: Word → category
    for word in words:
        exercise = LearningExercise(
            question=f"Category: {word['word']}",
            expected_answer=word['category'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Meaning → category (reasoning)
    for word in words[:15]:  # Subset
        exercise = LearningExercise(
            question=f"Category of '{word['meaning']}': {word['word']}",
            expected_answer=word['category'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_3_3_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 3.3.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'category_errors': [],
        'reasoning_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Category:' in question:
                error_patterns['category_errors'].append((question, answer, exercise.expected_answer))
            elif 'Category of' in question:
                error_patterns['reasoning_errors'].append((question, answer, exercise.expected_answer))
    
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
    if len(error_patterns['category_errors']) > 3:
        knowledge_gaps.append("word category classification")
    if len(error_patterns['reasoning_errors']) > 2:
        knowledge_gaps.append("category reasoning from meaning")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_3_3(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 3.3 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_3_3(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 3.3 assessment.
    
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
