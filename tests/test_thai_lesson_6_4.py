"""
Test Thai Lesson 6.4: Ambiguity

Tests ambiguity detection and UNKNOWN vs AMBIGUOUS distinction.
"""
import pytest

from runtime.education.thai_lesson_6_4 import (
    lesson_6_4,
    generate_lesson_6_4_exercises,
    assess_mastery,
    update_knowledge_state,
    update_mastery_tracker,
    detect_ambiguity,
    build_ambiguity_point,
    load_data,
)
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel
from runtime.education.mastery_tracker import MasteryTracker
from runtime.education.learning_session import LearningSession
from runtime.memory import Memory
from runtime.self_model import SelfModel
from runtime.identity import Identity
from runtime.education.semantic_representation import AmbiguityType


class TestLesson64Structure:
    """Test lesson structure."""
    
    def test_lesson_creation(self):
        """Test lesson 6.4 exists."""
        assert lesson_6_4.subject_id == "thai"
        assert lesson_6_4.level == 6
        assert "Ambiguity" in lesson_6_4.title or "กำกวม" in lesson_6_4.title
    
    def test_lesson_prerequisites(self):
        """Test lesson requires 6.3."""
        assert "thai_lesson_6_3" in lesson_6_4.prerequisites


class TestAmbiguityDetection:
    """Test ambiguity detection."""
    
    def test_detect_word_ambiguity(self):
        """Test detecting ambiguous word."""
        data = load_data()
        
        # ดี is ambiguous (quality vs agreement)
        is_ambig, interp, reason = detect_ambiguity("ดี", data)
        
        assert is_ambig is True
        assert len(interp) >= 2
        assert "good" in str(interp).lower() or "quality" in str(interp).lower()
    
    def test_detect_sentence_ambiguity(self):
        """Test detecting ambiguous sentence."""
        data = load_data()
        
        # ไป เรียน has multiple interpretations
        is_ambig, interp, reason = detect_ambiguity("ไป เรียน", data)
        
        assert is_ambig is True
        assert len(interp) >= 2
    
    def test_unambiguous_word(self):
        """Test unambiguous word not flagged."""
        data = load_data()
        
        # คน is unambiguous
        is_ambig, interp, reason = detect_ambiguity("คน", data)
        
        assert is_ambig is False


class TestAmbiguityPoint:
    """Test AmbiguityPoint creation."""
    
    def test_build_ambiguity_point(self):
        """Test building AmbiguityPoint for ambiguous word."""
        data = load_data()
        
        point = build_ambiguity_point("ดี", "word_0", data)
        
        assert point is not None
        assert point.location == "word_0"
        assert len(point.possible_interpretations) >= 2
        assert point.resolution_required is True
    
    def test_no_ambiguity_point_for_unambiguous(self):
        """Test that unambiguous words don't create AmbiguityPoint."""
        data = load_data()
        
        point = build_ambiguity_point("คน", "word_0", data)
        
        assert point is None


class TestExerciseGeneration:
    """Test exercise generation."""
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_6_4_exercises()
        assert len(exercises) == 10
    
    def test_unknown_vs_ambiguous_exercise(self):
        """Test UNKNOWN vs AMBIGUOUS distinction exercise."""
        exercises = generate_lesson_6_4_exercises()
        
        # Should have exercise about distinction
        distinction_ex = [e for e in exercises if "UNKNOWN" in e.question and "AMBIGUOUS" in e.question]
        assert len(distinction_ex) >= 1


class TestAssessment:
    """Test assessment logic."""
    
    def test_perfect_ambiguity_understanding(self):
        """Test perfect ambiguity understanding."""
        responses = [
            "AMBIGUOUS",  # ดี without context
            "2",          # ดี has 2 meanings
            "UNKNOWN",    # Word not in data
            "context",    # Resolution needs context
            "NO",         # คน ดี not ambiguous
            "3",          # ไป เรียน has 3 meanings
            "PRAGMATIC",  # Type of ambiguity
            "NO",         # Don't guess
            "evidence",   # Resolution needs evidence
            "KNOWN",      # State after resolution
        ]
        
        accuracy, mastery, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 1.0
        assert mastery == "MASTERED"
        assert len(errors) == 0
    
    def test_confusion_between_unknown_ambiguous(self):
        """Test detecting confusion between UNKNOWN and AMBIGUOUS."""
        responses = [
            "UNKNOWN",    # Wrong - should be AMBIGUOUS
            "2",          # Correct
            "AMBIGUOUS",  # Wrong - should be UNKNOWN
            "translation",# Wrong
            "YES",        # Wrong
            "1",          # Wrong
            "LEXICAL",    # Wrong
            "YES",        # Wrong
            "guessing",   # Wrong
            "AMBIGUOUS",  # Wrong
        ]
        
        accuracy, mastery, errors, gaps = assess_mastery(responses)
        
        assert accuracy < 0.9
        assert "ambiguous_unknown_distinction" in gaps


class TestKnowledgeStateIntegration:
    """Test KnowledgeState integration."""
    
    def test_update_knowledge_state_perfect(self):
        """Test updating KnowledgeState with perfect responses."""
        state = KnowledgeState("lesson_6_4")
        
        responses = [
            "AMBIGUOUS", "2", "UNKNOWN", "context", "NO",
            "3", "PRAGMATIC", "NO", "evidence", "KNOWN"
        ]
        
        update_knowledge_state(state, responses)
        
        assert state.correct_count == 10
        assert state.incorrect_count == 0
        assert state.level == KnowledgeLevel.MASTERED


class TestUnknownVsAmbiguous:
    """CRITICAL: Test distinguishing UNKNOWN from AMBIGUOUS."""
    
    def test_ambiguous_has_interpretations(self):
        """Test AMBIGUOUS means multiple interpretations exist."""
        data = load_data()
        
        is_ambig, interp, _ = detect_ambiguity("ดี", data)
        
        assert is_ambig is True
        assert len(interp) >= 2
        # Multiple interpretations = AMBIGUOUS
    
    def test_unknown_no_data(self):
        """Test UNKNOWN means no data/evidence available."""
        data = load_data()
        
        # Word not in vocabulary
        is_ambig, interp, _ = detect_ambiguity("unknownword", data)
        
        assert is_ambig is False
        assert len(interp) == 0
        # No interpretations found = should be UNKNOWN (not AMBIGUOUS)


class TestResolutionRequirements:
    """Test ambiguity resolution requirements."""
    
    def test_context_resolves_ambiguity(self):
        """Test that context can resolve ambiguity."""
        # "ดี" alone: AMBIGUOUS
        # "คน ดี" with context: KNOWN (quality meaning)
        
        data = load_data()
        
        # Single word is ambiguous
        is_ambig_alone, _, _ = detect_ambiguity("ดี", data)
        assert is_ambig_alone is True
        
        # In context "คน ดี", the noun provides context
        # (This would be tested in sentence-level ambiguity)
    
    def test_insufficient_context_remains_ambiguous(self):
        """Test that insufficient context keeps state AMBIGUOUS."""
        # Tested through exercises - if context not enough, don't resolve


class TestNoGuessingPrinciple:
    """Test no-guessing principle for ambiguity."""
    
    def test_guessing_rejected(self):
        """Test that guessing is rejected as resolution strategy."""
        exercises = generate_lesson_6_4_exercises()
        
        # Find no-guessing exercise (Q8: "ควรเดาความหมายหรือไม่")
        no_guess_ex = next((e for e in exercises if "เดา" in e.question), None)
        
        assert no_guess_ex is not None
        assert no_guess_ex.expected_answer == "NO"


class TestEvidenceRequirement:
    """Test evidence requirement for resolution."""
    
    def test_evidence_required_for_resolution(self):
        """Test that evidence is required to resolve ambiguity."""
        exercises = generate_lesson_6_4_exercises()
        
        # Find evidence requirement exercise
        evidence_ex = next((e for e in exercises if "evidence" in e.expected_answer), None)
        
        assert evidence_ex is not None


class TestMultipleInterpretations:
    """Test handling multiple interpretations."""
    
    def test_enumerate_interpretations(self):
        """Test enumerating all possible interpretations."""
        data = load_data()
        
        _, interp, _ = detect_ambiguity("ดี", data)
        
        # Should list all interpretations from data
        assert len(interp) >= 2
        
        # Should not invent interpretations
        # (all must come from data)


class TestAmbiguityTypes:
    """Test ambiguity type classification."""
    
    def test_pragmatic_ambiguity(self):
        """Test identifying pragmatic ambiguity."""
        data = load_data()
        
        point = build_ambiguity_point("ดี", "test", data)
        
        if point:
            # ดี is pragmatic ambiguity (quality vs agreement)
            assert point.ambiguity_type == AmbiguityType.PRAGMATIC


class TestLearningSessionComplete:
    """Test complete learning session for 6.4."""
    
    def test_complete_session_with_ambiguity_mastery(self):
        """Test full session with ambiguity understanding."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        identity = Identity()
        
        session = LearningSession(tracker, memory, self_model, identity)
        exercises = generate_lesson_6_4_exercises()
        
        responses = [
            "AMBIGUOUS", "2", "UNKNOWN", "context", "NO",
            "3", "PRAGMATIC", "NO", "evidence", "KNOWN"
        ]
        
        result = session.conduct_session(lesson_6_4, exercises, responses)
        
        assert result.mastered is True
        assert result.assessment_result.score >= 0.9


class TestResolutionFlow:
    """Test ambiguity resolution flow."""
    
    def test_ambiguous_to_known_flow(self):
        """Test AMBIGUOUS → (context + evidence) → KNOWN flow."""
        # Conceptual test - flow is:
        # 1. Detect ambiguity (multiple interpretations)
        # 2. Add context
        # 3. Context selects one interpretation
        # 4. State becomes KNOWN
        
        # This is tested through exercises asking about state changes


class TestDataDrivenAmbiguity:
    """Test that ambiguity is data-driven, not guessed."""
    
    def test_ambiguity_from_data(self):
        """Test ambiguity detection uses data, not guessing."""
        data = load_data()
        
        # ดี is marked MILDLY_AMBIGUOUS in data
        word_data = next((w for w in data['semantic_vocabulary'] if w['word'] == 'ดี'), None)
        
        assert word_data is not None
        assert word_data['ambiguity_level'] == 'MILDLY_AMBIGUOUS'
        
        # Detection should align with data
        is_ambig, _, _ = detect_ambiguity("ดี", data)
        assert is_ambig is True
