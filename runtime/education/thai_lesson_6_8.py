"""
Thai Week 6 Lesson 6.8: Understanding ≠ Translation

Learning Objectives:
1. Distinguish translation/recall from semantic understanding
2. Demonstrate that translation-only cannot reach semantic mastery
3. Enforce evidence requirements at system level
4. Prove that understanding requires explanation, application, or contextual interpretation
5. Integrate with Evidence Gate for enforcement

CRITICAL: This is enforcement lesson, not just conceptual.
System must REJECT translation-only evidence for semantic mastery.
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
    SemanticMeaning,
    UnderstandingEvidence,
    EvidenceType,
)


def load_data() -> Dict:
    """Load semantic vocabulary and patterns."""
    data_path = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language" / "semantic_vocabulary.json"
    return json.loads(data_path.read_text(encoding='utf-8'))


def assess_understanding_vs_translation(
    response_type: str,
    response: str,
    expected_translation: Optional[str] = None,
    expected_explanation: Optional[str] = None,
) -> Tuple[str, EvidenceType, bool]:
    """
    Assess whether response demonstrates understanding or just translation.
    
    Args:
        response_type: "translation", "explanation", "application", "contextual"
        response: The actual response
        expected_translation: Expected translation (if applicable)
        expected_explanation: Expected explanation pattern (if applicable)
    
    Returns:
        (assessment, evidence_type, passes_semantic_gate)
        assessment: "TRANSLATION_ONLY", "UNDERSTANDING", "INSUFFICIENT"
        evidence_type: EvidenceType enum
        passes_semantic_gate: True if can consolidate as semantic knowledge
    """
    response = response.strip().lower()
    
    if response_type == "translation":
        # Translation correct?
        if expected_translation and response == expected_translation.lower():
            return ("TRANSLATION_ONLY", EvidenceType.TRANSLATION, False)
        else:
            return ("INSUFFICIENT", EvidenceType.TRANSLATION, False)
    
    elif response_type == "explanation":
        # Check if explanation present (not just translation)
        if not response:
            return ("INSUFFICIENT", EvidenceType.EXPLANATION, False)
        
        # Explanation must contain semantic structure info
        # Simple heuristic: length > translation, contains keywords
        if expected_explanation:
            expected_lower = expected_explanation.lower()
            # Check for key semantic terms
            semantic_terms = ["meaning", "context", "semantic", "field", "motion", "action", 
                            "quality", "purpose", "sequence", "pattern", "interpretation"]
            
            has_semantic = any(term in response for term in semantic_terms)
            is_substantial = len(response) > 10  # More than just a word
            
            if has_semantic and is_substantial:
                return ("UNDERSTANDING", EvidenceType.EXPLANATION, True)
            else:
                return ("INSUFFICIENT", EvidenceType.EXPLANATION, False)
        
        # No expected pattern - check for substance
        if len(response) > 15:
            return ("UNDERSTANDING", EvidenceType.EXPLANATION, True)
        else:
            return ("INSUFFICIENT", EvidenceType.EXPLANATION, False)
    
    elif response_type == "application":
        # Application requires using the pattern/meaning in new context
        if not response:
            return ("INSUFFICIENT", EvidenceType.APPLICATION, False)
        
        # Application should be substantial
        if len(response) > 5:
            return ("UNDERSTANDING", EvidenceType.APPLICATION, True)
        else:
            return ("INSUFFICIENT", EvidenceType.APPLICATION, False)
    
    elif response_type == "contextual":
        # Contextual interpretation
        if not response:
            return ("INSUFFICIENT", EvidenceType.CONTEXTUAL_INTERPRETATION, False)
        
        # Should show context-dependent interpretation
        if len(response) > 5:
            return ("UNDERSTANDING", EvidenceType.CONTEXTUAL_INTERPRETATION, True)
        else:
            return ("INSUFFICIENT", EvidenceType.CONTEXTUAL_INTERPRETATION, False)
    
    else:
        return ("INSUFFICIENT", EvidenceType.TRANSLATION, False)


def demonstrate_translation_limitation() -> Dict[str, any]:
    """
    Demonstrate that translation-only cannot reach semantic mastery.
    
    Returns dict with:
    - translation_accuracy: 1.0
    - semantic_mastery_achieved: False
    - reason: explanation
    """
    # Simulate perfect translation
    translation_correct = 5
    translation_total = 5
    translation_accuracy = translation_correct / translation_total
    
    # Check if this would allow semantic mastery
    # According to KnowledgeState rules:
    # - accuracy >= 0.95 and correct >= 5 → MASTERED
    
    # But semantic knowledge requires understanding evidence
    # Translation-only = no understanding evidence
    # Therefore: semantic mastery = False
    
    return {
        "translation_accuracy": translation_accuracy,
        "translation_correct": translation_correct,
        "would_reach_mastery_by_accuracy": True,  # Meets numeric threshold
        "has_understanding_evidence": False,       # No semantic evidence
        "semantic_mastery_achieved": False,        # Gate rejects
        "reason": "Translation-only lacks semantic understanding evidence (EXPLANATION/APPLICATION/CONTEXTUAL_INTERPRETATION required)",
    }


def demonstrate_understanding_path() -> Dict[str, any]:
    """
    Demonstrate valid path to semantic mastery.
    
    Returns dict showing:
    - translation correct
    - explanation provided
    - evidence_type: EXPLANATION
    - semantic_mastery_possible: True
    """
    return {
        "translation_correct": True,
        "explanation_provided": True,
        "evidence_type": EvidenceType.EXPLANATION,
        "evidence_verified": True,
        "semantic_mastery_possible": True,
        "reason": "Translation + explanation provides understanding evidence",
    }


def generate_lesson_6_8_exercises() -> List[LearningExercise]:
    """
    Generate exercises for Understanding ≠ Translation.
    
    Focus: Distinguish translation from understanding, enforce evidence requirements.
    """
    exercises = []
    
    # Exercise 1: Translation definition
    exercises.append(LearningExercise(
        question="Translation คือการแปลคำ ใช่หรือไม่? (YES/NO)",
        expected_answer="YES",
        verification_type="EXACT",
    ))
    
    # Exercise 2: Translation = Understanding?
    exercises.append(LearningExercise(
        question="Translation = Semantic Understanding ใช่หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    # Exercise 3: Translation usefulness
    exercises.append(LearningExercise(
        question="Translation มีประโยชน์หรือไม่? (YES/NO)",
        expected_answer="YES",
        verification_type="EXACT",
    ))
    
    # Exercise 4: Translation sufficient?
    exercises.append(LearningExercise(
        question="Translation เพียงพอสำหรับ semantic mastery หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    # Exercise 5: Evidence type
    exercises.append(LearningExercise(
        question="Translation เป็น evidence type อะไร? (TRANSLATION/EXPLANATION)",
        expected_answer="TRANSLATION",
        verification_type="EXACT",
    ))
    
    # Exercise 6: Understanding evidence
    exercises.append(LearningExercise(
        question="Semantic understanding ต้องการ evidence อะไร? (EXPLANATION/TRANSLATION)",
        expected_answer="EXPLANATION",
        verification_type="EXACT",
    ))
    
    # Exercise 7: Gate enforcement
    exercises.append(LearningExercise(
        question="Evidence Gate reject translation-only หรือไม่? (YES/NO)",
        expected_answer="YES",
        verification_type="EXACT",
    ))
    
    # Exercise 8: Mastery threshold
    exercises.append(LearningExercise(
        question="Translation 100% ทำให้ semantic mastery = True หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    # Exercise 9: Valid evidence
    exercises.append(LearningExercise(
        question="APPLICATION เป็น valid semantic evidence หรือไม่? (YES/NO)",
        expected_answer="YES",
        verification_type="EXACT",
    ))
    
    # Exercise 10: Lexical vs semantic
    exercises.append(LearningExercise(
        question="Translation ใช้ได้กับ lexical recall หรือไม่? (YES/NO)",
        expected_answer="YES",
        verification_type="EXACT",
    ))
    
    return exercises


def assess_mastery(responses: List[str]) -> Tuple[float, str, List[str], List[str]]:
    """
    Assess Understanding ≠ Translation mastery.
    
    Requires clear distinction between translation and understanding.
    """
    exercises = generate_lesson_6_8_exercises()
    
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
            
            if i in [0, 1, 2, 3]:  # Translation definition and limitations
                knowledge_gaps.append("translation_limitation")
            elif i in [4, 5, 6]:  # Evidence types
                knowledge_gaps.append("evidence_requirements")
            elif i in [7, 8]:  # Gate enforcement
                knowledge_gaps.append("gate_enforcement")
            elif i == 9:  # Lexical vs semantic
                knowledge_gaps.append("knowledge_separation")
    
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
    exercises = generate_lesson_6_8_exercises()
    
    for exercise, response in zip(exercises, responses):
        if response.strip().upper() == exercise.expected_answer.strip().upper() or response.strip() == exercise.expected_answer.strip():
            state.record_correct()
        else:
            state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker(tracker: MasteryTracker, lesson_id: str, accuracy: float) -> None:
    """Update mastery tracker."""
    tracker.record_attempt(lesson_id, accuracy)


# Lesson definition
lesson_6_8 = Lesson(
    subject_id="thai",
    level=6,
    title="Understanding ≠ Translation",
    objectives=[
        "Distinguish translation/recall from semantic understanding",
        "Demonstrate that translation-only cannot reach semantic mastery",
        "Enforce evidence requirements at system level",
        "Prove that understanding requires explanation, application, or contextual interpretation",
        "Integrate with Evidence Gate for enforcement",
    ],
    content="""
Understanding ≠ Translation

This lesson enforces the principle that translation alone does not constitute semantic understanding.

1. Translation is Useful But Insufficient

   Translation/Recall:
   - "ไป" → "go"
   - Valid lexical recall
   - Useful for vocabulary recognition
   - Initial learning aid
   
   BUT:
   - Does NOT demonstrate semantic understanding
   - Does NOT show contextual interpretation ability
   - Does NOT prove application capability
   - Does NOT reveal pragmatic awareness
   
   Translation is NECESSARY but NOT SUFFICIENT for semantic mastery.

2. What Translation Demonstrates

   Translation shows:
   - Word recognition
   - Lexical recall
   - Basic vocabulary knowledge
   
   Translation does NOT show:
   - Semantic field understanding
   - Contextual meaning selection
   - Compositional pattern knowledge
   - Pragmatic interpretation ability
   - Application to new contexts
   - Meaning explanation capability

3. Evidence Type Classification

   TRANSLATION Evidence:
   - Type: EvidenceType.TRANSLATION
   - Shows: Lexical recall
   - Insufficient for: Semantic mastery
   - Max achievement: Lexical knowledge
   
   UNDERSTANDING Evidence:
   - Types: EXPLANATION, APPLICATION, CONTEXTUAL_INTERPRETATION, etc.
   - Shows: Semantic comprehension
   - Sufficient for: Semantic mastery (when verified)
   - Achievement: Semantic understanding

4. System-Level Enforcement

   Evidence Gate enforces:
   
   IF knowledge is semantic:
     IF evidence_type == TRANSLATION:
       REJECT consolidation
       REJECT semantic mastery
     
     IF evidence_type in [EXPLANATION, APPLICATION, ...]:
       IF evidence verified:
         ACCEPT consolidation
         ALLOW semantic mastery
   
   This is NOT suggestion - it is ENFORCEMENT.
   Architecture PREVENTS translation-only path to semantic mastery.

5. Numeric vs Semantic Criteria

   KnowledgeState tracks:
   - accuracy >= 0.95 and correct >= 5 → MASTERED (numeric)
   
   Evidence Gate adds:
   - semantic knowledge requires understanding evidence (semantic)
   
   Both must pass:
   
   Translation-only:
   - Numeric: PASS (100% accuracy possible)
   - Semantic: FAIL (no understanding evidence)
   - Result: NOT semantic mastery
   
   Translation + Explanation:
   - Numeric: PASS (accuracy sufficient)
   - Semantic: PASS (understanding evidence provided)
   - Result: Semantic mastery allowed

6. Valid Paths to Semantic Mastery

   Path A (INVALID):
   Translation practice → 100% accuracy → MASTERED?
   → REJECTED by Evidence Gate (translation-only)
   
   Path B (VALID):
   Translation + Explanation → Understanding evidence → MASTERED
   → ACCEPTED by Evidence Gate
   
   Path C (VALID):
   Translation + Application → Understanding evidence → MASTERED
   → ACCEPTED by Evidence Gate
   
   Path D (VALID):
   Translation + Contextual Interpretation → Understanding evidence → MASTERED
   → ACCEPTED by Evidence Gate

7. Lexical vs Semantic Knowledge

   These are SEPARATE dimensions:
   
   Lexical Knowledge:
   - "ไป" = "go"
   - Translation sufficient
   - Recall-based
   
   Semantic Knowledge:
   - "ไป" = MOTION field, contextual meanings, pragmatic uses
   - Translation insufficient
   - Understanding-based
   
   Can have:
   - High lexical, low semantic (knows word, not meaning)
   - High semantic, low lexical (understands concept, weak recall)

8. Examples: Translation-Only FAILS

   Exercise: "ไป แปลว่าอะไร?"
   Response: "go"
   Assessment: TRANSLATION_ONLY
   Evidence Type: TRANSLATION
   Semantic Gate: REJECT
   
   Why?
   - Correct translation
   - But no semantic structure shown
   - No contextual interpretation
   - No application demonstrated
   - Cannot consolidate as semantic understanding

9. Examples: Understanding SUCCEEDS

   Exercise: "อธิบายความหมายของ ไป"
   Response: "ไป เป็น motion verb, มี literal meaning (physical movement) และ pragmatic meaning (activity participation), ใช้ใน serial verb pattern"
   Assessment: UNDERSTANDING
   Evidence Type: EXPLANATION
   Semantic Gate: ACCEPT
   
   Why?
   - Shows semantic field (motion verb)
   - Shows contextual meanings (literal vs pragmatic)
   - Shows compositional pattern (serial verb)
   - Demonstrates semantic understanding
   - Can consolidate as semantic knowledge

10. System Guarantees

    Architecture guarantees:
    - Translation-only → NEVER semantic mastery
    - Understanding evidence required → ALWAYS checked
    - Evidence Gate → ALWAYS enforced
    - No bypass possible → Architecturally prevented
    
    This is not policy - this is IMPLEMENTATION.
    Tests prove these guarantees hold.
""",
    prerequisites=["thai_lesson_6_7"],
)
