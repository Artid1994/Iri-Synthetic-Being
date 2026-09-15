"""
Thai Week 2 Lesson 2.8: Leading ห and อ
Teaches how leading ห/อ modifies effective consonant class
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


def create_lesson_2_8() -> Lesson:
    """Create Lesson 2.8: Leading ห and อ."""
    lesson = Lesson(
        subject_id="thai_language",
        level=2,
        title="ห นำ / อ นำ (Leading ห and อ)",
        objectives=[
            "Recognize leading ห and อ consonants",
            "Understand effective class modification",
            "Calculate tone using effective class",
            "Distinguish original vs effective class",
        ],
        content="Leading ห (and อ) are silent consonants that modify the effective class "
                "of following sonorant consonants to high class, affecting tone calculation.",
        prerequisites=[],  # Requires lessons 2.1-2.7
    )
    return lesson


def load_leading_ho_examples() -> List[Dict]:
    """
    Generate examples demonstrating leading ห and อ.
    
    Leading ห + sonorant → effective high class
    (อ นำ is less common, focusing on ห นำ)
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
    
    # Define examples with leading ห
    # Format: (syllable, leading, main, original_class, effective_class, expected_tone, reason)
    examples = [
        # Leading ห + sonorant consonants
        # ห + ม → high class behavior
        ('หมา', 'ห', 'ม', 'low', 'high', 4, 'ห+ม → high+live'),
        ('หมี', 'ห', 'ม', 'low', 'high', 4, 'ห+ม → high+live'),
        
        # ห + น → high class behavior
        ('หนา', 'ห', 'น', 'low', 'high', 4, 'ห+น → high+live'),
        ('หนี', 'ห', 'น', 'low', 'high', 4, 'ห+น → high+live'),
        
        # ห + ง → high class behavior
        ('หงา', 'ห', 'ง', 'low', 'high', 4, 'ห+ง → high+live'),
        
        # ห + ย → high class behavior
        ('หยา', 'ห', 'ย', 'low', 'high', 4, 'ห+ย → high+live'),
        
        # ห + ว → high class behavior
        ('หวา', 'ห', 'ว', 'low', 'high', 4, 'ห+ว → high+live'),
        
        # ห + ล → high class behavior
        ('หลา', 'ห', 'ล', 'low', 'high', 4, 'ห+ล → high+live'),
    ]
    
    leading_examples = []
    
    for syllable_text, leading, main, orig_class, eff_class, expected_tone, reason in examples:
        analysis, errors = parser.parse_syllable(syllable_text)
        
        if analysis and len(errors) == 0:
            tone = calculator.calculate_tone(analysis)
            ipa = ipa_renderer.render_ipa(analysis, tone)
            
            # Verify tone matches
            if tone == expected_tone:
                leading_examples.append({
                    'syllable': syllable_text,
                    'leading_consonant': leading,
                    'main_consonant': main,
                    'original_class': orig_class,
                    'effective_class': eff_class,
                    'tone': tone,
                    'reason': reason,
                    'ipa': ipa,
                    'is_live': analysis.is_live,
                })
    
    return leading_examples


def generate_lesson_2_8_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 2.8.
    
    Exercise types:
    1. Leading consonant identification
    2. Main consonant identification
    3. Effective class determination
    4. Tone number
    5. WHY reasoning: leading + main → effective class → tone
    """
    examples = load_leading_ho_examples()
    exercises = []
    
    # Type 1: Leading consonant identification
    for ex in examples:
        exercise = LearningExercise(
            question=f"Leading consonant: {ex['syllable']}",
            expected_answer=ex['leading_consonant'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Main consonant identification
    for ex in examples:
        exercise = LearningExercise(
            question=f"Main consonant: {ex['syllable']}",
            expected_answer=ex['main_consonant'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Effective class
    for ex in examples:
        exercise = LearningExercise(
            question=f"Effective class: {ex['syllable']}",
            expected_answer=ex['effective_class'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 4: Tone number
    for ex in examples:
        exercise = LearningExercise(
            question=f"Tone number: {ex['syllable']}",
            expected_answer=str(ex['tone']),
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 5: WHY reasoning
    for ex in examples[:6]:  # Subset for manageable practice
        # Reasoning: effective class + live/dead → tone
        live_dead = 'live' if ex['is_live'] else 'dead'
        expected = f"{ex['effective_class']}+{live_dead}"
        
        exercise = LearningExercise(
            question=f"Why tone {ex['tone']} for {ex['syllable']}?",
            expected_answer=expected,
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_2_8_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 2.8.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'leading_errors': [],
        'main_consonant_errors': [],
        'effective_class_errors': [],
        'tone_number_errors': [],
        'reasoning_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Leading consonant' in question:
                error_patterns['leading_errors'].append((question, answer, exercise.expected_answer))
            elif 'Main consonant' in question:
                error_patterns['main_consonant_errors'].append((question, answer, exercise.expected_answer))
            elif 'Effective class' in question:
                error_patterns['effective_class_errors'].append((question, answer, exercise.expected_answer))
            elif 'Tone number' in question:
                error_patterns['tone_number_errors'].append((question, answer, exercise.expected_answer))
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
    if len(error_patterns['effective_class_errors']) > 2:
        knowledge_gaps.append("effective class calculation")
    if len(error_patterns['tone_number_errors']) > 2:
        knowledge_gaps.append("tone with leading consonants")
    if len(error_patterns['reasoning_errors']) > 2:
        knowledge_gaps.append("leading consonant reasoning")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_2_8(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 2.8 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_2_8(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 2.8 assessment.
    
    Consistent 90% threshold with lessons 2.1-2.7.
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
