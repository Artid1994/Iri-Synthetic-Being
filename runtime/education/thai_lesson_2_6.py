"""
Thai Week 2 Lesson 2.6: The Five Thai Tones
Teaches tone system and tone calculation reasoning
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


# Thai tone names
TONE_NAMES_TH = {
    0: "สามัญ",    # mid
    1: "เอก",       # low
    2: "โท",        # falling
    3: "ตรี",       # high
    4: "จัตวา",     # rising
}

TONE_NAMES_EN = {
    0: "mid",
    1: "low",
    2: "falling",
    3: "high",
    4: "rising",
}


def create_lesson_2_6() -> Lesson:
    """Create Lesson 2.6: The Five Thai Tones."""
    lesson = Lesson(
        subject_id="thai_language",
        level=2,
        title="เสียงวรรณยุกต์ (The Five Thai Tones)",
        objectives=[
            "Recognize all 5 Thai tone categories",
            "Understand tone number → tone name mapping",
            "Connect consonant class + live/dead → tone",
            "Calculate tone for no-mark syllables",
        ],
        content="Thai has 5 lexical tones: mid (0), low (1), falling (2), high (3), rising (4). "
                "Tone is determined by consonant class + live/dead + tone mark.",
        prerequisites=[],  # Requires lesson 2.5
    )
    return lesson


def load_tone_examples() -> List[Dict]:
    """
    Generate examples demonstrating all 5 tones.
    
    Focus on no-mark syllables (simplest case).
    Mid-class for clearest demonstration.
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
    
    # Define examples for each tone
    # Format: (syllable, expected_tone, class, live/dead, reason)
    examples = [
        # Tone 0 (mid)
        # Mid class + live
        ('กา', 0, 'mid', 'live', 'mid class + live + no mark'),
        ('กี', 0, 'mid', 'live', 'mid class + live + no mark'),
        ('กาม', 0, 'mid', 'live', 'mid class + live + no mark'),
        # Low class + live
        ('คา', 0, 'low', 'live', 'low class + live + no mark'),
        ('คี', 0, 'low', 'live', 'low class + live + no mark'),
        ('งา', 0, 'low', 'live', 'low class + live + no mark'),
        
        # Tone 1 (low)
        # Mid class + dead
        ('กิ', 1, 'mid', 'dead', 'mid class + dead short + no mark'),
        ('กุ', 1, 'mid', 'dead', 'mid class + dead short + no mark'),
        ('กับ', 1, 'mid', 'dead', 'mid class + dead short + stop'),
        ('กิก', 1, 'mid', 'dead', 'mid class + dead short + stop'),
        # High class + dead
        ('ขิ', 1, 'high', 'dead', 'high class + dead short + no mark'),
        ('ขุ', 1, 'high', 'dead', 'high class + dead short + no mark'),
        
        # Tone 3 (high)
        # Low class + dead
        ('คิ', 3, 'low', 'dead', 'low class + dead short + no mark'),
        ('คุ', 3, 'low', 'dead', 'low class + dead short + no mark'),
        ('งิ', 3, 'low', 'dead', 'low class + dead short + no mark'),
        
        # Tone 4 (rising)
        # High class + live
        ('ขา', 4, 'high', 'live', 'high class + live + no mark'),
        ('ขี', 4, 'high', 'live', 'high class + live + no mark'),
        ('ขาม', 4, 'high', 'live', 'high class + live + no mark'),
    ]
    
    tone_examples = []
    
    for syllable_text, expected_tone, cons_class, live_dead, reason in examples:
        analysis, errors = parser.parse_syllable(syllable_text)
        
        if analysis and len(errors) == 0:
            tone = calculator.calculate_tone(analysis)
            ipa = ipa_renderer.render_ipa(analysis, tone)
            
            # Verify tone matches
            if tone == expected_tone:
                tone_examples.append({
                    'syllable': syllable_text,
                    'tone': tone,
                    'tone_name_th': TONE_NAMES_TH[tone],
                    'tone_name_en': TONE_NAMES_EN[tone],
                    'consonant_class': cons_class,
                    'live_dead': live_dead,
                    'reason': reason,
                    'ipa': ipa,
                })
    
    return tone_examples


def generate_lesson_2_6_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 2.6.
    
    Exercise types:
    1. Tone number identification
    2. Tone name (English) identification
    3. Consonant class identification
    4. Live/dead classification
    5. Reasoning: WHY this tone? (explicit)
    """
    examples = load_tone_examples()
    exercises = []
    
    # Type 1: Tone number
    for ex in examples:
        exercise = LearningExercise(
            question=f"Tone number: {ex['syllable']}",
            expected_answer=str(ex['tone']),
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Tone name (English)
    for ex in examples:
        exercise = LearningExercise(
            question=f"Tone name: {ex['syllable']}",
            expected_answer=ex['tone_name_en'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Consonant class
    for ex in examples:
        exercise = LearningExercise(
            question=f"Consonant class: {ex['syllable']}",
            expected_answer=ex['consonant_class'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 4: Live/dead
    for ex in examples:
        exercise = LearningExercise(
            question=f"Live or dead: {ex['syllable']}",
            expected_answer=ex['live_dead'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 5: WHY reasoning (new - explicit)
    # For subset of examples, require explicit reasoning
    for ex in examples[:10]:  # First 10 for manageable practice
        # Construct expected reasoning
        if ex['consonant_class'] == 'mid' and ex['live_dead'] == 'live':
            expected = "mid+live"
        elif ex['consonant_class'] == 'mid' and ex['live_dead'] == 'dead':
            expected = "mid+dead"
        elif ex['consonant_class'] == 'high' and ex['live_dead'] == 'live':
            expected = "high+live"
        elif ex['consonant_class'] == 'high' and ex['live_dead'] == 'dead':
            expected = "high+dead"
        elif ex['consonant_class'] == 'low' and ex['live_dead'] == 'live':
            expected = "low+live"
        elif ex['consonant_class'] == 'low' and ex['live_dead'] == 'dead':
            expected = "low+dead"
        else:
            expected = "unknown"
        
        exercise = LearningExercise(
            question=f"Why tone {ex['tone']} for {ex['syllable']}?",
            expected_answer=expected,
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_2_6_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 2.6.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'tone_number_errors': [],
        'tone_name_errors': [],
        'class_errors': [],
        'live_dead_errors': [],
        'reasoning_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Tone number' in question:
                error_patterns['tone_number_errors'].append((question, answer, exercise.expected_answer))
            elif 'Tone name' in question:
                error_patterns['tone_name_errors'].append((question, answer, exercise.expected_answer))
            elif 'class' in question:
                error_patterns['class_errors'].append((question, answer, exercise.expected_answer))
            elif 'Live or dead' in question:
                error_patterns['live_dead_errors'].append((question, answer, exercise.expected_answer))
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
        knowledge_gaps.append("tone number identification")
    if len(error_patterns['class_errors']) > 2:
        knowledge_gaps.append("consonant class recognition")
    if len(error_patterns['live_dead_errors']) > 2:
        knowledge_gaps.append("live/dead classification")
    if len(error_patterns['reasoning_errors']) > 2:
        knowledge_gaps.append("tone calculation reasoning")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_2_6(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 2.6 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_2_6(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 2.6 assessment.
    
    Consistent 90% threshold with lessons 2.1-2.5.
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
