"""
Thai Week 4 Lesson 4.1: Basic Sentence Structure
Introduction to Thai sentence patterns: Subject-Verb-Object
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_4_1() -> Lesson:
    """Create Lesson 4.1: Basic Sentence Structure."""
    lesson = Lesson(
        subject_id="thai_language",
        level=4,
        title="โครงสร้างประโยคพื้นฐาน (Basic Sentence Structure)",
        objectives=[
            "Recognize Subject-Verb-Object (SVO) word order",
            "Identify subject, verb, and object in simple sentences",
            "Understand Thai word order patterns",
            "Read and comprehend basic sentences",
        ],
        content="Thai basic sentence structure: Subject + Verb + Object (SVO). "
                "Example: คน กิน น้ำ (person eat water = The person drinks water).",
        prerequisites=[],  # Requires Week 3 completion
    )
    return lesson


def load_basic_sentences() -> List[Dict]:
    """Load basic sentence patterns from grammar data."""
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    grammar_file = data_dir / "basic_grammar.json"
    
    grammar_data = json.loads(grammar_file.read_text(encoding='utf-8'))
    
    # Get basic sentence patterns
    patterns = grammar_data['basic_sentence_patterns']
    
    return patterns


def generate_lesson_4_1_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 4.1.
    
    Exercise types:
    1. Sentence → meaning
    2. Sentence → pattern (S-V, S-V-O, etc.)
    3. Word order identification
    """
    patterns = load_basic_sentences()
    exercises = []
    
    # Type 1: Sentence → meaning
    for pattern in patterns:
        exercise = LearningExercise(
            question=f"Meaning: {pattern['example_thai']}",
            expected_answer=pattern['example_meaning'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 2: Sentence → pattern
    for pattern in patterns:
        exercise = LearningExercise(
            question=f"Pattern: {pattern['example_thai']}",
            expected_answer=pattern['pattern'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    # Type 3: Structure identification
    for pattern in patterns:
        exercise = LearningExercise(
            question=f"Structure: {pattern['example_thai']}",
            expected_answer=pattern['structure'],
            verification_type="EXACT"
        )
        exercises.append(exercise)
    
    return exercises


def assess_lesson_4_1_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 4.1.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {
        'meaning_errors': [],
        'pattern_errors': [],
        'structure_errors': [],
    }
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            question = exercise.question
            if 'Meaning' in question:
                error_patterns['meaning_errors'].append((question, answer, exercise.expected_answer))
            elif 'Pattern' in question:
                error_patterns['pattern_errors'].append((question, answer, exercise.expected_answer))
            elif 'Structure' in question:
                error_patterns['structure_errors'].append((question, answer, exercise.expected_answer))
    
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
    if len(error_patterns['meaning_errors']) > 1:
        knowledge_gaps.append("sentence comprehension")
    if len(error_patterns['pattern_errors']) > 1:
        knowledge_gaps.append("sentence pattern recognition")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_4_1(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 4.1 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_4_1(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 4.1 assessment.
    
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
