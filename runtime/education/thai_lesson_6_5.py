"""
Thai Week 6 Lesson 6.5: Context (บริบท)

Learning Objectives:
1. Understand how context affects semantic interpretation
2. Identify required context types for interpretation
3. Use context to select correct meaning from ambiguous options
4. Recognize insufficient context → AMBIGUOUS
5. Recognize missing knowledge → UNKNOWN
6. Provide contextual evidence (not translation or guessing)

CRITICAL: Context must affect interpretation MECHANICALLY, not just conceptually.
Same word + different context → different verifiable interpretation.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Dict, Optional
import json

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel, ErrorType
from runtime.education.mastery_tracker import MasteryTracker
from runtime.memory import Memory
from runtime.self_model import SelfModel
from runtime.education.semantic_representation import (
    ContextualMeaning,
    ContextType,
    EvidenceStatus,
)


def load_data() -> Dict:
    """Load semantic vocabulary with context data."""
    data_path = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language" / "semantic_vocabulary.json"
    return json.loads(data_path.read_text(encoding='utf-8'))


def select_interpretation_with_context(
    word: str,
    context_clues: List[str],
    data: Dict
) -> Tuple[Optional[str], str, str]:
    """
    Select interpretation based on context.
    
    Args:
        word: Thai word
        context_clues: List of context identifiers (e.g., ['activity', 'noun'])
        data: Vocabulary data
    
    Returns:
        (selected_meaning, reason, state)
        state: KNOWN, AMBIGUOUS, UNKNOWN
    """
    vocab = data['semantic_vocabulary']
    word_data = next((w for w in vocab if w['word'] == word), None)
    
    if not word_data:
        return (None, "Word not in vocabulary", "UNKNOWN")
    
    contextual_meanings = word_data.get('contextual_meanings', [])
    
    if len(contextual_meanings) == 0:
        return (None, "No contextual meanings available", "UNKNOWN")
    
    if len(contextual_meanings) == 1:
        return (
            contextual_meanings[0]['meaning'],
            "Single meaning available",
            "KNOWN"
        )
    
    # Multiple meanings - context needed
    if not context_clues:
        meanings = [c['meaning'] for c in contextual_meanings]
        return (
            None,
            f"Ambiguous: {len(meanings)} possible meanings, context required",
            "AMBIGUOUS"
        )
    
    # Match context with required_context
    matches = []
    for ctx_meaning in contextual_meanings:
        required = ctx_meaning.get('required_context', [])
        
        # Check if any context clue matches required context
        if not required:  # No specific requirement (e.g., LITERAL) - can match if no better option
            if not context_clues:  # If no context provided, LITERAL is default
                matches.append((ctx_meaning, "default literal"))
            else:
                # LITERAL can be fallback but check for better matches first
                pass
        else:
            # Check overlap between context_clues and required
            overlap = set(context_clues) & set(required)
            if overlap:
                matches.append((ctx_meaning, f"matched: {list(overlap)}"))
    
    # If no matches found and we have LITERAL available, use it as fallback
    if len(matches) == 0:
        literal = next((c for c in contextual_meanings if not c.get('required_context')), None)
        if literal and context_clues:
            # Context provided but didn't match PRAGMATIC, could be LITERAL with location/etc
            matches.append((literal, "fallback to literal with context"))
    
    if len(matches) == 0:
        if context_clues:
            return (
                None,
                "Context provided but doesn't match any required context",
                "AMBIGUOUS"
            )
        else:
            return (
                None,
                f"Ambiguous: {len(contextual_meanings)} possible meanings, no context",
                "AMBIGUOUS"
            )
    
    if len(matches) == 1:
        return (
            matches[0][0]['meaning'],
            f"Context-selected ({matches[0][1]})",
            "KNOWN"
        )
    
    # Multiple matches still ambiguous
    return (
        None,
        f"Context matches {len(matches)} meanings, still ambiguous",
        "AMBIGUOUS"
    )


def generate_lesson_6_5_exercises() -> List[LearningExercise]:
    """
    Generate exercises for context understanding.
    
    Focus: context affects interpretation, context types, insufficiency
    """
    exercises = []
    
    # Exercise 1: Context changes meaning
    exercises.append(LearningExercise(
        question="'ไป' + context(บ้าน/location) → ความหมายแบบใด? (LITERAL/PRAGMATIC)",
        expected_answer="LITERAL",
        verification_type="EXACT",
    ))
    
    # Exercise 2: Context changes meaning
    exercises.append(LearningExercise(
        question="'ไป' + context(เรียน/activity) → ความหมายแบบใด? (LITERAL/PRAGMATIC)",
        expected_answer="PRAGMATIC",
        verification_type="EXACT",
    ))
    
    # Exercise 3: No context state
    exercises.append(LearningExercise(
        question="'ดี' ไม่มี context → state เป็นอะไร? (KNOWN/AMBIGUOUS/UNKNOWN)",
        expected_answer="AMBIGUOUS",
        verification_type="EXACT",
    ))
    
    # Exercise 4: Context resolves
    exercises.append(LearningExercise(
        question="'ดี' + context(คน/noun) → state เป็นอะไร? (KNOWN/AMBIGUOUS/UNKNOWN)",
        expected_answer="KNOWN",
        verification_type="EXACT",
    ))
    
    # Exercise 5: Required context type
    exercises.append(LearningExercise(
        question="'ไป' (PRAGMATIC) ต้องการ context ประเภทใด? (activity/location/time)",
        expected_answer="activity",
        verification_type="EXACT",
    ))
    
    # Exercise 6: Context type identification
    exercises.append(LearningExercise(
        question="'คน' เป็น context ประเภทใด? (activity/noun/response)",
        expected_answer="noun",
        verification_type="EXACT",
    ))
    
    # Exercise 7: Insufficient context
    exercises.append(LearningExercise(
        question="ถ้า context มีแต่ไม่ตรงกับ required_context จะเป็น KNOWN หรือ AMBIGUOUS?",
        expected_answer="AMBIGUOUS",
        verification_type="EXACT",
    ))
    
    # Exercise 8: Context mechanism
    exercises.append(LearningExercise(
        question="Context เปลี่ยน interpretation ได้จริงหรือเพียงแค่ metadata? (จริง/metadata)",
        expected_answer="จริง",
        verification_type="EXACT",
    ))
    
    # Exercise 9: Evidence type
    exercises.append(LearningExercise(
        question="การอธิบายว่า context ทำให้เลือก meaning ใด ต้องการ evidence type อะไร? (CONTEXTUAL_INTERPRETATION/TRANSLATION)",
        expected_answer="CONTEXTUAL_INTERPRETATION",
        verification_type="EXACT",
    ))
    
    # Exercise 10: Translation sufficiency
    exercises.append(LearningExercise(
        question="Translation เพียงอย่างเดียวพิสูจน์ contextual understanding ได้หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    return exercises


def assess_mastery(responses: List[str]) -> Tuple[float, str, List[str], List[str]]:
    """
    Assess context understanding.
    
    Requires demonstration that context affects interpretation.
    """
    exercises = generate_lesson_6_5_exercises()
    
    if len(responses) != len(exercises):
        raise ValueError(f"Expected {len(exercises)} responses, got {len(responses)}")
    
    correct = 0
    error_patterns = []
    knowledge_gaps = []
    
    for i, (exercise, response) in enumerate(zip(exercises, responses)):
        response = response.strip()
        expected = exercise.expected_answer.strip()
        
        if response.upper() == expected.upper() or response == expected:
            correct += 1
        else:
            error_patterns.append(f"Q{i+1}: Expected {expected}, got {response}")
            
            if i in [0, 1]:  # Context changes meaning
                knowledge_gaps.append("context_changes_meaning")
            elif i in [2, 3, 6]:  # State with/without context
                knowledge_gaps.append("context_sufficiency")
            elif i in [4, 5]:  # Context type
                knowledge_gaps.append("context_type_identification")
            elif i == 7:  # Mechanism
                knowledge_gaps.append("context_mechanism_understanding")
    
    accuracy = correct / len(exercises)
    
    if accuracy >= 0.9:
        mastery_level = "MASTERED"
    elif accuracy >= 0.7:
        mastery_level = "CAN_USE"
    else:
        mastery_level = "LEARNING"
    
    knowledge_gaps = list(set(knowledge_gaps))
    
    return accuracy, mastery_level, error_patterns, knowledge_gaps


def update_knowledge_state(state: KnowledgeState, responses: List[str]) -> None:
    """Update knowledge state from assessment."""
    exercises = generate_lesson_6_5_exercises()
    
    for exercise, response in zip(exercises, responses):
        if response.strip().upper() == exercise.expected_answer.strip().upper() or response.strip() == exercise.expected_answer.strip():
            state.record_correct()
        else:
            state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker(tracker: MasteryTracker, lesson_id: str, accuracy: float) -> None:
    """Update mastery tracker."""
    tracker.record_attempt(lesson_id, accuracy)


# Lesson definition
lesson_6_5 = Lesson(
    subject_id="thai",
    level=6,
    title="Context (บริบท)",
    objectives=[
        "Understand how context affects semantic interpretation mechanically",
        "Identify required context types for interpretation",
        "Use context to select correct meaning from ambiguous options",
        "Recognize insufficient context → AMBIGUOUS",
        "Recognize missing knowledge → UNKNOWN",
        "Provide contextual evidence (not translation or guessing)",
    ],
    content="""
Context (บริบท)

1. Context Affects Interpretation MECHANICALLY
   - Not just metadata or description
   - Context SELECTS interpretation from possibilities
   
   Example:
   "ไป" has 2 contextual meanings:
   - LITERAL: physical movement (required_context: [])
   - PRAGMATIC: attend/participate (required_context: [activity, event])
   
   Context determines which:
   - "ไป" + location context → LITERAL
   - "ไป" + activity context → PRAGMATIC

2. Context Types
   - activity: เรียน, กิน (action words)
   - noun: คน, น้ำ (entity words)
   - response/conversational: reply to question
   - location: บ้าน, ที่
   
3. Required Context
   Each contextual meaning may require specific context:
   - ไป (LITERAL): no specific requirement
   - ไป (PRAGMATIC): requires activity/event
   - ดี (LITERAL): requires noun (modification)
   - ดี (PRAGMATIC): requires conversational/response

4. Selection Process
   Word → Check contextual_meanings
   → Multiple meanings? → Check context_clues
   → Match context with required_context
   → Select matching meaning → KNOWN
   
   No match → AMBIGUOUS
   No meanings → UNKNOWN

5. States Based on Context
   - KNOWN: Context sufficient to select one meaning
     Example: "ดี" + noun context → quality meaning
   
   - AMBIGUOUS: Multiple meanings, context insufficient
     Example: "ดี" + no context → ambiguous
   
   - UNKNOWN: No data to interpret
     Example: Unknown word → UNKNOWN

6. Context Insufficiency
   - No context provided → AMBIGUOUS (if multiple meanings)
   - Context provided but doesn't match required → AMBIGUOUS
   - Context matches multiple meanings → AMBIGUOUS
   
   Do NOT force resolution

7. Evidence Requirement
   - CONTEXTUAL_INTERPRETATION evidence required
   - Must explain: context → meaning selection
   - Translation alone insufficient
   
8. Example Flow
   Input: "ไป เรียน"
   
   "ไป":
   - Possible meanings: LITERAL (movement), PRAGMATIC (attend)
   - Context: "เรียน" (activity)
   - Match: PRAGMATIC requires activity → MATCH
   - Result: PRAGMATIC meaning selected → KNOWN
   - Evidence: "เรียน provides activity context, matches PRAGMATIC requirement"
""",
    prerequisites=["thai_lesson_6_4"],
)
