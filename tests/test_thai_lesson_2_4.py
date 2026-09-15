"""
Test Thai Week 2 Lesson 2.4 Implementation
"""
import unittest

from runtime.education.thai_lesson_2_4 import (
    create_lesson_2_4,
    load_cvc_syllables,
    generate_lesson_2_4_exercises,
    assess_lesson_2_4_mastery,
    update_knowledge_state_2_4,
    update_mastery_tracker_2_4,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson24Implementation(unittest.TestCase):
    
    def test_create_lesson_2_4(self):
        """Test lesson creation."""
        lesson = create_lesson_2_4()
        
        self.assertEqual(lesson.subject_id, "thai_language")
        self.assertEqual(lesson.level, 2)
        self.assertIn("พยัญชนะท้าย", lesson.title)
        self.assertGreater(len(lesson.objectives), 0)
    
    def test_load_cvc_syllables(self):
        """Test loading CVC syllables."""
        syllables = load_cvc_syllables()
        
        self.assertGreater(len(syllables), 0)
        
        # All should have finals
        for syll in syllables:
            self.assertIn('final', syll)
            self.assertIn('final_type', syll)
            self.assertIn(syll['final_type'], ['sonorant', 'stop'])
            self.assertEqual(syll['structure'], 'CVC')
    
    def test_sonorant_vs_stop_finals(self):
        """Test that sonorants and stops are correctly classified."""
        syllables = load_cvc_syllables()
        
        sonorant_finals = {'ม', 'น', 'ง', 'ย', 'ว'}
        stop_finals = {'ก', 'จ', 'ด', 'ต', 'บ', 'ป'}
        
        for syll in syllables:
            if syll['final'] in sonorant_finals:
                self.assertEqual(syll['final_type'], 'sonorant')
            elif syll['final'] in stop_finals:
                self.assertEqual(syll['final_type'], 'stop')
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_2_4_exercises()
        
        self.assertGreater(len(exercises), 0)
        
        # Check for different types
        ipa_count = sum(1 for ex in exercises if 'IPA' in ex.question)
        structure_count = sum(1 for ex in exercises if 'structure' in ex.question)
        final_type_count = sum(1 for ex in exercises if 'type' in ex.question)
        
        self.assertGreater(ipa_count, 0)
        self.assertGreater(structure_count, 0)
        self.assertGreater(final_type_count, 0)
    
    def test_exercise_verification(self):
        """Test exercise verification."""
        exercises = generate_lesson_2_4_exercises()
        
        ex = exercises[0]
        self.assertTrue(ex.verify(ex.expected_answer))
        self.assertFalse(ex.verify("wrong"))
    
    def test_assess_mastery_perfect(self):
        """Test perfect score assessment."""
        exercises = generate_lesson_2_4_exercises()[:15]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_2_4_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 1.0)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_2_4_exercises()[:10]
        
        responses = []
        for i, ex in enumerate(exercises):
            if i < 9:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        assessment = assess_lesson_2_4_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 0.9)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_error_classification(self):
        """Test error classification."""
        exercises = generate_lesson_2_4_exercises()
        
        # Find IPA exercise
        ipa_exercise = None
        for ex in exercises:
            if 'IPA' in ex.question:
                ipa_exercise = ex
                break
        
        self.assertIsNotNone(ipa_exercise)
        
        responses = [(ipa_exercise, "wrong")]
        assessment = assess_lesson_2_4_mastery(responses)
        
        self.assertGreater(len(assessment['error_patterns']['ipa_errors']), 0)
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState integration."""
        knowledge_state = KnowledgeState("thai_week2_lesson4")
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'knowledge_gaps': [],
            'total_exercises': 25,
            'correct': 23,
        }
        
        update_knowledge_state_2_4(assessment, knowledge_state)
        
        self.assertGreater(knowledge_state.correct_count, 0)
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker integration."""
        mastery_tracker = MasteryTracker()
        lesson_id = "thai_week2_lesson4"
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'total_exercises': 25,
        }
        
        update_mastery_tracker_2_4(assessment, mastery_tracker, lesson_id)
        
        self.assertIn(lesson_id, mastery_tracker.records)
        self.assertTrue(mastery_tracker.records[lesson_id].mastered)


class TestLesson24Integration(unittest.TestCase):
    """Integration test for complete learning flow."""
    
    def test_complete_learning_flow(self):
        """Test full flow."""
        # 1. Create lesson
        lesson = create_lesson_2_4()
        self.assertIsNotNone(lesson)
        
        # 2. Load CVC syllables
        syllables = load_cvc_syllables()
        self.assertGreater(len(syllables), 0)
        
        # 3. Generate exercises
        exercises = generate_lesson_2_4_exercises()
        self.assertGreater(len(exercises), 0)
        
        # 4. Simulate practice (85%)
        responses = []
        for i, ex in enumerate(exercises[:20]):
            if i < 17:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        # 5. Assess
        assessment = assess_lesson_2_4_mastery(responses)
        self.assertEqual(assessment['accuracy'], 0.85)
        
        # 6. Update systems
        knowledge_state = KnowledgeState(lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_2_4(assessment, knowledge_state)
        update_mastery_tracker_2_4(assessment, mastery_tracker, lesson.id)
        
        # 7. Verify
        self.assertGreater(knowledge_state.correct_count, 0)
        self.assertIn(lesson.id, mastery_tracker.records)
        # 85% not mastered
        self.assertFalse(mastery_tracker.records[lesson.id].mastered)


if __name__ == '__main__':
    unittest.main()
