"""
Thai Week 3 Lesson 3.1: Single-Syllable Vocabulary
First vocabulary lesson: common single-syllable words with meaning
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


def create_lesson_3_1() -> Lesson:
    """Create Lesson 3.1: Single-Syllable Vocabulary."""
    lesson = Lesson(
        subject_id="thai_language",
        level=3,
        title="คำพยางค์เดียว (Single-Syllable Vocabulary)",
        objectives=[
            "Read and recognize 10+ single-syllable words",
            "Connect orthography → pronunciation → meaning",
            "Distinguish words by tone contrast",
            "Apply Week 2 phonology to real vocabulary",
        ],
        content="Common single-syllable Thai words with pronunciation and meaning. "
                "Practice reading real vocabulary with correct tone.",
        prerequisites=[],  # Requires Week 2 completion
    )
    return lesson


def load_single_syllable_vocabulary() -> List[Dict]:
    """
    Load single-syllable vocabulary from validated data.
    
    Returns words with:
    - Thai orthography
    - IPA pronunciation
    - English meaning
    - Category (noun/verb/adjective)
    """
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    vocab_file = data_dir / "vocabulary.json"
    
    vocab_data = json.loads(vocab_file.read_text(encoding='utf-8'))
    
    # Filter single-syllable words
    single_syllable_words = [
        w for w in vocab_data['vocabulary']
        if len(w['syllables']) == 1 and w['level'] == 1
    ]
    
    # Load parser for verification
    consonants_file = data_dir / "consonants.json"
    vowels_file = data_dir / "vowel_orthography.json"
    tones_file = data_dir / "tones.json"
    
    consonant_data = json.loads(consonants_file.read_text(encoding='utf-8'))
    vowel_data = json.loads(vowels_file.read_text(encoding='utf-8'))
    tone_data = json.loads(tones_file.read_text(encoding='utf-8'))
    
    parser = ThaiSyllableParser(consonant_data, vowel_data, tone_data)
    calculator = ThaiToneCalculator(consonant_data, vowel_data, tone_data)
    ipa_renderer = ThaiIPARenderer()
    
    # Verify each word can be parsed
    verified_words = []
    for word in single_syllable_words:
        analysis, errors = parser.parse_syllable(word['word'])
        if analysis and len(errors) == 0:
            tone = calculator.calculate_tone(analysis)
            ipa = ipa_renderer.render_ipa(analysis, tone)
            
            verified_words.append({
                'word': word['word'],
                'ipa': ipa,
                'meaning': word['meaning'],
                'category': word['category'],
                'tone': tone,
                'frequency': word['frequency'],
            })
    
    return verified_words


def generate_lesson_3_1_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 3.1.
    
    Exercise types:
    1. Word → meaning (recognition)
    2. Word → IPA (pronunciation)
    3. Meaning → word (production)
    4. Tone identification
    """
    words = load_single_syllable_vocabulary()
    exercises = []
    
    # Type 1: Word → meaning
    for word in words:
        exercise = LearningExercise(
            question=f"Meaning: {word['word']}",
            expected_answer=word['meaning'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Word → IPA
    for word in words:
        exercise = LearningExercise(
            question=f"IPA: {word['word']}",
            expected_answer=word['ipa'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Tone identification
    for word in words:
        exercise = LearningExercise(
            question=f"Tone number: {word['word']}",
            expected_answer=str(word['tone']),
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 4: Category identification
    for word in words:
        exercise = LearningExercise(
            question=f"Category: {word['word']}",
            expected_answer=word['category'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_3_1_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 3.1.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'meaning_errors': [],
        'ipa_errors': [],
        'tone_errors': [],
        'category_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Meaning' in question:
                error_patterns['meaning_errors'].append((question, answer, exercise.expected_answer))
            elif 'IPA' in question:
                error_patterns['ipa_errors'].append((question, answer, exercise.expected_answer))
            elif 'Tone' in question:
                error_patterns['tone_errors'].append((question, answer, exercise.expected_answer))
            elif 'Category' in question:
                error_patterns['category_errors'].append((question, answer, exercise.expected_answer))
    
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
    if len(error_patterns['meaning_errors']) > 2:
        knowledge_gaps.append("vocabulary recognition")
    if len(error_patterns['ipa_errors']) > 2:
        knowledge_gaps.append("word pronunciation")
    if len(error_patterns['tone_errors']) > 2:
        knowledge_gaps.append("tone in vocabulary")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_3_1(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 3.1 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_3_1(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 3.1 assessment.
    
    Consistent 90% threshold with Week 2.
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
