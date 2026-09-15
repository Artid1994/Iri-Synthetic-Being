"""
Thai Week 2 Lesson 2.3: Open Syllables (CV Structure)
Combines consonants and vowels into simple open syllables
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


def create_lesson_2_3() -> Lesson:
    """Create Lesson 2.3: Open Syllables (CV)."""
    lesson = Lesson(
        subject_id="thai_language",
        level=2,
        title="พยางค์เปิด (Open Syllables: CV Structure)",
        objectives=[
            "Combine consonants and vowels into CV syllables",
            "Parse CV syllables using orthographic rules",
            "Transcribe CV syllables to IPA with tone",
        ],
        content="Simple CV syllables: consonant + vowel with no final consonant. "
                "Learn to parse Thai orthography and produce IPA transcription.",
        prerequisites=[],  # Requires lessons 2.1 and 2.2
    )
    return lesson


def load_cv_syllables() -> List[Dict]:
    """
    Generate CV syllable examples from validated data.
    
    Uses:
    - Mid-class consonants (most regular tone behavior)
    - Common vowels (า ิ ี ุ ู)
    - Parser to validate syllable structure
    """
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    
    # Load data
    consonants_file = data_dir / "consonants.json"
    vowels_file = data_dir / "vowel_orthography.json"
    tones_file = data_dir / "tones.json"
    
    consonant_data = json.loads(consonants_file.read_text(encoding='utf-8'))
    vowel_data = json.loads(vowels_file.read_text(encoding='utf-8'))
    tone_data = json.loads(tones_file.read_text(encoding='utf-8'))
    
    # Initialize parser and renderer
    parser = ThaiSyllableParser(consonant_data, vowel_data, tone_data)
    calculator = ThaiToneCalculator(consonant_data, vowel_data, tone_data)
    ipa_renderer = ThaiIPARenderer()
    
    # Select mid-class consonants (most regular)
    mid_consonants = ['ก', 'จ', 'ด', 'ต', 'บ', 'ป', 'อ']
    
    # Select common vowels
    common_vowels = ['า', 'ิ', 'ี', 'ุ', 'ู']
    
    cv_syllables = []
    
    # Generate CV combinations
    for consonant in mid_consonants:
        for vowel in common_vowels:
            # Construct syllable
            syllable = consonant + vowel
            
            # Parse to validate
            analysis, errors = parser.parse_syllable(syllable)
            
            if analysis and len(errors) == 0:
                # Calculate tone
                tone = calculator.calculate_tone(analysis)
                
                # Render IPA
                ipa = ipa_renderer.render_ipa(analysis, tone)
                
                cv_syllables.append({
                    'syllable': syllable,
                    'consonant': consonant,
                    'vowel': vowel,
                    'ipa': ipa,
                    'tone': tone,
                    'structure': 'CV',
                })
    
    return cv_syllables


def generate_lesson_2_3_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 2.3.
    
    Exercise types:
    1. Syllable → IPA transcription
    2. Structure identification (all should be CV)
    3. Tone identification
    """
    cv_syllables = load_cv_syllables()
    exercises = []
    
    # Type 1: IPA transcription (primary skill)
    for syllable in cv_syllables:
        exercise = LearningExercise(
            question=f"IPA transcription: {syllable['syllable']}",
            expected_answer=syllable['ipa'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Structure identification
    for syllable in cv_syllables:
        exercise = LearningExercise(
            question=f"Syllable structure: {syllable['syllable']}",
            expected_answer="CV",
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Tone identification
    for syllable in cv_syllables:
        exercise = LearningExercise(
            question=f"Tone number: {syllable['syllable']}",
            expected_answer=str(syllable['tone']),
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_2_3_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 2.3.
    
    Uses unified 90% threshold for mastery.
    
    Args:
        responses: List of (exercise, learner_answer) tuples
    
    Returns:
        Assessment results with mastery level and error patterns
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors by type
    error_patterns = {
        'ipa_errors': [],
        'structure_errors': [],
        'tone_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'IPA' in question:
                error_patterns['ipa_errors'].append((question, answer, exercise.expected_answer))
            elif 'structure' in question:
                error_patterns['structure_errors'].append((question, answer, exercise.expected_answer))
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
    if len(error_patterns['ipa_errors']) > 3:
        knowledge_gaps.append("CV syllable IPA transcription")
    if len(error_patterns['tone_errors']) > 3:
        knowledge_gaps.append("tone identification")
    if len(error_patterns['structure_errors']) > 2:
        knowledge_gaps.append("syllable structure recognition")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_2_3(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 2.3 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_2_3(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 2.3 assessment.
    
    Consistent 90% threshold with lessons 2.1 and 2.2.
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
