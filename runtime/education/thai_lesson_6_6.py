"""
Thai Week 6 Lesson 6.6: Pragmatic Meaning (ความหมายเชิงปฏิบัติ)

Learning Objectives:
1. Distinguish lexical → contextual → sentence → pragmatic meaning
2. Extract pragmatic meaning from context and evidence
3. Recognize pragmatic meaning ≠ guessing speaker intention
4. Use evidence-based pragmatic interpretation
5. Reject unsupported intention attribution
6. Recognize insufficient evidence → AMBIGUOUS/UNKNOWN
7. Apply Evidence Gate to pragmatic understanding

CRITICAL: Pragmatic meaning is context-dependent interpretation, NOT mind-reading.
Evidence required: context clues, patterns, conversational structure.
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
    SentenceSemantics,
    SemanticMeaning,
    ContextualMeaning,
    ContextType,
    EvidenceStatus,
    EvidenceType,
    UnderstandingEvidence,
)


def load_data() -> Dict:
    """Load semantic vocabulary with pragmatic patterns."""
    data_path = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language" / "semantic_vocabulary.json"
    return json.loads(data_path.read_text(encoding='utf-8'))


def extract_pragmatic_meaning(
    sentence: str,
    context_clues: List[str],
    data: Dict
) -> Tuple[Optional[str], List[str], str]:
    """
    Extract pragmatic meaning from sentence with context evidence.
    
    Levels:
    1. Lexical: dictionary meaning of words
    2. Contextual: context-specific meaning
    3. Sentence: compositional meaning
    4. Pragmatic: context-dependent interpretation of USE
    
    Args:
        sentence: Thai sentence
        context_clues: List of context identifiers
        data: Vocabulary data
    
    Returns:
        (pragmatic_meaning, evidence_list, state)
        state: KNOWN, AMBIGUOUS, UNKNOWN
    """
    words = sentence.strip().split()
    vocab = data['semantic_vocabulary']
    pragmatic_patterns = data.get('pragmatic_patterns', [])
    
    if len(words) == 0:
        return (None, ["Empty sentence"], "UNKNOWN")
    
    evidence = []
    
    # Check for pragmatic patterns first (e.g., "VERB + ไหม")
    if len(words) >= 2:
        # Check "VERB + ไหม" pattern
        if words[-1] == "ไหม":
            verb = words[0]
            pattern = next((p for p in pragmatic_patterns if "ไหม" in p.get('form', '')), None)
            
            if pattern:
                literal = pattern.get('literal_meaning', '')
                pragmatic_func = pattern.get('pragmatic_function', '')
                
                # Check context to determine which pragmatic function
                if 'invitation' in context_clues or 'suggestion' in context_clues:
                    evidence.append(f"Pattern: {pattern['form']}")
                    evidence.append(f"Context: invitation/suggestion → {pragmatic_func}")
                    return (
                        f"{pragmatic_func} (invitation context)",
                        evidence,
                        "KNOWN"
                    )
                elif 'question' in context_clues:
                    evidence.append(f"Pattern: {pattern['form']}")
                    evidence.append(f"Context: question → yes/no question")
                    return (
                        f"{pragmatic_func} (question context)",
                        evidence,
                        "KNOWN"
                    )
                else:
                    # Pattern recognized but context ambiguous
                    evidence.append(f"Pattern: {pattern['form']}")
                    evidence.append(f"Ambiguous: {pragmatic_func} - context needed")
                    return (
                        None,
                        evidence,
                        "AMBIGUOUS"
                    )
    
    # Single word pragmatic interpretation
    if len(words) == 1:
        word = words[0]
        word_data = next((w for w in vocab if w['word'] == word), None)
        
        if not word_data:
            return (None, [f"Word '{word}' not in vocabulary"], "UNKNOWN")
        
        contextual_meanings = word_data.get('contextual_meanings', [])
        
        # Find PRAGMATIC contextual meaning
        pragmatic_cm = None
        literal_cm = None
        
        for cm in contextual_meanings:
            if cm.get('context_type') == 'PRAGMATIC':
                pragmatic_cm = cm
            elif cm.get('context_type') == 'LITERAL':
                literal_cm = cm
        
        if not pragmatic_cm:
            # No pragmatic meaning available
            if literal_cm:
                return (
                    None,
                    [f"Word '{word}' has no pragmatic meaning, only literal"],
                    "KNOWN"
                )
            else:
                return (None, [f"No meanings available for '{word}'"], "UNKNOWN")
        
        # Check if context matches required_context for pragmatic
        required = pragmatic_cm.get('required_context', [])
        
        if not required:
            # No specific requirement - pragmatic available
            evidence.append(f"Pragmatic meaning available: {pragmatic_cm['meaning']}")
            return (pragmatic_cm['meaning'], evidence, "KNOWN")
        
        # Check context match
        if not context_clues:
            evidence.append(f"Pragmatic requires context: {required}")
            evidence.append("No context provided")
            return (None, evidence, "AMBIGUOUS")
        
        overlap = set(context_clues) & set(required)
        if overlap:
            evidence.append(f"Context matches required: {list(overlap)}")
            evidence.append(f"Pragmatic meaning: {pragmatic_cm['meaning']}")
            return (pragmatic_cm['meaning'], evidence, "KNOWN")
        else:
            evidence.append(f"Context provided: {context_clues}")
            evidence.append(f"Pragmatic requires: {required}")
            evidence.append("No match - ambiguous")
            return (None, evidence, "AMBIGUOUS")
    
    # Multi-word sentences: build compositional then check pragmatic
    # For v1, simple composition
    word_meanings = []
    has_unknown = False
    for word in words:
        word_data = next((w for w in vocab if w['word'] == word), None)
        if word_data:
            word_meanings.append(word_data.get('lexical_meaning', word))
        else:
            word_meanings.append(f"[UNKNOWN:{word}]")
            has_unknown = True
    
    # If any word is unknown, cannot provide reliable interpretation
    if has_unknown:
        compositional = " ".join(word_meanings)
        evidence.append(f"Unknown words in sentence: {compositional}")
        evidence.append("Cannot interpret without vocabulary data")
        return (None, evidence, "UNKNOWN")
    
    compositional = " ".join(word_meanings)
    
    # Check if there's pragmatic extension beyond compositional
    # For serial verbs like "ไป กิน", pragmatic may be "go to eat" vs "go and eat"
    if len(words) == 2 and all(w in [v['word'] for v in vocab] for w in words):
        # Check semantic patterns
        patterns = data.get('semantic_patterns', [])
        
        # Check if VERB+VERB
        word1_data = next((w for w in vocab if w['word'] == words[0]), None)
        word2_data = next((w for w in vocab if w['word'] == words[1]), None)
        
        if word1_data and word2_data:
            field1 = word1_data.get('semantic_field', '')
            field2 = word2_data.get('semantic_field', '')
            
            # Check if both are motion/action
            if field1 in ['MOTION', 'ACTION'] and field2 in ['MOTION', 'ACTION']:
                # Serial verb pattern
                pattern = next((p for p in patterns if 'VERB + VERB' in p.get('pattern', '')), None)
                if pattern:
                    evidence.append(f"Pattern: {pattern['pattern']}")
                    evidence.append(f"Compositional: {compositional}")
                    
                    # Pragmatic interpretation depends on context
                    if 'purpose' in context_clues:
                        evidence.append("Context: purpose → 'to' interpretation")
                        return (f"{word_meanings[0]} to {word_meanings[1]}", evidence, "KNOWN")
                    elif 'sequence' in context_clues:
                        evidence.append("Context: sequence → 'and then' interpretation")
                        return (f"{word_meanings[0]} and then {word_meanings[1]}", evidence, "KNOWN")
                    else:
                        evidence.append("Ambiguous: purpose or sequence not specified")
                        return (None, evidence, "AMBIGUOUS")
    
    # Default: compositional only, no clear pragmatic extension
    evidence.append(f"Compositional: {compositional}")
    evidence.append("No pragmatic pattern identified")
    return (compositional, evidence, "KNOWN")


def generate_lesson_6_6_exercises() -> List[LearningExercise]:
    """
    Generate exercises for pragmatic meaning.
    
    Focus: lexical→contextual→sentence→pragmatic distinction, evidence requirements
    """
    exercises = []
    
    # Exercise 1: Lexical vs Pragmatic
    exercises.append(LearningExercise(
        question="'ดี' lexical meaning vs pragmatic meaning: lexical คือ 'good quality', pragmatic คือ? (agreement/movement)",
        expected_answer="agreement",
        verification_type="EXACT",
    ))
    
    # Exercise 2: Pragmatic pattern recognition
    exercises.append(LearningExercise(
        question="'ไป ไหม' ตรงกับ pragmatic pattern ใด? (VERB+ไหม/NOUN+ADJ)",
        expected_answer="VERB+ไหม",
        verification_type="EXACT",
    ))
    
    # Exercise 3: Context-dependent pragmatic
    exercises.append(LearningExercise(
        question="'ไป ไหม' + context(invitation) → pragmatic meaning เป็น? (question/invitation)",
        expected_answer="invitation",
        verification_type="EXACT",
    ))
    
    # Exercise 4: Insufficient context
    exercises.append(LearningExercise(
        question="'ไป ไหม' ไม่มี context → state เป็น? (KNOWN/AMBIGUOUS/UNKNOWN)",
        expected_answer="AMBIGUOUS",
        verification_type="EXACT",
    ))
    
    # Exercise 5: Pragmatic vs literal
    exercises.append(LearningExercise(
        question="'ไป' + context(activity) ให้ LITERAL หรือ PRAGMATIC meaning? (LITERAL/PRAGMATIC)",
        expected_answer="PRAGMATIC",
        verification_type="EXACT",
    ))
    
    # Exercise 6: Evidence requirement
    exercises.append(LearningExercise(
        question="Pragmatic interpretation ต้องการ evidence type ใด? (CONTEXTUAL_INTERPRETATION/TRANSLATION)",
        expected_answer="CONTEXTUAL_INTERPRETATION",
        verification_type="EXACT",
    ))
    
    # Exercise 7: Mind-reading rejection
    exercises.append(LearningExercise(
        question="ถ้าไม่มี context evidence สามารถ guess speaker intention ได้หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    # Exercise 8: Pragmatic meaning levels
    exercises.append(LearningExercise(
        question="ลำดับการตีความความหมาย: Lexical → ? → Sentence → Pragmatic (Contextual/Phonological)",
        expected_answer="Contextual",
        verification_type="EXACT",
    ))
    
    # Exercise 9: Unsupported intention
    exercises.append(LearningExercise(
        question="'ดี' + context(conversational) แต่ไม่มี evidence ว่าเป็น agreement ควรเป็น KNOWN หรือ AMBIGUOUS? (KNOWN/AMBIGUOUS)",
        expected_answer="AMBIGUOUS",
        verification_type="EXACT",
    ))
    
    # Exercise 10: Evidence Gate requirement
    exercises.append(LearningExercise(
        question="Pragmatic understanding ต้องผ่าน Evidence Gate หรือไม่? (YES/NO)",
        expected_answer="YES",
        verification_type="EXACT",
    ))
    
    return exercises


def assess_mastery(responses: List[str]) -> Tuple[float, str, List[str], List[str]]:
    """
    Assess pragmatic meaning understanding.
    
    Requires demonstration of evidence-based pragmatic interpretation.
    """
    exercises = generate_lesson_6_6_exercises()
    
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
            
            if i in [0, 4, 7]:  # Lexical vs pragmatic
                knowledge_gaps.append("lexical_pragmatic_distinction")
            elif i in [1, 2]:  # Pattern recognition
                knowledge_gaps.append("pragmatic_pattern_recognition")
            elif i in [3, 8]:  # Context sufficiency
                knowledge_gaps.append("context_evidence_requirement")
            elif i in [5, 9]:  # Evidence requirements
                knowledge_gaps.append("evidence_gate_understanding")
            elif i in [6]:  # Mind-reading rejection
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
    exercises = generate_lesson_6_6_exercises()
    
    for exercise, response in zip(exercises, responses):
        if response.strip().upper() == exercise.expected_answer.strip().upper() or response.strip() == exercise.expected_answer.strip():
            state.record_correct()
        else:
            state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker(tracker: MasteryTracker, lesson_id: str, accuracy: float) -> None:
    """Update mastery tracker."""
    tracker.record_attempt(lesson_id, accuracy)


# Lesson definition
lesson_6_6 = Lesson(
    subject_id="thai",
    level=6,
    title="Pragmatic Meaning (ความหมายเชิงปฏิบัติ)",
    objectives=[
        "Distinguish lexical → contextual → sentence → pragmatic meaning",
        "Extract pragmatic meaning from context and evidence",
        "Recognize pragmatic meaning ≠ guessing speaker intention",
        "Use evidence-based pragmatic interpretation",
        "Reject unsupported intention attribution",
        "Recognize insufficient evidence → AMBIGUOUS/UNKNOWN",
        "Apply Evidence Gate to pragmatic understanding",
    ],
    content="""
Pragmatic Meaning (ความหมายเชิงปฏิบัติ)

1. Four Levels of Meaning
   Lexical → Contextual → Sentence (Compositional) → Pragmatic
   
   Example: "ไป ไหม"
   - Lexical: "ไป" = go, "ไหม" = question particle
   - Contextual: "ไป" in this context = physical movement
   - Sentence: "go + question" = asking about going
   - Pragmatic: question vs invitation (depends on context)

2. Pragmatic Meaning Definition
   Context-dependent interpretation of language USE
   - NOT the words themselves
   - NOT speaker's hidden intention
   - What the utterance DOES in context (speech act)
   
3. Pragmatic vs Mind-Reading
   VALID: "ไป ไหม" + invitation context → invitation interpretation
   INVALID: "ไป ไหม" + no context → "must be invitation because..."
   
   Pragmatic interpretation requires EVIDENCE:
   - Context clues (conversational structure, situation)
   - Pragmatic patterns (VERB+ไหม, response patterns)
   - Prior conversational turns
   
   NO evidence → AMBIGUOUS, NOT guessed interpretation

4. Pragmatic Patterns (from semantic_vocabulary.json)
   
   Pattern: "VERB + ไหม"
   - Literal: VERB + question particle
   - Pragmatic functions:
     * Yes/no question: "ไป ไหม" (Will you go?)
     * Invitation: "ไป ไหม" (Shall we go?)
   - Context determines which
   
5. Single Word Pragmatic Meaning
   
   "ดี" (good):
   - Lexical: good quality
   - Contextual (LITERAL): good quality attribute (คน ดี)
   - Contextual (PRAGMATIC): agreement/acknowledgment in conversation
   
   Context required:
   - conversational/response context → PRAGMATIC
   - noun context → LITERAL

6. Evidence Requirements
   
   Pragmatic understanding requires:
   - Evidence Type: CONTEXTUAL_INTERPRETATION
   - Context clues documented
   - Pattern identification
   - Cannot be translation alone
   - Cannot be guessing
   
   Evidence Gate enforces this for consolidation.

7. Insufficient Evidence
   
   Cases:
   - No context provided → AMBIGUOUS
   - Context doesn't match pattern requirements → AMBIGUOUS
   - Conflicting context clues → AMBIGUOUS
   - Unknown pattern → UNKNOWN
   
   Do NOT force interpretation without evidence.

8. Pragmatic Interpretation Process
   
   Step 1: Extract lexical meanings
   Step 2: Identify contextual meanings for each word
   Step 3: Build compositional (sentence) meaning
   Step 4: Check for pragmatic patterns
   Step 5: Match context clues with pattern requirements
   Step 6: Select pragmatic interpretation IF evidence sufficient
   Step 7: Return AMBIGUOUS if insufficient, UNKNOWN if no data
   
   Evidence list must document each step.

9. Example: "ไป ไหม" with invitation context
   
   Evidence:
   - Pattern recognized: VERB+ไหม
   - Pragmatic function: yes/no question or invitation
   - Context: invitation/suggestion provided
   - Match: invitation context matches pattern option
   - Interpretation: invitation (Shall we go?)
   - Confidence: KNOWN
   
10. Evidence Gate Integration
    
    Pragmatic understanding is semantic knowledge.
    Must provide understanding evidence (not translation).
    Must pass Evidence Gate for consolidation.
    Provenance preserved throughout.
""",
    prerequisites=["thai_lesson_6_5"],
)
