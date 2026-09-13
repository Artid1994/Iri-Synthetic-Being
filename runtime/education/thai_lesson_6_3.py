"""
Thai Week 6 Lesson 6.3: Sentence Meaning (ความหมายของประโยค)

Learning Objectives:
1. Build sentence-level semantic representation using SentenceSemantics
2. Distinguish word meaning, contextual meaning, and sentence meaning
3. Identify semantic roles in sentences (agent, action, patient, property)
4. Recognize semantic relations between words
5. Understand compositional meaning (word combination → sentence meaning)
6. Provide EXPLANATION evidence (not just translation or parsing)

CRITICAL: Parsing ≠ Understanding, Translation ≠ Understanding
Sentence understanding requires evidence of semantic interpretation.
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
from runtime.knowledge_ingestion import (
    KnowledgeIngestionPipeline,
    DocumentLoader,
    KnowledgeExtractor,
    Concept,
)
from runtime.education.semantic_representation import (
    SentenceSemantics,
    SemanticMeaning,
    ContextualMeaning,
    EvidenceStatus,
    ContextType,
    UnderstandingEvidence,
    EvidenceType,
    AmbiguityPoint,
    AmbiguityType,
)


def load_data() -> Dict:
    """Load semantic vocabulary and patterns."""
    data_path = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language" / "semantic_vocabulary.json"
    return json.loads(data_path.read_text(encoding='utf-8'))


def build_sentence_semantics(sentence: str, data: Dict) -> SentenceSemantics:
    """
    Build SentenceSemantics representation from Thai sentence.
    
    Uses existing semantic patterns and word meanings.
    Does NOT guess - marks UNKNOWN/AMBIGUOUS when evidence insufficient.
    """
    words = sentence.strip().split()
    word_meanings = []
    
    # Get semantic meanings for each word
    vocab = data['semantic_vocabulary']
    for word in words:
        word_data = next((w for w in vocab if w['word'] == word), None)
        if word_data:
            # Build SemanticMeaning (simplified for available data)
            sem = SemanticMeaning(
                word=word,
                lexical_meaning=word_data.get('lexical_meaning', ''),
                semantic_field=word_data.get('semantic_field'),
                confidence=1.0,
                evidence_status=EvidenceStatus.KNOWN,
            )
            word_meanings.append(sem)
    
    # Check for known semantic patterns
    compositional_meaning = None
    evidence = []
    
    patterns = data.get('semantic_patterns', [])
    
    # Pattern 1: VERB + VERB (serial)
    if len(words) == 2:
        if all(w in ['ไป', 'มา', 'กิน'] for w in words):
            pattern = next((p for p in patterns if 'VERB + VERB' in p['pattern']), None)
            if pattern:
                compositional_meaning = f"{words[0]} + {words[1]}: {pattern['semantic_function']}"
                evidence.append(f"Serial verb pattern: {pattern['compositional_rule']}")
    
    # Pattern 2: NOUN + ADJECTIVE
    if len(words) == 2:
        noun_words = ['คน', 'น้ำ']
        adj_words = ['ดี']
        if words[0] in noun_words and words[1] in adj_words:
            pattern = next((p for p in patterns if 'NOUN + ADJECTIVE' in p['pattern']), None)
            if pattern:
                compositional_meaning = f"{words[0]} + {words[1]}: {pattern['semantic_function']}"
                evidence.append(f"Modification pattern: {pattern['compositional_rule']}")
    
    # If no pattern matched, mark as UNKNOWN
    if compositional_meaning is None and len(words) > 1:
        compositional_meaning = "UNKNOWN"
        evidence.append("No matching semantic pattern found")
    
    return SentenceSemantics(
        sentence=sentence,
        word_meanings=word_meanings,
        compositional_meaning=compositional_meaning,
        confidence=1.0 if compositional_meaning and compositional_meaning != "UNKNOWN" else 0.0,
        evidence=evidence,
    )


def generate_lesson_6_3_exercises() -> List[LearningExercise]:
    """
    Generate exercises for sentence semantics.
    
    Focus: sentence meaning, semantic roles, compositional meaning, word vs sentence meaning
    """
    exercises = []
    
    # Exercise 1: Identify sentence pattern
    exercises.append(LearningExercise(
        question="ประโยค 'ไป กิน' ใช้ pattern อะไร? (VERB+VERB/NOUN+ADJECTIVE/UNKNOWN)",
        expected_answer="VERB+VERB",
        verification_type="EXACT",
    ))
    
    # Exercise 2: Sentence meaning vs word meaning
    exercises.append(LearningExercise(
        question="ความหมายของประโยค 'ไป กิน' เหมือนกับผลรวมของ 'ไป' + 'กิน' หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    # Exercise 3: Compositional meaning
    exercises.append(LearningExercise(
        question="'ไป กิน' มี compositional meaning คืออะไร? (purpose/quality/location)",
        expected_answer="purpose",
        verification_type="EXACT",
    ))
    
    # Exercise 4: Semantic role - agent/action
    exercises.append(LearningExercise(
        question="ใน 'คน ดี' คำว่า 'คน' มี role อะไร? (entity/action/property)",
        expected_answer="entity",
        verification_type="EXACT",
    ))
    
    # Exercise 5: Semantic role - property
    exercises.append(LearningExercise(
        question="ใน 'คน ดี' คำว่า 'ดี' มี role อะไร? (entity/action/property)",
        expected_answer="property",
        verification_type="EXACT",
    ))
    
    # Exercise 6: Semantic relation
    exercises.append(LearningExercise(
        question="ใน 'คน ดี' ความสัมพันธ์ระหว่าง 'คน' กับ 'ดี' คืออะไร? (modification/action/purpose)",
        expected_answer="modification",
        verification_type="EXACT",
    ))
    
    # Exercise 7: Unknown pattern
    exercises.append(LearningExercise(
        question="ถ้าประโยคไม่ตรงกับ pattern ที่รู้จัก ควรระบุ compositional meaning เป็นอะไร? (UNKNOWN/guess/translation)",
        expected_answer="UNKNOWN",
        verification_type="EXACT",
    ))
    
    # Exercise 8: Translation vs understanding
    exercises.append(LearningExercise(
        question="การแปล 'ไป กิน' เป็น 'go eat' แสดงความเข้าใจ sentence semantics หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    # Exercise 9: Evidence type
    exercises.append(LearningExercise(
        question="การอธิบาย sentence meaning ต้องการ evidence type ใด? (TRANSLATION/EXPLANATION)",
        expected_answer="EXPLANATION",
        verification_type="EXACT",
    ))
    
    # Exercise 10: Sentence representation
    exercises.append(LearningExercise(
        question="SentenceSemantics ประกอบด้วยอะไรบ้าง? (ตอบ: words/meaning/structure)",
        expected_answer="meaning",
        verification_type="EXACT",
    ))
    
    return exercises


def assess_mastery(responses: List[str]) -> Tuple[float, str, List[str], List[str]]:
    """
    Assess sentence semantics understanding.
    
    Requires semantic explanation, not just translation or parsing.
    """
    exercises = generate_lesson_6_3_exercises()
    
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
            
            if i in [0, 2]:  # Pattern identification
                knowledge_gaps.append("pattern_identification")
            elif i in [3, 4, 5]:  # Semantic roles/relations
                knowledge_gaps.append("semantic_roles_understanding")
            elif i == 1:  # Word vs sentence meaning
                knowledge_gaps.append("compositional_understanding")
            elif i == 8:  # Evidence type
                knowledge_gaps.append("evidence_requirement_understanding")
    
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
    exercises = generate_lesson_6_3_exercises()
    
    for exercise, response in zip(exercises, responses):
        if response.strip().upper() == exercise.expected_answer.strip().upper():
            state.record_correct()
        else:
            state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker(tracker: MasteryTracker, lesson_id: str, accuracy: float) -> None:
    """Update mastery tracker."""
    tracker.record_attempt(lesson_id, accuracy)


# Lesson definition
lesson_6_3 = Lesson(
    subject_id="thai",
    level=6,
    title="Sentence Meaning (ความหมายของประโยค)",
    objectives=[
        "Build sentence-level semantic representation using SentenceSemantics",
        "Distinguish word meaning, contextual meaning, and sentence meaning",
        "Identify semantic roles (entity, action, property)",
        "Recognize semantic relations (modification, purpose, sequence)",
        "Understand compositional meaning from word combination",
        "Provide EXPLANATION evidence (not just translation or parsing)",
    ],
    content="""
Sentence Meaning (ความหมายของประโยค)

1. Word Meaning vs Sentence Meaning
   - Word: ไป = go, กิน = eat
   - Sentence: ไป กิน = go TO eat (purpose, not just two separate actions)
   - Sentence meaning ≠ sum of word meanings
   - Compositional rules create new meaning

2. Semantic Patterns
   a) VERB + VERB (serial): purpose or sequence
      - ไป กิน (go to eat): V1 provides direction/purpose for V2
      - Compositional rule: verb1.action + 'to' + verb2.action
   
   b) NOUN + ADJECTIVE: modification
      - คน ดี (good person): ADJ modifies NOUN
      - Compositional rule: noun.entity + adjective.property

3. Semantic Roles
   - Entity: thing/person (คน, น้ำ)
   - Action: verb (ไป, กิน)
   - Property: quality (ดี)
   
   In "คน ดี": คน = entity, ดี = property

4. Semantic Relations
   - Modification: NOUN + ADJ (คน ดี)
   - Purpose: VERB + VERB (ไป กิน)
   - Sequence: VERB + VERB in different context

5. Compositional Meaning
   - Meaning derived from word combination + pattern
   - Not just dictionary lookup
   - Requires understanding structural relationship

6. Unknown Patterns
   - If sentence doesn't match known patterns → UNKNOWN
   - Do NOT guess meaning
   - Mark as AMBIGUOUS or UNKNOWN

7. Translation ≠ Understanding
   - Translation: ไป กิน = "go eat"
   - Understanding: Serial verb with purpose relation, V1 directs V2
   
8. Evidence Requirement
   - EXPLANATION: Must explain semantic structure
   - Not sufficient: translation or word-by-word parsing
   - Required: compositional meaning + evidence
""",
    prerequisites=["thai_lesson_6_2"],
)
