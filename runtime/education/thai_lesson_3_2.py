"""
Thai Week 3 Lesson 3.2: Two-Syllable Vocabulary
Common two-syllable words with syllable boundary awareness
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


def create_lesson_3_2() -> Lesson:
    """Create Lesson 3.2: Two-Syllable Vocabulary."""
    lesson = Lesson(
        subject_id="thai_language",
        level=3,
        title="คำสองพยางค์ (Two-Syllable Vocabulary)",
        objectives=[
            "Read and recognize two-syllable words",
            "Identify syllable boundaries in words",
            "Apply tone rules to each syllable independently",
            "Connect multi-syllable pronunciation to meaning",
        ],
        content="Common two-syllable Thai words. "
                "Learn to parse word boundaries and pronounce each syllable correctly.",
        prerequisites=[],  # Requires lesson 3.1
    )
    return lesson


def load_two_syllable_vocabulary() -> List[Dict]:
    """Load two-syllable vocabulary from validated data."""
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    vocab_file = data_dir / "vocabulary.json"
    
    vocab_data = json.loads(vocab_file.read_text(encoding='utf-8'))
    
    # Filter two-syllable words
    two_syllable_words = [
        w for w in vocab_data['vocabulary']
        if len(w['syllables']) == 2 and w['level'] == 2
    ]
    
    # Load parser
    consonants_file = data_dir / "consonants.json"
    vowels_file = data_dir / "vowel_orthography.json"
    tones_file = data_dir / "tones.json"
    
    consonant_data = json.loads(consonants_file.read_text(encoding='utf-8'))
    vowel_data = json.loads(vowels_file.read_text(encoding='utf-8'))
    tone_data = json.loads(tones_file.read_text(encoding='utf-8'))
    
    parser = ThaiSyllableParser(consonant_data, vowel_data, tone_data)
    calculator = ThaiToneCalculator(consonant_data, vowel_data, tone_data)
    ipa_renderer = ThaiIPARenderer()
    
    # Parse each word's syllables
    verified_words = []
    for word in two_syllable_words:
        syllable_ipas = []
        all_valid = True
        
        for syllable in word['syllables']:
            analysis, errors = parser.parse_syllable(syllable)
            if analysis and len(errors) == 0:
                tone = calculator.calculate_tone(analysis)
                ipa = ipa_renderer.render_ipa(analysis, tone)
                syllable_ipas.append(ipa)
            else:
                all_valid = False
                break
        
        if all_valid:
            verified_words.append({
                'word': word['word'],
                'syllables': word['syllables'],
                'syllable_ipas': syllable_ipas,
                'full_ipa': '.'.join(syllable_ipas),
                'meaning': word['meaning'],
                'category': word['category'],
            })
    
    return verified_words


def generate_lesson_3_2_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 3.2.
    
    Exercise types:
    1. Word → meaning
    2. Word → full IPA
    3. Syllable count
    4. Syllable boundary identification
    """
    words = load_two_syllable_vocabulary()
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
            expected_answer=word['full_ipa'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Syllable count
    for word in words:
        exercise = LearningExercise(
            question=f"Syllable count: {word['word']}",
            expected_answer="2",
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 4: First syllable identification
    for word in words:
        exercise = LearningExercise(
            question=f"First syllable: {word['word']}",
            expected_answer=word['syllables'][0],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_3_2_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 3.2.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'meaning_errors': [],
        'ipa_errors': [],
        'syllable_count_errors': [],
        'boundary_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Meaning' in question:
                error_patterns['meaning_errors'].append((question, answer, exercise.expected_answer))
            elif 'IPA' in question:
                error_patterns['ipa_errors'].append((question, answer, exercise.expected_answer))
            elif 'count' in question:
                error_patterns['syllable_count_errors'].append((question, answer, exercise.expected_answer))
            elif 'First syllable' in question:
                error_patterns['boundary_errors'].append((question, answer, exercise.expected_answer))
    
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
        knowledge_gaps.append("two-syllable vocabulary recognition")
    if len(error_patterns['ipa_errors']) > 2:
        knowledge_gaps.append("multi-syllable pronunciation")
    if len(error_patterns['boundary_errors']) > 2:
        knowledge_gaps.append("syllable boundary identification")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_3_2(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 3.2 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_3_2(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 3.2 assessment.
    
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
