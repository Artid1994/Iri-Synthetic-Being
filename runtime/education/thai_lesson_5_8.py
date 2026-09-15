"""
Thai Week 5 Lesson 5.8: Expanded Sentence Patterns
Expanded patterns: S-V-O-LOC (location), S-VERB-VERB (serial), S-V-NUM-CL-O (quantity). Integration of Week 5 concepts.
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_5_8() -> Lesson:
    """Create Lesson 5.8: Expanded Sentence Patterns."""
    lesson = Lesson(
        subject_id="thai_language",
        level=5,
        title="รูปแบบประโยคขยาย (Expanded Sentence Patterns)",
        objectives=['Combine multiple grammatical elements', 'Form complex sentences: S-V-O-LOC, S-VERB-VERB', 'Integrate classifiers, serial verbs, and modifiers', 'Apply expanded patterns in context'],
        content="Expanded patterns: S-V-O-LOC (location), S-VERB-VERB (serial), S-V-NUM-CL-O (quantity). Integration of Week 5 concepts.",
        prerequisites=[],  # Requires lesson 5.7
    )
    return lesson


def load_expanded_patterns() -> List[Dict]:
    """
    Load examples for Expanded Sentence Patterns.
    
    Data source: advanced_grammar.json
    """
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    grammar_file = data_dir / "advanced_grammar.json"
    
    grammar_data = json.loads(grammar_file.read_text(encoding='utf-8'))
    
    examples = []
    
    # Expanded sentence patterns
    for pattern in grammar_data['expanded_sentence_patterns']:
        examples.append({
            'question': f"Pattern: {pattern['example']}",
            'answer': pattern['pattern'],
        })
        examples.append({
            'question': f"Meaning: {pattern['example']}",
            'answer': pattern['meaning'],
        })
    
    
    return examples


def generate_lesson_5_8_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 5.8.
    """
    examples = load_expanded_patterns()
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


def assess_lesson_5_8_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 5.8.
    
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
        knowledge_gaps.append("expanded sentence patterns")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_5_8(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 5.8 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_5_8(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """Update MasteryTracker based on Lesson 5.8 assessment."""
    record = mastery_tracker.record_attempt(
        lesson_id=lesson_id,
        score=assessment['accuracy']
    )
    
    if assessment['mastery_level'] == 'mastered':
        record.mastered = True
    else:
        record.mastered = False
