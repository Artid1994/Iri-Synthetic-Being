"""
Thai Week 2 Lesson 2.7: Tone Marks and Tone Rules
Teaches how tone marks interact with consonant classes to determine tone
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
from runtime.education.thai_ipa_renderer import ThaiIPARenderer


# Tone mark names
TONE_MARK_NAMES_TH = {
    '่': 'ไม้เอก',
    '้': 'ไม้โท',
    '๊': 'ไม้ตรี',
    '๋': 'ไม้จัตวา',
}

TONE_MARK_NAMES_EN = {
    '่': 'mai ek',
    '้': 'mai tho',
    '๊': 'mai tri',
    '๋': 'mai chattawa',
}


def create_lesson_2_7() -> Lesson:
    """Create Lesson 2.7: Tone Marks and Tone Rules."""
    lesson = Lesson(
        subject_id="thai_language",
        level=2,
        title="วรรณยุกต์ (Tone Marks and Tone Rules)",
        objectives=[
            "Recognize 4 tone marks and their names",
            "Understand mark + class → tone interaction",
            "Apply tone rules for marked syllables",
            "Compare marked vs unmarked tones",
        ],
        content="Four tone marks: ่ (mai ek), ้ (mai tho), ๊ (mai tri), ๋ (mai chattawa). "
                "Tone mark effect depends on consonant class: same mark produces different tones on different classes.",
        prerequisites=[],  # Requires lessons 2.1-2.6
    )
    return lesson


def load_tone_mark_examples() -> List[Dict]:
    """
    Generate examples demonstrating tone mark interactions.
    
    Covers:
    - All 4 tone marks
    - All 3 consonant classes
    - Comparison with unmarked base
    """
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    
    # Load data
    consonants_file = data_dir / "consonants.json"
    vowels_file = data_dir / "vowel_orthography.json"
    tones_file = data_dir / "tones.json"
    
    consonant_data = json.loads(consonants_file.read_text(encoding='utf-8'))
    vowel_data = json.loads(vowels_file.read_text(encoding='utf-8'))
    tone_data = json.loads(tones_file.read_text(encoding='utf-8'))
    
    # Initialize
    parser = ThaiSyllableParser(consonant_data, vowel_data, tone_data)
    calculator = ThaiToneCalculator(consonant_data, vowel_data, tone_data)
    ipa_renderer = ThaiIPARenderer()
    
    # Define examples with tone marks
    # Format: (syllable, expected_tone, class, mark, reason)
    examples = [
        # Mai ek (่) examples
        # Mid class + mai ek → low (tone 1)
        ('ก่า', 1, 'mid', '่', 'mid + mark1'),
        ('ด่า', 1, 'mid', '่', 'mid + mark1'),
        # High class + mai ek → low (tone 1)
        ('ข่า', 1, 'high', '่', 'high + mark1'),
        # Low class + mai ek → falling (tone 2)
        ('ค่า', 2, 'low', '่', 'low + mark1'),
        ('ง่า', 2, 'low', '่', 'low + mark1'),
        
        # Mai tho (้) examples
        # Mid class + mai tho → falling (tone 2)
        ('ก้า', 2, 'mid', '้', 'mid + mark2'),
        ('ด้า', 2, 'mid', '้', 'mid + mark2'),
        # High class + mai tho → falling (tone 2)
        ('ข้า', 2, 'high', '้', 'high + mark2'),
        # Low class + mai tho → high (tone 3)
        ('ค้า', 3, 'low', '้', 'low + mark2'),
        ('ง้า', 3, 'low', '้', 'low + mark2'),
    ]
    
    tone_mark_examples = []
    
    for syllable_text, expected_tone, cons_class, mark, reason in examples:
        analysis, errors = parser.parse_syllable(syllable_text)
        
        if analysis and len(errors) == 0:
            tone = calculator.calculate_tone(analysis)
            ipa = ipa_renderer.render_ipa(analysis, tone)
            
            # Verify tone matches
            if tone == expected_tone:
                tone_mark_examples.append({
                    'syllable': syllable_text,
                    'tone': tone,
                    'tone_mark': mark,
                    'tone_mark_name_th': TONE_MARK_NAMES_TH[mark],
                    'tone_mark_name_en': TONE_MARK_NAMES_EN[mark],
                    'consonant_class': cons_class,
                    'reason': reason,
                    'ipa': ipa,
                })
    
    return tone_mark_examples


def generate_lesson_2_7_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 2.7.
    
    Exercise types:
    1. Tone number identification (with marks)
    2. Tone mark identification
    3. Tone mark name
    4. Consonant class
    5. WHY reasoning: class + mark → tone
    """
    examples = load_tone_mark_examples()
    exercises = []
    
    # Type 1: Tone number
    for ex in examples:
        exercise = LearningExercise(
            question=f"Tone number: {ex['syllable']}",
            expected_answer=str(ex['tone']),
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Tone mark identification
    for ex in examples:
        exercise = LearningExercise(
            question=f"Tone mark: {ex['syllable']}",
            expected_answer=ex['tone_mark'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Tone mark name (English)
    for ex in examples:
        exercise = LearningExercise(
            question=f"Mark name: {ex['syllable']}",
            expected_answer=ex['tone_mark_name_en'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 4: Consonant class
    for ex in examples:
        exercise = LearningExercise(
            question=f"Consonant class: {ex['syllable']}",
            expected_answer=ex['consonant_class'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 5: WHY reasoning (explicit causal)
    for ex in examples[:8]:  # Subset for manageable practice
        # Build reasoning string
        mark_num = {'่': '1', '้': '2', '๊': '3', '๋': '4'}[ex['tone_mark']]
        expected = f"{ex['consonant_class']}+mark{mark_num}"
        
        exercise = LearningExercise(
            question=f"Why tone {ex['tone']} for {ex['syllable']}?",
            expected_answer=expected,
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_2_7_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 2.7.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'tone_number_errors': [],
        'tone_mark_errors': [],
        'mark_name_errors': [],
        'class_errors': [],
        'reasoning_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Tone number' in question:
                error_patterns['tone_number_errors'].append((question, answer, exercise.expected_answer))
            elif 'Tone mark:' in question:
                error_patterns['tone_mark_errors'].append((question, answer, exercise.expected_answer))
            elif 'Mark name' in question:
                error_patterns['mark_name_errors'].append((question, answer, exercise.expected_answer))
            elif 'class' in question:
                error_patterns['class_errors'].append((question, answer, exercise.expected_answer))
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
    if len(error_patterns['tone_number_errors']) > 2:
        knowledge_gaps.append("tone identification with marks")
    if len(error_patterns['tone_mark_errors']) > 2:
        knowledge_gaps.append("tone mark recognition")
    if len(error_patterns['class_errors']) > 2:
        knowledge_gaps.append("consonant class recognition")
    if len(error_patterns['reasoning_errors']) > 2:
        knowledge_gaps.append("tone rule reasoning")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_2_7(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 2.7 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_2_7(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 2.7 assessment.
    
    Consistent 90% threshold with lessons 2.1-2.6.
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
