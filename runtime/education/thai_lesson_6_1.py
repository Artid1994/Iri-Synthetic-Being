"""
Thai Week 6 Lesson 6.1: Semantic Meaning (ความหมายเชิงหมวดหมู่)

Learning Objectives:
1. Distinguish word form, pronunciation, translation, and semantic meaning
2. Identify semantic fields (MOTION, QUALITY, ACTION, OBJECT, PERSON)
3. Understand that meaning ≠ translation
4. Recognize evidence status (KNOWN/AMBIGUOUS/UNKNOWN)
5. Provide explanation evidence (not just translation)

This lesson uses Knowledge Ingestion Pipeline:
SOURCE → PROVENANCE → EXTRACT → LEARN → EVIDENCE → CONSOLIDATE
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Dict
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
    """Load semantic vocabulary knowledge base."""
    data_path = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language" / "semantic_vocabulary.json"
    return json.loads(data_path.read_text(encoding='utf-8'))


def generate_lesson_6_1_exercises() -> List[LearningExercise]:
    """
    Generate exercises for semantic meaning.
    
    Focus: semantic field identification, meaning vs translation, explanation
    """
    data = load_data()
    words = data['semantic_vocabulary']
    
    exercises = []
    
    # All exercises use EXACT verification (case-insensitive comparison in assess)
    exercises.append(LearningExercise(
        question="คำว่า 'ไป' อยู่ใน semantic field ใด? (MOTION, QUALITY, ACTION, OBJECT, PERSON)",
        expected_answer="MOTION",
        verification_type="EXACT",
    ))
    
    exercises.append(LearningExercise(
        question="คำว่า 'ดี' อยู่ใน semantic field ใด?",
        expected_answer="QUALITY",
        verification_type="EXACT",
    ))
    
    exercises.append(LearningExercise(
        question="คำว่า 'กิน' อยู่ใน semantic field ใด?",
        expected_answer="ACTION",
        verification_type="EXACT",
    ))
    
    exercises.append(LearningExercise(
        question="การแปล 'ไป' เป็น 'go' เป็นหลักฐานของความเข้าใจความหมายเชิงหมวดหมู่หรือไม่? (YES/NO)",
        expected_answer="NO",
        verification_type="EXACT",
    ))
    
    exercises.append(LearningExercise(
        question="MOTION semantic field หมายถึงคำที่เกี่ยวกับอะไร? (การเคลื่อนที่/คุณภาพ/วัตถุ)",
        expected_answer="การเคลื่อนที่",
        verification_type="EXACT",
    ))
    
    exercises.append(LearningExercise(
        question="ถ้าเราไม่มีข้อมูลเกี่ยวกับความหมายของคำ ควรระบุ evidence status เป็นอะไร? (KNOWN/UNKNOWN)",
        expected_answer="UNKNOWN",
        verification_type="EXACT",
    ))
    
    exercises.append(LearningExercise(
        question="การอธิบายความหมายเชิงหมวดหมู่ต้องการ evidence type ใด? (TRANSLATION/EXPLANATION)",
        expected_answer="EXPLANATION",
        verification_type="EXACT",
    ))
    
    exercises.append(LearningExercise(
        question="คำว่า 'คน' อยู่ใน semantic field ใด?",
        expected_answer="PERSON",
        verification_type="EXACT",
    ))
    
    exercises.append(LearningExercise(
        question="คำว่า 'น้ำ' อยู่ใน semantic field ใด?",
        expected_answer="OBJECT",
        verification_type="EXACT",
    ))
    
    # Understanding check - requires concept explanation
    exercises.append(LearningExercise(
        question="Semantic meaning แตกต่างจาก translation อย่างไร? (ตอบ: concept/category/meaning)",
        expected_answer="concept",  # Will check with case-insensitive contains
        verification_type="EXACT",
    ))
    
    return exercises


def assess_mastery(responses: List[str]) -> Tuple[float, str, List[str], List[str]]:
    """
    Assess semantic meaning understanding.
    
    CRITICAL: This assesses explanation ability, not just translation.
    
    Returns: (accuracy, mastery_level, error_patterns, knowledge_gaps)
    """
    exercises = generate_lesson_6_1_exercises()
    
    if len(responses) != len(exercises):
        raise ValueError(f"Expected {len(exercises)} responses, got {len(responses)}")
    
    correct = 0
    error_patterns = []
    knowledge_gaps = []
    
    for i, (exercise, response) in enumerate(zip(exercises, responses)):
        response = response.strip()
        expected = exercise.expected_answer.strip()
        
        # Case-insensitive comparison for all
        if i == 9:  # Last question: check contains
            if expected.lower() in response.lower() or "category" in response.lower() or "meaning" in response.lower():
                correct += 1
            else:
                error_patterns.append(f"Q{i+1}: Response missing key concept")
                knowledge_gaps.append("semantic_meaning_concept")
        else:
            if response.upper() == expected.upper():
                correct += 1
            else:
                error_patterns.append(f"Q{i+1}: Expected {expected}, got {response}")
                
                # Identify knowledge gaps
                if i < 3:  # Semantic field identification
                    knowledge_gaps.append("semantic_field_identification")
                elif i == 3:  # Meaning vs translation
                    knowledge_gaps.append("meaning_translation_distinction")
                elif i == 6:  # Explanation requirement
                    knowledge_gaps.append("explanation_requirement")
    
    accuracy = correct / len(exercises)
    
    # Mastery level based on accuracy
    if accuracy >= 0.9:
        mastery_level = "MASTERED"
    elif accuracy >= 0.7:
        mastery_level = "CAN_USE"
    else:
        mastery_level = "LEARNING"
    
    # Deduplicate gaps
    knowledge_gaps = list(set(knowledge_gaps))
    
    return accuracy, mastery_level, error_patterns, knowledge_gaps


def update_knowledge_state(
    state: KnowledgeState,
    responses: List[str],
) -> None:
    """Update knowledge state from assessment."""
    exercises = generate_lesson_6_1_exercises()
    
    for exercise, response in zip(exercises, responses):
        response = response.strip()
        expected = exercise.expected_answer.strip()
        
        # Check if last exercise (concept explanation)
        if "แตกต่าง" in exercise.question:
            # Contains check for concept understanding
            if expected.lower() in response.lower() or "category" in response.lower() or "meaning" in response.lower():
                state.record_correct()
            else:
                state.record_error(ErrorType.PARTIAL)
        else:
            # Case-insensitive exact match
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


# Lesson definition
lesson_6_1 = Lesson(
    subject_id="thai",
    level=6,
    title="Semantic Meaning (ความหมายเชิงหมวดหมู่)",
    objectives=[
        "Distinguish word form, pronunciation, translation, and semantic meaning",
        "Identify semantic fields (MOTION, QUALITY, ACTION, OBJECT, PERSON)",
        "Understand that meaning ≠ translation",
        "Recognize evidence status (KNOWN/AMBIGUOUS/UNKNOWN)",
        "Provide explanation evidence (not just translation)",
    ],
    content="""
Semantic Meaning (ความหมายเชิงหมวดหมู่)

1. Word Form vs Meaning
   - รูปคำ (form): ไป
   - การออกเสียง (pronunciation): /pai/
   - คำแปล (translation): go
   - ความหมาย (semantic meaning): MOTION concept - movement away from origin

2. Semantic Fields
   Categories that group words by meaning:
   - MOTION: การเคลื่อนที่ (ไป, มา)
   - QUALITY: คุณภาพ (ดี, เลว)
   - ACTION: การกระทำ (กิน, ดื่ม)
   - OBJECT: วัตถุ (น้ำ, ข้าว)
   - PERSON: บุคคล (คน, เด็ก)

3. Translation ≠ Understanding
   - Translation: surface correspondence
   - Understanding: conceptual meaning, category, usage

4. Evidence Status
   - KNOWN: verified from authoritative source
   - AMBIGUOUS: multiple interpretations possible
   - UNKNOWN: no evidence available

5. Evidence Requirement
   - Translation alone: insufficient for semantic understanding
   - Explanation required: must identify semantic field, concept
""",
    prerequisites=["thai_week_5"],
)
