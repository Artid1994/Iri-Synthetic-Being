import unittest
import tempfile
from pathlib import Path

from runtime.education import (
    KnowledgeState,
    KnowledgeLevel,
    ErrorType,
    EducationPersistence,
    MasteryTracker,
    MasteryRecord,
    LearningSession,
    Lesson,
)
from runtime.learning_exercise import LearningExercise
from runtime.memory import Memory
from runtime.self_model import SelfModel
from runtime.identity import Identity


class TestKnowledgeState(unittest.TestCase):
    def test_knowledge_state_progression(self):
        """Test knowledge level progression based on performance."""
        state = KnowledgeState(concept_id="test_concept")
        
        # Start as UNKNOWN
        self.assertEqual(state.level, KnowledgeLevel.UNKNOWN)
        
        # One correct -> LEARNING
        state.record_correct()
        self.assertEqual(state.level, KnowledgeLevel.LEARNING)
        
        # Two correct (100% accuracy) -> UNDERSTOOD
        state.record_correct()
        self.assertEqual(state.level, KnowledgeLevel.UNDERSTOOD)
        
        # Three correct (100% accuracy) -> CAN_USE
        state.record_correct()
        self.assertEqual(state.level, KnowledgeLevel.CAN_USE)
        
        # Five correct total (100% accuracy) -> MASTERED
        state.record_correct()
        state.record_correct()
        self.assertEqual(state.level, KnowledgeLevel.MASTERED)
    
    def test_knowledge_state_error_types(self):
        """Test different error types are tracked."""
        state = KnowledgeState(concept_id="test")
        
        state.record_error(ErrorType.UNKNOWN)
        self.assertEqual(state.last_error_type, ErrorType.UNKNOWN)
        
        state.record_error(ErrorType.PARTIAL)
        self.assertEqual(state.last_error_type, ErrorType.PARTIAL)
        self.assertEqual(state.incorrect_count, 2)
    
    def test_knowledge_state_needs_remediation(self):
        """Test remediation detection."""
        state = KnowledgeState(concept_id="test")
        
        self.assertFalse(state.needs_remediation())
        
        # Three incorrect with UNKNOWN level triggers remediation
        state.record_error(ErrorType.UNKNOWN)
        state.record_error(ErrorType.UNKNOWN)
        state.record_error(ErrorType.UNKNOWN)
        
        self.assertTrue(state.needs_remediation())


class TestEducationPersistence(unittest.TestCase):
    def test_save_and_load_mastery_records(self):
        """Test mastery records persistence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = EducationPersistence(storage_dir=Path(tmpdir))
            
            # Create records
            records = {
                "lesson1": MasteryRecord(
                    lesson_id="lesson1",
                    mastery_score=0.9,
                    attempts=2,
                    mastered=True,
                ),
                "lesson2": MasteryRecord(
                    lesson_id="lesson2",
                    mastery_score=0.5,
                    attempts=1,
                    mastered=False,
                ),
            }
            
            # Save
            persistence.save_mastery_records(records)
            
            # Load
            loaded = persistence.load_mastery_records()
            
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded["lesson1"].mastery_score, 0.9)
            self.assertTrue(loaded["lesson1"].mastered)
            self.assertEqual(loaded["lesson2"].mastery_score, 0.5)
            self.assertFalse(loaded["lesson2"].mastered)
    
    def test_save_and_load_knowledge_states(self):
        """Test knowledge states persistence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = EducationPersistence(storage_dir=Path(tmpdir))
            
            # Create states
            state1 = KnowledgeState(concept_id="concept1")
            state1.record_correct()
            state1.record_correct()
            
            state2 = KnowledgeState(concept_id="concept2")
            state2.record_error(ErrorType.PARTIAL)
            
            states = {
                "concept1": state1,
                "concept2": state2,
            }
            
            # Save
            persistence.save_knowledge_states(states)
            
            # Load
            loaded = persistence.load_knowledge_states()
            
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded["concept1"].correct_count, 2)
            self.assertEqual(loaded["concept1"].level, KnowledgeLevel.UNDERSTOOD)
            self.assertEqual(loaded["concept2"].incorrect_count, 1)
            self.assertEqual(loaded["concept2"].last_error_type, ErrorType.PARTIAL)
    
    def test_learning_history(self):
        """Test learning history persistence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = EducationPersistence(storage_dir=Path(tmpdir))
            
            # Append events
            persistence.append_learning_event({
                "lesson_id": "lesson1",
                "score": 0.9,
                "attempts": 1,
            })
            persistence.append_learning_event({
                "lesson_id": "lesson2",
                "score": 0.7,
                "attempts": 2,
            })
            
            # Load history
            history = persistence.load_learning_history()
            
            self.assertEqual(len(history), 2)
            self.assertEqual(history[0]["lesson_id"], "lesson1")
            self.assertEqual(history[1]["score"], 0.7)


class TestLearningSessionKnowledgeTracking(unittest.TestCase):
    def test_session_tracks_knowledge_states(self):
        """Test that sessions track knowledge states per concept."""
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
            objectives=["Learn concept"],
        )
        
        exercises = [
            LearningExercise(
                question="Q1",
                expected_answer="A1",
                verification_type="EXACT",
            ),
        ]
        
        # First attempt: correct
        result = session.conduct_session(lesson, exercises, ["A1"])
        
        # Verify knowledge state was created
        concept_id = f"{lesson.id}:Q1"
        knowledge_state = session.get_knowledge_state(concept_id)
        
        self.assertIsNotNone(knowledge_state)
        self.assertEqual(knowledge_state.correct_count, 1)
        self.assertEqual(knowledge_state.incorrect_count, 0)
    
    def test_session_detects_knowledge_gaps(self):
        """Test that sessions detect concepts needing remediation."""
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
            objectives=["Learn concept"],
        )
        
        exercises = [
            LearningExercise(
                question="Q1",
                expected_answer="A1",
                verification_type="EXACT",
            ),
        ]
        
        # Three failed attempts -> should trigger remediation
        session.conduct_session(lesson, exercises, ["wrong"])
        session.conduct_session(lesson, exercises, ["wrong"])
        result = session.conduct_session(lesson, exercises, ["wrong"])
        
        self.assertTrue(result.requires_remediation)
        self.assertGreater(len(result.knowledge_gaps), 0)
    
    def test_session_distinguishes_error_types(self):
        """Test that sessions distinguish between error types."""
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
            title="Test",
            objectives=["obj"],
        )
        
        # Test UNKNOWN (empty answer)
        ex1 = LearningExercise("Q1", "answer", "EXACT")
        session.conduct_session(lesson, [ex1], [""])
        
        concept_id = f"{lesson.id}:Q1"
        state = session.get_knowledge_state(concept_id)
        self.assertEqual(state.last_error_type, ErrorType.UNKNOWN)
        
        # Test PARTIAL (overlapping words)
        ex2 = LearningExercise("Q2", "the correct answer", "EXACT")
        session.conduct_session(lesson, [ex2], ["correct"])
        
        concept_id2 = f"{lesson.id}:Q2"
        state2 = session.get_knowledge_state(concept_id2)
        self.assertEqual(state2.last_error_type, ErrorType.PARTIAL)


class TestMasteryTrackerPersistence(unittest.TestCase):
    def test_mastery_tracker_auto_saves(self):
        """Test that mastery tracker auto-saves when persistence configured."""
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = EducationPersistence(storage_dir=Path(tmpdir))
            tracker = MasteryTracker()
            tracker.set_persistence(persistence)
            
            # Record attempt
            tracker.record_attempt("lesson1", 0.9)
            
            # Verify auto-saved
            loaded = persistence.load_mastery_records()
            self.assertIn("lesson1", loaded)
            self.assertEqual(loaded["lesson1"].mastery_score, 0.9)
    
    def test_mastery_tracker_loads_records(self):
        """Test that mastery tracker can load existing records."""
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = EducationPersistence(storage_dir=Path(tmpdir))
            
            # Save records
            records = {
                "lesson1": MasteryRecord(
                    lesson_id="lesson1",
                    mastery_score=0.85,
                    attempts=2,
                    mastered=True,
                ),
            }
            persistence.save_mastery_records(records)
            
            # Load into tracker
            tracker = MasteryTracker()
            tracker.load_records(persistence.load_mastery_records())
            
            self.assertTrue(tracker.is_mastered("lesson1"))
            progress = tracker.get_progress("lesson1")
            self.assertEqual(progress.attempts, 2)


if __name__ == "__main__":
    unittest.main()
