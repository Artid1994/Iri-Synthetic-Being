"""
Test Thai Week 2 Lesson 2.10 Implementation
"""
import unittest

from runtime.education.thai_lesson_2_10 import (
    create_lesson_2_10,
    load_integrated_examples,
    generate_lesson_2_10_exercises,
    assess_lesson_2_10_mastery,
    update_knowledge_state_2_10,
    update_mastery_tracker_2_10,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson210Implementation(unittest.TestCase):
    
    def test_create_lesson_2_10(self):
        """Test lesson creation."""
        lesson = create_lesson_2_10()
        
        self.assertEqual(lesson.subject_id, "thai_language")
        self.assertEqual(lesson.level, 2)
        self.assertIn("บูรณาการ", lesson.title)
        self.assertGreater(len(lesson.objectives), 0)
    
    def test_load_integrated_examples(self):
        """Test loading integrated examples."""
        examples = load_integrated_examples()
        
        self.assertGreater(len(examples), 0)
        
        # Check structure
        for ex in examples:
            self.assertIn('syllable', ex)
            self.assertIn('pattern', ex)
            self.assertIn('structure', ex)
            self.assertIn('consonant_class', ex)
            self.assertIn('live_dead', ex)
            self.assertIn('tone', ex)
            self.assertIn('reason', ex)
            self.assertIn('ipa', ex)
    
    def test_multiple_patterns_present(self):
        """Test that examples cover multiple patterns."""
        examples = load_integrated_examples()
        
        patterns = set(ex['pattern'] for ex in examples)
        
        # Should have diverse patterns
        self.assertGreaterEqual(len(patterns), 5)
    
    def test_multiple_structures_present(self):
        """Test that examples cover multiple structures."""
        examples = load_integrated_examples()
        
        structures = set(ex['structure'] for ex in examples)
        
        # Should have CV, CVC, CCV
        self.assertGreaterEqual(len(structures), 2)
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_2_10_exercises()
        
        self.assertGreater(len(exercises), 0)
        
        # Check types
        structure = sum(1 for ex in exercises if 'Structure' in ex.question)
        cons_class = sum(1 for ex in exercises if 'class' in ex.question)
        live_dead = sum(1 for ex in exercises if 'Live or dead' in ex.question)
        tone_num = sum(1 for ex in exercises if 'Tone number' in ex.question)
        ipa = sum(1 for ex in exercises if 'IPA' in ex.question)
        reasoning = sum(1 for ex in exercises if 'Why' in ex.question)
        
        self.assertGreater(structure, 0)
        self.assertGreater(cons_class, 0)
        self.assertGreater(live_dead, 0)
        self.assertGreater(tone_num, 0)
        self.assertGreater(ipa, 0, "Missing IPA exercises")
        self.assertGreater(reasoning, 0, "Missing WHY reasoning exercises")
    
    def test_reasoning_format(self):
        """Test reasoning format."""
        exercises = generate_lesson_2_10_exercises()
        
        reasoning_exercises = [ex for ex in exercises if 'Why' in ex.question]
        
        self.assertGreater(len(reasoning_exercises), 0)
        
        # Check format includes complete reasoning
        for ex in reasoning_exercises[:3]:
            self.assertIn('+', ex.expected_answer)
    
    def test_exercise_verification(self):
        """Test exercise verification."""
        exercises = generate_lesson_2_10_exercises()
        
        ex = exercises[0]
        self.assertTrue(ex.verify(ex.expected_answer))
        self.assertFalse(ex.verify("wrong"))
    
    def test_assess_mastery_perfect(self):
        """Test perfect score assessment."""
        exercises = generate_lesson_2_10_exercises()[:15]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_2_10_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 1.0)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_2_10_exercises()[:10]
        
        responses = []
        for i, ex in enumerate(exercises):
            if i < 9:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        assessment = assess_lesson_2_10_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 0.9)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_error_classification(self):
        """Test error classification."""
        exercises = generate_lesson_2_10_exercises()
        
        # Find IPA exercise
        ipa_exercise = None
        for ex in exercises:
            if 'IPA' in ex.question:
                ipa_exercise = ex
                break
        
        self.assertIsNotNone(ipa_exercise)
        
        responses = [(ipa_exercise, "wrong")]
        assessment = assess_lesson_2_10_mastery(responses)
        
        self.assertGreater(len(assessment['error_patterns']['ipa_errors']), 0)
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState integration."""
        knowledge_state = KnowledgeState("thai_week2_lesson10")
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'knowledge_gaps': [],
            'total_exercises': 25,
            'correct': 23,
        }
        
        update_knowledge_state_2_10(assessment, knowledge_state)
        
        self.assertGreater(knowledge_state.correct_count, 0)
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker integration."""
        mastery_tracker = MasteryTracker()
        lesson_id = "thai_week2_lesson10"
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'total_exercises': 25,
        }
        
        update_mastery_tracker_2_10(assessment, mastery_tracker, lesson_id)
        
        self.assertIn(lesson_id, mastery_tracker.records)
        self.assertTrue(mastery_tracker.records[lesson_id].mastered)


class TestLesson210Integration(unittest.TestCase):
    """Integration test for complete learning flow."""
    
    def test_complete_learning_flow(self):
        """Test full flow."""
        # 1. Create lesson
        lesson = create_lesson_2_10()
        self.assertIsNotNone(lesson)
        
        # 2. Load examples
        examples = load_integrated_examples()
        self.assertGreater(len(examples), 0)
        
        # 3. Generate exercises
        exercises = generate_lesson_2_10_exercises()
        self.assertGreater(len(exercises), 0)
        
        # 4. Simulate practice (85%)
        responses = []
        for i, ex in enumerate(exercises[:20]):
            if i < 17:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        # 5. Assess
        assessment = assess_lesson_2_10_mastery(responses)
        self.assertEqual(assessment['accuracy'], 0.85)
        
        # 6. Update systems
        knowledge_state = KnowledgeState(lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_2_10(assessment, knowledge_state)
        update_mastery_tracker_2_10(assessment, mastery_tracker, lesson.id)
        
        # 7. Verify
        self.assertGreater(knowledge_state.correct_count, 0)
        self.assertIn(lesson.id, mastery_tracker.records)
        # 85% not mastered
        self.assertFalse(mastery_tracker.records[lesson.id].mastered)


if __name__ == '__main__':
    unittest.main()
