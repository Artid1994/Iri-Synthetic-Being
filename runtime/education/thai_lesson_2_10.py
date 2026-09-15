"""
Thai Week 2 Lesson 2.10: Integrated Thai Reading
Comprehensive integration of all lessons 2.1-2.9
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


def create_lesson_2_10() -> Lesson:
    """Create Lesson 2.10: Integrated Thai Reading."""
    lesson = Lesson(
        subject_id="thai_language",
        level=2,
        title="การอ่านแบบบูรณาการ (Integrated Thai Reading)",
        objectives=[
            "Apply complete reasoning: grapheme → structure → IPA → tone",
            "Integrate all patterns: CV, CVC, clusters, marks, leading ห",
            "Explain WHY each syllable has its tone",
            "Demonstrate mastery of Thai Week 2 foundation",
        ],
        content="Integration of lessons 2.1-2.9: complete Thai syllable reading with reasoning. "
                "No new rules - applying all learned patterns together.",
        prerequisites=[],  # Requires ALL lessons 2.1-2.9
    )
    return lesson


def load_integrated_examples() -> List[Dict]:
    """
    Generate diverse examples integrating all lesson patterns.
    
    Includes:
    - Simple CV (2.3)
    - CVC with finals (2.4)
    - Live/dead contrast (2.5)
    - Tone marks (2.7)
    - Leading ห (2.8)
    - Clusters (2.9)
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
    
    # Define integrated examples
    # Format: (syllable, pattern, structure, class, live/dead, tone, reason)
    examples = [
        # Lesson 2.3: Simple CV
        ('กา', 'CV', 'CV', 'mid', 'live', 0, 'CV: mid+live'),
        ('คี', 'CV', 'CV', 'low', 'live', 0, 'CV: low+live'),
        
        # Lesson 2.4: CVC with finals
        ('กาม', 'CVC-sonorant', 'CVC', 'mid', 'live', 0, 'CVC: mid+live+sonorant'),
        ('กับ', 'CVC-stop', 'CVC', 'mid', 'dead', 1, 'CVC: mid+dead+stop'),
        
        # Lesson 2.5: Live/dead contrast
        ('กิ', 'dead-short', 'CV', 'mid', 'dead', 1, 'CV: mid+dead+short'),
        ('กิน', 'live-sonorant', 'CVC', 'mid', 'live', 0, 'CVC: mid+live+sonorant'),
        
        # Lesson 2.6: Tones (unmarked)
        ('ขา', 'high-live', 'CV', 'high', 'live', 4, 'CV: high+live'),
        
        # Lesson 2.7: Tone marks
        ('ก่า', 'marked', 'CV', 'mid', 'live', 1, 'CV: mid+mark1'),
        ('ก้า', 'marked', 'CV', 'mid', 'live', 2, 'CV: mid+mark2'),
        
        # Lesson 2.8: Leading ห
        ('หมา', 'leading-ho', 'CV', 'high', 'live', 4, 'CV: ห+ม→high+live'),
        
        # Lesson 2.9: Clusters
        ('กรา', 'cluster', 'CCV', 'mid', 'live', 0, 'Cluster: mid+live'),
        ('กริ', 'cluster', 'CCV', 'mid', 'dead', 1, 'Cluster: mid+dead'),
    ]
    
    integrated_examples = []
    
    for syllable_text, pattern, structure, cls, live_dead, expected_tone, reason in examples:
        analysis, errors = parser.parse_syllable(syllable_text)
        
        if analysis and len(errors) == 0:
            tone = calculator.calculate_tone(analysis)
            ipa = ipa_renderer.render_ipa(analysis, tone)
            
            # Verify tone matches
            if tone == expected_tone:
                integrated_examples.append({
                    'syllable': syllable_text,
                    'pattern': pattern,
                    'structure': structure,
                    'consonant_class': cls,
                    'live_dead': live_dead,
                    'tone': tone,
                    'reason': reason,
                    'ipa': ipa,
                })
    
    return integrated_examples


def generate_lesson_2_10_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 2.10.
    
    Exercise types:
    1. Structure identification (CV/CVC/CCV)
    2. Consonant class
    3. Live/dead classification
    4. Tone number
    5. IPA transcription
    6. WHY reasoning (complete chain)
    """
    examples = load_integrated_examples()
    exercises = []
    
    # Type 1: Structure
    for ex in examples:
        exercise = LearningExercise(
            question=f"Structure: {ex['syllable']}",
            expected_answer=ex['structure'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Consonant class
    for ex in examples:
        exercise = LearningExercise(
            question=f"Consonant class: {ex['syllable']}",
            expected_answer=ex['consonant_class'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Live/dead
    for ex in examples:
        exercise = LearningExercise(
            question=f"Live or dead: {ex['syllable']}",
            expected_answer=ex['live_dead'],
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
    
    # Type 5: IPA transcription
    for ex in examples:
        exercise = LearningExercise(
            question=f"IPA: {ex['syllable']}",
            expected_answer=ex['ipa'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 6: WHY reasoning (complete)
    for ex in examples[:8]:  # Subset
        # Complete reasoning: class + live/dead
        expected = f"{ex['consonant_class']}+{ex['live_dead']}"
        
        exercise = LearningExercise(
            question=f"Why tone {ex['tone']} for {ex['syllable']}?",
            expected_answer=expected,
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_2_10_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 2.10.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'structure_errors': [],
        'class_errors': [],
        'live_dead_errors': [],
        'tone_number_errors': [],
        'ipa_errors': [],
        'reasoning_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Structure' in question:
                error_patterns['structure_errors'].append((question, answer, exercise.expected_answer))
            elif 'class' in question:
                error_patterns['class_errors'].append((question, answer, exercise.expected_answer))
            elif 'Live or dead' in question:
                error_patterns['live_dead_errors'].append((question, answer, exercise.expected_answer))
            elif 'Tone number' in question:
                error_patterns['tone_number_errors'].append((question, answer, exercise.expected_answer))
            elif 'IPA' in question:
                error_patterns['ipa_errors'].append((question, answer, exercise.expected_answer))
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
    if len(error_patterns['structure_errors']) > 2:
        knowledge_gaps.append("syllable structure analysis")
    if len(error_patterns['class_errors']) > 2:
        knowledge_gaps.append("consonant class identification")
    if len(error_patterns['live_dead_errors']) > 2:
        knowledge_gaps.append("live/dead classification")
    if len(error_patterns['tone_number_errors']) > 2:
        knowledge_gaps.append("tone identification")
    if len(error_patterns['ipa_errors']) > 2:
        knowledge_gaps.append("IPA transcription")
    if len(error_patterns['reasoning_errors']) > 2:
        knowledge_gaps.append("integrated tone reasoning")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_2_10(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 2.10 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_2_10(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 2.10 assessment.
    
    Consistent 90% threshold with lessons 2.1-2.9.
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
