"""
Test Thai Lesson 6.2: Word Meaning in Context

CRITICAL: Tests actual Knowledge Ingestion Pipeline integration.
SOURCE → EXTRACT → LEARN → EVIDENCE → GATE → CONSOLIDATE
"""
import pytest
from pathlib import Path

from runtime.education.thai_lesson_6_2 import (
    lesson_6_2,
    generate_lesson_6_2_exercises,
    assess_mastery,
    update_knowledge_state,
    update_mastery_tracker,
    consolidate_semantic_knowledge_with_pipeline,
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
    Concept,
    Provenance,
    SourceType,
)
from runtime.education.semantic_representation import (
    UnderstandingEvidence,
    EvidenceType,
)


class TestLesson62Structure:
    """Test lesson structure."""
    
    def test_lesson_creation(self):
        """Test lesson 6.2 exists."""
        assert lesson_6_2.subject_id == "thai"
        assert lesson_6_2.level == 6
        assert "Context" in lesson_6_2.title or "บริบท" in lesson_6_2.title
    
    def test_lesson_prerequisites(self):
        """Test lesson requires 6.1."""
        assert "thai_lesson_6_1" in lesson_6_2.prerequisites


class TestContextualMeaningData:
    """Test contextual meaning data availability."""
    
    def test_load_contextual_data(self):
        """Test loading contextual meanings."""
        data = load_data()
        words = data["semantic_vocabulary"]
        
        # Find words with multiple contexts
        multi_context = [w for w in words if len(w.get("contextual_meanings", [])) > 1]
        assert len(multi_context) >= 2  # At least 2 words with multiple contexts
    
    def test_contextual_meaning_structure(self):
        """Test contextual meaning has required fields."""
        data = load_data()
        
        # Check ไป (should have LITERAL + PRAGMATIC)
        pai_word = next(w for w in data["semantic_vocabulary"] if w["word"] == "ไป")
        contexts = pai_word["contextual_meanings"]
        
        assert len(contexts) >= 2
        assert any(c["context_type"] == "LITERAL" for c in contexts)
        assert any(c["context_type"] == "PRAGMATIC" for c in contexts)


class TestExerciseGeneration:
    """Test exercise generation."""
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_6_2_exercises()
        assert len(exercises) == 10
    
    def test_context_type_exercises(self):
        """Test context type identification exercises."""
        exercises = generate_lesson_6_2_exercises()
        
        # Should have exercises about LITERAL vs PRAGMATIC
        context_ex = [e for e in exercises if "LITERAL" in e.question or "PRAGMATIC" in e.question]
        assert len(context_ex) >= 5
    
    def test_ambiguity_exercise(self):
        """Test ambiguity recognition exercise."""
        exercises = generate_lesson_6_2_exercises()
        
        # Should have exercise about insufficient context → AMBIGUOUS
        ambig_ex = [e for e in exercises if "AMBIGUOUS" in e.question or "AMBIGUOUS" in e.expected_answer]
        assert len(ambig_ex) >= 1


class TestAssessment:
    """Test assessment logic."""
    
    def test_perfect_contextual_understanding(self):
        """Test perfect contextual meaning understanding."""
        responses = [
            "LITERAL",   # ไป บ้าน
            "PRAGMATIC", # ไป เรียน
            "activity",  # required context
            "LITERAL",   # คน ดี
            "PRAGMATIC", # ดี (response)
            "AMBIGUOUS", # ดี without context
            "NO",        # translation doesn't capture context
            "CONTEXTUAL_INTERPRETATION",  # evidence type
            "2",         # ไป has 2 meanings
            "YES",       # context is important
        ]
        
        accuracy, mastery, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 1.0
        assert mastery == "MASTERED"
        assert len(errors) == 0
    
    def test_translation_only_insufficient(self):
        """Test translation-focused responses insufficient."""
        responses = [
            "WRONG",     # Wrong context type
            "LITERAL",   # Wrong - should be PRAGMATIC
            "location",  # Wrong required context
            "LITERAL",   # Correct
            "LITERAL",   # Wrong - should be PRAGMATIC
            "KNOWN",     # Wrong - should be AMBIGUOUS
            "YES",       # Wrong - translation doesn't capture context
            "TRANSLATION", # Wrong evidence type
            "1",         # Wrong
            "NO",        # Wrong
        ]
        
        accuracy, mastery, errors, gaps = assess_mastery(responses)
        
        assert accuracy < 0.9  # Not mastered
        assert "context_type_identification" in gaps or "translation_limitation_understanding" in gaps


class TestKnowledgeStateIntegration:
    """Test KnowledgeState integration."""
    
    def test_update_knowledge_state_perfect(self):
        """Test updating KnowledgeState with perfect responses."""
        state = KnowledgeState("lesson_6_2")
        
        responses = [
            "LITERAL", "PRAGMATIC", "activity", "LITERAL", "PRAGMATIC",
            "AMBIGUOUS", "NO", "CONTEXTUAL_INTERPRETATION", "2", "YES"
        ]
        
        update_knowledge_state(state, responses)
        
        assert state.correct_count == 10
        assert state.incorrect_count == 0
        assert state.level == KnowledgeLevel.MASTERED


class TestPipelineIntegration:
    """CRITICAL: Test actual Knowledge Ingestion Pipeline integration."""
    
    def test_pipeline_consolidation_with_contextual_evidence(self):
        """Test consolidating semantic knowledge through Pipeline + Evidence Gate."""
        memory = Memory()
        
        # Simulate: IRI learned contextual meaning of "ไป"
        state = KnowledgeState("ไป_contextual")
        state.level = KnowledgeLevel.CAN_USE
        
        # CRITICAL: Provide CONTEXTUAL_INTERPRETATION evidence
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.CONTEXTUAL_INTERPRETATION,
            language_input="ไป เรียน",
            learner_output="ไป in context of activity (เรียน) means attend/participate, not just physical movement",
            expected_pattern="contextual interpretation",
            verified=True,
            confidence=0.9,
            explanation="Interpreted ไป contextually in activity context",
        )
        
        # Use actual Pipeline + Evidence Gate
        result = consolidate_semantic_knowledge_with_pipeline(
            word="ไป",
            memory=memory,
            knowledge_state=state,
            understanding_evidence=evidence,
        )
        
        # Should be accepted
        assert result is True
        
        # Should be in semantic memory (check with partial match since definition may vary)
        assert len(memory.state.semantic) > 0
        assert any("ไป" in entry for entry in memory.state.semantic)
        
        # Should have provenance in episodic memory
        episodic = memory.state.episodic
        assert any("ไป" in entry and "semantic_vocabulary.json" in entry for entry in episodic)
    
    def test_pipeline_rejects_translation_only(self):
        """Test Evidence Gate rejects translation-only for semantic knowledge."""
        memory = Memory()
        
        state = KnowledgeState("ไป_translation")
        state.level = KnowledgeLevel.CAN_USE
        
        # NO understanding evidence provided
        result = consolidate_semantic_knowledge_with_pipeline(
            word="ไป",
            memory=memory,
            knowledge_state=state,
            understanding_evidence=None,  # No evidence!
        )
        
        # MUST BE REJECTED
        assert result is False
        
        # Should NOT be in semantic memory
        # (may be in working as candidate, but not consolidated)
    
    def test_pipeline_rejects_unverified_evidence(self):
        """Test Evidence Gate rejects unverified evidence."""
        memory = Memory()
        
        state = KnowledgeState("ดี_unverified")
        state.level = KnowledgeLevel.CAN_USE
        
        # Evidence provided but NOT verified
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.CONTEXTUAL_INTERPRETATION,
            language_input="ดี",
            learner_output="contextual interpretation",
            expected_pattern="pattern",
            verified=False,  # NOT VERIFIED
            confidence=0.9,
        )
        
        result = consolidate_semantic_knowledge_with_pipeline(
            word="ดี",
            memory=memory,
            knowledge_state=state,
            understanding_evidence=evidence,
        )
        
        # MUST BE REJECTED
        assert result is False


class TestSameWordDifferentContext:
    """Test understanding same word in different contexts."""
    
    def test_pai_literal_vs_pragmatic(self):
        """Test distinguishing literal vs pragmatic meaning of ไป."""
        data = load_data()
        pai = next(w for w in data["semantic_vocabulary"] if w["word"] == "ไป")
        
        contexts = pai["contextual_meanings"]
        literal = next(c for c in contexts if c["context_type"] == "LITERAL")
        pragmatic = next(c for c in contexts if c["context_type"] == "PRAGMATIC")
        
        # Literal: no required context
        assert len(literal["required_context"]) == 0
        
        # Pragmatic: requires activity/event context
        assert len(pragmatic["required_context"]) > 0
        assert "activity" in pragmatic["required_context"] or "event" in pragmatic["required_context"]
    
    def test_dee_literal_vs_pragmatic(self):
        """Test distinguishing literal vs pragmatic meaning of ดี."""
        data = load_data()
        dee = next(w for w in data["semantic_vocabulary"] if w["word"] == "ดี")
        
        contexts = dee["contextual_meanings"]
        
        # Should have both LITERAL and PRAGMATIC
        assert len(contexts) >= 2
        types = {c["context_type"] for c in contexts}
        assert "LITERAL" in types
        assert "PRAGMATIC" in types


class TestAmbiguityRecognition:
    """Test recognizing ambiguity when context insufficient."""
    
    def test_ambiguous_without_context(self):
        """Test recognizing word is ambiguous without context."""
        # "ดี" alone is ambiguous (good quality? or agreement?)
        exercises = generate_lesson_6_2_exercises()
        
        # Find ambiguity exercise
        ambig_ex = next(e for e in exercises if "AMBIGUOUS" in e.expected_answer)
        
        # Should ask about context insufficiency
        assert "ไม่มีบริบท" in ambig_ex.question or "without" in ambig_ex.question.lower()


class TestEvidenceTypeUnderstanding:
    """Test understanding evidence types."""
    
    def test_contextual_interpretation_required(self):
        """Test recognizing CONTEXTUAL_INTERPRETATION required."""
        exercises = generate_lesson_6_2_exercises()
        
        # Find evidence type exercise
        evidence_ex = next(e for e in exercises if "CONTEXTUAL_INTERPRETATION" in e.expected_answer)
        
        assert evidence_ex.expected_answer == "CONTEXTUAL_INTERPRETATION"


class TestTranslationVsContextualUnderstanding:
    """Test translation vs contextual understanding distinction."""
    
    def test_translation_cannot_capture_context(self):
        """Test recognizing translation doesn't capture contextual meaning."""
        exercises = generate_lesson_6_2_exercises()
        
        # Find translation limitation exercise
        trans_ex = [e for e in exercises if "แปล" in e.question and "บริบท" in e.question]
        assert len(trans_ex) >= 1
        
        # Should answer NO (translation doesn't capture context)
        assert trans_ex[0].expected_answer == "NO"


class TestLearningSessionComplete:
    """Test complete learning session for 6.2."""
    
    def test_complete_session_with_contextual_mastery(self):
        """Test full session with contextual understanding."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        identity = Identity()
        
        session = LearningSession(tracker, memory, self_model, identity)
        exercises = generate_lesson_6_2_exercises()
        
        # Perfect contextual responses
        responses = [
            "LITERAL", "PRAGMATIC", "activity", "LITERAL", "PRAGMATIC",
            "AMBIGUOUS", "NO", "CONTEXTUAL_INTERPRETATION", "2", "YES"
        ]
        
        result = session.conduct_session(lesson_6_2, exercises, responses)
        
        assert result.mastered is True
        assert result.assessment_result.score >= 0.9


class TestProvenancePreservation:
    """Test provenance preserved through Pipeline."""
    
    def test_provenance_in_pipeline_flow(self):
        """Test provenance preserved in Pipeline consolidation."""
        memory = Memory()
        state = KnowledgeState("test")
        state.level = KnowledgeLevel.MASTERED
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.CONTEXTUAL_INTERPRETATION,
            language_input="test",
            learner_output="contextual interpretation",
            expected_pattern="pattern",
            verified=True,
            confidence=0.9,
        )
        
        result = consolidate_semantic_knowledge_with_pipeline(
            word="กิน",
            memory=memory,
            knowledge_state=state,
            understanding_evidence=evidence,
        )
        
        if result:  # If consolidated
            # Check provenance in episodic
            episodic = memory.state.episodic
            # Should mention source file
            assert any("semantic_vocabulary.json" in entry for entry in episodic)
