"""
Test Semantic Core Architecture
Tests semantic representation data structures and verification.
"""
import pytest
import json
from pathlib import Path

from runtime.education.semantic_representation import (
    SemanticMeaning,
    ContextualMeaning,
    SentenceSemantics,
    AmbiguityPoint,
    UnderstandingEvidence,
    SemanticVerifier,
    EvidenceStatus,
    ContextType,
    AmbiguityType,
    EvidenceType,
)


class TestSemanticMeaningStructure:
    """Test SemanticMeaning data structure."""
    
    def test_create_basic_semantic_meaning(self):
        """Test creating basic SemanticMeaning."""
        sem = SemanticMeaning(
            word="test",
            lexical_meaning="a test",
            confidence=1.0
        )
        assert sem.word == "test"
        assert sem.lexical_meaning == "a test"
        assert sem.confidence == 1.0
    
    def test_semantic_meaning_validation(self):
        """Test SemanticMeaning validation."""
        with pytest.raises(ValueError, match="Word cannot be empty"):
            SemanticMeaning(word="", lexical_meaning="test", confidence=1.0)
        
        with pytest.raises(ValueError, match="Lexical meaning cannot be empty"):
            SemanticMeaning(word="test", lexical_meaning="", confidence=1.0)
        
        with pytest.raises(ValueError, match="Confidence must be"):
            SemanticMeaning(word="test", lexical_meaning="test", confidence=1.5)
    
    def test_semantic_meaning_with_contextual(self):
        """Test SemanticMeaning with contextual meanings."""
        cm = ContextualMeaning(
            context_type=ContextType.LITERAL,
            meaning="literal meaning",
            confidence=1.0
        )
        
        sem = SemanticMeaning(
            word="ไป",
            lexical_meaning="go",
            contextual_meanings=[cm],
            confidence=1.0
        )
        
        assert len(sem.contextual_meanings) == 1
        assert sem.contextual_meanings[0].meaning == "literal meaning"
    
    def test_get_meaning_in_context(self):
        """Test retrieving meaning for specific context."""
        cm_literal = ContextualMeaning(
            context_type=ContextType.LITERAL,
            meaning="literal meaning",
            confidence=1.0
        )
        cm_pragmatic = ContextualMeaning(
            context_type=ContextType.PRAGMATIC,
            meaning="pragmatic meaning",
            confidence=0.8
        )
        
        sem = SemanticMeaning(
            word="ดี",
            lexical_meaning="good",
            contextual_meanings=[cm_literal, cm_pragmatic],
            confidence=1.0
        )
        
        literal = sem.get_meaning_in_context(ContextType.LITERAL)
        assert literal is not None
        assert literal.meaning == "literal meaning"
        
        pragmatic = sem.get_meaning_in_context(ContextType.PRAGMATIC)
        assert pragmatic is not None
        assert pragmatic.meaning == "pragmatic meaning"
    
    def test_is_ambiguous(self):
        """Test ambiguity detection."""
        unambiguous = SemanticMeaning(
            word="test",
            lexical_meaning="test",
            ambiguity_level="UNAMBIGUOUS",
            confidence=1.0
        )
        assert not unambiguous.is_ambiguous()
        
        ambiguous = SemanticMeaning(
            word="test",
            lexical_meaning="test",
            ambiguity_level="MILDLY_AMBIGUOUS",
            confidence=0.8
        )
        assert ambiguous.is_ambiguous()


class TestContextualMeaning:
    """Test ContextualMeaning structure."""
    
    def test_create_contextual_meaning(self):
        """Test creating ContextualMeaning."""
        cm = ContextualMeaning(
            context_type=ContextType.LITERAL,
            meaning="test meaning",
            required_context=["context1"],
            examples=["example1"],
            confidence=0.9,
            data_status=EvidenceStatus.KNOWN
        )
        
        assert cm.context_type == ContextType.LITERAL
        assert cm.meaning == "test meaning"
        assert len(cm.required_context) == 1
        assert cm.confidence == 0.9
    
    def test_contextual_meaning_validation(self):
        """Test validation."""
        with pytest.raises(ValueError, match="Confidence must be"):
            ContextualMeaning(
                context_type=ContextType.LITERAL,
                meaning="test",
                confidence=-0.1
            )
        
        with pytest.raises(ValueError, match="Meaning cannot be empty"):
            ContextualMeaning(
                context_type=ContextType.LITERAL,
                meaning="",
                confidence=1.0
            )


class TestSentenceSemantics:
    """Test SentenceSemantics structure."""
    
    def test_create_sentence_semantics(self):
        """Test creating SentenceSemantics."""
        ss = SentenceSemantics(
            sentence="ไป กิน",
            compositional_meaning="go eat",
            confidence=1.0
        )
        
        assert ss.sentence == "ไป กิน"
        assert ss.compositional_meaning == "go eat"
    
    def test_sentence_with_ambiguity(self):
        """Test sentence with ambiguity points."""
        amb = AmbiguityPoint(
            location="word:0",
            ambiguity_type=AmbiguityType.LEXICAL,
            possible_interpretations=["meaning1", "meaning2"]
        )
        
        ss = SentenceSemantics(
            sentence="test",
            ambiguity_points=[amb],
            confidence=0.7
        )
        
        assert ss.has_ambiguity()
        assert len(ss.ambiguity_points) == 1
    
    def test_get_final_meaning(self):
        """Test getting final meaning (pragmatic over compositional)."""
        ss = SentenceSemantics(
            sentence="test",
            compositional_meaning="compositional",
            pragmatic_meaning="pragmatic",
            confidence=0.9
        )
        
        assert ss.get_final_meaning() == "pragmatic"
        
        ss2 = SentenceSemantics(
            sentence="test",
            compositional_meaning="compositional",
            confidence=0.9
        )
        
        assert ss2.get_final_meaning() == "compositional"


class TestAmbiguityPoint:
    """Test AmbiguityPoint structure."""
    
    def test_create_ambiguity_point(self):
        """Test creating AmbiguityPoint."""
        amb = AmbiguityPoint(
            location="word:1",
            ambiguity_type=AmbiguityType.LEXICAL,
            possible_interpretations=["meaning1", "meaning2"]
        )
        
        assert amb.location == "word:1"
        assert amb.ambiguity_type == AmbiguityType.LEXICAL
        assert len(amb.possible_interpretations) == 2
    
    def test_ambiguity_validation(self):
        """Test ambiguity validation."""
        with pytest.raises(ValueError, match="at least one"):
            AmbiguityPoint(
                location="word:0",
                ambiguity_type=AmbiguityType.LEXICAL,
                possible_interpretations=[]
            )
        
        with pytest.raises(ValueError, match="at least 2"):
            AmbiguityPoint(
                location="word:0",
                ambiguity_type=AmbiguityType.LEXICAL,
                possible_interpretations=["only one"]
            )


class TestUnderstandingEvidence:
    """Test UnderstandingEvidence structure."""
    
    def test_create_understanding_evidence(self):
        """Test creating UnderstandingEvidence."""
        ev = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="ไป กิน",
            learner_output="Serial verb: V1 + V2",
            expected_pattern="Explanation of structure",
            verified=True,
            confidence=0.9
        )
        
        assert ev.evidence_type == EvidenceType.EXPLANATION
        assert ev.verified is True
        assert ev.confidence == 0.9
    
    def test_evidence_validation(self):
        """Test evidence validation."""
        with pytest.raises(ValueError, match="Language input cannot be empty"):
            UnderstandingEvidence(
                evidence_type=EvidenceType.EXPLANATION,
                language_input="",
                learner_output="output",
                expected_pattern="pattern",
                confidence=0.9
            )


class TestSemanticVerifier:
    """Test SemanticVerifier logic."""
    
    def test_validate_semantic_meaning_valid(self):
        """Test validation of valid SemanticMeaning."""
        sem = SemanticMeaning(
            word="test",
            lexical_meaning="meaning",
            evidence_status=EvidenceStatus.KNOWN,
            confidence=0.9
        )
        
        valid, errors = SemanticVerifier.validate_semantic_meaning(sem)
        assert valid is True
        assert len(errors) == 0
    
    def test_validate_semantic_meaning_confidence_mismatch(self):
        """Test validation catches confidence/status mismatch."""
        sem_unknown_high = SemanticMeaning(
            word="test",
            lexical_meaning="meaning",
            evidence_status=EvidenceStatus.UNKNOWN,
            confidence=0.9  # Too high for UNKNOWN
        )
        
        valid, errors = SemanticVerifier.validate_semantic_meaning(sem_unknown_high)
        assert valid is False
        assert any("UNKNOWN" in err for err in errors)
        
        sem_known_low = SemanticMeaning(
            word="test",
            lexical_meaning="meaning",
            evidence_status=EvidenceStatus.KNOWN,
            confidence=0.3  # Too low for KNOWN
        )
        
        valid, errors = SemanticVerifier.validate_semantic_meaning(sem_known_low)
        assert valid is False
        assert any("KNOWN" in err for err in errors)
    
    def test_validate_understanding_evidence_explanation(self):
        """Test validation of explanation evidence."""
        # Too short
        ev_short = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="test",
            learner_output="short",
            expected_pattern="pattern",
            confidence=0.9
        )
        
        valid, errors = SemanticVerifier.validate_understanding_evidence(ev_short)
        assert valid is False
        assert any("too short" in err.lower() for err in errors)
        
        # Adequate length
        ev_good = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="test",
            learner_output="This is a serial verb construction",
            expected_pattern="pattern",
            confidence=0.9
        )
        
        valid, errors = SemanticVerifier.validate_understanding_evidence(ev_good)
        assert valid is True
    
    def test_validate_understanding_evidence_transfer(self):
        """Test validation of transfer evidence."""
        # Uses input (not transfer)
        ev_not_transfer = UnderstandingEvidence(
            evidence_type=EvidenceType.TRANSFER,
            language_input="ไป กิน",
            learner_output="ไป กิน is the answer",
            expected_pattern="new example",
            confidence=0.9
        )
        
        valid, errors = SemanticVerifier.validate_understanding_evidence(ev_not_transfer)
        assert valid is False
        assert any("new material" in err for err in errors)


class TestSemanticKnowledgeBase:
    """Test semantic vocabulary knowledge base."""
    
    def test_semantic_vocabulary_loads(self):
        """Test semantic_vocabulary.json loads correctly."""
        vocab_file = Path("./03_Hippocampus/knowledge_base/thai_language/semantic_vocabulary.json")
        assert vocab_file.exists()
        
        data = json.loads(vocab_file.read_text())
        assert "semantic_vocabulary" in data
        assert len(data["semantic_vocabulary"]) > 0
        
        # Check first word structure
        word = data["semantic_vocabulary"][0]
        assert "word" in word
        assert "lexical_meaning" in word
        assert "semantic_field" in word
        assert "contextual_meanings" in word
        assert "evidence_status" in word
    
    def test_understanding_tests_loads(self):
        """Test understanding_tests.json loads correctly."""
        tests_file = Path("./03_Hippocampus/knowledge_base/thai_language/understanding_tests.json")
        assert tests_file.exists()
        
        data = json.loads(tests_file.read_text())
        assert "translation_is_not_understanding" in data
        assert "memorization_is_not_understanding" in data
        assert "understanding_evidence_types" in data
        assert "assessment_rules" in data
        
        # Check assessment rules
        rules = data["assessment_rules"]
        assert rules["translation_only_max_score"] == 0.70
        assert rules["memorization_only_max_score"] == 0.70
        assert rules["mastery_threshold"] == 0.90
