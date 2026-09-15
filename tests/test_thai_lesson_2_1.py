"""
Test Thai Week 2 Lesson 2.1 Implementation
"""
import unittest
from pathlib import Path

from runtime.education.thai_lesson_2_1 import (
    create_lesson_2_1,
    load_mid_class_consonants,
    generate_lesson_2_1_exercises,
    assess_lesson_2_1_mastery,
    update_knowledge_state_2_1,
    update_mastery_tracker_2_1,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson21Implementation(unittest.TestCase):
    
    def test_create_lesson_2_1(self):
        """Test lesson creation."""
        lesson = create_lesson_2_1()
        
        self.assertEqual(lesson.subject_id, "thai_language")
        self.assertEqual(lesson.level, 2)
        self.assertIn("พยัญชนะ", lesson.title)
        self.assertGreater(len(lesson.objectives), 0)
    
    def test_load_mid_class_consonants(self):
        """Test loading mid-class consonants from validated data."""
        consonants = load_mid_class_consonants()
        
        self.assertGreater(len(consonants), 0)
        
        # Check that all are mid class
        for cons in consonants:
            self.assertEqual(cons['class'], 'mid')
        
        # Check required fields
        for cons in consonants:
            self.assertIn('grapheme', cons)
            self.assertIn('ipa', cons)
            self.assertIn('place', cons)
            self.assertIn('manner', cons)
            self.assertIn('voicing', cons)
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_2_1_exercises()
        
        self.assertGreater(len(exercises), 0)
        
        # Check exercise structure
        for ex in exercises:
            self.assertTrue(hasattr(ex, 'question'))
            self.assertTrue(hasattr(ex, 'expected_answer'))
            self.assertTrue(hasattr(ex, 'verify'))
    
    def test_exercise_verification(self):
        """Test that exercises can verify answers."""
        exercises = generate_lesson_2_1_exercises()
        
        # Test correct answer
        ex = exercises[0]
        self.assertTrue(ex.verify(ex.expected_answer))
        
        # Test incorrect answer
        self.assertFalse(ex.verify("wrong_answer"))
    
    def test_assess_mastery_perfect(self):
        """Test assessment with perfect score."""
        exercises = generate_lesson_2_1_exercises()[:10]
        
        # Simulate perfect responses
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_2_1_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 1.0)
        self.assertEqual(assessment['mastery_level'], 'mastered')
        self.assertEqual(len(assessment['knowledge_gaps']), 0)
    
    def test_assess_mastery_with_errors(self):
        """Test assessment with some errors."""
        exercises = generate_lesson_2_1_exercises()[:10]
        
        # Simulate 70% accuracy
        responses = []
        for i, ex in enumerate(exercises):
            if i < 7:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        assessment = assess_lesson_2_1_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 0.7)
        self.assertIn(assessment['mastery_level'], ['developing', 'proficient'])
    
    def test_error_classification(self):
        """Test that errors are classified by type."""
        exercises = generate_lesson_2_1_exercises()
        
        # Find IPA exercise and answer incorrectly
        ipa_exercise = None
        for ex in exercises:
            if 'IPA' in ex.question:
                ipa_exercise = ex
                break
        
        self.assertIsNotNone(ipa_exercise)
        
        responses = [(ipa_exercise, "wrong_ipa")]
        assessment = assess_lesson_2_1_mastery(responses)
        
        self.assertGreater(len(assessment['error_patterns']['ipa_errors']), 0)
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState update after assessment."""
        knowledge_state = KnowledgeState("thai_week2_lesson1")
        
        # Simulate high accuracy assessment
        assessment = {
            'accuracy': 0.95,
            'mastery_level': 'mastered',
            'knowledge_gaps': [],
            'total_exercises': 20,
            'correct': 19,
        }
        
        update_knowledge_state_2_1(assessment, knowledge_state)
        
        # Check that state was updated
        self.assertGreater(knowledge_state.correct_count, 0)
        self.assertIn(knowledge_state.level.value, ['can_use', 'mastered'])
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker update after assessment."""
        mastery_tracker = MasteryTracker()
        lesson_id = "thai_week2_lesson1"
        
        # Simulate mastered assessment
        assessment = {
            'accuracy': 0.95,
            'mastery_level': 'mastered',
            'total_exercises': 20,
        }
        
        update_mastery_tracker_2_1(assessment, mastery_tracker, lesson_id)
        
        # Check that practice was recorded
        self.assertIn(lesson_id, mastery_tracker.records)


class TestLesson21Integration(unittest.TestCase):
    """Integration tests for complete learning flow."""
    
    def test_complete_learning_flow(self):
        """Test complete flow: lesson → practice → assess → update."""
        # 1. Create lesson
        lesson = create_lesson_2_1()
        self.assertIsNotNone(lesson)
        
        # 2. Generate exercises
        exercises = generate_lesson_2_1_exercises()
        self.assertGreater(len(exercises), 0)
        
        # 3. Simulate learner practice (80% accuracy)
        responses = []
        for i, ex in enumerate(exercises[:25]):
            if i < 20:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "incorrect"))
        
        # 4. Assess mastery
        assessment = assess_lesson_2_1_mastery(responses)
        self.assertEqual(assessment['accuracy'], 0.8)
        
        # 5. Update knowledge state
        knowledge_state = KnowledgeState(lesson.id)
        update_knowledge_state_2_1(assessment, knowledge_state)
        
        # 6. Update mastery tracker
        mastery_tracker = MasteryTracker()
        update_mastery_tracker_2_1(assessment, mastery_tracker, lesson.id)
        
        # Verify integration
        self.assertGreater(knowledge_state.correct_count, 0)
        self.assertIn(lesson.id, mastery_tracker.records)


if __name__ == '__main__':
    unittest.main()
