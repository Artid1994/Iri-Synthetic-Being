"""
Test Thai Week 2 Lesson 2.6 Implementation
"""
import unittest

from runtime.education.thai_lesson_2_6 import (
    create_lesson_2_6,
    load_tone_examples,
    generate_lesson_2_6_exercises,
    assess_lesson_2_6_mastery,
    update_knowledge_state_2_6,
    update_mastery_tracker_2_6,
    TONE_NAMES_TH,
    TONE_NAMES_EN,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson26Implementation(unittest.TestCase):
    
    def test_create_lesson_2_6(self):
        """Test lesson creation."""
        lesson = create_lesson_2_6()
        
        self.assertEqual(lesson.subject_id, "thai_language")
        self.assertEqual(lesson.level, 2)
        self.assertIn("วรรณยุกต์", lesson.title)
        self.assertGreater(len(lesson.objectives), 0)
    
    def test_tone_names_defined(self):
        """Test that all 5 tones have names."""
        self.assertEqual(len(TONE_NAMES_TH), 5)
        self.assertEqual(len(TONE_NAMES_EN), 5)
        
        for i in range(5):
            self.assertIn(i, TONE_NAMES_TH)
            self.assertIn(i, TONE_NAMES_EN)
    
    def test_load_tone_examples(self):
        """Test loading tone examples."""
        examples = load_tone_examples()
        
        self.assertGreater(len(examples), 0)
        
        # Check structure
        for ex in examples:
            self.assertIn('syllable', ex)
            self.assertIn('tone', ex)
            self.assertIn('tone_name_th', ex)
            self.assertIn('tone_name_en', ex)
            self.assertIn('consonant_class', ex)
            self.assertIn('live_dead', ex)
            self.assertIn('reason', ex)
    
    def test_multiple_tones_represented(self):
        """Test that examples cover multiple tones."""
        examples = load_tone_examples()
        
        unique_tones = set(ex['tone'] for ex in examples)
        
        # Should have at least 4 different tones (0, 1, 3, 4)
        self.assertGreaterEqual(len(unique_tones), 4)
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_2_6_exercises()
        
        self.assertGreater(len(exercises), 0)
        
        # Check types
        tone_num = sum(1 for ex in exercises if 'Tone number' in ex.question)
        tone_name = sum(1 for ex in exercises if 'Tone name' in ex.question)
        cons_class = sum(1 for ex in exercises if 'class' in ex.question)
        live_dead = sum(1 for ex in exercises if 'Live or dead' in ex.question)
        reasoning = sum(1 for ex in exercises if 'Why' in ex.question)
        
        self.assertGreater(tone_num, 0)
        self.assertGreater(tone_name, 0)
        self.assertGreater(cons_class, 0)
        self.assertGreater(live_dead, 0)
        self.assertGreater(reasoning, 0, "Missing WHY reasoning exercises")
    
    def test_balanced_class_coverage(self):
        """Test that all three consonant classes are represented."""
        examples = load_tone_examples()
        
        classes = set(ex['consonant_class'] for ex in examples)
        
        # Should have all three classes
        self.assertIn('mid', classes)
        self.assertIn('high', classes)
        self.assertIn('low', classes)
    
    def test_reasoning_exercises(self):
        """Test that WHY exercises are present."""
        exercises = generate_lesson_2_6_exercises()
        
        reasoning_exercises = [ex for ex in exercises if 'Why' in ex.question]
        
        self.assertGreater(len(reasoning_exercises), 0)
        
        # Check format
        for ex in reasoning_exercises[:3]:
            # Should have format like "mid+live", "high+dead"
            self.assertIn('+', ex.expected_answer)
    
    def test_exercise_verification(self):
        """Test exercise verification."""
        exercises = generate_lesson_2_6_exercises()
        
        ex = exercises[0]
        self.assertTrue(ex.verify(ex.expected_answer))
        self.assertFalse(ex.verify("wrong"))
    
    def test_assess_mastery_perfect(self):
        """Test perfect score assessment."""
        exercises = generate_lesson_2_6_exercises()[:15]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_2_6_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 1.0)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_2_6_exercises()[:10]
        
        responses = []
        for i, ex in enumerate(exercises):
            if i < 9:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        assessment = assess_lesson_2_6_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 0.9)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_error_classification(self):
        """Test error classification."""
        exercises = generate_lesson_2_6_exercises()
        
        # Find tone number exercise
        tone_exercise = None
        for ex in exercises:
            if 'Tone number' in ex.question:
                tone_exercise = ex
                break
        
        self.assertIsNotNone(tone_exercise)
        
        responses = [(tone_exercise, "wrong")]
        assessment = assess_lesson_2_6_mastery(responses)
        
        self.assertGreater(len(assessment['error_patterns']['tone_number_errors']), 0)
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState integration."""
        knowledge_state = KnowledgeState("thai_week2_lesson6")
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'knowledge_gaps': [],
            'total_exercises': 25,
            'correct': 23,
        }
        
        update_knowledge_state_2_6(assessment, knowledge_state)
        
        self.assertGreater(knowledge_state.correct_count, 0)
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker integration."""
        mastery_tracker = MasteryTracker()
        lesson_id = "thai_week2_lesson6"
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'total_exercises': 25,
        }
        
        update_mastery_tracker_2_6(assessment, mastery_tracker, lesson_id)
        
        self.assertIn(lesson_id, mastery_tracker.records)
        self.assertTrue(mastery_tracker.records[lesson_id].mastered)


class TestLesson26Integration(unittest.TestCase):
    """Integration test for complete learning flow."""
    
    def test_complete_learning_flow(self):
        """Test full flow."""
        # 1. Create lesson
        lesson = create_lesson_2_6()
        self.assertIsNotNone(lesson)
        
        # 2. Load examples
        examples = load_tone_examples()
        self.assertGreater(len(examples), 0)
        
        # 3. Generate exercises
        exercises = generate_lesson_2_6_exercises()
        self.assertGreater(len(exercises), 0)
        
        # 4. Simulate practice (85%)
        responses = []
        for i, ex in enumerate(exercises[:20]):
            if i < 17:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        # 5. Assess
        assessment = assess_lesson_2_6_mastery(responses)
        self.assertEqual(assessment['accuracy'], 0.85)
        
        # 6. Update systems
        knowledge_state = KnowledgeState(lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_2_6(assessment, knowledge_state)
        update_mastery_tracker_2_6(assessment, mastery_tracker, lesson.id)
        
        # 7. Verify
        self.assertGreater(knowledge_state.correct_count, 0)
        self.assertIn(lesson.id, mastery_tracker.records)
        # 85% not mastered
        self.assertFalse(mastery_tracker.records[lesson.id].mastered)


if __name__ == '__main__':
    unittest.main()
