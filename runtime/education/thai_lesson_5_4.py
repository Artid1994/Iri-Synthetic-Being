"""
Thai Week 5 Lesson 5.4: Location Expressions
Location pattern: อยู่ + LOCATION. Example: อยู่ บ้าน (be at home).
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_5_4() -> Lesson:
    """Create Lesson 5.4: Location Expressions."""
    lesson = Lesson(
        subject_id="thai_language",
        level=5,
        title="การแสดงตำแหน่งที่ (Location Expressions)",
        objectives=['Use อยู่ for location expressions', 'Form location sentences: อยู่ + LOCATION', 'Understand locative structures', 'Apply location expressions in context'],
        content="Location pattern: อยู่ + LOCATION. Example: อยู่ บ้าน (be at home).",
        prerequisites=[],  # Requires lesson 5.3
    )
    return lesson


def load_location_expressions() -> List[Dict]:
    """
    Load examples for Location Expressions.
    
    Data source: advanced_grammar.json
    """
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    grammar_file = data_dir / "advanced_grammar.json"
    
    grammar_data = json.loads(grammar_file.read_text(encoding='utf-8'))
    
    examples = []
    
    # Location expressions
    for pattern in grammar_data['conversational_patterns']:
        if pattern['pattern'] == 'location expression':
            examples.append({
                'question': f"Meaning: {pattern['example']}",
                'answer': pattern['meaning'],
            })
            examples.append({
                'question': 'Location structure',
                'answer': pattern['structure'],
            })
    
    
    return examples


def generate_lesson_5_4_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 5.4.
    """
    examples = load_location_expressions()
    exercises = []
    
    for example in examples:
        if 'question' in example and 'answer' in example:
            exercise = LearningExercise(
                question=example['question'],
                expected_answer=example['answer'],
                verification_type="EXACT"
            )
            exercises.append(exercise)
    
    return exercises


def assess_lesson_5_4_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 5.4.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    error_patterns = {'errors': []}
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            error_patterns['errors'].append((exercise.question, answer, exercise.expected_answer))
    
    if accuracy >= 0.90:
        mastery_level = "mastered"
    elif accuracy >= 0.75:
        mastery_level = "proficient"
    elif accuracy >= 0.60:
        mastery_level = "developing"
    else:
        mastery_level = "novice"
    
    knowledge_gaps = []
    if len(error_patterns['errors']) > 2:
        knowledge_gaps.append("location expressions")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_5_4(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 5.4 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_5_4(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """Update MasteryTracker based on Lesson 5.4 assessment."""
    record = mastery_tracker.record_attempt(
        lesson_id=lesson_id,
        score=assessment['accuracy']
    )
    
    if assessment['mastery_level'] == 'mastered':
        record.mastered = True
    else:
        record.mastered = False
