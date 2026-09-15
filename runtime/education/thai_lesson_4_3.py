"""
Thai Week 4 Lesson 4.3: Negation
Thai negation: ไม่ (not) before verb. Example: ไม่ ดี (not good), ไม่ กิน (not eat). Practice negating sentences.
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_4_3() -> Lesson:
    """Create Lesson 4.3: Negation."""
    lesson = Lesson(
        subject_id="thai_language",
        level=4,
        title="การปฏิเสธ (Negation)",
        objectives=['Use ไม่ (mai) for negation', 'Understand negation word order (NEG + Verb)', 'Form negative sentences', 'Distinguish affirmative vs negative meaning'],
        content="Thai negation: ไม่ (not) before verb. Example: ไม่ ดี (not good), ไม่ กิน (not eat). Practice negating sentences.",
        prerequisites=[],  # Requires lesson 4.2
    )
    return lesson


def load_negation_examples() -> List[Dict]:
    """
    Load examples for Negation.
    
    Data source: Combine vocabulary verbs/adjectives with ไม่ particle
    """
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    
    # Load grammar and vocabulary data
    grammar_file = data_dir / "basic_grammar.json"
    vocab_file = data_dir / "vocabulary.json"
    
    grammar_data = json.loads(grammar_file.read_text(encoding='utf-8'))
    vocab_data = json.loads(vocab_file.read_text(encoding='utf-8'))
    
    # Generate examples based on lesson focus
    examples = []
    
    # Negation: create negative versions
    verbs = [w for w in vocab_data['vocabulary'] if w['category'] == 'verb'][:5]
    for verb in verbs:
        examples.append({
            'question': f"Negate: {verb['word']}",
            'answer': f"ไม่ {verb['word']}",
        })
    
    
    return examples


def generate_lesson_4_3_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 4.3.
    
    Exercise types based on lesson objectives.
    """
    examples = load_negation_examples()
    exercises = []
    
    # Generate exercises from examples
    for example in examples:
        if 'question' in example and 'answer' in example:
            exercise = LearningExercise(
                question=example['question'],
                expected_answer=example['answer'],
                verification_type="EXACT"
            )
            exercises.append(exercise)
    
    return exercises


def assess_lesson_4_3_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 4.3.
    
    Uses unified 90% threshold.
    """
    total = len(responses)
    correct = sum(1 for ex, ans in responses if ex.verify(ans))
    accuracy = correct / total if total > 0 else 0.0
    
    # Classify errors
    error_patterns = {'errors': []}
    
    for exercise, answer in responses:
        if not exercise.verify(answer):
            error_patterns['errors'].append((exercise.question, answer, exercise.expected_answer))
    
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
    if len(error_patterns['errors']) > 2:
        knowledge_gaps.append("negation")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_4_3(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 4.3 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_4_3(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 4.3 assessment.
    
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
