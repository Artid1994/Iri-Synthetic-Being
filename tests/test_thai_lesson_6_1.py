"""
Test Thai Lesson 6.1: Semantic Meaning

Tests learning flow through Knowledge Ingestion Pipeline:
SOURCE → EXTRACT → LEARN → EVIDENCE → CONSOLIDATE
"""
import pytest
from pathlib import Path

from runtime.education.thai_lesson_6_1 import (
    lesson_6_1,
    generate_lesson_6_1_exercises,
    assess_mastery,
    update_knowledge_state,
    update_mastery_tracker,
    load_data,
)
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel
from runtime.education.mastery_tracker import MasteryTracker
from runtime.education.learning_session import LearningSession
from runtime.memory import Memory
from runtime.self_model import SelfModel
from runtime.identity import Identity
from runtime.knowledge_ingestion import (
    KnowledgeIngestionPipeline,
    DocumentLoader,
)
from runtime.education.semantic_representation import (
    UnderstandingEvidence,
    EvidenceType,
)


class TestLesson61Structure:
    """Test lesson structure."""
    
    def test_lesson_creation(self):
        """Test lesson 6.1 exists."""
        assert lesson_6_1.subject_id == "thai"
        assert lesson_6_1.level == 6
        assert "Semantic Meaning" in lesson_6_1.title
    
    def test_lesson_objectives(self):
        """Test lesson has semantic meaning objectives."""
        objectives = lesson_6_1.objectives
        assert len(objectives) >= 5
        assert any("translation" in obj.lower() for obj in objectives)
        assert any("semantic" in obj.lower() for obj in objectives)
    
    def test_lesson_prerequisites(self):
        """Test lesson requires Week 5."""
        assert "thai_week_5" in lesson_6_1.prerequisites


class TestDataLoading:
    """Test semantic vocabulary loading."""
    
    def test_load_semantic_vocabulary(self):
        """Test loading semantic_vocabulary.json."""
        data = load_data()
        assert "semantic_vocabulary" in data
        assert len(data["semantic_vocabulary"]) >= 5
    
    def test_semantic_fields_present(self):
        """Test semantic fields in data."""
        data = load_data()
        words = data["semantic_vocabulary"]
        
        fields = {w["semantic_field"] for w in words}
        assert "MOTION" in fields
        assert "QUALITY" in fields
        assert "ACTION" in fields


class TestExerciseGeneration:
    """Test exercise generation."""
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_6_1_exercises()
        assert len(exercises) == 10
    
    def test_semantic_field_exercises(self):
        """Test semantic field identification exercises."""
        exercises = generate_lesson_6_1_exercises()
        
        # At least 5 exercises about semantic fields
        field_exercises = [e for e in exercises if "semantic field" in e.question]
        assert len(field_exercises) >= 5
    
    def test_translation_distinction_exercise(self):
        """Test meaning vs translation exercise."""
        exercises = generate_lesson_6_1_exercises()
        
        # Exercise about translation ≠ understanding
        translation_ex = [e for e in exercises if "แปล" in e.question and "หลักฐาน" in e.question]
        assert len(translation_ex) >= 1
        assert translation_ex[0].expected_answer == "NO"


class TestAssessment:
    """Test assessment logic."""
    
    def test_perfect_responses(self):
        """Test perfect semantic understanding."""
        responses = [
            "MOTION",
            "QUALITY",
            "ACTION",
            "NO",
            "การเคลื่อนที่",
            "UNKNOWN",
            "EXPLANATION",
            "PERSON",
            "OBJECT",
            "concept field",  # Contains "concept"
        ]
        
        accuracy, mastery, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 1.0
        assert mastery == "MASTERED"
        assert len(errors) == 0
        assert len(gaps) == 0
    
    def test_translation_only_insufficient(self):
        """Test translation-only responses insufficient."""
        responses = [
            "MOTION",  # Correct
            "QUALITY",  # Correct
            "ACTION",  # Correct
            "YES",  # WRONG - thinks translation = understanding
            "การเคลื่อนที่",  # Correct
            "KNOWN",  # WRONG
            "TRANSLATION",  # WRONG - thinks translation sufficient
            "PERSON",  # Correct
            "OBJECT",  # Correct
            "translation",  # WRONG - no concept understanding
        ]
        
        accuracy, mastery, errors, gaps = assess_mastery(responses)
        
        assert accuracy < 0.9  # Not mastered
        assert "meaning_translation_distinction" in gaps
    
    def test_insufficient_knowledge_gaps(self):
        """Test knowledge gap detection."""
        responses = [
            "WRONG",  # Wrong field
            "WRONG",  # Wrong field
            "WRONG",  # Wrong field
            "NO",  # Correct
            "การเคลื่อนที่",  # Correct
            "UNKNOWN",  # Correct
            "EXPLANATION",  # Correct
            "PERSON",  # Correct
            "OBJECT",  # Correct
            "concept",  # Correct
        ]
        
        accuracy, mastery, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 0.7  # 7/10 correct
        assert "semantic_field_identification" in gaps


class TestKnowledgeStateIntegration:
    """Test KnowledgeState integration."""
    
    def test_update_knowledge_state_correct(self):
        """Test updating KnowledgeState with correct responses."""
        state = KnowledgeState("lesson_6_1")
        
        responses = [
            "MOTION", "QUALITY", "ACTION", "NO", "การเคลื่อนที่",
            "UNKNOWN", "EXPLANATION", "PERSON", "OBJECT", "concept"
        ]
        
        update_knowledge_state(state, responses)
        
        assert state.correct_count == 10
        assert state.incorrect_count == 0
        assert state.level == KnowledgeLevel.MASTERED
    
    def test_update_knowledge_state_errors(self):
        """Test KnowledgeState with errors."""
        state = KnowledgeState("lesson_6_1")
        
        responses = [
            "WRONG", "QUALITY", "ACTION", "YES", "การเคลื่อนที่",
            "WRONG", "EXPLANATION", "PERSON", "OBJECT", "concept"
        ]
        
        update_knowledge_state(state, responses)
        
        assert state.correct_count == 7
        assert state.incorrect_count == 3
        # 7/10 = 70% accuracy = UNDERSTOOD (not CAN_USE which requires 85%)
        assert state.level == KnowledgeLevel.UNDERSTOOD


class TestMasteryTrackerIntegration:
    """Test MasteryTracker integration."""
    
    def test_update_mastery_tracker(self):
        """Test updating MasteryTracker."""
        tracker = MasteryTracker()
        
        update_mastery_tracker(tracker, "lesson_6_1", 0.95)
        
        assert tracker.is_mastered("lesson_6_1")


class TestLearningSessionComplete:
    """Test complete learning session."""
    
    def test_complete_learning_session(self):
        """Test full learning session for 6.1."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        identity = Identity()
        
        session = LearningSession(tracker, memory, self_model, identity)
        
        exercises = generate_lesson_6_1_exercises()
        
        # Perfect responses
        responses = [
            "MOTION", "QUALITY", "ACTION", "NO", "การเคลื่อนที่",
            "UNKNOWN", "EXPLANATION", "PERSON", "OBJECT", "concept"
        ]
        
        result = session.conduct_session(lesson_6_1, exercises, responses)
        
        assert result.mastered is True
        assert result.assessment_result.score >= 0.9


class TestTranslationVsUnderstanding:
    """CRITICAL: Test translation ≠ understanding distinction."""
    
    def test_translation_recognition_insufficient(self):
        """Test that translation/recognition alone doesn't prove semantic understanding."""
        # Simulate: Can translate correctly but can't explain semantic field
        responses = [
            "MOTION",  # Correct - but could be memorized
            "QUALITY",  # Correct - but could be memorized
            "ACTION",  # Correct - but could be memorized
            "YES",  # WRONG - thinks translation proves understanding
            "ไม่รู้",  # WRONG - can't explain what MOTION means
            "KNOWN",  # WRONG - assumes memorization = knowledge
            "TRANSLATION",  # WRONG - thinks translation sufficient
            "PERSON",  # Correct - but could be memorized
            "OBJECT",  # Correct - but could be memorized
            "ไม่ทราบ",  # WRONG - can't explain semantic meaning concept
        ]
        
        accuracy, mastery, errors, gaps = assess_mastery(responses)
        
        # Should NOT reach MASTERED
        assert mastery != "MASTERED"
        assert accuracy < 0.9


class TestEvidenceRequirement:
    """Test evidence requirement for semantic consolidation."""
    
    def test_semantic_knowledge_requires_explanation_evidence(self):
        """Test semantic knowledge from 6.1 requires understanding evidence."""
        # This would be tested in integration with Knowledge Ingestion Pipeline
        # Here we verify the lesson enforces explanation requirement
        
        exercises = generate_lesson_6_1_exercises()
        
        # Find explanation requirement exercise
        exp_exercise = None
        for ex in exercises:
            if "evidence type" in ex.question or "EXPLANATION" in ex.expected_answer:
                exp_exercise = ex
                break
        
        assert exp_exercise is not None
        assert exp_exercise.expected_answer == "EXPLANATION"


class TestUnknownAmbiguousHandling:
    """Test UNKNOWN/AMBIGUOUS handling."""
    
    def test_unknown_evidence_status_recognized(self):
        """Test recognizing UNKNOWN evidence status."""
        exercises = generate_lesson_6_1_exercises()
        
        # Exercise about UNKNOWN status
        unknown_ex = [e for e in exercises if "UNKNOWN" in e.expected_answer]
        assert len(unknown_ex) >= 1
    
    def test_no_guessing_when_insufficient_evidence(self):
        """Test lesson teaches: don't guess when evidence insufficient."""
        # Implicitly tested by UNKNOWN exercise
        # Lesson content must emphasize evidence requirement
        assert "Evidence Status" in lesson_6_1.content
        assert "UNKNOWN" in lesson_6_1.content


class TestProvenanceIntegration:
    """Test provenance preserved through learning."""
    
    def test_semantic_data_has_provenance(self):
        """Test loaded semantic data maintains source information."""
        data = load_data()
        
        # Data comes from semantic_vocabulary.json
        # Provenance would be tracked during ingestion
        # Here we verify data structure supports it
        assert "semantic_vocabulary" in data
        
        # Each word should have verifiable structure
        for word in data["semantic_vocabulary"]:
            assert "word" in word
            assert "semantic_field" in word
            assert "evidence_status" in word or "data_status" in word.get("note", "KNOWN")
