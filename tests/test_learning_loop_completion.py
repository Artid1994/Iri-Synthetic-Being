"""
Test Remaining Integration Capabilities
Tests for problem-solving, capability tracking, and verification.
"""
import pytest
from runtime.education.self_directed_controller import SelfDirectedLearningController
from runtime.education.knowledge_state import KnowledgeState, ErrorType
from runtime.education.mastery_tracker import MasteryTracker
from runtime.memory import Memory
from runtime.self_model import SelfModel
from runtime.learning_exercise import LearningExercise


class TestProblemSolvingPath:
    """Test problem → answer → verification → learning path."""
    
    def test_exercise_verification_deterministic(self):
        """Test that exercises use deterministic verification (no LLM needed)."""
        exercise = LearningExercise(
            question="What is 2+2?",
            expected_answer="4",
            verification_type="EXACT"
        )
        
        # Correct answer
        assert exercise.verify("4") is True
        
        # Incorrect answer
        assert exercise.verify("5") is False
    
    def test_problem_to_knowledge_update_path(self):
        """Test: Problem → Verify → Update KnowledgeState."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        controller = SelfDirectedLearningController(tracker, memory, self_model)
        
        # Register knowledge state
        state = KnowledgeState(concept_id="test_concept")
        controller.register_knowledge_state("test_concept", state)
        
        # Simulate exercise attempts
        exercises = [
            LearningExercise("Q1", "A1", "EXACT"),
            LearningExercise("Q2", "A2", "EXACT"),
            LearningExercise("Q3", "A3", "EXACT"),
        ]
        
        # Attempt 1: Wrong answer → record error
        if not exercises[0].verify("wrong"):
            state.record_error(ErrorType.INCORRECT)
        
        # Attempt 2: Correct answer → record correct
        if exercises[1].verify("A2"):
            state.record_correct()
        
        # Attempt 3: Correct answer → record correct
        if exercises[2].verify("A3"):
            state.record_correct()
        
        # Verify state updated
        assert state.correct_count == 2
        assert state.incorrect_count == 1


class TestCapabilityTracking:
    """Test SelfModel capability tracking from learning."""
    
    def test_selfmodel_update_on_mastery(self):
        """Test SelfModel updates when mastery achieved."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        controller = SelfDirectedLearningController(tracker, memory, self_model)
        
        # Record initial state
        initial_knowledge = self_model.state.self_knowledge
        initial_history_len = len(self_model.state.self_history)
        
        # Update from mastery
        controller.update_from_mastery(
            lesson_id="lesson_test",
            mastered=True,
            score=0.95
        )
        
        # Verify SelfModel updated
        assert self_model.state.self_knowledge > initial_knowledge
        assert len(self_model.state.self_history) > initial_history_len
        assert any("lesson_test" in entry for entry in self_model.state.self_history)
    
    def test_selfmodel_tracks_learning_progress(self):
        """Test SelfModel tracks in-progress learning."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        controller = SelfDirectedLearningController(tracker, memory, self_model)
        
        initial_awareness = self_model.state.self_awareness
        
        # Update from in-progress learning
        controller.update_from_mastery(
            lesson_id="lesson_partial",
            mastered=False,
            score=0.75
        )
        
        # Verify awareness increased (self-awareness of learning process)
        assert self_model.state.self_awareness > initial_awareness
        assert any("Practicing" in entry for entry in self_model.state.self_history)
    
    def test_multiple_masteries_accumulate(self):
        """Test that multiple masteries accumulate in SelfModel."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        controller = SelfDirectedLearningController(tracker, memory, self_model)
        
        # Master multiple lessons
        for i in range(5):
            controller.update_from_mastery(
                lesson_id=f"lesson_{i}",
                mastered=True,
                score=0.92
            )
        
        # Verify cumulative increase
        assert self_model.state.self_knowledge >= 0.05  # 5 * 0.01
        assert len(self_model.state.self_history) == 5


class TestVerificationBeforeKnowledge:
    """Test that verification happens before knowledge update."""
    
    def test_verification_rejects_low_confidence(self):
        """Test verification blocks low-confidence results."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        controller = SelfDirectedLearningController(tracker, memory, self_model)
        
        # Attempt to verify low-confidence learning
        accepted, reason = controller.verify_learning_result(
            concept="test_concept",
            evidence="weak evidence",
            confidence=0.3
        )
        
        assert accepted is False
        assert "confidence" in reason.lower()
    
    def test_verification_accepts_high_confidence(self):
        """Test verification accepts high-confidence results."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        controller = SelfDirectedLearningController(tracker, memory, self_model)
        
        accepted, reason = controller.verify_learning_result(
            concept="test_concept",
            evidence="strong evidence",
            confidence=0.95
        )
        
        assert accepted is True
    
    def test_verification_threshold_boundary(self):
        """Test verification at 0.7 threshold."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        controller = SelfDirectedLearningController(tracker, memory, self_model)
        
        # Exactly at threshold
        accepted, _ = controller.verify_learning_result("test", "evidence", 0.7)
        assert accepted is True
        
        # Just below threshold
        accepted, _ = controller.verify_learning_result("test", "evidence", 0.69)
        assert accepted is False


class TestErrorPatternHandling:
    """Test error pattern detection and response."""
    
    def test_error_patterns_detected(self):
        """Test that error patterns are identified in assessment."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        controller = SelfDirectedLearningController(tracker, memory, self_model)
        
        # Create state with errors
        state = KnowledgeState(concept_id="weak_area")
        state.record_error(ErrorType.PARTIAL)
        state.record_error(ErrorType.PARTIAL)
        state.record_error(ErrorType.PARTIAL)
        
        controller.register_knowledge_state("weak_area", state)
        
        # Detect gaps
        gaps = controller.detect_gaps()
        
        assert len(gaps) > 0
        assert gaps[0].concept_id == "weak_area"
        assert gaps[0].gap_type == "remediation"
    
    def test_remediation_prioritized(self):
        """Test that error patterns trigger remediation priority."""
        tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        controller = SelfDirectedLearningController(tracker, memory, self_model)
        
        # Create weak state
        weak_state = KnowledgeState(concept_id="weak_lesson")
        weak_state.record_error(ErrorType.INCORRECT)
        weak_state.record_error(ErrorType.INCORRECT)
        weak_state.record_error(ErrorType.INCORRECT)
        controller.register_knowledge_state("weak_lesson", weak_state)
        
        # Detect gaps
        gaps = controller.detect_gaps()
        
        # Should be high priority
        assert gaps[0].priority == 3
