"""
Thai Week 3 Lesson 3.5: Compound Words
Understanding compound word formation in Thai
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_3_5() -> Lesson:
    """Create Lesson 3.5: Compound Words."""
    lesson = Lesson(
        subject_id="thai_language",
        level=3,
        title="คำประสม (Compound Words)",
        objectives=[
            "Recognize compound words (two meaningful parts)",
            "Understand compound formation patterns",
            "Decompose compounds into components",
            "Derive compound meaning from parts",
        ],
        content="Thai compound words combine two meaningful morphemes: ทำ+งาน (do+work=work), "
                "ครอบ+ครัว (cover+kitchen=family). Practice analyzing compound structure.",
        prerequisites=[],  # Requires lessons 3.1-3.4
    )
    return lesson


def load_compound_vocabulary() -> List[Dict]:
    """Load compound vocabulary from data."""
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    vocab_file = data_dir / "vocabulary.json"
    
    vocab_data = json.loads(vocab_file.read_text(encoding='utf-8'))
    
    # Identify compound words
    # For now, use words tagged as having meaningful component syllables
    compound_words = [
        w for w in vocab_data['vocabulary']
        if len(w['syllables']) == 2 and w['word'] in ['ทำงาน', 'หนังสือ', 'ครอบครัว', 'ขอบคุณ']
    ]
    
    # Add component meanings (manual for now)
    compound_analysis = []
    if any(w['word'] == 'ทำงาน' for w in compound_words):
        compound_analysis.append({
            'word': 'ทำงาน',
            'component1': 'ทำ',
            'meaning1': 'do',
            'component2': 'งาน',
            'meaning2': 'work',
            'full_meaning': 'work',
        })
    
    return compound_analysis


def generate_lesson_3_5_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 3.5.
    
    Exercise types:
    1. Compound → meaning
    2. Compound → first component
    3. Compound → second component
    4. Component decomposition
    """
    compounds = load_compound_vocabulary()
    exercises = []
    
    # Type 1: Compound → meaning
    for comp in compounds:
        exercise = LearningExercise(
            question=f"Meaning: {comp['word']}",
            expected_answer=comp['full_meaning'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: First component
    for comp in compounds:
        exercise = LearningExercise(
            question=f"First component: {comp['word']}",
            expected_answer=comp['component1'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Second component
    for comp in compounds:
        exercise = LearningExercise(
            question=f"Second component: {comp['word']}",
            expected_answer=comp['component2'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_3_5_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 3.5.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'meaning_errors': [],
        'component_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Meaning' in question:
                error_patterns['meaning_errors'].append((question, answer, exercise.expected_answer))
            elif 'component' in question:
                error_patterns['component_errors'].append((question, answer, exercise.expected_answer))
    
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
    if len(error_patterns['component_errors']) > 1:
        knowledge_gaps.append("compound decomposition")
    if len(error_patterns['meaning_errors']) > 1:
        knowledge_gaps.append("compound meaning")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_3_5(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 3.5 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_3_5(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 3.5 assessment.
    
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
