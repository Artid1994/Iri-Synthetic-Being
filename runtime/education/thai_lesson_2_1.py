"""
Thai Week 2 Lesson 2.1: Consonant Pronunciation
Complete implementation with exercises and assessment
"""
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


@dataclass
class ConsonantPronunciationExercise:
    """Exercise for consonant pronunciation learning."""
    consonant: str
    ipa: str
    place: str
    manner: str
    voicing: str
    class_name: str
    question_type: str  # 'ipa', 'feature', 'class'


def create_lesson_2_1() -> Lesson:
    """Create Lesson 2.1: Consonant Pronunciation (Mid Class)."""
    lesson = Lesson(
        subject_id="thai_language",
        level=2,
        title="การออกเสียงพยัญชนะ (Consonant Pronunciation - Mid Class)",
        objectives=[
            "Transcribe mid-class consonants to IPA",
            "Identify phonological features (place, manner, voicing)",
            "Distinguish aspirated vs unaspirated consonants",
        ],
        content="Mid-class consonants: ก จ ฎ ฏ ด ต บ ป อ with IPA and phonological features",
        prerequisites=[],
    )
    return lesson


def load_mid_class_consonants() -> List[Dict]:
    """Load mid-class consonant data from validated phonology."""
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    phon_file = data_dir / "consonant_phonology.json"
    
    consonant_phon = json.loads(phon_file.read_text(encoding='utf-8'))
    
    # Filter mid-class consonants
    mid_consonants = [
        c for c in consonant_phon['consonant_phonemes']
        if c.get('class') == 'mid'
    ]
    
    return mid_consonants


def generate_lesson_2_1_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 2.1.
    
    Exercise types:
    1. IPA transcription (consonant → IPA)
    2. Feature identification (consonant → place/manner/voicing)
    3. Class verification (consonant → class)
    """
    mid_consonants = load_mid_class_consonants()
    exercises = []
    
    # Type 1: IPA transcription exercises
    for cons in mid_consonants:
        ipa_clean = cons['ipa'].strip('/')
        exercise = LearningExercise(
            question=f"IPA transcription: {cons['grapheme']}",
            expected_answer=ipa_clean,
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Place of articulation exercises
    for cons in mid_consonants:
        exercise = LearningExercise(
            question=f"Place of articulation: {cons['grapheme']}",
            expected_answer=cons['place'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Manner of articulation exercises
    for cons in mid_consonants:
        exercise = LearningExercise(
            question=f"Manner of articulation: {cons['grapheme']}",
            expected_answer=cons['manner'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 4: Voicing exercises
    for cons in mid_consonants:
        exercise = LearningExercise(
            question=f"Voicing: {cons['grapheme']}",
            expected_answer=cons['voicing'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 5: Class verification
    for cons in mid_consonants:
        exercise = LearningExercise(
            question=f"Consonant class: {cons['grapheme']}",
            expected_answer="mid",
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_2_1_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict[str, any]:
    """
    Assess mastery of Lesson 2.1.
    
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
        'place_errors': [],
        'manner_errors': [],
        'voicing_errors': [],
        'class_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'IPA' in question:
                error_patterns['ipa_errors'].append((question, answer, exercise.expected_answer))
            elif 'Place' in question:
                error_patterns['place_errors'].append((question, answer, exercise.expected_answer))
            elif 'Manner' in question:
                error_patterns['manner_errors'].append((question, answer, exercise.expected_answer))
            elif 'Voicing' in question:
                error_patterns['voicing_errors'].append((question, answer, exercise.expected_answer))
            elif 'class' in question:
                error_patterns['class_errors'].append((question, answer, exercise.expected_answer))
    
    # Determine mastery level (aligned with education system: 90% threshold)
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
    if len(error_patterns['place_errors']) > 2:
        knowledge_gaps.append("place of articulation")
    if len(error_patterns['manner_errors']) > 2:
        knowledge_gaps.append("manner of articulation")
    if len(error_patterns['voicing_errors']) > 1:
        knowledge_gaps.append("voicing distinction")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_2_1(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """
    Update KnowledgeState based on Lesson 2.1 assessment.
    
    Args:
        assessment: Assessment results from assess_lesson_2_1_mastery
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


def update_mastery_tracker_2_1(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 2.1 assessment.
    
    Aligned threshold: Only mark mastered if assessment says "mastered" (90%+).
    Overrides MasteryTracker's internal 80% auto-mastery.
    
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
    # MasteryTracker auto-marks at 80%, but we require 90% for consistency
    if assessment['mastery_level'] == 'mastered':
        record.mastered = True
    else:
        # Explicitly set to False if not mastered by assessment
        record.mastered = False
