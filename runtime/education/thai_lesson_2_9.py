"""
Thai Week 2 Lesson 2.9: Initial Consonant Clusters
Teaches consonant clusters (C1+C2) and their phonological behavior
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


def create_lesson_2_9() -> Lesson:
    """Create Lesson 2.9: Initial Consonant Clusters."""
    lesson = Lesson(
        subject_id="thai_language",
        level=2,
        title="กลุ่มพยัญชนะต้น (Initial Consonant Clusters)",
        objectives=[
            "Recognize initial consonant clusters C1+C2",
            "Identify C1 (first) and C2 (second) consonants",
            "Understand cluster phonology and IPA",
            "Apply tone rules using C1 class",
        ],
        content="Thai initial consonant clusters: C1 (stop/fricative) + C2 (liquid/glide). "
                "C1 determines consonant class for tone. Common: กร คร ปร ตร พล ขว กล etc.",
        prerequisites=[],  # Requires lessons 2.1-2.8
    )
    return lesson


def load_cluster_examples() -> List[Dict]:
    """
    Generate examples demonstrating initial consonant clusters.
    
    Thai clusters: typically stop + liquid/glide
    C1 + C2 where:
    - C1: ก ข ค จ ต ป พ ฟ etc. (stops/fricatives)
    - C2: ร ล ว (liquids/glides)
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
    
    # Define cluster examples
    # Format: (syllable, c1, c2, c1_class, expected_tone, reason)
    examples = [
        # กร cluster (ก + ร)
        ('กรา', 'ก', 'ร', 'mid', 0, 'mid+live cluster'),
        ('กริ', 'ก', 'ร', 'mid', 1, 'mid+dead cluster'),
        
        # คร cluster (ค + ร)
        ('ครา', 'ค', 'ร', 'low', 0, 'low+live cluster'),
        
        # ขร cluster (ข + ร)
        ('ขรา', 'ข', 'ร', 'high', 4, 'high+live cluster'),
        
        # ปร cluster (ป + ร)
        ('ปรา', 'ป', 'ร', 'mid', 0, 'mid+live cluster'),
        
        # ตร cluster (ต + ร)
        ('ตรา', 'ต', 'ร', 'mid', 0, 'mid+live cluster'),
        
        # กล cluster (ก + ล)
        ('กลา', 'ก', 'ล', 'mid', 0, 'mid+live cluster'),
        
        # คล cluster (ค + ล)
        ('คลา', 'ค', 'ล', 'low', 0, 'low+live cluster'),
        
        # ขว cluster (ข + ว)
        ('ขวา', 'ข', 'ว', 'high', 4, 'high+live cluster'),
        
        # กว cluster (ก + ว)
        ('กวา', 'ก', 'ว', 'mid', 0, 'mid+live cluster'),
    ]
    
    cluster_examples = []
    
    for syllable_text, c1, c2, c1_class, expected_tone, reason in examples:
        analysis, errors = parser.parse_syllable(syllable_text)
        
        if analysis and len(errors) == 0:
            # Check if it's a cluster: syllable starts with C1+C2 pattern
            # Clusters have initial consonant that is 2 characters long
            is_cluster = len(c1 + c2) == 2 and syllable_text.startswith(c1 + c2)
            
            if is_cluster:
                tone = calculator.calculate_tone(analysis)
                ipa = ipa_renderer.render_ipa(analysis, tone)
            if is_cluster:
                tone = calculator.calculate_tone(analysis)
                ipa = ipa_renderer.render_ipa(analysis, tone)
                
                # Verify tone matches
                if tone == expected_tone:
                    cluster_examples.append({
                        'syllable': syllable_text,
                        'c1': c1,
                        'c2': c2,
                        'c1_class': c1_class,
                        'cluster': c1 + c2,
                        'tone': tone,
                        'reason': reason,
                        'ipa': ipa,
                        'is_live': analysis.is_live,
                    })
    
    return cluster_examples


def generate_lesson_2_9_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 2.9.
    
    Exercise types:
    1. C1 identification
    2. C2 identification
    3. C1 class identification
    4. Tone number
    5. WHY reasoning: C1 class + live/dead → tone
    """
    examples = load_cluster_examples()
    exercises = []
    
    # Type 1: C1 identification
    for ex in examples:
        exercise = LearningExercise(
            question=f"First consonant (C1): {ex['syllable']}",
            expected_answer=ex['c1'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: C2 identification
    for ex in examples:
        exercise = LearningExercise(
            question=f"Second consonant (C2): {ex['syllable']}",
            expected_answer=ex['c2'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: C1 class (determines tone)
    for ex in examples:
        exercise = LearningExercise(
            question=f"C1 class: {ex['syllable']}",
            expected_answer=ex['c1_class'],
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
    for ex in examples[:6]:  # Subset
        live_dead = 'live' if ex['is_live'] else 'dead'
        expected = f"{ex['c1_class']}+{live_dead}"
        
        exercise = LearningExercise(
            question=f"Why tone {ex['tone']} for {ex['syllable']}?",
            expected_answer=expected,
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_2_9_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 2.9.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'c1_errors': [],
        'c2_errors': [],
        'c1_class_errors': [],
        'tone_number_errors': [],
        'reasoning_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'First consonant' in question:
                error_patterns['c1_errors'].append((question, answer, exercise.expected_answer))
            elif 'Second consonant' in question:
                error_patterns['c2_errors'].append((question, answer, exercise.expected_answer))
            elif 'C1 class' in question:
                error_patterns['c1_class_errors'].append((question, answer, exercise.expected_answer))
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
    if len(error_patterns['c1_errors']) > 2:
        knowledge_gaps.append("cluster C1 identification")
    if len(error_patterns['c1_class_errors']) > 2:
        knowledge_gaps.append("C1 class determination")
    if len(error_patterns['tone_number_errors']) > 2:
        knowledge_gaps.append("tone with clusters")
    if len(error_patterns['reasoning_errors']) > 2:
        knowledge_gaps.append("cluster tone reasoning")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_2_9(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 2.9 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_2_9(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 2.9 assessment.
    
    Consistent 90% threshold with lessons 2.1-2.8.
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
