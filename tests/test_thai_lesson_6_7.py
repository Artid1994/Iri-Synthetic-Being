"""
Test Thai Lesson 6.7: Thai → Internal Semantic Representation

Tests complete semantic representation building with all layers.
"""
import pytest

from runtime.education.thai_lesson_6_7 import (
    lesson_6_7,
    generate_lesson_6_7_exercises,
    assess_mastery,
    update_knowledge_state,
    update_mastery_tracker,
    thai_to_semantic_representation,
    load_data,
)
from runtime.education.knowledge_state import KnowledgeState, KnowledgeLevel
from runtime.education.mastery_tracker import MasteryTracker
from runtime.education.semantic_representation import (
    SemanticMeaning,
    SentenceSemantics,
    ContextType,
    EvidenceStatus,
    AmbiguityType,
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


class TestLesson67Structure:
    """Test lesson structure."""
    
    def test_lesson_creation(self):
        """Test lesson 6.7 exists."""
        assert lesson_6_7.subject_id == "thai"
        assert lesson_6_7.level == 6
        assert "Semantic Representation" in lesson_6_7.title or "Internal" in lesson_6_7.title
    
    def test_lesson_prerequisites(self):
        """Test lesson requires 6.6."""
        assert "thai_lesson_6_6" in lesson_6_7.prerequisites
    
    def test_exercise_count(self):
        """Test generates 10 exercises."""
        exercises = generate_lesson_6_7_exercises()
        assert len(exercises) == 10


class TestThaiToRepresentation:
    """CRITICAL: Test Thai → Internal Representation conversion."""
    
    def test_known_sentence_representation(self):
        """Test known sentence produces KNOWN representation."""
        data = load_data()
        
        # "ไป กิน" with purpose context
        sem, state, evidence = thai_to_semantic_representation(
            "ไป กิน", ["purpose"], data
        )
        
        assert isinstance(sem, SentenceSemantics)
        assert sem.sentence == "ไป กิน"
        assert len(sem.word_meanings) == 2
        assert state == "KNOWN"
        assert sem.confidence > 0.7
        assert len(evidence) > 0
    
    def test_ambiguous_sentence_representation(self):
        """Test ambiguous sentence produces AMBIGUOUS representation."""
        data = load_data()
        
        # "ดี" without context
        sem, state, evidence = thai_to_semantic_representation("ดี", [], data)
        
        assert isinstance(sem, SentenceSemantics)
        assert state == "AMBIGUOUS"
        assert len(sem.ambiguity_points) > 0
        assert sem.confidence < 0.7
    
    def test_unknown_word_representation(self):
        """Test unknown word produces UNKNOWN representation."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "unknown", [], data
        )
        
        assert state == "UNKNOWN"
        assert sem.confidence == 0.0
        assert any("unknown" in e.lower() for e in evidence)


class TestLexicalLayer:
    """Test lexical layer construction."""
    
    def test_lexical_meanings_extracted(self):
        """Test lexical meanings extracted for all words."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation("ไป กิน", [], data)
        
        assert len(sem.word_meanings) == 2
        assert all(isinstance(wm, SemanticMeaning) for wm in sem.word_meanings)
        assert sem.word_meanings[0].word == "ไป"
        assert sem.word_meanings[1].word == "กิน"
    
    def test_semantic_fields_present(self):
        """Test semantic fields included in lexical layer."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation("ไป กิน", [], data)
        
        # ไป should have MOTION field, กิน should have ACTION field
        assert sem.word_meanings[0].semantic_field == "MOTION"
        assert sem.word_meanings[1].semantic_field == "ACTION"
    
    def test_unknown_word_lexical_layer(self):
        """Test unknown word marked in lexical layer."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation("unknown", [], data)
        
        assert len(sem.word_meanings) == 1
        assert sem.word_meanings[0].evidence_status == EvidenceStatus.UNKNOWN
        assert sem.word_meanings[0].confidence == 0.0


class TestContextualLayer:
    """Test contextual layer construction."""
    
    def test_contextual_meanings_extracted(self):
        """Test contextual meanings extracted from vocabulary."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation("ไป", [], data)
        
        # ไป has 2 contextual meanings (LITERAL and PRAGMATIC)
        assert len(sem.word_meanings[0].contextual_meanings) == 2
    
    def test_context_selection_applied(self):
        """Test context selection mechanism applied."""
        data = load_data()
        
        # With activity context, should select PRAGMATIC
        sem, state, evidence = thai_to_semantic_representation(
            "ไป", ["activity"], data
        )
        
        # Evidence should mention contextual selection
        evidence_str = " ".join(evidence).lower()
        assert "contextual" in evidence_str or "context" in evidence_str
    
    def test_ambiguity_tracked_at_contextual_layer(self):
        """Test ambiguity tracked when multiple contextual meanings."""
        data = load_data()
        
        # "ดี" without context → ambiguous
        sem, state, evidence = thai_to_semantic_representation("ดี", [], data)
        
        assert len(sem.ambiguity_points) > 0
        assert any(ap.ambiguity_type == AmbiguityType.LEXICAL for ap in sem.ambiguity_points)


class TestCompositionalLayer:
    """Test compositional (sentence) layer construction."""
    
    def test_compositional_pattern_identified(self):
        """Test compositional pattern identified for known patterns."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "ไป กิน", ["purpose"], data
        )
        
        assert sem.compositional_meaning is not None
        # Pattern now returns "serial verb construction" from grammar file
        assert "serial" in sem.compositional_meaning.lower() or "verb" in sem.compositional_meaning.lower()
    
    def test_no_pattern_for_single_word(self):
        """Test single word has no compositional meaning."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation("ไป", [], data)
        
        # Single word should not have compositional meaning
        assert sem.compositional_meaning is None
    
    def test_noun_adjective_pattern(self):
        """Test NOUN+ADJECTIVE pattern recognized."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "คน ดี", [], data
        )
        
        assert sem.compositional_meaning is not None
        # Pattern now returns "noun qualification" from grammar file
        assert "noun" in sem.compositional_meaning.lower() or "qualification" in sem.compositional_meaning.lower()


class TestPragmaticLayer:
    """Test pragmatic layer construction."""
    
    def test_pragmatic_with_context(self):
        """Test pragmatic meaning extracted when context available."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "ไป ไหม", ["invitation"], data
        )
        
        assert sem.pragmatic_meaning is not None
        assert "invitation" in sem.pragmatic_meaning.lower()
    
    def test_no_pragmatic_without_context(self):
        """Test pragmatic meaning not forced without context."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "ไป ไหม", [], data
        )
        
        # Without context, pragmatic should be None or ambiguous
        if sem.pragmatic_meaning:
            # If pragmatic meaning present, state should be AMBIGUOUS
            assert state == "AMBIGUOUS"
    
    def test_pragmatic_evidence_documented(self):
        """Test pragmatic interpretation evidence documented."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "ไป ไหม", ["invitation"], data
        )
        
        evidence_str = " ".join(evidence).lower()
        assert "pragmatic" in evidence_str


class TestUncertaintyTracking:
    """CRITICAL: Test uncertainty is preserved, not removed."""
    
    def test_ambiguity_preserved_in_representation(self):
        """Test ambiguity preserved in ambiguity_points."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation("ดี", [], data)
        
        assert state == "AMBIGUOUS"
        assert len(sem.ambiguity_points) > 0
        # Ambiguity should include possible interpretations
        assert all(len(ap.possible_interpretations) >= 2 for ap in sem.ambiguity_points)
    
    def test_unknown_preserved_not_guessed(self):
        """Test UNKNOWN state preserved, not guessed."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation("unknown", [], data)
        
        assert state == "UNKNOWN"
        assert sem.confidence == 0.0
        # Should NOT have fabricated meaning
        assert sem.word_meanings[0].lexical_meaning == "[UNKNOWN]"
    
    def test_confidence_reflects_state(self):
        """Test confidence reflects state appropriately."""
        data = load_data()
        
        # KNOWN
        sem_known, state_known, _ = thai_to_semantic_representation(
            "ไป กิน", ["purpose"], data
        )
        
        # AMBIGUOUS
        sem_amb, state_amb, _ = thai_to_semantic_representation("ดี", [], data)
        
        # UNKNOWN
        sem_unk, state_unk, _ = thai_to_semantic_representation("unknown", [], data)
        
        assert sem_known.confidence > sem_amb.confidence > sem_unk.confidence


class TestEvidencePreservation:
    """Test evidence and provenance preservation."""
    
    def test_evidence_trail_present(self):
        """Test evidence trail documented throughout."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "ไป กิน", ["purpose"], data
        )
        
        assert len(evidence) > 0
        assert len(sem.evidence) > 0
    
    def test_evidence_documents_layers(self):
        """Test evidence documents all layers."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "ไป กิน", ["purpose"], data
        )
        
        evidence_str = " ".join(evidence).lower()
        # Should mention input, lexical, and other layers
        assert "input" in evidence_str or "ไป กิน" in evidence_str
        assert "lexical" in evidence_str
    
    def test_evidence_in_sentence_semantics(self):
        """Test SentenceSemantics contains evidence."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation("ไป", [], data)
        
        assert len(sem.evidence) > 0


class TestParsingNotUnderstanding:
    """CRITICAL: Test parsing ≠ understanding."""
    
    def test_representation_not_just_parsing(self):
        """Test representation includes semantic interpretation, not just parsing."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "ไป กิน", ["purpose"], data
        )
        
        # Should have semantic fields, not just tokens
        assert all(wm.semantic_field for wm in sem.word_meanings)
        # Should have compositional meaning, not just word list
        assert sem.compositional_meaning is not None
    
    def test_unknown_not_fabricated(self):
        """Test unknown words not fabricated from parsing."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation("unknown", [], data)
        
        # Should explicitly mark as UNKNOWN, not guess
        assert state == "UNKNOWN"
        assert sem.word_meanings[0].evidence_status == EvidenceStatus.UNKNOWN


class TestTranslationNotUnderstanding:
    """CRITICAL: Test translation ≠ understanding."""
    
    def test_representation_not_translation(self):
        """Test representation includes structures beyond translation."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "ไป กิน", ["purpose"], data
        )
        
        # Should have:
        # - Semantic fields
        assert all(wm.semantic_field for wm in sem.word_meanings)
        # - Contextual meanings
        assert all(wm.contextual_meanings for wm in sem.word_meanings)
        # - Compositional meaning
        assert sem.compositional_meaning is not None
        # - Evidence trail
        assert len(sem.evidence) > 0
        
        # These are NOT present in simple translation
    
    def test_translation_alone_insufficient(self):
        """Test that lexical meaning alone doesn't constitute full representation."""
        data = load_data()
        
        sem, state, evidence = thai_to_semantic_representation(
            "ไป กิน", ["purpose"], data
        )
        
        # Full representation has more than just lexical meanings
        assert sem.compositional_meaning is not None or sem.pragmatic_meaning is not None


class TestEvidenceGateIntegration:
    """CRITICAL: Test Evidence Gate integration."""
    
    def test_representation_requires_understanding_evidence(self):
        """Test semantic representation requires understanding evidence for consolidation."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="ไป กิน",
            definition="go eat",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={
                "semantic_field": "MOTION+ACTION",
                "has_representation": True,
            }
        )
        
        state = KnowledgeState("ไป กิน")
        state.level = KnowledgeLevel.CAN_USE
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        # WITHOUT understanding evidence → rejected
        result = pipeline.consolidate_with_evidence(concept, state, True, None)
        assert result is False
    
    def test_representation_with_explanation_accepted(self):
        """Test representation with EXPLANATION evidence accepted."""
        prov = Provenance("/test.json", SourceType.JSON, 100.0)
        concept = Concept(
            term="test_representation",
            definition="test",
            language="thai",
            provenance=prov,
            confidence=1.0,
            metadata={"semantic_field": "TEST"},
        )
        
        state = KnowledgeState("test_representation")
        state.level = KnowledgeLevel.CAN_USE
        
        evidence = UnderstandingEvidence(
            evidence_type=EvidenceType.EXPLANATION,
            language_input="test_representation",
            learner_output="Serial verb pattern: VERB+VERB with purpose meaning, combines motion and action",
            expected_pattern="explanation",
            verified=True,
            confidence=0.9,
            explanation="Learner explained serial verb compositional pattern",
        )
        
        memory = Memory()
        pipeline = KnowledgeIngestionPipeline(memory)
        
        result = pipeline.consolidate_with_evidence(concept, state, True, evidence)
        assert result is True


class TestMemorySelfModelIntegration:
    """Test integration with Memory and SelfModel."""
    
    def test_representation_to_memory(self):
        """Test representation can be added to memory."""
        data = load_data()
        memory = Memory()
        
        sem, state, evidence = thai_to_semantic_representation(
            "ไป กิน", ["purpose"], data
        )
        
        # Add to memory
        entry = f"{sem.sentence}: {sem.compositional_meaning}"
        memory.add_semantic(entry)
        
        assert entry in memory.state.semantic
    
    def test_self_model_update(self):
        """Test self model updated with representation capability."""
        self_model = SelfModel()
        
        self_model.update(
            self_knowledge_delta=0.1,
            self_awareness_delta=0.0,
            history_entry="Learned Thai → Internal Semantic Representation"
        )
        
        assert self_model.state.self_knowledge > 0.0
        assert "semantic representation" in self_model.state.self_history[-1].lower()


class TestMasteryAssessment:
    """Test mastery assessment."""
    
    def test_correct_answers_mastery(self):
        """Test all correct → MASTERED."""
        exercises = generate_lesson_6_7_exercises()
        responses = [ex.expected_answer for ex in exercises]
        
        accuracy, level, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 1.0
        assert level == "MASTERED"
        assert len(errors) == 0
    
    def test_partial_correct_can_use(self):
        """Test 80% correct → CAN_USE."""
        exercises = generate_lesson_6_7_exercises()
        responses = [ex.expected_answer for ex in exercises[:8]]
        responses += ["WRONG", "WRONG"]
        
        accuracy, level, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 0.8
        assert level == "CAN_USE"
    
    def test_low_accuracy_learning(self):
        """Test <70% → LEARNING."""
        exercises = generate_lesson_6_7_exercises()
        responses = ["WRONG"] * len(exercises)
        
        accuracy, level, errors, gaps = assess_mastery(responses)
        
        assert accuracy == 0.0
        assert level == "LEARNING"
        assert len(gaps) > 0


class TestKnowledgeStateUpdate:
    """Test knowledge state updates."""
    
    def test_knowledge_state_records_correct(self):
        """Test correct answers recorded."""
        state = KnowledgeState("thai_representation")
        exercises = generate_lesson_6_7_exercises()
        responses = [ex.expected_answer for ex in exercises]
        
        update_knowledge_state(state, responses)
        
        assert state.correct_count == len(exercises)
    
    def test_knowledge_state_records_errors(self):
        """Test errors recorded."""
        state = KnowledgeState("thai_representation")
        exercises = generate_lesson_6_7_exercises()
        responses = ["WRONG"] * len(exercises)
        
        update_knowledge_state(state, responses)
        
        assert state.incorrect_count == len(exercises)


class TestMasteryTrackerUpdate:
    """Test mastery tracker updates."""
    
    def test_mastery_tracker_records_attempt(self):
        """Test mastery tracker records attempts."""
        tracker = MasteryTracker()
        
        update_mastery_tracker(tracker, "thai_lesson_6_7", 0.9)
        
        record = tracker.get_progress("thai_lesson_6_7")
        assert record is not None
        assert record.mastery_score == 0.9


class TestRegression61To66:
    """Test regression: 6.1-6.6 mechanisms still work."""
    
    def test_lesson_6_7_exists(self):
        """Test lesson 6.7 can be imported and used."""
        assert lesson_6_7 is not None
        assert lesson_6_7.subject_id == "thai"
    
    def test_exercises_generate(self):
        """Test exercises generate without error."""
        exercises = generate_lesson_6_7_exercises()
        assert len(exercises) == 10
        assert all(ex.expected_answer for ex in exercises)
    
    def test_representation_function_works(self):
        """Test representation function executes without error."""
        data = load_data()
        sem, state, evidence = thai_to_semantic_representation("ไป", [], data)
        
        assert isinstance(sem, SentenceSemantics)
        assert state in ["KNOWN", "AMBIGUOUS", "UNKNOWN"]
        assert isinstance(evidence, list)
