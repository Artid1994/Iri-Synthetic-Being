import unittest

from runtime.education import (
    Subject,
    SubjectType,
    Lesson,
    LearningSession,
    MasteryTracker,
)
from runtime.learning_exercise import LearningExercise
from runtime.memory import Memory
from runtime.self_model import SelfModel
from runtime.identity import Identity


class TestLearningSessionIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.mastery_tracker = MasteryTracker()
        self.memory = Memory()
        self.self_model = SelfModel()
        self.identity = Identity()
        
        self.session = LearningSession(
            mastery_tracker=self.mastery_tracker,
            memory=self.memory,
            self_model=self.self_model,
            identity=self.identity,
        )
        
        self.lesson = Lesson(
            subject_id="thai",
            level=1,
            title="Thai Consonants",
            objectives=[
                "Recognize 44 Thai consonants",
                "Pronounce consonant sounds correctly",
            ],
        )
    
    def test_successful_learning_session(self):
        """Test a complete successful learning session."""
        exercises = [
            LearningExercise(
                question="What is ก?",
                expected_answer="ko kai",
                verification_type="EXACT",
            ),
            LearningExercise(
                question="What is ข?",
                expected_answer="kho khai",
                verification_type="EXACT",
            ),
        ]
        
        result = self.session.conduct_session(self.lesson, exercises)
        
        # Verify assessment
        self.assertTrue(result.assessment_result.passed)
        self.assertEqual(result.assessment_result.score, 1.0)
        self.assertTrue(result.mastered)
        self.assertEqual(result.exercises_attempted, 2)
        self.assertFalse(result.requires_remediation)
        
        # Verify mastery tracking
        self.assertTrue(self.mastery_tracker.is_mastered(self.lesson.id))
        progress = self.mastery_tracker.get_progress(self.lesson.id)
        self.assertEqual(progress.attempts, 1)
        
        # Verify memory consolidation
        self.assertGreater(len(self.memory.state.episodic), 0)
        self.assertGreater(len(self.memory.state.semantic), 0)
        
        # Verify self-model update
        self.assertGreater(self.self_model.state.self_knowledge, 0.0)
        self.assertGreater(len(self.self_model.state.self_history), 0)
        
        # Verify identity experience
        self.assertEqual(self.identity.state.experience, 1)
    
    def test_failed_session_no_remediation_yet(self):
        """Test a failed session that doesn't require remediation yet."""
        exercises = [
            LearningExercise(
                question="Q1",
                expected_answer="A1",
                verification_type="EXACT",
            ),
            LearningExercise(
                question="Q2",
                expected_answer="A2",
                verification_type="EXACT",
            ),
        ]
        
        # Provide wrong answers (0/2 correct = 0% score)
        wrong_answers = ["wrong1", "wrong2"]
        
        result = self.session.conduct_session(self.lesson, exercises, wrong_answers)
        
        self.assertFalse(result.mastered)
        self.assertFalse(result.requires_remediation)  # Only 1st attempt
    
    def test_failed_session_requires_remediation(self):
        """Test that remediation is required after 3 failed attempts."""
        exercises = [
            LearningExercise(
                question="Q1",
                expected_answer="A1",
                verification_type="EXACT",
            ),
            LearningExercise(
                question="Q2",
                expected_answer="A2",
                verification_type="EXACT",
            ),
        ]
        
        wrong_answers = ["wrong1", "wrong2"]
        
        # Conduct 3 failed sessions
        self.session.conduct_session(self.lesson, exercises, wrong_answers)
        self.session.conduct_session(self.lesson, exercises, wrong_answers)
        result = self.session.conduct_session(self.lesson, exercises, wrong_answers)
        
        self.assertTrue(result.requires_remediation)
    
    def test_session_updates_identity_experience(self):
        """Test that each session adds experience."""
        exercises = [
            LearningExercise(
                question="Q1",
                expected_answer="A1",
                verification_type="EXACT",
            ),
        ]
        
        initial_experience = self.identity.state.experience
        
        self.session.conduct_session(self.lesson, exercises)
        
        self.assertEqual(
            self.identity.state.experience,
            initial_experience + 1,
        )
    
    def test_session_requires_valid_lesson(self):
        """Test that session requires a valid Lesson instance."""
        exercises = [
            LearningExercise(
                question="Q1",
                expected_answer="A1",
                verification_type="EXACT",
            ),
        ]
        
        with self.assertRaises(TypeError):
            self.session.conduct_session("not a lesson", exercises)
    
    def test_session_requires_exercises(self):
        """Test that session requires at least one exercise."""
        with self.assertRaises(ValueError):
            self.session.conduct_session(self.lesson, [])
    
    def test_multiple_sessions_weighted_scoring(self):
        """Test that multiple sessions use weighted average scoring."""
        exercises = [
            LearningExercise(
                question="Q1",
                expected_answer="A1",
                verification_type="EXACT",
            ),
        ]
        
        # First session: 50% score
        self.mastery_tracker.record_attempt(self.lesson.id, 0.5)
        
        # Second session: 100% score
        # Expected: 0.7 * 1.0 + 0.3 * 0.5 = 0.85
        result = self.session.conduct_session(self.lesson, exercises)
        
        progress = self.mastery_tracker.get_progress(self.lesson.id)
        self.assertAlmostEqual(progress.mastery_score, 0.85, places=2)
        self.assertTrue(progress.mastered)  # 0.85 > 0.8 threshold


class TestEducationMemoryIntegration(unittest.TestCase):
    def test_mastered_lesson_creates_memory_entries(self):
        """Test that mastered lessons create both episodic and semantic memories."""
        mastery_tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        identity = Identity()
        
        session = LearningSession(
            mastery_tracker=mastery_tracker,
            memory=memory,
            self_model=self_model,
            identity=identity,
        )
        
        lesson = Lesson(
            subject_id="thai",
            level=1,
            title="Test Lesson",
            objectives=["Objective 1", "Objective 2"],
        )
        
        exercises = [
            LearningExercise(
                question="Q",
                expected_answer="A",
                verification_type="EXACT",
            ),
        ]
        
        initial_episodic = len(memory.state.episodic)
        initial_semantic = len(memory.state.semantic)
        
        result = session.conduct_session(lesson, exercises)
        
        # Should create episodic memory
        self.assertEqual(len(memory.state.episodic), initial_episodic + 1)
        
        # Should create semantic memories (one per objective)
        self.assertEqual(len(memory.state.semantic), initial_semantic + 2)


class TestEducationSelfModelIntegration(unittest.TestCase):
    def test_mastered_lesson_increases_self_knowledge(self):
        """Test that mastered lessons increase self-knowledge."""
        mastery_tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        identity = Identity()
        
        session = LearningSession(
            mastery_tracker=mastery_tracker,
            memory=memory,
            self_model=self_model,
            identity=identity,
        )
        
        lesson = Lesson(
            subject_id="thai",
            level=1,
            title="Test Lesson",
            objectives=["Learn something"],
        )
        
        exercises = [
            LearningExercise(
                question="Q",
                expected_answer="A",
                verification_type="EXACT",
            ),
        ]
        
        initial_knowledge = self_model.state.self_knowledge
        
        session.conduct_session(lesson, exercises)
        
        self.assertGreater(
            self_model.state.self_knowledge,
            initial_knowledge,
        )
    
    def test_failed_lesson_still_adds_history(self):
        """Test that even failed lessons add to self-history."""
        mastery_tracker = MasteryTracker()
        memory = Memory()
        self_model = SelfModel()
        identity = Identity()
        
        session = LearningSession(
            mastery_tracker=mastery_tracker,
            memory=memory,
            self_model=self_model,
            identity=identity,
        )
        
        lesson = Lesson(
            subject_id="thai",
            level=1,
            title="Test Lesson",
            objectives=["Learn something"],
        )
        
        exercises = [
            LearningExercise(
                question="Q",
                expected_answer="A",
                verification_type="EXACT",
            ),
        ]
        
        # Simulate failed attempt
        mastery_tracker.record_attempt(lesson.id, 0.3)
        
        initial_history_length = len(self_model.state.self_history)
        
        session.conduct_session(lesson, exercises)
        
        self.assertGreater(
            len(self_model.state.self_history),
            initial_history_length,
        )


if __name__ == "__main__":
    unittest.main()
