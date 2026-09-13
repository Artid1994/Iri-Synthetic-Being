"""
Regression Tests for Evidence Gate
Tests that translation-only cannot bypass semantic understanding requirements.
"""
import pytest
from pathlib import Path
import json

from runtime.knowledge_ingestion import (
    Concept,
    Provenance,
    KnowledgeIngestionPipeline,
    SourceType,
)
from runtime.memory import Memory
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel
from runtime.education.semantic_representation import (
    UnderstandingEvidence,
    EvidenceType,
)


class TestTranslationOnlyRejection:
    """CRITICAL: Test translation-only evidence is rejected for semantic knowledge."""
    
    def test_translation_only_semantic_rejected(self):
        """Translation-only evidence rejected for semantic concept."""
        # Semantic concept with contextual_meanings
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="ไป",
            definition="go",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={
                "semantic_field": "MOTION",
                "contextual_meanings": [{"context": "literal"}],
            }
        )
        
        # High mastery level from translation practice
        state = KnowledgeState("ไป")
        state.record_correct()
        state.record_correct()
        state.record_correct()
        assert state.level == KnowledgeLevel.CAN_USE
        
        # NO understanding evidence provided
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(
            concept,
            state,
            evidence_verified=True,
            understanding_evidence=None,  # No evidence!
        )
        
        # MUST BE REJECTED
        assert result is False, "Semantic knowledge without understanding evidence must be rejected"
    
    def test_non_semantic_allows_mastery_only(self):
        """Non-semantic knowledge (phonology) can use mastery without understanding evidence."""
        # Non-semantic concept (no semantic_field, no contextual_meanings)
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="ก",
            definition="k sound",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"type": "consonant"},  # Not semantic
        )
        
        # Mastery level
        state = KnowledgeState("ก")
        state.record_correct()
        state.record_correct()
        state.record_correct()
        assert state.level == KnowledgeLevel.CAN_USE
        
        # No understanding evidence needed for non-semantic
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(
            concept,
            state,
            evidence_verified=True,
            understanding_evidence=None,  # OK for non-semantic
        )
        
        # MUST BE ACCEPTED
        assert result is True, "Non-semantic knowledge should consolidate with mastery only"


class TestUnderstandingEvidenceTypes:
    """Test different evidence types for semantic knowledge."""
    
    def test_explanation_evidence_accepted(self):
        """Explanation evidence accepted for semantic knowledge."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="ไป",
            definition="go",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "MOTION"},
        )
        
        state = KnowledgeState("ไป")
        state.level = KnowledgeLevel.CAN_USE
        
        # Explanation evidence
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="ไป",
            learner_output="Motion verb indicating direction away from speaker",
            expected_pattern="explanation",
            verified=True,
            confidence=0.9,
            explanation="Learner explained semantic field and directional meaning",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        
        assert result is True
        assert memory.semantic_contains("ไป: go")
    
    def test_application_evidence_accepted(self):
        """Application evidence accepted."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="กิน",
            definition="eat",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "ACTION"},
        )
        
        state = KnowledgeState("กิน")
        state.level = KnowledgeLevel.MASTERED
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.APPLICATION,
            language_input="กิน",
            learner_output="ไป กิน (go eat) - applied to new sentence",
            expected_pattern="application",
            verified=True,
            confidence=0.9,
            explanation="Applied ACTION verb in serial verb construction",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        
        assert result is True
    
    def test_transfer_evidence_accepted(self):
        """Transfer evidence accepted."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="ดี",
            definition="good",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "QUALITY"},
        )
        
        state = KnowledgeState("ดี")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.TRANSFER,
            language_input="คน ดี",
            learner_output="บ้าน ดี (good house) - transferred pattern",
            expected_pattern="transfer",
            verified=True,
            confidence=0.9,
            explanation="Transferred NOUN+ADJECTIVE pattern to new noun",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        
        assert result is True
    
    def test_unverified_evidence_rejected(self):
        """Unverified evidence rejected even if provided."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="test",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("test")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="test",
            learner_output="explanation",
            expected_pattern="pattern",
            verified=False,  # NOT VERIFIED
            confidence=0.9,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        
        assert result is False, "Unverified evidence must be rejected"


class TestAmbiguityHandling:
    """Test ambiguous knowledge handling."""
    
    def test_highly_ambiguous_rejected(self):
        """Highly ambiguous semantic knowledge rejected."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="ambiguous_word",
            definition="multiple meanings",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={
                "semantic_field": "TEST",
                "ambiguity_level": "HIGHLY_AMBIGUOUS",
            }
        )
        
        state = KnowledgeState("ambiguous_word")
        state.level = KnowledgeLevel.MASTERED
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="test",
            learner_output="explanation",
            expected_pattern="pattern",
            verified=True,
            confidence=0.9,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        
        assert result is False, "Highly ambiguous knowledge must be rejected"
    
    def test_mildly_ambiguous_accepted_with_evidence(self):
        """Mildly ambiguous accepted if evidence provided."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="mildly_ambiguous",
            definition="somewhat unclear",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={
                "semantic_field": "TEST",
                "ambiguity_level": "MILDLY_AMBIGUOUS",
            }
        )
        
        state = KnowledgeState("mildly_ambiguous")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.CONTEXTUAL_INTERPRETATION,
            language_input="test",
            learner_output="context-based interpretation",
            expected_pattern="pattern",
            verified=True,
            confidence=0.8,
            explanation="Interpreted meaning based on context",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        
        # MILDLY_AMBIGUOUS should be accepted with proper evidence
        assert result is True


class TestUnknownKnowledgeRejection:
    """Test UNKNOWN level rejected."""
    
    def test_unknown_level_rejected(self):
        """UNKNOWN level rejected regardless of evidence."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="unknown",
            definition="never practiced",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("unknown")
        # level = UNKNOWN (default)
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="test",
            learner_output="explanation",
            expected_pattern="pattern",
            verified=True,
            confidence=0.9,
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        
        assert result is False, "UNKNOWN level must be rejected"


class TestProvenanceWithEvidenceType:
    """Test provenance includes evidence type."""
    
    def test_provenance_records_evidence_type(self):
        """Test consolidated memory records evidence type."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="verified",
            definition="with evidence",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("verified")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.APPLICATION,
            language_input="test",
            learner_output="application",
            expected_pattern="pattern",
            verified=True,
            confidence=0.9,
            explanation="Applied pattern to new example",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        
        assert result is True
        
        # Check provenance in episodic memory includes evidence type
        episodic = memory.state.episodic
        found = False
        for entry in episodic:
            if "verified" in entry and "application" in entry:
                found = True
                break
        
        assert found, "Provenance must record evidence type"
