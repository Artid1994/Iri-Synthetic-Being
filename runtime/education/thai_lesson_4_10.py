"""
Thai Week 4 Lesson 4.10: Integrated Sentence Understanding
Final integration: Weeks 2-4 combined. Read Thai sentences with full comprehension (sound → word → meaning → structure).
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_4_10() -> Lesson:
    """Create Lesson 4.10: Integrated Sentence Understanding."""
    lesson = Lesson(
        subject_id="thai_language",
        level=4,
        title="ความเข้าใจประโยคแบบบูรณาการ (Integrated Sentence Understanding)",
        objectives=['Demonstrate Week 4 sentence mastery', 'Read and comprehend varied sentence types', 'Apply all grammatical patterns', 'Integrate phonology + vocabulary + grammar'],
        content="Final integration: Weeks 2-4 combined. Read Thai sentences with full comprehension (sound → word → meaning → structure).",
        prerequisites=[],  # Requires lesson 4.9
    )
    return lesson


def load_integrated_sentences() -> List[Dict]:
    """
    Load examples for Integrated Sentence Understanding.
    
    Data source: Comprehensive sentence set covering all Week 4 patterns
    """
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    
    # Load grammar and vocabulary data
    grammar_file = data_dir / "basic_grammar.json"
    vocab_file = data_dir / "vocabulary.json"
    
    grammar_data = json.loads(grammar_file.read_text(encoding='utf-8'))
    vocab_data = json.loads(vocab_file.read_text(encoding='utf-8'))
    
    # Generate examples based on lesson focus
    examples = []
    
    # Integrated: all patterns
    for pattern in grammar_data['basic_sentence_patterns']:
        examples.append({
            'question': f"Comprehend: {pattern['example_thai']}",
            'answer': pattern['example_meaning'],
        })
    
    
    return examples


def generate_lesson_4_10_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 4.10.
    
    Exercise types based on lesson objectives.
    """
    examples = load_integrated_sentences()
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


def assess_lesson_4_10_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 4.10.
    
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
        knowledge_gaps.append("integrated sentence understanding")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_4_10(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 4.10 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_4_10(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """
    Update MasteryTracker based on Lesson 4.10 assessment.
    
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
