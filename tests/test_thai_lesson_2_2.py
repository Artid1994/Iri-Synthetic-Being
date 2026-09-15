"""
Test Thai Week 2 Lesson 2.2 Implementation
"""
import unittest

from runtime.education.thai_lesson_2_2 import (
    create_lesson_2_2,
    load_core_vowels,
    generate_lesson_2_2_exercises,
    assess_lesson_2_2_mastery,
    update_knowledge_state_2_2,
    update_mastery_tracker_2_2,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson22Implementation(unittest.TestCase):
    
    def test_create_lesson_2_2(self):
        """Test lesson creation."""
        lesson = create_lesson_2_2()
        
        self.assertEqual(lesson.subject_id, "thai_language")
        self.assertEqual(lesson.level, 2)
        self.assertIn("สระ", lesson.title)
        self.assertGreater(len(lesson.objectives), 0)
    
    def test_load_core_vowels(self):
        """Test loading core vowels from validated data."""
        vowels = load_core_vowels()
        
        self.assertGreater(len(vowels), 0)
        
        # Check required fields
        for vowel in vowels:
            self.assertIn('orthography', vowel)
            self.assertIn('ipa', vowel)
            self.assertIn('length', vowel)
            self.assertIn(vowel['length'], ['short', 'long'])
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_2_2_exercises()
        
        self.assertGreater(len(exercises), 0)
        
        # Check exercise structure
        for ex in exercises:
            self.assertTrue(hasattr(ex, 'question'))
            self.assertTrue(hasattr(ex, 'expected_answer'))
            self.assertTrue(hasattr(ex, 'verify'))
    
    def test_exercise_verification(self):
        """Test that exercises can verify answers."""
        exercises = generate_lesson_2_2_exercises()
        
        # Test correct answer
        ex = exercises[0]
        self.assertTrue(ex.verify(ex.expected_answer))
        
        # Test incorrect answer
        self.assertFalse(ex.verify("wrong_answer"))
    
    def test_assess_mastery_perfect(self):
        """Test assessment with perfect score."""
        exercises = generate_lesson_2_2_exercises()[:10]
        
        # Simulate perfect responses
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_2_2_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 1.0)
        self.assertEqual(assessment['mastery_level'], 'mastered')
        self.assertEqual(len(assessment['knowledge_gaps']), 0)
    
    def test_assess_mastery_with_errors(self):
        """Test assessment with some errors."""
        exercises = generate_lesson_2_2_exercises()[:10]
        
        # Simulate 70% accuracy
        responses = []
        for i, ex in enumerate(exercises):
            if i < 7:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        assessment = assess_lesson_2_2_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 0.7)
        self.assertIn(assessment['mastery_level'], ['developing', 'proficient'])
    
    def test_error_classification(self):
        """Test that errors are classified by type."""
        exercises = generate_lesson_2_2_exercises()
        
        # Find IPA exercise and answer incorrectly
        ipa_exercise = None
        for ex in exercises:
            if 'IPA' in ex.question:
                ipa_exercise = ex
                break
        
        self.assertIsNotNone(ipa_exercise)
        
        responses = [(ipa_exercise, "wrong_ipa")]
        assessment = assess_lesson_2_2_mastery(responses)
        
        self.assertGreater(len(assessment['error_patterns']['ipa_errors']), 0)
    
    def test_mastery_threshold_90_percent(self):
        """Test that 90% is the mastery threshold (consistent with 2.1)."""
        exercises = generate_lesson_2_2_exercises()[:10]
        
        # Test 90% accuracy
        responses = []
        for i, ex in enumerate(exercises):
            if i < 9:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        assessment = assess_lesson_2_2_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 0.9)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState update after assessment."""
        knowledge_state = KnowledgeState("thai_week2_lesson2")
        
        assessment = {
            'accuracy': 0.95,
            'mastery_level': 'mastered',
            'knowledge_gaps': [],
            'total_exercises': 20,
            'correct': 19,
        }
        
        update_knowledge_state_2_2(assessment, knowledge_state)
        
        self.assertGreater(knowledge_state.correct_count, 0)
        self.assertIn(knowledge_state.level.value, ['can_use', 'mastered'])
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker update after assessment."""
        mastery_tracker = MasteryTracker()
        lesson_id = "thai_week2_lesson2"
        
        assessment = {
            'accuracy': 0.95,
            'mastery_level': 'mastered',
            'total_exercises': 20,
        }
        
        update_mastery_tracker_2_2(assessment, mastery_tracker, lesson_id)
        
        self.assertIn(lesson_id, mastery_tracker.records)
        self.assertTrue(mastery_tracker.records[lesson_id].mastered)


class TestLesson22Integration(unittest.TestCase):
    """Integration tests for complete learning flow."""
    
    def test_complete_learning_flow(self):
        """Test complete flow: lesson → practice → assess → update."""
        # 1. Create lesson
        lesson = create_lesson_2_2()
        self.assertIsNotNone(lesson)
        
        # 2. Generate exercises
        exercises = generate_lesson_2_2_exercises()
        self.assertGreater(len(exercises), 0)
        
        # 3. Simulate learner practice (80% accuracy)
        responses = []
        for i, ex in enumerate(exercises[:25]):
            if i < 20:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "incorrect"))
        
        # 4. Assess mastery
        assessment = assess_lesson_2_2_mastery(responses)
        self.assertEqual(assessment['accuracy'], 0.8)
        
        # 5. Update knowledge state
        knowledge_state = KnowledgeState(lesson.id)
        update_knowledge_state_2_2(assessment, knowledge_state)
        
        # 6. Update mastery tracker
        mastery_tracker = MasteryTracker()
        update_mastery_tracker_2_2(assessment, mastery_tracker, lesson.id)
        
        # Verify integration
        self.assertGreater(knowledge_state.correct_count, 0)
        self.assertIn(lesson.id, mastery_tracker.records)


if __name__ == '__main__':
    unittest.main()
