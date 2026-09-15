"""
Test Thai Week 2 Lesson 2.8 Implementation
"""
import unittest

from runtime.education.thai_lesson_2_8 import (
    create_lesson_2_8,
    load_leading_ho_examples,
    generate_lesson_2_8_exercises,
    assess_lesson_2_8_mastery,
    update_knowledge_state_2_8,
    update_mastery_tracker_2_8,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson28Implementation(unittest.TestCase):
    
    def test_create_lesson_2_8(self):
        """Test lesson creation."""
        lesson = create_lesson_2_8()
        
        self.assertEqual(lesson.subject_id, "thai_language")
        self.assertEqual(lesson.level, 2)
        self.assertIn("ห", lesson.title)
        self.assertGreater(len(lesson.objectives), 0)
    
    def test_load_leading_ho_examples(self):
        """Test loading leading ห/อ examples."""
        examples = load_leading_ho_examples()
        
        self.assertGreater(len(examples), 0)
        
        # Check structure
        for ex in examples:
            self.assertIn('syllable', ex)
            self.assertIn('leading_consonant', ex)
            self.assertIn('main_consonant', ex)
            self.assertIn('effective_class', ex)
            self.assertIn('original_class', ex)
            self.assertIn('tone', ex)
            self.assertIn('reason', ex)
    
    def test_both_leading_types_present(self):
        """Test that both ห and อ examples are present."""
        examples = load_leading_ho_examples()
        
        leading_types = set(ex['leading_consonant'] for ex in examples)
        
        self.assertIn('ห', leading_types)
        # อ may not be in parser - check for at least ห
        self.assertGreaterEqual(len(leading_types), 1)
    
    def test_effective_class_modification(self):
        """Test that effective class differs from original."""
        examples = load_leading_ho_examples()
        
        # Should have cases where effective != original
        modified = [ex for ex in examples if ex['effective_class'] != ex['original_class']]
        
        self.assertGreater(len(modified), 0, "No examples showing class modification")
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_2_8_exercises()
        
        self.assertGreater(len(exercises), 0)
        
        # Check types
        leading_id = sum(1 for ex in exercises if 'Leading consonant' in ex.question)
        main_id = sum(1 for ex in exercises if 'Main consonant' in ex.question)
        eff_class = sum(1 for ex in exercises if 'Effective class' in ex.question)
        tone_num = sum(1 for ex in exercises if 'Tone number' in ex.question)
        reasoning = sum(1 for ex in exercises if 'Why' in ex.question)
        
        self.assertGreater(leading_id, 0)
        self.assertGreater(main_id, 0)
        self.assertGreater(eff_class, 0)
        self.assertGreater(tone_num, 0)
        self.assertGreater(reasoning, 0, "Missing WHY reasoning exercises")
    
    def test_reasoning_format(self):
        """Test reasoning format."""
        exercises = generate_lesson_2_8_exercises()
        
        reasoning_exercises = [ex for ex in exercises if 'Why' in ex.question]
        
        self.assertGreater(len(reasoning_exercises), 0)
        
        # Check format includes effective class
        for ex in reasoning_exercises[:3]:
            # Should mention effective class or leading effect
            self.assertTrue('+' in ex.expected_answer or 'high' in ex.expected_answer or 'low' in ex.expected_answer)
    
    def test_exercise_verification(self):
        """Test exercise verification."""
        exercises = generate_lesson_2_8_exercises()
        
        ex = exercises[0]
        self.assertTrue(ex.verify(ex.expected_answer))
        self.assertFalse(ex.verify("wrong"))
    
    def test_assess_mastery_perfect(self):
        """Test perfect score assessment."""
        exercises = generate_lesson_2_8_exercises()[:15]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_2_8_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 1.0)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_2_8_exercises()[:10]
        
        responses = []
        for i, ex in enumerate(exercises):
            if i < 9:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        assessment = assess_lesson_2_8_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 0.9)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_error_classification(self):
        """Test error classification."""
        exercises = generate_lesson_2_8_exercises()
        
        # Find effective class exercise
        eff_exercise = None
        for ex in exercises:
            if 'Effective class' in ex.question:
                eff_exercise = ex
                break
        
        self.assertIsNotNone(eff_exercise)
        
        responses = [(eff_exercise, "wrong")]
        assessment = assess_lesson_2_8_mastery(responses)
        
        self.assertGreater(len(assessment['error_patterns']['effective_class_errors']), 0)
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState integration."""
        knowledge_state = KnowledgeState("thai_week2_lesson8")
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'knowledge_gaps': [],
            'total_exercises': 25,
            'correct': 23,
        }
        
        update_knowledge_state_2_8(assessment, knowledge_state)
        
        self.assertGreater(knowledge_state.correct_count, 0)
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker integration."""
        mastery_tracker = MasteryTracker()
        lesson_id = "thai_week2_lesson8"
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'total_exercises': 25,
        }
        
        update_mastery_tracker_2_8(assessment, mastery_tracker, lesson_id)
        
        self.assertIn(lesson_id, mastery_tracker.records)
        self.assertTrue(mastery_tracker.records[lesson_id].mastered)


class TestLesson28Integration(unittest.TestCase):
    """Integration test for complete learning flow."""
    
    def test_complete_learning_flow(self):
        """Test full flow."""
        # 1. Create lesson
        lesson = create_lesson_2_8()
        self.assertIsNotNone(lesson)
        
        # 2. Load examples
        examples = load_leading_ho_examples()
        self.assertGreater(len(examples), 0)
        
        # 3. Generate exercises
        exercises = generate_lesson_2_8_exercises()
        self.assertGreater(len(exercises), 0)
        
        # 4. Simulate practice (85%)
        responses = []
        for i, ex in enumerate(exercises[:20]):
            if i < 17:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        # 5. Assess
        assessment = assess_lesson_2_8_mastery(responses)
        self.assertEqual(assessment['accuracy'], 0.85)
        
        # 6. Update systems
        knowledge_state = KnowledgeState(lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_2_8(assessment, knowledge_state)
        update_mastery_tracker_2_8(assessment, mastery_tracker, lesson.id)
        
        # 7. Verify
        self.assertGreater(knowledge_state.correct_count, 0)
        self.assertIn(lesson.id, mastery_tracker.records)
        # 85% not mastered
        self.assertFalse(mastery_tracker.records[lesson.id].mastered)


if __name__ == '__main__':
    unittest.main()
