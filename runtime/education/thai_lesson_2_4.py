"""
Thai Week 2 Lesson 2.4: Final Consonants (CVC Structure)
Teaches final consonant neutralization and CVC syllable structure
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


def create_lesson_2_4() -> Lesson:
    """Create Lesson 2.4: Final Consonants."""
    lesson = Lesson(
        subject_id="thai_language",
        level=2,
        title="พยัญชนะท้าย (Final Consonants - CVC Structure)",
        objectives=[
            "Recognize 8 phonetic final categories",
            "Understand final consonant neutralization",
            "Distinguish sonorant vs stop finals",
            "Parse and transcribe CVC syllables",
        ],
        content="Thai final consonants: 8 phonetic categories (-k, -t, -p, -m, -n, -ŋ, -j, -w). "
                "Multiple orthographic finals neutralize to same phonetic final.",
        prerequisites=[],  # Requires lesson 2.3
    )
    return lesson


def load_cvc_syllables() -> List[Dict]:
    """
    Generate CVC syllable examples from validated data.
    
    Demonstrates:
    - Final neutralization (ก ข ค → -k)
    - Sonorant finals (ม น ง ย ว)
    - Stop finals (ก จ ด ต บ ป)
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
    calculator = ThaiToneCalculator(consonant_data, vowel_data, tone_data)
    ipa_renderer = ThaiIPARenderer()
    
    # Use mid-class initials
    initials = ['ก', 'ด', 'บ']
    
    # Use common vowels
    vowels = ['า', 'ิ', 'ี']
    
    # Define finals by category
    # Sonorants: ม น ง ย ว
    # Stops: ก จ ด ต บ ป
    finals = {
        'sonorant': ['ม', 'น', 'ง', 'ย', 'ว'],
        'stop': ['ก', 'จ', 'ด', 'ต', 'บ', 'ป'],
    }
    
    cvc_syllables = []
    
    for initial in initials:
        for vowel in vowels:
            for final_type, final_list in finals.items():
                for final in final_list:
                    # Construct CVC syllable
                    syllable = initial + vowel + final
                    
                    # Parse
                    analysis, errors = parser.parse_syllable(syllable)
                    
                    if analysis and len(errors) == 0 and analysis.final_consonant:
                        # Calculate tone
                        tone = calculator.calculate_tone(analysis)
                        
                        # Render IPA
                        ipa = ipa_renderer.render_ipa(analysis, tone)
                        
                        cvc_syllables.append({
                            'syllable': syllable,
                            'initial': initial,
                            'vowel': vowel,
                            'final': final,
                            'final_type': final_type,
                            'ipa': ipa,
                            'tone': tone,
                            'structure': 'CVC',
                            'is_live': analysis.is_live,
                        })
    
    return cvc_syllables


def generate_lesson_2_4_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 2.4.
    
    Exercise types:
    1. IPA transcription
    2. Structure identification (all CVC)
    3. Final type (sonorant vs stop)
    4. Live/dead classification
    """
    cvc_syllables = load_cvc_syllables()
    exercises = []
    
    # Type 1: IPA transcription
    for syllable in cvc_syllables[:25]:  # Limit for manageable practice
        exercise = LearningExercise(
            question=f"IPA transcription: {syllable['syllable']}",
            expected_answer=syllable['ipa'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Structure identification
    for syllable in cvc_syllables[:25]:
        exercise = LearningExercise(
            question=f"Syllable structure: {syllable['syllable']}",
            expected_answer="CVC",
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Final type identification
    for syllable in cvc_syllables[:25]:
        exercise = LearningExercise(
            question=f"Final consonant type: {syllable['syllable']}",
            expected_answer=syllable['final_type'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_2_4_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 2.4.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'ipa_errors': [],
        'structure_errors': [],
        'final_type_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'IPA' in question:
                error_patterns['ipa_errors'].append((question, answer, exercise.expected_answer))
            elif 'structure' in question:
                error_patterns['structure_errors'].append((question, answer, exercise.expected_answer))
            elif 'type' in question:
                error_patterns['final_type_errors'].append((question, answer, exercise.expected_answer))
    
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
        knowledge_gaps.append("CVC syllable IPA transcription")
    if len(error_patterns['final_type_errors']) > 3:
        knowledge_gaps.append("final consonant type distinction")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_2_4(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 2.4 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_2_4(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 2.4 assessment.
    
    Consistent 90% threshold with lessons 2.1-2.3.
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
