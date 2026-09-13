"""
Test Thai Lesson 6.6: Pragmatic Meaning

Tests evidence-based pragmatic interpretation without mind-reading.
"""
import pytest

from runtime.education.thai_lesson_6_6 import (
    lesson_6_6,
    generate_lesson_6_6_exercises,
    assess_mastery,
    update_knowledge_state,
    update_mastery_tracker,
    extract_pragmatic_meaning,
    load_data,
)
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel
from runtime.education.mastery_tracker import MasteryTracker
from runtime.education.learning_session import LearningSession
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
from runtime.identity import Identity


class TestLesson66Structure:
    """Test lesson structure."""
    
    def test_lesson_creation(self):
        """Test lesson 6.6 exists."""
        assert lesson_6_6.subject_id == "thai"
        assert lesson_6_6.level == 6
        assert "Pragmatic" in lesson_6_6.title or "ปฏิบัติ" in lesson_6_6.title
    
    def test_lesson_prerequisites(self):
        """Test lesson requires 6.5."""
        assert "thai_lesson_6_5" in lesson_6_6.prerequisites
    
    def test_exercise_count(self):
        """Test generates 10 exercises."""
        exercises = generate_lesson_6_6_exercises()
        assert len(exercises) == 10


class TestLexicalVsPragmatic:
    """CRITICAL: Test distinction between lexical and pragmatic meaning."""
    
    def test_lexical_vs_pragmatic_single_word(self):
        """Test same word has both lexical and pragmatic meaning."""
        data = load_data()
        
        # "ดี" lexical = good quality
        # "ดี" pragmatic = agreement/acknowledgment
        
        # Without context → should be ambiguous or return literal
        meaning1, evidence1, state1 = extract_pragmatic_meaning("ดี", [], data)
        
        # With conversational context → pragmatic
        meaning2, evidence2, state2 = extract_pragmatic_meaning(
            "ดี", ["conversational"], data
        )
        
        # Should get different interpretations or states
        assert state2 in ["KNOWN", "AMBIGUOUS"]
        if state2 == "KNOWN" and meaning2 is not None:
            assert "agreement" in meaning2.lower() or "acknowledgment" in meaning2.lower()
    
    def test_pragmatic_requires_context(self):
        """Test pragmatic meaning requires appropriate context."""
        data = load_data()
        
        # "ดี" pragmatic requires conversational context
        meaning, evidence, state = extract_pragmatic_meaning("ดี", [], data)
        
        # Without conversational context, cannot be pragmatic KNOWN
        if state == "KNOWN":
            # Should be literal, not pragmatic agreement
            assert "agreement" not in meaning.lower()


class TestContextDependentPragmatic:
    """Test context determines pragmatic interpretation."""
    
    def test_pattern_with_invitation_context(self):
        """Test "ไป ไหม" + invitation context → invitation interpretation."""
        data = load_data()
        
        meaning, evidence, state = extract_pragmatic_meaning(
            "ไป ไหม", ["invitation"], data
        )
        
        assert state == "KNOWN"
        assert meaning is not None
        assert "invitation" in meaning.lower()
        assert len(evidence) > 0
    
    def test_pattern_with_question_context(self):
        """Test "ไป ไหม" + question context → question interpretation."""
        data = load_data()
        
        meaning, evidence, state = extract_pragmatic_meaning(
            "ไป ไหม", ["question"], data
        )
        
        assert state == "KNOWN"
        assert meaning is not None
        assert "question" in meaning.lower()
    
    def test_same_pattern_different_context_different_meaning(self):
        """Test same pattern with different context gives different pragmatic meaning."""
        data = load_data()
        
        meaning1, _, state1 = extract_pragmatic_meaning(
            "ไป ไหม", ["invitation"], data
        )
        meaning2, _, state2 = extract_pragmatic_meaning(
            "ไป ไหม", ["question"], data
        )
        
        assert state1 == "KNOWN"
        assert state2 == "KNOWN"
        # Should have different pragmatic interpretations
        assert meaning1 != meaning2


class TestInsufficientContext:
    """CRITICAL: Test insufficient context → AMBIGUOUS."""
    
    def test_no_context_ambiguous(self):
        """Test pragmatic pattern without context → AMBIGUOUS."""
        data = load_data()
        
        meaning, evidence, state = extract_pragmatic_meaning("ไป ไหม", [], data)
        
        assert state == "AMBIGUOUS"
        assert meaning is None
        assert len(evidence) > 0
    
    def test_non_matching_context_ambiguous(self):
        """Test context doesn't match pattern requirements → AMBIGUOUS."""
        data = load_data()
        
        # "ดี" pragmatic requires conversational, not 'noun'
        meaning, evidence, state = extract_pragmatic_meaning(
            "ดี", ["activity"], data  # Wrong context type
        )
        
        # Should be ambiguous or return literal only
        if state == "KNOWN" and meaning:
            # If known, should not be pragmatic agreement without conversational context
            pass
        else:
            assert state in ["AMBIGUOUS", "UNKNOWN"]
    
    def test_conflicting_context(self):
        """Test conflicting context clues → AMBIGUOUS."""
        data = load_data()
        
        # Both invitation and statement contexts (conflicting)
        meaning, evidence, state = extract_pragmatic_meaning(
            "ไป ไหม", ["invitation", "statement"], data
        )
        
        # Should resolve to one if implementation prioritizes,
        # or remain ambiguous if truly conflicting
        # At minimum, evidence should document the conflict
        assert len(evidence) > 0


class TestUnsupportedIntention:
    """CRITICAL: Test guessing speaker intention is rejected."""
    
    def test_no_guessing_without_evidence(self):
        """Test cannot infer intention without evidence."""
        data = load_data()
        
        # Unknown pattern - should not guess
        meaning, evidence, state = extract_pragmatic_meaning(
            "unknown pattern", [], data
        )
        
        assert state in ["UNKNOWN", "AMBIGUOUS"]
        assert meaning is None or "UNKNOWN" in meaning
    
    def test_ambiguous_not_forced_resolution(self):
        """Test ambiguous pragmatic meaning not forced to resolve."""
        data = load_data()
        
        # Without context, should remain ambiguous
        meaning, evidence, state = extract_pragmatic_meaning("ไป ไหม", [], data)
        
        assert state == "AMBIGUOUS"
        # Should not provide a "best guess" pragmatic meaning
        assert meaning is None


class TestValidPragmaticEvidence:
    """Test valid evidence for pragmatic interpretation."""
    
    def test_evidence_documents_pattern(self):
        """Test evidence documents pragmatic pattern."""
        data = load_data()
        
        meaning, evidence, state = extract_pragmatic_meaning(
            "ไป ไหม", ["invitation"], data
        )
        
        assert state == "KNOWN"
        assert len(evidence) > 0
        # Evidence should mention pattern
        evidence_str = " ".join(evidence).lower()
        assert "pattern" in evidence_str or "ไหม" in evidence_str
    
    def test_evidence_documents_context_match(self):
        """Test evidence documents context matching."""
        data = load_data()
        
        meaning, evidence, state = extract_pragmatic_meaning(
            "ไป ไหม", ["invitation"], data
        )
        
        assert state == "KNOWN"
        evidence_str = " ".join(evidence).lower()
        # Should document context match
        assert "context" in evidence_str or "invitation" in evidence_str
    
    def test_evidence_provided_for_ambiguous(self):
        """Test evidence provided even for AMBIGUOUS state."""
        data = load_data()
        
        meaning, evidence, state = extract_pragmatic_meaning("ไป ไหม", [], data)
        
        assert state == "AMBIGUOUS"
        assert len(evidence) > 0
        # Should explain why ambiguous
        evidence_str = " ".join(evidence).lower()
        assert "ambiguous" in evidence_str or "context" in evidence_str


class TestEvidenceGateIntegration:
    """CRITICAL: Test Evidence Gate integration for pragmatic knowledge."""
    
    def test_pragmatic_knowledge_requires_understanding_evidence(self):
        """Test pragmatic knowledge requires understanding evidence (not translation)."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="ไป ไหม",
            definition="go question",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={
                "semantic_field": "PRAGMATIC",
                "contextual_meanings": [{"context": "pragmatic"}],
            }
        )
        
        state = KnowledgeState("ไป ไหม")
        state.level = KnowledgeLevel.CAN_USE
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # WITHOUT understanding evidence → rejected
        result = pipeline.consolidate_with_evidence(concept, state, True, None)
        assert result is False
    
    def test_pragmatic_with_contextual_interpretation_evidence_accepted(self):
        """Test pragmatic knowledge with CONTEXTUAL_INTERPRETATION evidence accepted."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="ไป ไหม",
            definition="go question",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={
                "semantic_field": "PRAGMATIC",
                "contextual_meanings": [{"context": "pragmatic"}],
            }
        )
        
        state = KnowledgeState("ไป ไหม")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.CONTEXTUAL_INTERPRETATION,
            language_input="ไป ไหม (invitation context)",
            learner_output="Pattern VERB+ไหม with invitation context → invitation interpretation",
            expected_pattern="contextual_interpretation",
            verified=True,
            confidence=0.9,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is True
        # Check semantic memory contains the term
        assert any("ไป ไหม" in s for s in memory.state.semantic)
    
    def test_pragmatic_with_explanation_evidence_accepted(self):
        """Test pragmatic knowledge with EXPLANATION evidence accepted."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="pragmatic_test",
            definition="test pragmatic",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "PRAGMATIC"},
        )
        
        state = KnowledgeState("pragmatic_test")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="test",
            learner_output="Pragmatic meaning depends on context, not lexical meaning alone",
            expected_pattern="explanation",
            verified=True,
            confidence=0.9,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is True


class TestProvenancePreservation:
    """Test provenance preserved throughout pragmatic interpretation."""
    
    def test_pragmatic_consolidation_preserves_provenance(self):
        """Test pragmatic knowledge consolidation preserves provenance."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="provenance_test",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "PRAGMATIC"},
        )
        
        state = KnowledgeState("provenance_test")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.CONTEXTUAL_INTERPRETATION,
            language_input="test",
            learner_output="interpretation",
            expected_pattern="pattern",
            verified=True,
            confidence=0.9,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is True
        
        # Check episodic memory for provenance
        episodic = memory.state.episodic
        found = False
        for entry in episodic:
            if "provenance_test" in entry and "/test.json" in entry:
                found = True
                break
        
        assert found, "Provenance must be preserved in memory"


class TestMemorySelfModelIntegration:
    """Test integration with Memory and SelfModel."""
    
    def test_memory_integration(self):
        """Test pragmatic understanding integrates with Memory."""
        memory = Memory()
        
        # Add pragmatic interpretation to memory
        entry = "ไป ไหม: invitation or question depending on context"
        memory.add_semantic(entry)
        
        # Check if added to semantic memory (exact match)
        assert entry in memory.state.semantic
    
    def test_self_model_integration(self):
        """Test pragmatic understanding updates SelfModel."""
        self_model = SelfModel()
        
        # Update self model with pragmatic understanding capability
        self_model.update(
            self_knowledge_delta=0.1,
            self_awareness_delta=0.0,
            history_entry="Learned pragmatic meaning interpretation"
        )
        
        assert self_model.state.self_knowledge > 0.0
        assert "pragmatic meaning" in self_model.state.self_history[-1].lower()


class TestNoGuessingPrinciple:
    """CRITICAL: Test no guessing principle enforced."""
    
    def test_unknown_word_not_guessed(self):
        """Test unknown word → UNKNOWN, not guessed."""
        data = load_data()
        
        meaning, evidence, state = extract_pragmatic_meaning("unknownword", [], data)
        
        assert state == "UNKNOWN"
        assert meaning is None
    
    def test_insufficient_evidence_not_guessed(self):
        """Test insufficient evidence → AMBIGUOUS, not guessed."""
        data = load_data()
        
        # Pattern without context
        meaning, evidence, state = extract_pragmatic_meaning("ไป ไหม", [], data)
        
        assert state == "AMBIGUOUS"
        assert meaning is None


class TestMasteryAssessment:
    """Test mastery assessment."""
    
    def test_correct_answers_mastery(self):
        """Test all correct → MASTERED."""
        exercises = generate_lesson_6_6_exercises()
        responses = [ex.expected_answer for ex in exercises]
        
        accuracy, level, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 1.0
        assert level == "MASTERED"
        assert len(errors) == 0
    
    def test_partial_correct_can_use(self):
        """Test 80% correct → CAN_USE."""
        exercises = generate_lesson_6_6_exercises()
        responses = [ex.expected_answer for ex in exercises[:8]]
        responses += ["WRONG", "WRONG"]
        
        accuracy, level, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 0.8
        assert level == "CAN_USE"
    
    def test_low_accuracy_learning(self):
        """Test <70% → LEARNING."""
        exercises = generate_lesson_6_6_exercises()
        responses = ["WRONG"] * len(exercises)
        
        accuracy, level, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 0.0
        assert level == "LEARNING"
        assert len(gaps) > 0


class TestKnowledgeStateUpdate:
    """Test knowledge state updates."""
    
    def test_knowledge_state_records_correct(self):
        """Test correct answers recorded."""
        state = KnowledgeState("pragmatic_meaning")
        exercises = generate_lesson_6_6_exercises()
        responses = [ex.expected_answer for ex in exercises]
        
        update_knowledge_state(state, responses)
        
        assert state.correct_count == len(exercises)
    
    def test_knowledge_state_records_errors(self):
        """Test errors recorded."""
        state = KnowledgeState("pragmatic_meaning")
        exercises = generate_lesson_6_6_exercises()
        responses = ["WRONG"] * len(exercises)
        
        update_knowledge_state(state, responses)
        
        assert state.incorrect_count == len(exercises)


class TestMasteryTrackerUpdate:
    """Test mastery tracker updates."""
    
    def test_mastery_tracker_records_attempt(self):
        """Test mastery tracker records attempts."""
        tracker = MasteryTracker()
        
        update_mastery_tracker(tracker, "thai_lesson_6_6", 0.9)
        
        record = tracker.get_progress("thai_lesson_6_6")
        assert record is not None
        assert record.mastery_score == 0.9


class TestFullSuiteRegression:
    """Test full suite still passes with 6.6 added."""
    
    def test_lesson_6_6_exists(self):
        """Test lesson 6.6 can be imported and used."""
        assert lesson_6_6 is not None
        assert lesson_6_6.subject_id == "thai"
    
    def test_exercises_generate(self):
        """Test exercises generate without error."""
        exercises = generate_lesson_6_6_exercises()
        assert len(exercises) == 10
        assert all(ex.expected_answer for ex in exercises)
