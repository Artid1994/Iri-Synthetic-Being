"""
Thai Week 6 Lesson 6.7: Thai → Internal Semantic Representation

Learning Objectives:
1. Convert Thai input to complete internal semantic representation
2. Build all semantic layers: lexical → contextual → compositional → pragmatic
3. Track uncertainty at each level (KNOWN/AMBIGUOUS/UNKNOWN)
4. Preserve evidence and provenance throughout
5. Integrate with Evidence Gate for consolidation
6. Recognize parsing ≠ understanding, translation ≠ understanding

CRITICAL: This is the integration lesson combining 6.1-6.6 mechanisms.
Must produce verifiable semantic representations, not guesses.
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
    ContextualMeaning,
    SentenceSemantics,
    ContextType,
    EvidenceStatus,
    AmbiguityPoint,
    AmbiguityType,
    UnderstandingEvidence,
    EvidenceType,
)

# Import existing functions from previous lessons
from runtime.education.thai_lesson_6_5 import select_interpretation_with_context
from runtime.education.thai_lesson_6_6 import extract_pragmatic_meaning


def load_data() -> Dict:
    """Load semantic vocabulary and patterns."""
    data_path = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language" / "semantic_vocabulary.json"
    return json.loads(data_path.read_text(encoding='utf-8'))


def thai_to_semantic_representation(
    thai_input: str,
    context_clues: Optional[List[str]] = None,
    data: Optional[Dict] = None
) -> Tuple[SentenceSemantics, str, List[str]]:
    """
    Convert Thai input to complete internal semantic representation.

    Builds all layers:
    1. Lexical meanings (word-level)
    2. Contextual meanings (context-dependent)
    3. Compositional meaning (sentence-level)
    4. Pragmatic meaning (when evidence supports)

    Args:
        thai_input: Thai sentence/phrase
        context_clues: Optional context information
        data: Vocabulary/pattern data (loads if not provided)

    Returns:
        (SentenceSemantics, state, evidence_trail)
        state: KNOWN, AMBIGUOUS, UNKNOWN
        evidence_trail: List of evidence strings documenting interpretation
    """
    if data is None:
        data = load_data()

    if context_clues is None:
        context_clues = []

    thai_input = thai_input.strip()
    if not thai_input:
        return (
            SentenceSemantics(sentence="", confidence=0.0),
            "UNKNOWN",
            ["Empty input"]
        )

    words = thai_input.split()
    vocab = data['semantic_vocabulary']
    patterns = data.get('semantic_patterns', [])

    evidence_trail = []
    evidence_trail.append(f"Input: {thai_input}")
    evidence_trail.append(f"Context: {context_clues if context_clues else 'none'}")

    # Layer 1: Lexical meanings
    word_meanings = []
    unknown_words = []

    for word in words:
        word_data = next((w for w in vocab if w['word'] == word), None)

        if not word_data:
            unknown_words.append(word)
            # Create placeholder SemanticMeaning for unknown word
            sem = SemanticMeaning(
                word=word,
                lexical_meaning=f"[UNKNOWN]",
                semantic_field=None,
                confidence=0.0,
                evidence_status=EvidenceStatus.UNKNOWN,
            )
            word_meanings.append(sem)
        else:
            # Build SemanticMeaning from vocabulary data
            contextual_meanings = []
            for cm_data in word_data.get('contextual_meanings', []):
                cm = ContextualMeaning(
                    context_type=ContextType[cm_data['context_type']],
                    meaning=cm_data['meaning'],
                    required_context=cm_data.get('required_context', []),
                    examples=cm_data.get('examples', []),
                    confidence=cm_data.get('confidence', 1.0),
                    data_status=EvidenceStatus[cm_data.get('data_status', 'KNOWN')],
                )
                contextual_meanings.append(cm)

            sem = SemanticMeaning(
                word=word,
                lexical_meaning=word_data.get('lexical_meaning', ''),
                semantic_field=word_data.get('semantic_field'),
                contextual_meanings=contextual_meanings,
                ambiguity_level=word_data.get('ambiguity_level', 'UNAMBIGUOUS'),
                confidence=word_data.get('confidence', 1.0),
                evidence_status=EvidenceStatus.KNOWN,
            )
            word_meanings.append(sem)

    evidence_trail.append(f"Lexical: {len(word_meanings)} words, {len(unknown_words)} unknown")

    # If any unknown words, cannot build reliable representation
    if unknown_words:
        evidence_trail.append(f"Unknown words: {unknown_words}")
        return (
            SentenceSemantics(
                sentence=thai_input,
                word_meanings=word_meanings,
                compositional_meaning=None,
                pragmatic_meaning=None,
                confidence=0.0,
                evidence=evidence_trail,
            ),
            "UNKNOWN",
            evidence_trail
        )

    # Layer 2: Contextual meanings (use existing mechanism from 6.5)
    contextual_interpretations = []
    ambiguity_points = []

    for i, word in enumerate(words):
        # Check if word has multiple contextual meanings
        sem = word_meanings[i]
        if len(sem.contextual_meanings) > 1:
            # Use context selection mechanism
            selected_meaning, reason, state = select_interpretation_with_context(
                word, context_clues, data
            )

            if state == "AMBIGUOUS":
                # Track ambiguity
                possible = [cm.meaning for cm in sem.contextual_meanings]
                ambiguity_points.append(AmbiguityPoint(
                    location=f"word:{i}:{word}",
                    ambiguity_type=AmbiguityType.LEXICAL,
                    possible_interpretations=possible,
                    resolution_required=True,
                    resolution_strategy="CONTEXT",
                ))
                evidence_trail.append(f"Ambiguous: {word} - {len(possible)} meanings")
            elif state == "KNOWN" and selected_meaning:
                contextual_interpretations.append(f"{word}={selected_meaning}")
                evidence_trail.append(f"Contextual: {word} → {selected_meaning[:30]}")
        else:
            # Single meaning
            if sem.contextual_meanings:
                contextual_interpretations.append(f"{word}={sem.contextual_meanings[0].meaning}")

    # Load basic grammar patterns for compositional semantics
    from pathlib import Path
    data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
    grammar_path = data_dir / 'basic_grammar.json'
    patterns = []
    if grammar_path.exists():
        grammar_data = json.loads(grammar_path.read_text())
        patterns = grammar_data.get('compositional_patterns', [])

    # Layer 3: Compositional meaning (sentence-level patterns)
    compositional_meaning = None
    compositional_evidence = []

    # Enhanced pattern matching for compositional semantics
    if len(words) >= 2:
        # Get semantic fields for all words
        word_data = [next((w for w in vocab if w['word'] == word), None) for word in words]
        fields = [wd.get('semantic_field', '') if wd else '' for wd in word_data]

        # 3-word patterns (SVO, etc.)
        if len(words) >= 3 and word_data[0] and word_data[1] and word_data[2]:
            # PRONOUN + VERB-like + PRONOUN (SVO)
            verb_like = ['MOTION', 'ACTION', 'EMOTION', 'PREFERENCE', 'STATE', 'POSSESSION']
            if fields[0] == 'PRONOUN' and fields[1] in verb_like and fields[2] == 'PRONOUN':
                pattern = next((p for p in patterns if 'PRONOUN + VERB + PRONOUN' in p.get('pattern', '')), None)
                if pattern:
                    compositional_meaning = pattern['semantic_function']
                    compositional_evidence.append(f"Pattern: {pattern['pattern']}")
                    evidence_trail.append(f"Compositional: {pattern['pattern']}")

        # 2-word patterns
        if compositional_meaning is None and len(words) >= 2 and word_data[0] and word_data[1]:
            verb_like = ['MOTION', 'ACTION', 'EMOTION', 'PREFERENCE', 'STATE', 'POSSESSION']

            # NEGATION + VERB
            if fields[0] == 'NEGATION' and fields[1] in verb_like:
                pattern = next((p for p in patterns if 'NEGATION + VERB' in p.get('pattern', '')), None)
                if pattern:
                    compositional_meaning = pattern['semantic_function']
                    compositional_evidence.append(f"Pattern: {pattern['pattern']}")
                    evidence_trail.append(f"Compositional: {pattern['pattern']}")

            # VERB + VERB (serial verbs)
            elif fields[0] in verb_like and fields[1] in verb_like:
                pattern = next((p for p in patterns if 'VERB + VERB' in p.get('pattern', '')), None)
                if pattern:
                    compositional_meaning = pattern['semantic_function']
                    compositional_evidence.append(f"Pattern: {pattern['pattern']}")
                    evidence_trail.append(f"Compositional: {pattern['pattern']}")

            # NOUN/TIME + DEMONSTRATIVE
            elif fields[0] in ['PERSON', 'OBJECT', 'FOOD', 'TIME'] and fields[1] == 'DEMONSTRATIVE':
                pattern = next((p for p in patterns if 'NOUN + DEMONSTRATIVE' in p.get('pattern', '')), None)
                if pattern:
                    compositional_meaning = pattern['semantic_function']
                    compositional_evidence.append(f"Pattern: {pattern['pattern']}")
                    evidence_trail.append(f"Compositional: {pattern['pattern']}")

            # VERB + INTERROGATIVE
            elif fields[0] in verb_like and fields[1] == 'INTERROGATIVE':
                pattern = next((p for p in patterns if 'VERB + INTERROGATIVE' in p.get('pattern', '')), None)
                if pattern:
                    compositional_meaning = pattern['semantic_function']
                    compositional_evidence.append(f"Pattern: {pattern['pattern']}")
                    evidence_trail.append(f"Compositional: {pattern['pattern']}")

            # NOUN + ADJECTIVE
            elif fields[0] in ['PERSON', 'OBJECT', 'FOOD'] and fields[1] in ['QUALITY', 'NATIONALITY']:
                pattern = next((p for p in patterns if 'NOUN + ADJECTIVE' in p.get('pattern', '')), None)
                if pattern:
                    compositional_meaning = pattern['semantic_function']
                    compositional_evidence.append(f"Pattern: {pattern['pattern']}")
                    evidence_trail.append(f"Compositional: {pattern['pattern']}")

    if compositional_meaning is None and len(words) > 1:
        evidence_trail.append("Compositional: No matching pattern")

    # Layer 4: Pragmatic meaning (use existing mechanism from 6.6)
    pragmatic_meaning = None
    pragmatic_evidence = []

    if context_clues:
        # Try to extract pragmatic meaning
        prag_result, prag_ev, prag_state = extract_pragmatic_meaning(
            thai_input, context_clues, data
        )

        if prag_state == "KNOWN" and prag_result:
            pragmatic_meaning = prag_result
            pragmatic_evidence = prag_ev
            evidence_trail.append(f"Pragmatic: {prag_result[:40]}")
        elif prag_state == "AMBIGUOUS":
            evidence_trail.append("Pragmatic: ambiguous without sufficient context")
            # Track pragmatic ambiguity if not already tracked at lexical level
            if not any(ap.ambiguity_type == AmbiguityType.PRAGMATIC for ap in ambiguity_points):
                ambiguity_points.append(AmbiguityPoint(
                    location="sentence:pragmatic",
                    ambiguity_type=AmbiguityType.PRAGMATIC,
                    possible_interpretations=["interpretation depends on context"],
                    resolution_required=True,
                    resolution_strategy="CONTEXT",
                ))
    else:
        evidence_trail.append("Pragmatic: no context provided")

    # Determine overall state
    if ambiguity_points:
        overall_state = "AMBIGUOUS"
        evidence_trail.append(f"Overall: AMBIGUOUS ({len(ambiguity_points)} points)")
    elif not compositional_meaning and len(words) > 1:
        overall_state = "AMBIGUOUS"
        evidence_trail.append("Overall: AMBIGUOUS (no compositional pattern)")
    else:
        overall_state = "KNOWN"
        evidence_trail.append("Overall: KNOWN")

    # Calculate confidence
    if overall_state == "KNOWN":
        confidence = 0.9
    elif overall_state == "AMBIGUOUS":
        confidence = 0.5
    else:
        confidence = 0.0

    # Build complete SentenceSemantics
    sentence_sem = SentenceSemantics(
        sentence=thai_input,
        word_meanings=word_meanings,
        compositional_meaning=compositional_meaning,
        pragmatic_meaning=pragmatic_meaning,
        ambiguity_points=ambiguity_points,
        confidence=confidence,
        evidence=evidence_trail + compositional_evidence + pragmatic_evidence,
    )

    return (sentence_sem, overall_state, evidence_trail)


def generate_lesson_6_7_exercises() -> List[LearningExercise]:
    """
    Generate exercises for Thai → Internal Semantic Representation.

    Focus: complete representation, all layers, uncertainty tracking, evidence
    """
    exercises = []

    # Exercise 1: Representation completeness
    exercises.append(LearningExercise(
        question="Internal representation ต้องมีกี่ layers? (2/3/4)",
        expected_answer="4",
        verification_type="EXACT",
    ))

    # Exercise 2: Layer identification
    exercises.append(LearningExercise(
        question="4 layers คือ: Lexical, ?, Compositional, Pragmatic (Contextual/Phonological)",
        expected_answer="Contextual",
        verification_type="EXACT",
    ))

    # Exercise 3: Lexical layer
    exercises.append(LearningExercise(
        question="Lexical layer เก็บอะไร? (dictionary meaning/sentence meaning)",
        expected_answer="dictionary meaning",
        verification_type="EXACT",
    ))

    # Exercise 4: Unknown word handling
    exercises.append(LearningExercise(
        question="ถ้ามีคำที่ unknown representation ควรเป็น KNOWN หรือ UNKNOWN? (KNOWN/UNKNOWN)",
        expected_answer="UNKNOWN",
        verification_type="EXACT",
    ))

    # Exercise 5: Ambiguity tracking
    exercises.append(LearningExercise(
        question="Ambiguity ต้องถูก track ไว้ใน representation หรือถูกลบทิ้ง? (track/ลบ)",
        expected_answer="track",
        verification_type="EXACT",
    ))

    # Exercise 6: Parsing vs Understanding
    exercises.append(LearningExercise(
        question="Parsing Thai sentence = Understanding หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))

    # Exercise 7: Translation vs Understanding
    exercises.append(LearningExercise(
        question="Translation = Understanding หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))

    # Exercise 8: Evidence requirement
    exercises.append(LearningExercise(
        question="Semantic representation ต้องมี evidence หรือไม่? (YES/NO)",
        expected_answer="YES",
        verification_type="EXACT",
    ))

    # Exercise 9: Pragmatic layer requirement
    exercises.append(LearningExercise(
        question="Pragmatic layer ต้องการอะไร? (context evidence/imagination)",
        expected_answer="context evidence",
        verification_type="EXACT",
    ))

    # Exercise 10: Representation vs Translation
    exercises.append(LearningExercise(
        question="Internal representation เหมือนกับ translation หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))

    return exercises


def assess_mastery(responses: List[str]) -> Tuple[float, str, List[str], List[str]]:
    """
    Assess Thai → Internal Representation understanding.

    Requires demonstration of complete representation building.
    """
    exercises = generate_lesson_6_7_exercises()

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

            if i in [0, 1, 2]:  # Representation structure
                knowledge_gaps.append("representation_structure")
            elif i in [3, 4]:  # Uncertainty handling
                knowledge_gaps.append("uncertainty_tracking")
            elif i in [5, 6, 7]:  # Understanding vs other operations
                knowledge_gaps.append("understanding_distinction")
            elif i in [8, 9]:  # Evidence requirements
                knowledge_gaps.append("evidence_requirements")

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
    exercises = generate_lesson_6_7_exercises()

    for exercise, response in zip(exercises, responses):
        if response.strip().upper() == exercise.expected_answer.strip().upper() or response.strip() == exercise.expected_answer.strip():
            state.record_correct()
        else:
            state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker(tracker: MasteryTracker, lesson_id: str, accuracy: float) -> None:
    """Update mastery tracker."""
    tracker.record_attempt(lesson_id, accuracy)


# Lesson definition
lesson_6_7 = Lesson(
    subject_id="thai",
    level=6,
    title="Thai → Internal Semantic Representation",
    objectives=[
        "Convert Thai input to complete internal semantic representation",
        "Build all semantic layers: lexical → contextual → compositional → pragmatic",
        "Track uncertainty at each level (KNOWN/AMBIGUOUS/UNKNOWN)",
        "Preserve evidence and provenance throughout",
        "Integrate with Evidence Gate for consolidation",
        "Recognize parsing ≠ understanding, translation ≠ understanding",
    ],
    content="""
Thai → Internal Semantic Representation

This lesson integrates all mechanisms from 6.1-6.6 to build complete semantic representations.

1. Four-Layer Architecture

   Thai Input
   ↓
   Layer 1: LEXICAL MEANINGS
   - Dictionary meanings of individual words
   - Semantic fields (MOTION, ACTION, QUALITY, etc.)
   - Unknown words marked as UNKNOWN
   ↓
   Layer 2: CONTEXTUAL MEANINGS
   - Context-dependent word interpretations
   - Uses context selection mechanism (6.5)
   - Tracks ambiguity when multiple interpretations possible
   ↓
   Layer 3: COMPOSITIONAL MEANING
   - Sentence-level meaning from word combination
   - Semantic patterns (VERB+VERB, NOUN+ADJECTIVE)
   - Structural interpretation
   ↓
   Layer 4: PRAGMATIC MEANING
   - Context-dependent use/function
   - Uses pragmatic extraction mechanism (6.6)
   - Only when context evidence supports
   ↓
   INTERNAL SEMANTIC REPRESENTATION
   - Complete SentenceSemantics object
   - All layers preserved
   - Uncertainty tracked
   - Evidence documented

2. Representation Structure

   SentenceSemantics contains:
   - sentence: original Thai input
   - word_meanings: List[SemanticMeaning] (lexical + contextual)
   - compositional_meaning: sentence-level pattern meaning
   - pragmatic_meaning: context-dependent interpretation (when applicable)
   - ambiguity_points: List[AmbiguityPoint] (tracks all ambiguities)
   - confidence: 0.0-1.0 (based on state)
   - evidence: List[str] (full evidence trail)

3. State Determination

   KNOWN:
   - All words in vocabulary
   - Compositional pattern identified
   - No unresolved ambiguity
   - Confidence: 0.9

   AMBIGUOUS:
   - Multiple interpretations possible
   - Context insufficient to resolve
   - Ambiguity tracked in ambiguity_points
   - Confidence: 0.5

   UNKNOWN:
   - Unknown words present
   - No vocabulary data
   - Cannot build reliable representation
   - Confidence: 0.0

4. Uncertainty Preservation

   Ambiguity is PART of representation, not removed:
   - Lexical ambiguity → AmbiguityPoint
   - Pragmatic ambiguity → AmbiguityPoint
   - Multiple interpretations preserved
   - Resolution strategy documented
   - Never forced resolution without evidence

5. Evidence Trail

   Every interpretation step documented:
   - Input + context
   - Lexical lookups
   - Context selection
   - Pattern matching
   - Pragmatic extraction
   - State determination
   - All evidence preserved in SentenceSemantics.evidence

6. Parsing ≠ Understanding

   Thai → Representation is NOT:
   - Just tokenization
   - Just word lookup
   - Just pattern matching
   - Just translation

   It REQUIRES:
   - Semantic interpretation at all layers
   - Context integration
   - Ambiguity tracking
   - Evidence documentation
   - Understanding verification

7. Translation ≠ Understanding

   Internal representation is NOT translation:
   - Translation: Thai → English words
   - Representation: Thai → Semantic structures

   Representation includes:
   - Semantic fields
   - Contextual meanings
   - Compositional rules
   - Pragmatic functions
   - Ambiguity points
   - Evidence trails

   Translation alone cannot produce this.

8. Example: "ไป กิน"

   Input: "ไป กิน"
   Context: ["purpose"]

   Layer 1 (Lexical):
   - ไป: go (MOTION)
   - กิน: eat (ACTION)

   Layer 2 (Contextual):
   - ไป: physical movement (LITERAL)
   - กิน: consume food (LITERAL)

   Layer 3 (Compositional):
   - Pattern: VERB + VERB (serial)
   - Function: purpose or sequence

   Layer 4 (Pragmatic):
   - Context: purpose
   - Meaning: "go to eat" (purpose interpretation)

   State: KNOWN
   Confidence: 0.9
   Evidence: ["Pattern: VERB+VERB", "Context: purpose", ...]

9. Example: "ดี"

   Input: "ดี"
   Context: []

   Layer 1 (Lexical):
   - ดี: good (QUALITY)

   Layer 2 (Contextual):
   - LITERAL: good quality
   - PRAGMATIC: agreement
   - Ambiguity: 2 interpretations, no context

   Layer 3 (Compositional):
   - N/A (single word)

   Layer 4 (Pragmatic):
   - Context insufficient
   - Cannot determine LITERAL vs PRAGMATIC

   State: AMBIGUOUS
   Confidence: 0.5
   Ambiguity Points: [
     {location: "word:0:ดี", type: LEXICAL, interpretations: [...]}
   ]
   Evidence: ["Ambiguous: 2 meanings, no context", ...]

10. Evidence Gate Integration

    Semantic representation can be consolidated to Memory ONLY if:
    - Understanding evidence provided (not just translation)
    - Evidence type: EXPLANATION, APPLICATION, CONTEXTUAL_INTERPRETATION, etc.
    - Evidence verified
    - State: KNOWN or MILDLY_AMBIGUOUS
    - Confidence >= 0.7

    Translation-only → rejected by Evidence Gate
    Parsing-only → rejected by Evidence Gate

    Representation + Understanding Evidence → consolidation allowed
""",
    prerequisites=["thai_lesson_6_6"],
)
