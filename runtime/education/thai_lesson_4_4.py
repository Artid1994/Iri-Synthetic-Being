"""
Thai Week 4 Lesson 4.4: Yes-No Questions
Yes-no questions: Statement + ไหม (question particle). Example: ดี ไหม (good QUESTION = Is it good?)
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_4_4() -> Lesson:
    """Create Lesson 4.4: Yes-No Questions."""
    lesson = Lesson(
        subject_id="thai_language",
        level=4,
        title="คำถามแบบใช่-ไม่ใช่ (Yes-No Questions)",
        objectives=['Form yes-no questions with ไหม', 'Understand question particle placement (sentence-final)', 'Distinguish statements from questions', 'Comprehend question meaning'],
        content="Yes-no questions: Statement + ไหม (question particle). Example: ดี ไหม (good QUESTION = Is it good?)",
        prerequisites=[],  # Requires lesson 4.3
    )
    return lesson


def load_yes_no_questions() -> List[Dict]:
    """
    Load examples for Yes-No Questions.
    
    Data source: basic_grammar.json particles + sentence patterns
    """
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    
    # Load grammar and vocabulary data
    grammar_file = data_dir / "basic_grammar.json"
    vocab_file = data_dir / "vocabulary.json"
    
    grammar_data = json.loads(grammar_file.read_text(encoding='utf-8'))
    vocab_data = json.loads(vocab_file.read_text(encoding='utf-8'))
    
    # Generate examples based on lesson focus
    examples = []
    
    # Yes-no questions: add ไหม to statements
    sentences = grammar_data['basic_sentence_patterns'][:3]
    for sent in sentences:
        examples.append({
            'question': f"Yes-no question: {sent['example_thai']}",
            'answer': f"{sent['example_thai']} ไหม",
        })
    
    
    return examples


def generate_lesson_4_4_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 4.4.
    
    Exercise types based on lesson objectives.
    """
    examples = load_yes_no_questions()
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


def assess_lesson_4_4_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 4.4.
    
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
        knowledge_gaps.append("yes-no questions")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_4_4(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 4.4 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_4_4(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 4.4 assessment.
    
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
