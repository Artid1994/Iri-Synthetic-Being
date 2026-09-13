"""
Test Thai Lesson 6.8: Understanding ≠ Translation

Tests system-level enforcement that translation-only cannot reach semantic mastery.
"""
import pytest

from runtime.education.thai_lesson_6_8 import (
    lesson_6_8,
    generate_lesson_6_8_exercises,
    assess_mastery,
    update_knowledge_state,
    update_mastery_tracker,
    assess_understanding_vs_translation,
    demonstrate_translation_limitation,
    demonstrate_understanding_path,
    load_data,
)
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel
from runtime.education.mastery_tracker import MasteryTracker
from runtime.education.semantic_representation import (
    UnderstandingEvidence,
    EvidenceType,
)
from runtime.knowledge_ingestion import (
    Concept,
    Provenance,
    KnowledgeIngestionPipeline,
    SourceType,
)
from runtime.memory import Memory
from runtime.self_model import SelfModel


class TestLesson68Structure:
    """Test lesson structure."""
    
    def test_lesson_creation(self):
        """Test lesson 6.8 exists."""
        assert lesson_6_8.subject_id == "thai"
        assert lesson_6_8.level == 6
        assert "Translation" in lesson_6_8.title
    
    def test_lesson_prerequisites(self):
        """Test lesson requires 6.7."""
        assert "thai_lesson_6_7" in lesson_6_8.prerequisites
    
    def test_exercise_count(self):
        """Test generates 10 exercises."""
        exercises = generate_lesson_6_8_exercises()
        assert len(exercises) == 10


class TestTranslationVsUnderstanding:
    """CRITICAL: Test translation ≠ understanding distinction."""
    
    def test_translation_only_insufficient(self):
        """Test translation-only is insufficient for semantic understanding."""
        assessment, evidence_type, passes_gate = assess_understanding_vs_translation(
            "translation", "go", "go", None
        )
        
        assert assessment == "TRANSLATION_ONLY"
        assert evidence_type == EvidenceType.TRANSLATION
        assert passes_gate is False
    
    def test_explanation_is_understanding(self):
        """Test explanation demonstrates understanding."""
        assessment, evidence_type, passes_gate = assess_understanding_vs_translation(
            "explanation",
            "ไป is a motion verb with literal and pragmatic meanings",
            None,
            "motion verb"
        )
        
        assert assessment == "UNDERSTANDING"
        assert evidence_type == EvidenceType.EXPLANATION
        assert passes_gate is True
    
    def test_application_is_understanding(self):
        """Test application demonstrates understanding."""
        assessment, evidence_type, passes_gate = assess_understanding_vs_translation(
            "application",
            "ไป กิน (go eat)",
            None,
            None
        )
        
        assert assessment == "UNDERSTANDING"
        assert evidence_type == EvidenceType.APPLICATION
        assert passes_gate is True


class TestTranslationLimitation:
    """CRITICAL: Test translation-only limitations."""
    
    def test_perfect_translation_fails_semantic_gate(self):
        """Test 100% translation accuracy still fails semantic mastery."""
        result = demonstrate_translation_limitation()
        
        assert result["translation_accuracy"] == 1.0
        assert result["would_reach_mastery_by_accuracy"] is True
        assert result["has_understanding_evidence"] is False
        assert result["semantic_mastery_achieved"] is False
    
    def test_translation_useful_but_insufficient(self):
        """Test translation is useful but not sufficient."""
        result = demonstrate_translation_limitation()
        
        # Translation correct
        assert result["translation_accuracy"] == 1.0
        
        # But no semantic mastery
        assert result["semantic_mastery_achieved"] is False
        assert "insufficient" in result["reason"].lower() or "lacks" in result["reason"].lower()


class TestUnderstandingPath:
    """Test valid path to semantic understanding."""
    
    def test_translation_plus_explanation_succeeds(self):
        """Test translation + explanation allows semantic mastery."""
        result = demonstrate_understanding_path()
        
        assert result["translation_correct"] is True
        assert result["explanation_provided"] is True
        assert result["evidence_type"] == EvidenceType.EXPLANATION
        assert result["semantic_mastery_possible"] is True
    
    def test_understanding_requires_evidence(self):
        """Test understanding path requires evidence."""
        result = demonstrate_understanding_path()
        
        assert result["evidence_verified"] is True
        assert result["evidence_type"] in [
            EvidenceType.EXPLANATION,
            EvidenceType.APPLICATION,
            EvidenceType.CONTEXTUAL_INTERPRETATION,
        ]


class TestEvidenceGateEnforcement:
    """CRITICAL: Test Evidence Gate rejects translation-only."""
    
    def test_gate_rejects_translation_only(self):
        """Test Evidence Gate explicitly rejects TRANSLATION evidence type."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="ไป",
            definition="go",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "MOTION"},  # Mark as semantic
        )
        
        state = KnowledgeState("ไป")
        state.level = KnowledgeLevel.MASTERED  # High level from translation practice
        
        # TRANSLATION evidence
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.TRANSLATION,
            language_input="ไป",
            learner_output="go",
            expected_pattern="go",
            verified=True,
            confidence=1.0,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Should REJECT despite MASTERED state
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is False
    
    def test_gate_accepts_explanation(self):
        """Test Evidence Gate accepts EXPLANATION evidence."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="test_word",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("test_word")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="test_word",
            learner_output="This is a motion verb with semantic field MOTION",
            expected_pattern="explanation",
            verified=True,
            confidence=0.9,
            explanation="Learner explained semantic field and verb type",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is True
    
    def test_gate_accepts_application(self):
        """Test Evidence Gate accepts APPLICATION evidence."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="test_application",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("test_application")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.APPLICATION,
            language_input="test pattern",
            learner_output="applied to new context",
            expected_pattern="application",
            verified=True,
            confidence=0.9,
            explanation="Applied pattern to novel context",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is True


class TestNumericVsSemanticCriteria:
    """Test numeric criteria alone insufficient for semantic mastery."""
    
    def test_high_accuracy_translation_still_rejected(self):
        """Test high accuracy translation-only still rejected."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="high_accuracy_word",
            definition="translation",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        # Simulate high accuracy practice
        state = KnowledgeState("high_accuracy_word")
        for _ in range(10):
            state.record_correct()
        
        assert state.level == KnowledgeLevel.MASTERED
        
        # But translation evidence
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.TRANSLATION,
            language_input="word",
            learner_output="translation",
            expected_pattern="translation",
            verified=True,
            confidence=1.0,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Still rejected
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is False
    
    def test_moderate_accuracy_understanding_accepted(self):
        """Test moderate accuracy with understanding evidence accepted."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="moderate_word",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        # Moderate accuracy (CAN_USE level)
        state = KnowledgeState("moderate_word")
        state.record_correct()
        state.record_correct()
        state.record_correct()
        
        assert state.level == KnowledgeLevel.CAN_USE
        
        # But understanding evidence
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="word",
            learner_output="semantic explanation with structure",
            expected_pattern="explanation",
            verified=True,
            confidence=0.8,
            explanation="Learner provided structural semantic explanation",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Accepted
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is True


class TestLexicalVsSemanticKnowledge:
    """Test lexical and semantic knowledge separation."""
    
    def test_translation_valid_for_lexical(self):
        """Test translation valid for lexical knowledge."""
        # Translation is valid evidence for lexical recall
        assessment, evidence_type, _ = assess_understanding_vs_translation(
            "translation", "go", "go", None
        )
        
        assert evidence_type == EvidenceType.TRANSLATION
        # Translation is valid evidence TYPE (just not sufficient for semantic mastery)
        assert assessment == "TRANSLATION_ONLY"
    
    def test_non_semantic_knowledge_allows_translation(self):
        """Test non-semantic knowledge doesn't require understanding evidence."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="phonological_fact",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={},  # No semantic_field = non-semantic
        )
        
        state = KnowledgeState("phonological_fact")
        state.level = KnowledgeLevel.CAN_USE
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Non-semantic knowledge: no evidence requirement
        result = pipeline.consolidate_with_evidence(concept, state, True, None)
        assert result is True


class TestMemorySelfModelProtection:
    """Test Memory and SelfModel don't claim semantic mastery from translation-only."""
    
    def test_memory_rejects_translation_only_semantic(self):
        """Test Memory doesn't consolidate semantic claim from translation-only."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="semantic_word",
            definition="translation",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "MOTION"},
        )
        
        state = KnowledgeState("semantic_word")
        state.level = KnowledgeLevel.MASTERED
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.TRANSLATION,
            language_input="word",
            learner_output="translation",
            expected_pattern="translation",
            verified=True,
            confidence=1.0,
        )
        
        memory = Memory()
        initial_count = len(memory.state.semantic)
        
        pipeline = KnowledgeIngestionPipeline(memory)
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        
        assert result is False
        # Memory should not have added semantic entry
        assert len(memory.state.semantic) == initial_count


class TestMasteryAssessment:
    """Test mastery assessment."""
    
    def test_correct_answers_mastery(self):
        """Test all correct → MASTERED."""
        exercises = generate_lesson_6_8_exercises()
        responses = [ex.expected_answer for ex in exercises]
        
        accuracy, level, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 1.0
        assert level == "MASTERED"
        assert len(errors) == 0
    
    def test_partial_correct_can_use(self):
        """Test 80% correct → CAN_USE."""
        exercises = generate_lesson_6_8_exercises()
        responses = [ex.expected_answer for ex in exercises[:8]]
        responses += ["WRONG", "WRONG"]
        
        accuracy, level, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 0.8
        assert level == "CAN_USE"
    
    def test_low_accuracy_learning(self):
        """Test <70% → LEARNING."""
        exercises = generate_lesson_6_8_exercises()
        responses = ["WRONG"] * len(exercises)
        
        accuracy, level, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 0.0
        assert level == "LEARNING"
        assert len(gaps) > 0


class TestKnowledgeStateUpdate:
    """Test knowledge state updates."""
    
    def test_knowledge_state_records_correct(self):
        """Test correct answers recorded."""
        state = KnowledgeState("thai_translation_understanding")
        exercises = generate_lesson_6_8_exercises()
        responses = [ex.expected_answer for ex in exercises]
        
        update_knowledge_state(state, responses)
        
        assert state.correct_count == len(exercises)
    
    def test_knowledge_state_records_errors(self):
        """Test errors recorded."""
        state = KnowledgeState("thai_translation_understanding")
        exercises = generate_lesson_6_8_exercises()
        responses = ["WRONG"] * len(exercises)
        
        update_knowledge_state(state, responses)
        
        assert state.incorrect_count == len(exercises)


class TestMasteryTrackerUpdate:
    """Test mastery tracker updates."""
    
    def test_mastery_tracker_records_attempt(self):
        """Test mastery tracker records attempts."""
        tracker = MasteryTracker()
        
        update_mastery_tracker(tracker, "thai_lesson_6_8", 0.9)
        
        record = tracker.get_progress("thai_lesson_6_8")
        assert record is not None
        assert record.mastery_score == 0.9


class TestRegression61To67:
    """Test regression: 6.1-6.7 mechanisms still work."""
    
    def test_lesson_6_8_exists(self):
        """Test lesson 6.8 can be imported and used."""
        assert lesson_6_8 is not None
        assert lesson_6_8.subject_id == "thai"
    
    def test_exercises_generate(self):
        """Test exercises generate without error."""
        exercises = generate_lesson_6_8_exercises()
        assert len(exercises) == 10
        assert all(ex.expected_answer for ex in exercises)
    
    def test_assessment_works(self):
        """Test assessment executes without error."""
        exercises = generate_lesson_6_8_exercises()
        responses = [ex.expected_answer for ex in exercises]
        
        accuracy, level, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 1.0
        assert level == "MASTERED"


class TestNoLLM:
    """Test no LLM dependency."""
    
    def test_no_llm_calls(self):
        """Test all functions work without LLM."""
        # All functions should work without external LLM
        data = load_data()
        assert data is not None
        
        result = demonstrate_translation_limitation()
        assert result["semantic_mastery_achieved"] is False
        
        assessment, _, _ = assess_understanding_vs_translation(
            "translation", "go", "go", None
        )
        assert assessment == "TRANSLATION_ONLY"
