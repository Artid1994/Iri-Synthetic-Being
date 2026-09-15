"""
Thai Week 2 Lesson 2.2: Vowel Pronunciation
Complete implementation with exercises and assessment
"""
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_2_2() -> Lesson:
    """Create Lesson 2.2: Vowel Pronunciation."""
    lesson = Lesson(
        subject_id="thai_language",
        level=2,
        title="การออกเสียงสระ (Vowel Pronunciation)",
        objectives=[
            "Transcribe Thai vowels to IPA",
            "Distinguish short vs long vowels",
            "Recognize vowel position (leading, above, below, trailing)",
        ],
        content="Thai vowel system: 9 short + 9 long vowels with IPA transcription and length distinction",
        prerequisites=[],  # Requires lesson 2.1
    )
    return lesson


def load_core_vowels() -> List[Dict]:
    """Load core Thai vowel phonemes from validated data."""
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    
    # Load vowel phonology
    phon_file = data_dir / "vowel_phonology.json"
    vowel_phon = json.loads(phon_file.read_text(encoding='utf-8'))
    
    # Load vowel orthography
    orth_file = data_dir / "vowel_orthography.json"
    vowel_orth = json.loads(orth_file.read_text(encoding='utf-8'))
    
    # Build vowel list with phonology + orthography
    vowels = []
    for phon in vowel_phon['vowel_phonemes']:
        # Skip diphthongs for lesson 2.2 (focus on monophthongs)
        if phon.get('type') == 'diphthong':
            continue
        
        # Get first orthographic representation
        if phon['orthography']:
            ortho = phon['orthography'][0]
            
            vowels.append({
                'orthography': ortho,
                'ipa': phon['ipa'].strip('/'),
                'length': phon['length'],
                'height': phon.get('height', 'unknown'),
                'backness': phon.get('backness', 'unknown'),
            })
    
    return vowels


def generate_lesson_2_2_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 2.2.
    
    Exercise types:
    1. IPA transcription (vowel → IPA)
    2. Length identification (vowel → short/long)
    3. Orthography identification (IPA → orthography)
    """
    vowels = load_core_vowels()
    exercises = []
    
    # Type 1: IPA transcription
    for vowel in vowels:
        exercise = LearningExercise(
            question=f"IPA transcription: {vowel['orthography']}",
            expected_answer=vowel['ipa'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Length identification
    for vowel in vowels:
        exercise = LearningExercise(
            question=f"Vowel length: {vowel['orthography']}",
            expected_answer=vowel['length'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Height identification
    for vowel in vowels:
        if vowel['height'] != 'unknown':
            exercise = LearningExercise(
                question=f"Vowel height: {vowel['orthography']}",
                expected_answer=vowel['height'],
                verification_type="EXACT"
            )
            exercises.append(exercise)
    
    return exercises


def assess_lesson_2_2_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 2.2.
    
    Uses unified 90% threshold for mastery (consistent with lesson 2.1).
    
    Args:
        responses: List of (exercise, learner_answer) tuples
    
    Returns:
        Assessment results with mastery level, error patterns, and knowledge gaps
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors by type
    error_patterns = {
        'ipa_errors': [],
        'length_errors': [],
        'height_errors': [],
        'general_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'IPA' in question:
                error_patterns['ipa_errors'].append((question, answer, exercise.expected_answer))
            elif 'length' in question:
                error_patterns['length_errors'].append((question, answer, exercise.expected_answer))
            elif 'height' in question:
                error_patterns['height_errors'].append((question, answer, exercise.expected_answer))
            else:
                error_patterns['general_errors'].append((question, answer, exercise.expected_answer))
    
    # Determine mastery level (aligned with lesson 2.1: 90% threshold)
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
    if len(error_patterns['ipa_errors']) > 2:
        knowledge_gaps.append("IPA transcription")
    if len(error_patterns['length_errors']) > 2:
        knowledge_gaps.append("short/long distinction")
    if len(error_patterns['height_errors']) > 2:
        knowledge_gaps.append("vowel height")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_2_2(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """
    Update KnowledgeState based on Lesson 2.2 assessment.
    
    Args:
        assessment: Assessment results from assess_lesson_2_2_mastery
        knowledge_state: KnowledgeState instance to update
    """
    # Record correct/incorrect based on assessment
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        # Classify error type based on gaps
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_2_2(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 2.2 assessment.
    
    Aligned threshold: Only mark mastered if assessment says "mastered" (90%+).
    Consistent with lesson 2.1 mastery rules.
    
    Args:
        assessment: Assessment results
        mastery_tracker: MasteryTracker instance
        lesson_id: Lesson identifier
    """
    # Record attempt with score
    record = mastery_tracker.record_attempt(
        lesson_id=lesson_id,
        score=assessment['accuracy']
    )
    
    # Override mastered flag based on assessment (90% threshold)
    if assessment['mastery_level'] == 'mastered':
        record.mastered = True
    else:
        record.mastered = False
