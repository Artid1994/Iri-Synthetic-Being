"""
Thai Week 6 Lesson 6.2: Word Meaning in Context (ความหมายของคำในบริบท)

Learning Objectives:
1. Understand same word can have different meanings in different contexts
2. Identify required context for interpretation
3. Distinguish LITERAL from PRAGMATIC contextual meanings
4. Recognize when context is insufficient (AMBIGUOUS/UNKNOWN)
5. Provide CONTEXTUAL_INTERPRETATION evidence (not just translation)

CRITICAL: This lesson integrates Knowledge Ingestion Pipeline end-to-end.
SOURCE → EXTRACT → LEARN → EVIDENCE → GATE → CONSOLIDATE
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Dict, Optional
import json
import time

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
    Provenance,
    SourceType,
)
from runtime.education.semantic_representation import (
    SemanticMeaning,
    ContextualMeaning,
    EvidenceStatus,
    ContextType,
    UnderstandingEvidence,
    EvidenceType,
)


def load_data() -> Dict:
    """Load semantic vocabulary with contextual meanings."""
    data_path = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language" / "semantic_vocabulary.json"
    return json.loads(data_path.read_text(encoding='utf-8'))


def generate_lesson_6_2_exercises() -> List[LearningExercise]:
    """
    Generate exercises for word meaning in context.
    
    Focus: contextual meaning, required context, ambiguity detection
    """
    data = load_data()
    
    exercises = []
    
    # Exercise 1: Context changes meaning (ไป)
    # LITERAL: physical movement vs PRAGMATIC: attend/participate
    exercises.append(LearningExercise(
        question="'ไป บ้าน' ใช้ความหมายแบบ LITERAL หรือ PRAGMATIC?",
        expected_answer="LITERAL",
        verification_type="EXACT",
    ))
    
    # Exercise 2: Context changes meaning (ไป)
    exercises.append(LearningExercise(
        question="'ไป เรียน' ใช้ความหมายแบบ LITERAL หรือ PRAGMATIC?",
        expected_answer="PRAGMATIC",
        verification_type="EXACT",
    ))
    
    # Exercise 3: Required context (ไป + PRAGMATIC)
    exercises.append(LearningExercise(
        question="'ไป เรียน' (PRAGMATIC) ต้องการบริบทประเภทใด? (activity/location/time)",
        expected_answer="activity",
        verification_type="EXACT",
    ))
    
    # Exercise 4: Context changes meaning (ดี)
    exercises.append(LearningExercise(
        question="'คน ดี' ใช้ความหมายแบบ LITERAL หรือ PRAGMATIC?",
        expected_answer="LITERAL",
        verification_type="EXACT",
    ))
    
    # Exercise 5: Context changes meaning (ดี as response)
    exercises.append(LearningExercise(
        question="'ดี' (ตอบรับข้อเสนอ) ใช้ความหมายแบบ LITERAL หรือ PRAGMATIC?",
        expected_answer="PRAGMATIC",
        verification_type="EXACT",
    ))
    
    # Exercise 6: Insufficient context → AMBIGUOUS
    exercises.append(LearningExercise(
        question="ถ้าเจอคำว่า 'ดี' โดยไม่มีบริบท ควรระบุว่า KNOWN หรือ AMBIGUOUS?",
        expected_answer="AMBIGUOUS",
        verification_type="EXACT",
    ))
    
    # Exercise 7: Translation vs contextual understanding
    exercises.append(LearningExercise(
        question="การแปล 'ไป' เป็น 'go' บอกความหมายตามบริบทได้หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    # Exercise 8: Evidence type needed
    exercises.append(LearningExercise(
        question="การอธิบายความหมายตามบริบทต้องการ evidence type ใด? (TRANSLATION/CONTEXTUAL_INTERPRETATION)",
        expected_answer="CONTEXTUAL_INTERPRETATION",
        verification_type="EXACT",
    ))
    
    # Exercise 9: Same word, different context understanding
    exercises.append(LearningExercise(
        question="คำว่า 'ไป' มีความหมายกี่แบบใน semantic_vocabulary? (1/2/3)",
        expected_answer="2",
        verification_type="EXACT",
    ))
    
    # Exercise 10: Context importance
    exercises.append(LearningExercise(
        question="บริบทมีความสำคัญต่อความหมายของคำหรือไม่? (YES/NO)",
        expected_answer="YES",
        verification_type="EXACT",
    ))
    
    return exercises


def assess_mastery(responses: List[str]) -> Tuple[float, str, List[str], List[str]]:
    """
    Assess contextual meaning understanding.
    
    Requires contextual interpretation ability, not just translation.
    """
    exercises = generate_lesson_6_2_exercises()
    
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
            
            # Identify knowledge gaps
            if i in [0, 1, 3, 4]:  # Context type identification
                knowledge_gaps.append("context_type_identification")
            elif i == 2:  # Required context
                knowledge_gaps.append("required_context_understanding")
            elif i == 5:  # Ambiguity recognition
                knowledge_gaps.append("ambiguity_recognition")
            elif i == 6:  # Translation limitation
                knowledge_gaps.append("translation_limitation_understanding")
            elif i == 7:  # Evidence type
                knowledge_gaps.append("evidence_type_understanding")
    
    accuracy = correct / len(exercises)
    
    if accuracy >= 0.9:
        mastery_level = "MASTERED"
    elif accuracy >= 0.7:
        mastery_level = "CAN_USE"
    else:
        mastery_level = "LEARNING"
    
    knowledge_gaps = list(set(knowledge_gaps))
    
    return accuracy, mastery_level, error_patterns, knowledge_gaps


def update_knowledge_state(
    state: KnowledgeState,
    responses: List[str],
) -> None:
    """Update knowledge state from assessment."""
    exercises = generate_lesson_6_2_exercises()
    
    for exercise, response in zip(exercises, responses):
        response = response.strip()
        expected = exercise.expected_answer.strip()
        
        if response.upper() == expected.upper():
            state.record_correct()
        else:
            state.record_error(ErrorType.INCORRECT)


def update_mastery_tracker(
    tracker: MasteryTracker,
    lesson_id: str,
    accuracy: float,
) -> None:
    """Update mastery tracker."""
    tracker.record_attempt(lesson_id, accuracy)


def consolidate_semantic_knowledge_with_pipeline(
    word: str,
    memory: Memory,
    knowledge_state: KnowledgeState,
    understanding_evidence: Optional[UnderstandingEvidence] = None,
) -> bool:
    """
    CRITICAL: Use actual Knowledge Ingestion Pipeline + Evidence Gate.
    
    This demonstrates end-to-end integration:
    SOURCE → EXTRACT → LEARN → EVIDENCE → GATE → CONSOLIDATE
    
    Returns: True if consolidated, False if rejected by Evidence Gate
    """
    # Load semantic vocabulary as source
    data_path = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language" / "semantic_vocabulary.json"
    
    # Use DocumentLoader to load source
    source = DocumentLoader.load(data_path)
    
    # Extract concepts
    concepts, _, _ = KnowledgeExtractor.extract(source)
    
    # Find concept for this word
    target_concept = None
    for concept in concepts:
        if concept.term == word:
            target_concept = concept
            break
    
    if target_concept is None:
        return False  # Word not found
    
    # Create pipeline
    pipeline = KnowledgeIngestionPipeline(memory)
    
    # CRITICAL: Use actual Evidence Gate with understanding evidence
    # Check if understanding_evidence provided and handle verified attribute safely
    evidence_verified = understanding_evidence.verified if understanding_evidence else False
    
    result = pipeline.consolidate_with_evidence(
        concept=target_concept,
        knowledge_state=knowledge_state,
        evidence_verified=evidence_verified,
        understanding_evidence=understanding_evidence,
    )
    
    return result


# Lesson definition
lesson_6_2 = Lesson(
    subject_id="thai",
    level=6,
    title="Word Meaning in Context (ความหมายของคำในบริบท)",
    objectives=[
        "Understand same word can have different meanings in different contexts",
        "Identify required context for interpretation",
        "Distinguish LITERAL from PRAGMATIC contextual meanings",
        "Recognize when context is insufficient (AMBIGUOUS/UNKNOWN)",
        "Provide CONTEXTUAL_INTERPRETATION evidence (not just translation)",
    ],
    content="""
Word Meaning in Context (ความหมายของคำในบริบท)

1. Same Word, Different Contexts
   - ไป บ้าน (LITERAL): physical movement → home
   - ไป เรียน (PRAGMATIC): attend class (not just physical movement)

2. Context Types
   - LITERAL: Direct, physical meaning
   - PRAGMATIC: Usage-dependent, functional meaning
   - IDIOMATIC: Fixed expression meaning
   - CULTURAL: Culture-specific meaning

3. Required Context
   - Some meanings need specific context clues
   - ไป + activity → PRAGMATIC (attend/participate)
   - ไป + location → LITERAL (physical movement)

4. Insufficient Context → AMBIGUOUS
   - "ดี" alone: good quality? or agreement? → AMBIGUOUS
   - "ดี" with noun: คน ดี → LITERAL (good person)
   - "ดี" as response: (response) ดี → PRAGMATIC (okay/agreed)

5. Translation Cannot Capture Context
   - Translation: ไป = go (loses context)
   - Understanding: ไป in context X means Y

6. Evidence Requirement
   - CONTEXTUAL_INTERPRETATION: explain meaning based on context
   - Not sufficient: translation only
   - Required: context identification + meaning interpretation
""",
    prerequisites=["thai_lesson_6_1"],
)
