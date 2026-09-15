"""
Thai Week 2 Lesson 2.5: Live vs Dead Syllables
Teaches syllable classification rules for tone system
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker
from runtime.education.thai_syllable_parser import ThaiSyllableParser
from runtime.education.thai_tone_calculator import ThaiToneCalculator


def create_lesson_2_5() -> Lesson:
    """Create Lesson 2.5: Live vs Dead Syllables."""
    lesson = Lesson(
        subject_id="thai_language",
        level=2,
        title="พยางค์เป็น-ตาย (Live vs Dead Syllables)",
        objectives=[
            "Classify syllables as live or dead",
            "Apply live/dead rules: long vowel OR sonorant = live",
            "Understand vowel length effect on classification",
            "Recognize open dead syllables (short/no final)",
        ],
        content="Live/dead classification is fundamental to Thai tone rules. "
                "Live: long vowel OR sonorant final. Dead: short vowel + stop final OR short vowel alone.",
        prerequisites=[],  # Requires lessons 2.2-2.4
    )
    return lesson


def load_live_dead_syllables() -> List[Dict]:
    """
    Generate balanced syllable examples demonstrating all live/dead patterns.
    
    Patterns:
    1. Live: long vowel, no final (กา)
    2. Live: long vowel + any final (กาม, กาก)
    3. Live: short vowel + sonorant final (กิน)
    4. Dead: short vowel + stop final (กับ)
    5. Dead: short vowel, no final (กะ)
    """
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    
    # Load data
    consonants_file = data_dir / "consonants.json"
    vowels_file = data_dir / "vowel_orthography.json"
    tones_file = data_dir / "tones.json"
    
    consonant_data = json.loads(consonants_file.read_text(encoding='utf-8'))
    vowel_data = json.loads(vowels_file.read_text(encoding='utf-8'))
    tone_data = json.loads(tones_file.read_text(encoding='utf-8'))
    
    # Initialize parser
    parser = ThaiSyllableParser(consonant_data, vowel_data, tone_data)
    
    # Define examples for each pattern
    # Using mid-class ก for consistency
    examples = [
        # Pattern 1: Live - long vowel, no final
        ('กา', 'live', 'long vowel, no final'),
        ('กี', 'live', 'long vowel, no final'),
        ('กู', 'live', 'long vowel, no final'),
        
        # Pattern 2: Live - long vowel + any final
        ('กาม', 'live', 'long vowel + final'),
        ('กาน', 'live', 'long vowel + final'),
        ('กาก', 'live', 'long vowel + stop'),
        ('กาด', 'live', 'long vowel + stop'),
        ('กีบ', 'live', 'long vowel + stop'),
        
        # Pattern 3: Live - short vowel + sonorant
        ('กิน', 'live', 'short vowel + sonorant'),
        ('กุม', 'live', 'short vowel + sonorant'),
        ('กุง', 'live', 'short vowel + sonorant'),
        ('กิว', 'live', 'short vowel + sonorant'),
        
        # Pattern 4: Dead - short vowel + stop
        ('กับ', 'dead', 'short vowel + stop'),
        ('กิก', 'dead', 'short vowel + stop'),
        ('กิด', 'dead', 'short vowel + stop'),
        ('กุต', 'dead', 'short vowel + stop'),
        ('กุบ', 'dead', 'short vowel + stop'),
        
        # Pattern 5: Dead - short vowel, no final
        ('กะ', 'dead', 'short vowel, no final'),
        ('กิ', 'dead', 'short vowel, no final'),
        ('กุ', 'dead', 'short vowel, no final'),
    ]
    
    syllables = []
    
    for syllable_text, expected_class, reason in examples:
        analysis, errors = parser.parse_syllable(syllable_text)
        
        if analysis and len(errors) == 0:
            # Verify parser agrees
            actual_class = 'live' if analysis.is_live else 'dead'
            
            syllables.append({
                'syllable': syllable_text,
                'classification': expected_class,
                'reason': reason,
                'parser_agrees': (actual_class == expected_class),
                'vowel_length': analysis.vowel_length,
                'final': analysis.final_consonant if analysis.final_consonant else 'none',
            })
    
    return syllables


def generate_lesson_2_5_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 2.5.
    
    Exercise types:
    1. Classification (live/dead)
    2. Reason identification (why is it live/dead)
    3. Vowel length identification
    4. Final type effect
    """
    syllables = load_live_dead_syllables()
    exercises = []
    
    # Type 1: Classification
    for syll in syllables:
        exercise = LearningExercise(
            question=f"Classify syllable: {syll['syllable']}",
            expected_answer=syll['classification'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Vowel length (essential for classification)
    for syll in syllables:
        exercise = LearningExercise(
            question=f"Vowel length: {syll['syllable']}",
            expected_answer=syll['vowel_length'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Reasoning - why live?
    # For live syllables, test understanding
    live_syllables = [s for s in syllables if s['classification'] == 'live']
    for syll in live_syllables[:10]:  # Subset for manageable practice
        if 'long' in syll['reason']:
            exercise = LearningExercise(
                question=f"Why is {syll['syllable']} LIVE?",
                expected_answer="long vowel",
                verification_type="EXACT"
            )
            exercises.append(exercise)
        elif 'sonorant' in syll['reason']:
            exercise = LearningExercise(
                question=f"Why is {syll['syllable']} LIVE?",
                expected_answer="sonorant final",
                verification_type="EXACT"
            )
            exercises.append(exercise)
    
    return exercises


def assess_lesson_2_5_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 2.5.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'classification_errors': [],
        'vowel_length_errors': [],
        'reasoning_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Classify' in question:
                error_patterns['classification_errors'].append((question, answer, exercise.expected_answer))
            elif 'length' in question:
                error_patterns['vowel_length_errors'].append((question, answer, exercise.expected_answer))
            elif 'Why' in question:
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
    if len(error_patterns['classification_errors']) > 3:
        knowledge_gaps.append("live/dead classification")
    if len(error_patterns['vowel_length_errors']) > 2:
        knowledge_gaps.append("vowel length recognition")
    if len(error_patterns['reasoning_errors']) > 2:
        knowledge_gaps.append("classification reasoning")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_2_5(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 2.5 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_2_5(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 2.5 assessment.
    
    Consistent 90% threshold with lessons 2.1-2.4.
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
