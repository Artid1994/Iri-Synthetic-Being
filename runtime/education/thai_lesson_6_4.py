"""
Thai Week 6 Lesson 6.4: Ambiguity (ความกำกวม)

Learning Objectives:
1. Detect semantic ambiguity in words and sentences
2. Distinguish UNKNOWN vs AMBIGUOUS vs KNOWN
3. Identify possible interpretations when ambiguous
4. Recognize when context is insufficient for resolution
5. Use context to resolve ambiguity when evidence sufficient
6. Provide evidence for ambiguity claims (not guessing)

CRITICAL: AMBIGUOUS ≠ UNKNOWN
- AMBIGUOUS: Multiple valid interpretations exist
- UNKNOWN: No interpretation can be formed (no data/evidence)
- KNOWN: Single interpretation with sufficient evidence
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Dict, Optional
import json

from runtime.education.lesson import Lesson
from runtime.learning_exercise import LearningExercise
from runtime.education.assessment import Assessment, AssessmentResult
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel, ErrorType
from runtime.education.mastery_tracker import MasteryTracker
from runtime.memory import Memory
from runtime.self_model import SelfModel
from runtime.education.semantic_representation import (
    SentenceSemantics,
    SemanticMeaning,
    AmbiguityPoint,
    AmbiguityType,
    ContextualMeaning,
    EvidenceStatus,
    ContextType,
    UnderstandingEvidence,
    EvidenceType,
)


def load_data() -> Dict:
    """Load semantic vocabulary with ambiguity data."""
    data_path = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language" / "semantic_vocabulary.json"
    return json.loads(data_path.read_text(encoding='utf-8'))


def detect_ambiguity(word_or_sentence: str, data: Dict) -> Tuple[bool, List[str], str]:
    """
    Detect if word/sentence is ambiguous.
    
    Returns: (is_ambiguous, possible_interpretations, ambiguity_reason)
    """
    # Check ambiguity examples
    ambiguity_examples = data.get('ambiguity_examples', [])
    
    for ex in ambiguity_examples:
        if ex['sentence'] == word_or_sentence:
            return (
                True,
                ex['possible_meanings'],
                f"Context required: {', '.join(ex['resolution_clues'])}"
            )
    
    # Check word-level ambiguity
    vocab = data['semantic_vocabulary']
    for w in vocab:
        if w['word'] == word_or_sentence:
            if w.get('ambiguity_level') == 'MILDLY_AMBIGUOUS':
                contexts = w.get('contextual_meanings', [])
                if len(contexts) > 1:
                    meanings = [c['meaning'] for c in contexts]
                    return (
                        True,
                        meanings,
                        f"Word has {len(contexts)} contextual meanings"
                    )
    
    return (False, [], "No ambiguity detected")


def build_ambiguity_point(
    word_or_sentence: str,
    location: str,
    data: Dict
) -> Optional[AmbiguityPoint]:
    """
    Build AmbiguityPoint if ambiguity detected.
    
    Returns None if not ambiguous.
    """
    is_ambiguous, interpretations, reason = detect_ambiguity(word_or_sentence, data)
    
    if not is_ambiguous:
        return None
    
    # Determine ambiguity type
    ambiguity_type = AmbiguityType.LEXICAL  # Default for word-level
    
    # Check if pragmatic ambiguity
    if any('pragmatic' in i.lower() for i in interpretations):
        ambiguity_type = AmbiguityType.PRAGMATIC
    
    return AmbiguityPoint(
        location=location,
        ambiguity_type=ambiguity_type,
        possible_interpretations=interpretations,
        resolution_required=True,
        resolution_strategy="CONTEXT_REQUIRED",
    )


def generate_lesson_6_4_exercises() -> List[LearningExercise]:
    """
    Generate exercises for ambiguity.
    
    Focus: detection, UNKNOWN vs AMBIGUOUS, resolution
    """
    exercises = []
    
    # Exercise 1: Detect ambiguity
    exercises.append(LearningExercise(
        question="คำว่า 'ดี' (โดยไม่มีบริบท) เป็น AMBIGUOUS หรือ UNKNOWN?",
        expected_answer="AMBIGUOUS",
        verification_type="EXACT",
    ))
    
    # Exercise 2: Count interpretations
    exercises.append(LearningExercise(
        question="คำว่า 'ดี' มีความหมายที่เป็นไปได้กี่แบบ? (1/2/3)",
        expected_answer="2",
        verification_type="EXACT",
    ))
    
    # Exercise 3: UNKNOWN vs AMBIGUOUS
    exercises.append(LearningExercise(
        question="คำที่ไม่มีในข้อมูลเลยเป็น AMBIGUOUS หรือ UNKNOWN?",
        expected_answer="UNKNOWN",
        verification_type="EXACT",
    ))
    
    # Exercise 4: Resolution requirement
    exercises.append(LearningExercise(
        question="'ดี' ต้องการอะไรเพื่อ resolve ambiguity? (context/translation/guessing)",
        expected_answer="context",
        verification_type="EXACT",
    ))
    
    # Exercise 5: Context resolves
    exercises.append(LearningExercise(
        question="'คน ดี' (มี context) ยังคง AMBIGUOUS หรือเปล่า? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    # Exercise 6: Multiple interpretations
    exercises.append(LearningExercise(
        question="'ไป เรียน' มีความหมายที่เป็นไปได้กี่แบบ? (1/2/3)",
        expected_answer="3",
        verification_type="EXACT",
    ))
    
    # Exercise 7: Ambiguity type
    exercises.append(LearningExercise(
        question="Ambiguity ของ 'ดี' เป็นประเภทใด? (LEXICAL/STRUCTURAL/PRAGMATIC)",
        expected_answer="PRAGMATIC",
        verification_type="EXACT",
    ))
    
    # Exercise 8: Forced resolution
    exercises.append(LearningExercise(
        question="ถ้า context ยังไม่พอ ควรเดาความหมายหรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    # Exercise 9: Evidence requirement
    exercises.append(LearningExercise(
        question="การ resolve ambiguity ต้องการอะไร? (evidence/guessing/translation)",
        expected_answer="evidence",
        verification_type="EXACT",
    ))
    
    # Exercise 10: State after resolution
    exercises.append(LearningExercise(
        question="หลัง resolve ambiguity ด้วย context สถานะเป็นอะไร? (AMBIGUOUS/KNOWN/UNKNOWN)",
        expected_answer="KNOWN",
        verification_type="EXACT",
    ))
    
    return exercises


def assess_mastery(responses: List[str]) -> Tuple[float, str, List[str], List[str]]:
    """
    Assess ambiguity understanding.
    
    Requires ability to distinguish UNKNOWN/AMBIGUOUS/KNOWN.
    """
    exercises = generate_lesson_6_4_exercises()
    
    if len(responses) != len(exercises):
        raise ValueError(f"Expected {len(exercises)} responses, got {len(responses)}")
    
    correct = 0
    error_patterns = []
    knowledge_gaps = []
    
    for i, (exercise, response) in enumerate(zip(exercises, responses)):
        response = response.strip()
        expected = exercise.expected_answer.strip()
        
        if response.upper() == expected.upper():
            correct += 1
        else:
            error_patterns.append(f"Q{i+1}: Expected {expected}, got {response}")
            
            if i in [0, 2]:  # AMBIGUOUS vs UNKNOWN
                knowledge_gaps.append("ambiguous_unknown_distinction")
            elif i in [1, 5]:  # Interpretation counting
                knowledge_gaps.append("interpretation_enumeration")
            elif i in [3, 8]:  # Resolution requirements
                knowledge_gaps.append("resolution_understanding")
            elif i == 7:  # Forced resolution
                knowledge_gaps.append("no_guessing_principle")
    
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
    exercises = generate_lesson_6_4_exercises()
    
    for exercise, response in zip(exercises, responses):
        if response.strip().upper() == exercise.expected_answer.strip().upper():
            state.record_correct()
        else:
            state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker(tracker: MasteryTracker, lesson_id: str, accuracy: float) -> None:
    """Update mastery tracker."""
    tracker.record_attempt(lesson_id, accuracy)


# Lesson definition
lesson_6_4 = Lesson(
    subject_id="thai",
    level=6,
    title="Ambiguity (ความกำกวม)",
    objectives=[
        "Detect semantic ambiguity in words and sentences",
        "Distinguish UNKNOWN vs AMBIGUOUS vs KNOWN states",
        "Identify possible interpretations when ambiguous",
        "Recognize when context insufficient for resolution",
        "Use context to resolve ambiguity when evidence sufficient",
        "Understand no-guessing principle for ambiguous cases",
    ],
    content="""
Ambiguity (ความกำกวม)

1. Three States of Knowledge
   - KNOWN: Single interpretation with sufficient evidence
     Example: "คน ดี" with full context → "good person"
   
   - AMBIGUOUS: Multiple valid interpretations exist
     Example: "ดี" alone → could be quality OR agreement
   
   - UNKNOWN: No interpretation possible (no data/evidence)
     Example: Word not in vocabulary → UNKNOWN

2. Types of Ambiguity
   - LEXICAL: Word has multiple meanings
     Example: "ไป" → physical movement OR attend
   
   - PRAGMATIC: Interpretation depends on pragmatic context
     Example: "ดี" → quality adjective OR conversational agreement
   
   - STRUCTURAL: Sentence structure ambiguous
     Example: (not in current data)

3. Detecting Ambiguity
   - Check if multiple contextual meanings exist
   - Check ambiguity examples in data
   - Do NOT guess - if data says ambiguous, it's ambiguous

4. Possible Interpretations
   - "ดี": [good quality, okay/fine]
   - "ไป เรียน": [go study, go to study, attend class]
   - Must enumerate all valid interpretations from data

5. Resolution Requirements
   - AMBIGUOUS requires: context + evidence
   - Cannot resolve with: translation, guessing
   - If context insufficient: remains AMBIGUOUS
   
   Example:
   - "ดี" alone: AMBIGUOUS (need context)
   - "คน ดี": KNOWN (context = noun modifier)
   - "ดี" (response to question): KNOWN (context = agreement)

6. No Guessing Principle
   - If ambiguous and context insufficient: stay AMBIGUOUS
   - Do NOT force resolution
   - Do NOT guess meaning
   - Wait for adequate evidence

7. Resolution Process
   AMBIGUOUS + context → check evidence → if sufficient → KNOWN
   AMBIGUOUS + no context → remains AMBIGUOUS

8. Evidence for Resolution
   - Contextual clues (surrounding words, sentence structure)
   - Pragmatic situation (question/response, modification)
   - Not sufficient: translation alone
""",
    prerequisites=["thai_lesson_6_3"],
)
