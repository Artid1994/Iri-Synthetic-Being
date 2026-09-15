"""
Thai Week 5 Lesson 5.9: Semantic Relationships
Semantic relationships: time sequence (basic markers), cause-effect (UNKNOWN), comparison (UNKNOWN). Focus on KNOWN relationships only.
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker


def create_lesson_5_9() -> Lesson:
    """Create Lesson 5.9: Semantic Relationships."""
    lesson = Lesson(
        subject_id="thai_language",
        level=5,
        title="ความสัมพันธ์เชิงความหมาย (Semantic Relationships)",
        objectives=['Recognize time-sequence relationships (แล้ว, ก่อน, หลัง)', 'Understand word-to-word semantic connections', 'Identify sentence-to-sentence relationships', 'Apply WHY reasoning to semantic patterns'],
        content="Semantic relationships: time sequence (basic markers), cause-effect (UNKNOWN), comparison (UNKNOWN). Focus on KNOWN relationships only.",
        prerequisites=[],  # Requires lesson 5.8
    )
    return lesson


def load_semantic_relationships() -> List[Dict]:
    """
    Load examples for Semantic Relationships.
    
    Data source: advanced_grammar.json
    """
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    grammar_file = data_dir / "advanced_grammar.json"
    
    grammar_data = json.loads(grammar_file.read_text(encoding='utf-8'))
    
    examples = []
    
    # Semantic relationships
    semantic = grammar_data['semantic_relationships']
    for rel in semantic['relationships']:
        if rel['data_status'] in ['KNOWN', 'PARTIAL']:
            if 'thai_markers' in rel:
                for marker in rel['thai_markers']:
                    examples.append({
                        'question': f"Time marker: {marker}",
                        'answer': rel['type'],
                    })
        examples.append({
            'question': f"Status of {rel['type']} relationships",
            'answer': rel['data_status'],
        })
    
    
    return examples


def generate_lesson_5_9_exercises() -> List[LearningExercise]:
    """
    Generate practice exercises for Lesson 5.9.
    """
    examples = load_semantic_relationships()
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


def assess_lesson_5_9_mastery(responses: List[Tuple[LearningExercise, str]]) -> Dict:
    """
    Assess mastery of Lesson 5.9.
    
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
        knowledge_gaps.append("semantic relationships")
    
    return {
        'accuracy': accuracy,
        'mastery_level': mastery_level,
        'error_patterns': error_patterns,
        'knowledge_gaps': knowledge_gaps,
        'total_exercises': total,
        'correct': correct,
    }


def update_knowledge_state_5_9(assessment: Dict, knowledge_state: KnowledgeState) -> None:
    """Update KnowledgeState based on Lesson 5.9 assessment."""
    for _ in range(assessment['correct']):
        knowledge_state.record_correct()
    
    incorrect = assessment['total_exercises'] - assessment['correct']
    for _ in range(incorrect):
        if assessment['knowledge_gaps']:
            knowledge_state.record_error(ErrorType.PARTIAL)
        else:
            knowledge_state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker_5_9(assessment: Dict, mastery_tracker: MasteryTracker, lesson_id: str) -> None:
    """Update MasteryTracker based on Lesson 5.9 assessment."""
    record = mastery_tracker.record_attempt(
        lesson_id=lesson_id,
        score=assessment['accuracy']
    )
    
    if assessment['mastery_level'] == 'mastered':
        record.mastered = True
    else:
        record.mastered = False
