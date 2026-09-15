"""
Thai Week 3 Lesson 3.4: Tone Contrast in Vocabulary
Understanding how tone changes word meaning
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_3_4() -> Lesson:
    """Create Lesson 3.4: Tone Contrast in Vocabulary."""
    lesson = Lesson(
        subject_id="thai_language",
        level=3,
        title="ความแตกต่างของเสียงวรรณยุกต์ (Tone Contrast)",
        objectives=[
            "Recognize minimal pairs differing only in tone",
            "Understand that tone changes meaning",
            "Distinguish words by tone alone",
            "Apply precise tone identification to vocabulary",
        ],
        content="Tone is lexical in Thai: same segments, different tone = different meaning. "
                "Practice distinguishing words that differ only by tone.",
        prerequisites=[],  # Requires lessons 3.1-3.3
    )
    return lesson


def load_tone_contrast_examples() -> List[Dict]:
    """
    Generate tone contrast examples.
    
    Shows pairs/sets of words with same consonants/vowels but different tones.
    """
    # Manual tone contrast examples (common minimal pairs)
    examples = [
        {
            'words': [
                {'word': 'มา', 'tone': 0, 'meaning': 'come'},
                {'word': 'หมา', 'tone': 4, 'meaning': 'dog'},
            ],
            'contrast': 'mid vs rising tone'
        },
        {
            'words': [
                {'word': 'ไก่', 'tone': 1, 'meaning': 'chicken'},
                {'word': 'ไข่', 'tone': 1, 'meaning': 'egg'},
            ],
            'contrast': 'different consonant class'
        },
        {
            'words': [
                {'word': 'ดี', 'tone': 0, 'meaning': 'good'},
            ],
            'contrast': 'single example'
        },
    ]
    
    return examples


def generate_lesson_3_4_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 3.4.
    
    Exercise types:
    1. Word + tone → meaning
    2. Tone identification
    3. Contrast recognition
    """
    examples = load_tone_contrast_examples()
    exercises = []
    
    # Type 1: Word → meaning (tone-dependent)
    for example in examples:
        for word in example['words']:
            exercise = LearningExercise(
                question=f"Meaning: {word['word']}",
                expected_answer=word['meaning'],
                verification_type="EXACT"
            )
            exercises.append(exercise)
    
    # Type 2: Word → tone
    for example in examples:
        for word in example['words']:
            exercise = LearningExercise(
                question=f"Tone number: {word['word']}",
                expected_answer=str(word['tone']),
                verification_type="EXACT"
            )
            exercises.append(exercise)
    
    return exercises


def assess_lesson_3_4_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 3.4.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'meaning_errors': [],
        'tone_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Meaning' in question:
                error_patterns['meaning_errors'].append((question, answer, exercise.expected_answer))
            elif 'Tone' in question:
                error_patterns['tone_errors'].append((question, answer, exercise.expected_answer))
    
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
    if len(error_patterns['tone_errors']) > 1:
        knowledge_gaps.append("tone contrast recognition")
    if len(error_patterns['meaning_errors']) > 1:
        knowledge_gaps.append("tone-dependent meaning")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_3_4(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 3.4 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_3_4(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 3.4 assessment.
    
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
