"""
Test Week 6.9: Understanding ≠ Memorization Enforcement

CRITICAL: These are regression tests proving memorization loopholes are closed.
Tests architectural enforcement, not just lesson exercises.
"""
import pytest

from runtime.education.semantic_representation import (
    UnderstandingEvidence,
    EvidenceType,
    SemanticVerifier,
)
from runtime.knowledge_ingestion import (
    Concept,
    Provenance,
    KnowledgeIngestionPipeline,
    SourceType,
)
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel
from runtime.memory import Memory


class TestMemorizationLoopholes:
    """CRITICAL: Test memorization attack paths are blocked."""
    
    def test_memorized_answer_as_explanation_rejected(self):
        """Test memorized answer labeled as EXPLANATION is rejected."""
        # Attack: Just repeat input, label as EXPLANATION
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="ไป กิน",
            learner_output="ไป กิน",  # Same as input
            expected_pattern="explanation",
            verified=True,
            confidence=1.0,
        )
        
        # SemanticVerifier should catch this
        valid, errors = SemanticVerifier.validate_understanding_evidence(evidence)
        assert valid is False
        assert any("repeat input" in e.lower() for e in errors)
    
    def test_application_same_as_input_rejected(self):
        """Test APPLICATION that just repeats input is rejected."""
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.APPLICATION,
            language_input="VERB+VERB pattern",
            learner_output="VERB+VERB pattern",  # Same as input
            expected_pattern="application",
            verified=True,
            confidence=1.0,
        )
        
        valid, errors = SemanticVerifier.validate_understanding_evidence(evidence)
        assert valid is False
        assert any("new example" in e.lower() for e in errors)
    
    def test_transfer_with_memorized_input_rejected(self):
        """Test TRANSFER containing memorized input is rejected."""
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.TRANSFER,
            language_input="ไป กิน",
            learner_output="The pattern is ไป กิน serial verb",  # Contains input
            expected_pattern="transfer",
            verified=True,
            confidence=1.0,
        )
        
        valid, errors = SemanticVerifier.validate_understanding_evidence(evidence)
        assert valid is False
        assert any("new material" in e.lower() or "memorized" in e.lower() for e in errors)
    
    def test_short_explanation_rejected(self):
        """Test too-short EXPLANATION is rejected."""
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="ไป",
            learner_output="go",  # Too short
            expected_pattern="explanation",
            verified=True,
            confidence=1.0,
        )
        
        valid, errors = SemanticVerifier.validate_understanding_evidence(evidence)
        assert valid is False
        assert any("too short" in e.lower() for e in errors)


class TestEvidenceGateIntegration:
    """CRITICAL: Test Evidence Gate calls SemanticVerifier."""
    
    def test_gate_rejects_memorized_explanation(self):
        """Test Evidence Gate rejects memorized answer labeled as EXPLANATION."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="test_memorized",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("test_memorized")
        state.level = KnowledgeLevel.MASTERED
        
        # Memorized answer labeled as EXPLANATION
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="ไป กิน",
            learner_output="ไป กิน",  # Same as input
            expected_pattern="explanation",
            verified=True,
            confidence=1.0,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Should REJECT (SemanticVerifier catches same-as-input)
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is False
    
    def test_gate_rejects_application_same_as_input(self):
        """Test Evidence Gate rejects APPLICATION same as input."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="test_app",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("test_app")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.APPLICATION,
            language_input="pattern",
            learner_output="pattern",  # Same
            expected_pattern="application",
            verified=True,
            confidence=1.0,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is False
    
    def test_gate_rejects_short_explanation(self):
        """Test Evidence Gate rejects too-short explanation."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="test_short",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("test_short")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="word",
            learner_output="go",  # Too short
            expected_pattern="explanation",
            verified=True,
            confidence=1.0,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is False
    
    def test_gate_accepts_valid_explanation(self):
        """Test Evidence Gate accepts valid explanation."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="test_valid",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("test_valid")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="ไป",
            learner_output="Motion verb with literal and pragmatic meanings",
            expected_pattern="explanation",
            verified=True,
            confidence=0.9,
            explanation="Learner provided semantic field and meaning types",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is True
    
    def test_gate_accepts_valid_application(self):
        """Test Evidence Gate accepts valid application."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="test_valid_app",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("test_valid_app")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.APPLICATION,
            language_input="VERB+VERB pattern",
            learner_output="ไป กิน (go eat)",  # Different from input
            expected_pattern="application",
            verified=True,
            confidence=0.9,
            explanation="Learner applied pattern to new example",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is True


class TestHighAccuracyMemorization:
    """Test high accuracy from memorization doesn't bypass gate."""
    
    def test_perfect_accuracy_memorized_rejected(self):
        """Test perfect accuracy with memorized evidence rejected."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="perfect_memorized",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        # Perfect numeric score
        state = KnowledgeState("perfect_memorized")
        for _ in range(10):
            state.record_correct()
        
        assert state.level == KnowledgeLevel.MASTERED
        
        # But memorized evidence
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="test input",
            learner_output="test input",  # Memorized
            expected_pattern="explanation",
            verified=True,
            confidence=1.0,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Still rejected despite perfect score
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is False


class TestEvidenceTypeMislabeling:
    """Test mislabeled evidence types are caught."""
    
    def test_translation_mislabeled_as_explanation(self):
        """Test translation output mislabeled as EXPLANATION is caught."""
        # Translation output
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,  # Mislabeled
            language_input="ไป",
            learner_output="go",  # This is translation, not explanation
            expected_pattern="explanation",
            verified=True,
            confidence=1.0,
        )
        
        # SemanticVerifier catches: too short
        valid, errors = SemanticVerifier.validate_understanding_evidence(evidence)
        assert valid is False
        assert any("too short" in e.lower() for e in errors)


class TestMemoryProtection:
    """Test Memory doesn't accept memorization claims."""
    
    def test_memory_rejects_memorized_semantic(self):
        """Test Memory rejects semantic claim from memorized evidence."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="memory_test",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("memory_test")
        state.level = KnowledgeLevel.MASTERED
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="input",
            learner_output="input",  # Memorized
            expected_pattern="explanation",
            verified=True,
            confidence=1.0,
        )
        
        memory = Memory()
        initial_count = len(memory.state.semantic)
        
        pipeline = KnowledgeIngestionPipeline(memory)
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        
        assert result is False
        assert len(memory.state.semantic) == initial_count


class TestRegression61To68:
    """Test 6.1-6.8 still work after 6.9 changes."""
    
    def test_translation_rejection_still_works(self):
        """Test translation-only rejection (6.8) still works."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="translation_test",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("translation_test")
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
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Should still reject TRANSLATION type
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is False
    
    def test_valid_understanding_still_accepted(self):
        """Test valid understanding evidence (6.1-6.8) still accepted."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="understanding_test",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("understanding_test")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="input",
            learner_output="This is a detailed explanation with semantic content",
            expected_pattern="explanation",
            verified=True,
            confidence=0.9,
            explanation="Learner provided detailed semantic explanation",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # Should still accept valid evidence
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is True


class TestNoLLM:
    """Test no LLM dependency."""
    
    def test_validation_works_without_llm(self):
        """Test SemanticVerifier works without LLM."""
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="test",
            learner_output="test",
            expected_pattern="explanation",
            verified=True,
            confidence=1.0,
        )
        
        # Should work deterministically
        valid, errors = SemanticVerifier.validate_understanding_evidence(evidence)
        assert valid is False
        assert len(errors) > 0
