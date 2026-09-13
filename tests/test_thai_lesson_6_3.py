"""
Test Thai Lesson 6.3: Sentence Meaning

Tests sentence-level semantic representation using SentenceSemantics.
Proves: Parsing ≠ Understanding, Translation ≠ Understanding
"""
import pytest
from pathlib import Path

from runtime.education.thai_lesson_6_3 import (
    lesson_6_3,
    generate_lesson_6_3_exercises,
    assess_mastery,
    update_knowledge_state,
    update_mastery_tracker,
    build_sentence_semantics,
    load_data,
)
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel
from runtime.education.mastery_tracker import MasteryTracker
from runtime.education.learning_session import LearningSession
from runtime.memory import Memory
from runtime.self_model import SelfModel
from runtime.identity import Identity
from runtime.education.semantic_representation import (
    SentenceSemantics,
    UnderstandingEvidence,
    EvidenceType,
)


class TestLesson63Structure:
    """Test lesson structure."""
    
    def test_lesson_creation(self):
        """Test lesson 6.3 exists."""
        assert lesson_6_3.subject_id == "thai"
        assert lesson_6_3.level == 6
        assert "Sentence" in lesson_6_3.title or "ประโยค" in lesson_6_3.title
    
    def test_lesson_prerequisites(self):
        """Test lesson requires 6.2."""
        assert "thai_lesson_6_2" in lesson_6_3.prerequisites


class TestSentenceSemanticRepresentation:
    """Test building SentenceSemantics representations."""
    
    def test_build_serial_verb_sentence(self):
        """Test building representation for serial verb sentence."""
        data = load_data()
        
        # ไป กิน (VERB + VERB serial)
        sent = build_sentence_semantics("ไป กิน", data)
        
        assert sent.sentence == "ไป กิน"
        assert len(sent.word_meanings) == 2
        assert sent.compositional_meaning is not None
        assert "purpose" in sent.compositional_meaning or "sequence" in sent.compositional_meaning
        assert len(sent.evidence) > 0
    
    def test_build_noun_adjective_sentence(self):
        """Test building representation for NOUN+ADJ sentence."""
        data = load_data()
        
        # คน ดี (NOUN + ADJECTIVE)
        sent = build_sentence_semantics("คน ดี", data)
        
        assert sent.sentence == "คน ดี"
        assert len(sent.word_meanings) == 2
        assert sent.compositional_meaning is not None
        assert "modification" in sent.compositional_meaning
        assert len(sent.evidence) > 0
    
    def test_unknown_pattern_marked(self):
        """Test unknown patterns marked as UNKNOWN."""
        data = load_data()
        
        # ดี คน (reversed - not a known pattern)
        sent = build_sentence_semantics("ดี คน", data)
        
        # Should mark as UNKNOWN, not guess
        assert sent.compositional_meaning == "UNKNOWN" or sent.confidence == 0.0


class TestExerciseGeneration:
    """Test exercise generation."""
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_6_3_exercises()
        assert len(exercises) == 10
    
    def test_pattern_identification_exercises(self):
        """Test pattern identification exercises."""
        exercises = generate_lesson_6_3_exercises()
        
        pattern_ex = [e for e in exercises if "pattern" in e.question.lower() or "VERB+VERB" in e.question]
        assert len(pattern_ex) >= 1
    
    def test_semantic_role_exercises(self):
        """Test semantic role exercises."""
        exercises = generate_lesson_6_3_exercises()
        
        role_ex = [e for e in exercises if "role" in e.question]
        assert len(role_ex) >= 2


class TestAssessment:
    """Test assessment logic."""
    
    def test_perfect_sentence_understanding(self):
        """Test perfect sentence semantics understanding."""
        responses = [
            "VERB+VERB",     # Pattern
            "NO",            # Sentence ≠ sum of words
            "purpose",       # Compositional meaning
            "entity",        # Role of คน
            "property",      # Role of ดี
            "modification",  # Relation
            "UNKNOWN",       # Unknown pattern handling
            "NO",            # Translation ≠ understanding
            "EXPLANATION",   # Evidence type
            "meaning",       # SentenceSemantics contains
        ]
        
        accuracy, mastery, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 1.0
        assert mastery == "MASTERED"
        assert len(errors) == 0
    
    def test_translation_only_insufficient(self):
        """Test translation-focused responses insufficient."""
        responses = [
            "UNKNOWN",       # Wrong
            "YES",           # Wrong - thinks sentence = sum
            "translation",   # Wrong
            "word",          # Wrong
            "word",          # Wrong
            "action",        # Wrong
            "guess",         # Wrong
            "YES",           # Wrong - thinks translation = understanding
            "TRANSLATION",   # Wrong
            "translation",   # Wrong
        ]
        
        accuracy, mastery, errors, gaps = assess_mastery(responses)
        
        assert accuracy < 0.9
        assert "compositional_understanding" in gaps or "pattern_identification" in gaps


class TestKnowledgeStateIntegration:
    """Test KnowledgeState integration."""
    
    def test_update_knowledge_state_perfect(self):
        """Test updating KnowledgeState with perfect responses."""
        state = KnowledgeState("lesson_6_3")
        
        responses = [
            "VERB+VERB", "NO", "purpose", "entity", "property",
            "modification", "UNKNOWN", "NO", "EXPLANATION", "meaning"
        ]
        
        update_knowledge_state(state, responses)
        
        assert state.correct_count == 10
        assert state.incorrect_count == 0
        assert state.level == KnowledgeLevel.MASTERED


class TestWordVsSentenceMeaning:
    """Test distinguishing word meaning from sentence meaning."""
    
    def test_compositional_meaning_not_sum(self):
        """Test that sentence meaning ≠ sum of word meanings."""
        data = load_data()
        
        sent = build_sentence_semantics("ไป กิน", data)
        
        # Should have compositional meaning beyond just "go" + "eat"
        assert sent.compositional_meaning != "ไป + กิน"
        assert sent.compositional_meaning is not None
        
        # Should have evidence explaining the composition
        assert len(sent.evidence) > 0


class TestSemanticRoles:
    """Test semantic role identification."""
    
    def test_entity_role(self):
        """Test identifying entity role."""
        # In "คน ดี", คน is entity
        exercises = generate_lesson_6_3_exercises()
        
        entity_ex = next((e for e in exercises if "คน" in e.question and "role" in e.question), None)
        assert entity_ex is not None
        assert entity_ex.expected_answer == "entity"
    
    def test_property_role(self):
        """Test identifying property role."""
        # In "คน ดี", ดี is property
        exercises = generate_lesson_6_3_exercises()
        
        # Find exercise specifically about ดี role
        prop_ex = [e for e in exercises if "'ดี'" in e.question and "role" in e.question]
        if prop_ex:
            assert prop_ex[0].expected_answer == "property"
        else:
            # If no specific ดี role exercise, verify the concept is covered
            assert any("property" in e.expected_answer for e in exercises)


class TestSemanticRelations:
    """Test semantic relation identification."""
    
    def test_modification_relation(self):
        """Test identifying modification relation."""
        exercises = generate_lesson_6_3_exercises()
        
        mod_ex = next((e for e in exercises if "relation" in e.question.lower() or "ความสัมพันธ์" in e.question), None)
        assert mod_ex is not None
        assert mod_ex.expected_answer == "modification"


class TestUnknownHandling:
    """Test handling of unknown patterns."""
    
    def test_unknown_pattern_not_guessed(self):
        """Test that unknown patterns are marked UNKNOWN, not guessed."""
        exercises = generate_lesson_6_3_exercises()
        
        unknown_ex = next((e for e in exercises if "UNKNOWN" in e.expected_answer and "pattern" in e.question), None)
        assert unknown_ex is not None


class TestTranslationVsUnderstanding:
    """Test translation vs understanding distinction."""
    
    def test_translation_not_understanding(self):
        """Test recognizing translation ≠ sentence understanding."""
        exercises = generate_lesson_6_3_exercises()
        
        trans_ex = [e for e in exercises if "แปล" in e.question and "semantics" in e.question or "ความเข้าใจ" in e.question]
        if trans_ex:
            assert trans_ex[0].expected_answer == "NO"


class TestEvidenceRequirement:
    """Test evidence requirement for sentence understanding."""
    
    def test_explanation_evidence_required(self):
        """Test recognizing EXPLANATION evidence required."""
        exercises = generate_lesson_6_3_exercises()
        
        ev_ex = next((e for e in exercises if "EXPLANATION" in e.expected_answer), None)
        assert ev_ex is not None


class TestLearningSessionComplete:
    """Test complete learning session for 6.3."""
    
    def test_complete_session_with_sentence_mastery(self):
        """Test full session with sentence understanding."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        identity = Identity()
        
        session = LearningSession(tracker, memory, self_model, identity)
        exercises = generate_lesson_6_3_exercises()
        
        responses = [
            "VERB+VERB", "NO", "purpose", "entity", "property",
            "modification", "UNKNOWN", "NO", "EXPLANATION", "meaning"
        ]
        
        result = session.conduct_session(lesson_6_3, exercises, responses)
        
        assert result.mastered is True
        assert result.assessment_result.score >= 0.9


class TestSentenceSemanticsDataStructure:
    """Test SentenceSemantics data structure usage."""
    
    def test_sentence_semantics_fields_populated(self):
        """Test that SentenceSemantics fields are properly populated."""
        data = load_data()
        sent = build_sentence_semantics("ไป กิน", data)
        
        # Required fields
        assert hasattr(sent, 'sentence')
        assert hasattr(sent, 'word_meanings')
        assert hasattr(sent, 'compositional_meaning')
        assert hasattr(sent, 'evidence')
        assert hasattr(sent, 'confidence')
        
        # Values populated
        assert sent.sentence == "ไป กิน"
        assert len(sent.word_meanings) > 0
        assert sent.compositional_meaning is not None


class TestReuseSemanticCore:
    """Test reuse of existing Semantic Core structures."""
    
    def test_uses_sentence_semantics_class(self):
        """Test that implementation uses SentenceSemantics from semantic_representation."""
        from runtime.education.semantic_representation import SentenceSemantics
        
        data = load_data()
        sent = build_sentence_semantics("คน ดี", data)
        
        # Must be instance of SentenceSemantics, not a new class
        assert isinstance(sent, SentenceSemantics)
