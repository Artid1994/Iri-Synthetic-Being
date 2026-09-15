"""
Test Thai Week 2 Lesson 2.5 Implementation
"""
import unittest

from runtime.education.thai_lesson_2_5 import (
    create_lesson_2_5,
    load_live_dead_syllables,
    generate_lesson_2_5_exercises,
    assess_lesson_2_5_mastery,
    update_knowledge_state_2_5,
    update_mastery_tracker_2_5,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson25Implementation(unittest.TestCase):
    
    def test_create_lesson_2_5(self):
        """Test lesson creation."""
        lesson = create_lesson_2_5()
        
        self.assertEqual(lesson.subject_id, "thai_language")
        self.assertEqual(lesson.level, 2)
        self.assertIn("เป็น", lesson.title)
        self.assertGreater(len(lesson.objectives), 0)
    
    def test_load_live_dead_syllables(self):
        """Test loading balanced live/dead examples."""
        syllables = load_live_dead_syllables()
        
        self.assertGreater(len(syllables), 0)
        
        # Check both classifications present
        live_count = sum(1 for s in syllables if s['classification'] == 'live')
        dead_count = sum(1 for s in syllables if s['classification'] == 'dead')
        
        self.assertGreater(live_count, 0)
        self.assertGreater(dead_count, 0)
        
        # Check parser agreement
        for syll in syllables:
            self.assertTrue(syll['parser_agrees'])
    
    def test_live_patterns_coverage(self):
        """Test that all live patterns are represented."""
        syllables = load_live_dead_syllables()
        live = [s for s in syllables if s['classification'] == 'live']
        
        reasons = [s['reason'] for s in live]
        
        # Should have long vowel examples
        self.assertTrue(any('long' in r for r in reasons))
        # Should have sonorant final examples
        self.assertTrue(any('sonorant' in r for r in reasons))
    
    def test_dead_patterns_coverage(self):
        """Test that all dead patterns are represented."""
        syllables = load_live_dead_syllables()
        dead = [s for s in syllables if s['classification'] == 'dead']
        
        reasons = [s['reason'] for s in dead]
        
        # Should have stop final examples
        self.assertTrue(any('stop' in r for r in reasons))
        # Should have no final examples
        self.assertTrue(any('no final' in r for r in reasons))
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_2_5_exercises()
        
        self.assertGreater(len(exercises), 0)
        
        # Check exercise types
        classification_count = sum(1 for ex in exercises if 'Classify' in ex.question)
        length_count = sum(1 for ex in exercises if 'length' in ex.question)
        reasoning_count = sum(1 for ex in exercises if 'Why' in ex.question)
        
        self.assertGreater(classification_count, 0)
        self.assertGreater(length_count, 0)
        self.assertGreater(reasoning_count, 0)
    
    def test_exercise_verification(self):
        """Test exercise verification."""
        exercises = generate_lesson_2_5_exercises()
        
        ex = exercises[0]
        self.assertTrue(ex.verify(ex.expected_answer))
        self.assertFalse(ex.verify("wrong"))
    
    def test_assess_mastery_perfect(self):
        """Test perfect score assessment."""
        exercises = generate_lesson_2_5_exercises()[:15]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_2_5_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 1.0)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_2_5_exercises()[:10]
        
        responses = []
        for i, ex in enumerate(exercises):
            if i < 9:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        assessment = assess_lesson_2_5_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 0.9)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_error_classification(self):
        """Test error classification."""
        exercises = generate_lesson_2_5_exercises()
        
        # Find classification exercise
        class_exercise = None
        for ex in exercises:
            if 'Classify' in ex.question:
                class_exercise = ex
                break
        
        self.assertIsNotNone(class_exercise)
        
        responses = [(class_exercise, "wrong")]
        assessment = assess_lesson_2_5_mastery(responses)
        
        self.assertGreater(len(assessment['error_patterns']['classification_errors']), 0)
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState integration."""
        knowledge_state = KnowledgeState("thai_week2_lesson5")
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'knowledge_gaps': [],
            'total_exercises': 25,
            'correct': 23,
        }
        
        update_knowledge_state_2_5(assessment, knowledge_state)
        
        self.assertGreater(knowledge_state.correct_count, 0)
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker integration."""
        mastery_tracker = MasteryTracker()
        lesson_id = "thai_week2_lesson5"
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'total_exercises': 25,
        }
        
        update_mastery_tracker_2_5(assessment, mastery_tracker, lesson_id)
        
        self.assertIn(lesson_id, mastery_tracker.records)
        self.assertTrue(mastery_tracker.records[lesson_id].mastered)


class TestLesson25Integration(unittest.TestCase):
    """Integration test for complete learning flow."""
    
    def test_complete_learning_flow(self):
        """Test full flow."""
        # 1. Create lesson
        lesson = create_lesson_2_5()
        self.assertIsNotNone(lesson)
        
        # 2. Load syllables
        syllables = load_live_dead_syllables()
        self.assertGreater(len(syllables), 0)
        
        # 3. Generate exercises
        exercises = generate_lesson_2_5_exercises()
        self.assertGreater(len(exercises), 0)
        
        # 4. Simulate practice (85%)
        responses = []
        for i, ex in enumerate(exercises[:20]):
            if i < 17:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        # 5. Assess
        assessment = assess_lesson_2_5_mastery(responses)
        self.assertEqual(assessment['accuracy'], 0.85)
        
        # 6. Update systems
        knowledge_state = KnowledgeState(lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_2_5(assessment, knowledge_state)
        update_mastery_tracker_2_5(assessment, mastery_tracker, lesson.id)
        
        # 7. Verify
        self.assertGreater(knowledge_state.correct_count, 0)
        self.assertIn(lesson.id, mastery_tracker.records)
        # 85% not mastered
        self.assertFalse(mastery_tracker.records[lesson.id].mastered)


if __name__ == '__main__':
    unittest.main()
