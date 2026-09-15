"""
Test Thai Week 2 Lesson 2.9 Implementation
"""
import unittest

from runtime.education.thai_lesson_2_9 import (
    create_lesson_2_9,
    load_cluster_examples,
    generate_lesson_2_9_exercises,
    assess_lesson_2_9_mastery,
    update_knowledge_state_2_9,
    update_mastery_tracker_2_9,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson29Implementation(unittest.TestCase):
    
    def test_create_lesson_2_9(self):
        """Test lesson creation."""
        lesson = create_lesson_2_9()
        
        self.assertEqual(lesson.subject_id, "thai_language")
        self.assertEqual(lesson.level, 2)
        self.assertIn("กลุ่ม", lesson.title)
        self.assertGreater(len(lesson.objectives), 0)
    
    def test_load_cluster_examples(self):
        """Test loading cluster examples."""
        examples = load_cluster_examples()
        
        self.assertGreater(len(examples), 0)
        
        # Check structure
        for ex in examples:
            self.assertIn('syllable', ex)
            self.assertIn('c1', ex)
            self.assertIn('c2', ex)
            self.assertIn('c1_class', ex)
            self.assertIn('cluster', ex)
            self.assertIn('tone', ex)
            self.assertIn('reason', ex)
    
    def test_cluster_types_present(self):
        """Test that multiple cluster types are represented."""
        examples = load_cluster_examples()
        
        c2_types = set(ex['c2'] for ex in examples)
        
        # Should have different C2 types (ร ล ว)
        self.assertGreaterEqual(len(c2_types), 2)
    
    def test_balanced_class_coverage(self):
        """Test that multiple C1 classes are represented."""
        examples = load_cluster_examples()
        
        classes = set(ex['c1_class'] for ex in examples)
        
        # Should have at least 2 classes
        self.assertGreaterEqual(len(classes), 2)
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_2_9_exercises()
        
        self.assertGreater(len(exercises), 0)
        
        # Check types
        c1_id = sum(1 for ex in exercises if 'First consonant' in ex.question)
        c2_id = sum(1 for ex in exercises if 'Second consonant' in ex.question)
        c1_class = sum(1 for ex in exercises if 'C1 class' in ex.question)
        tone_num = sum(1 for ex in exercises if 'Tone number' in ex.question)
        reasoning = sum(1 for ex in exercises if 'Why' in ex.question)
        
        self.assertGreater(c1_id, 0)
        self.assertGreater(c2_id, 0)
        self.assertGreater(c1_class, 0)
        self.assertGreater(tone_num, 0)
        self.assertGreater(reasoning, 0, "Missing WHY reasoning exercises")
    
    def test_reasoning_format(self):
        """Test reasoning format."""
        exercises = generate_lesson_2_9_exercises()
        
        reasoning_exercises = [ex for ex in exercises if 'Why' in ex.question]
        
        self.assertGreater(len(reasoning_exercises), 0)
        
        # Check format includes class+live/dead
        for ex in reasoning_exercises[:3]:
            self.assertIn('+', ex.expected_answer)
    
    def test_exercise_verification(self):
        """Test exercise verification."""
        exercises = generate_lesson_2_9_exercises()
        
        ex = exercises[0]
        self.assertTrue(ex.verify(ex.expected_answer))
        self.assertFalse(ex.verify("wrong"))
    
    def test_assess_mastery_perfect(self):
        """Test perfect score assessment."""
        exercises = generate_lesson_2_9_exercises()[:15]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_2_9_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 1.0)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_2_9_exercises()[:10]
        
        responses = []
        for i, ex in enumerate(exercises):
            if i < 9:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        assessment = assess_lesson_2_9_mastery(responses)
        
        self.assertEqual(assessment['accuracy'], 0.9)
        self.assertEqual(assessment['mastery_level'], 'mastered')
    
    def test_error_classification(self):
        """Test error classification."""
        exercises = generate_lesson_2_9_exercises()
        
        # Find C1 class exercise
        c1_exercise = None
        for ex in exercises:
            if 'C1 class' in ex.question:
                c1_exercise = ex
                break
        
        self.assertIsNotNone(c1_exercise)
        
        responses = [(c1_exercise, "wrong")]
        assessment = assess_lesson_2_9_mastery(responses)
        
        self.assertGreater(len(assessment['error_patterns']['c1_class_errors']), 0)
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState integration."""
        knowledge_state = KnowledgeState("thai_week2_lesson9")
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'knowledge_gaps': [],
            'total_exercises': 25,
            'correct': 23,
        }
        
        update_knowledge_state_2_9(assessment, knowledge_state)
        
        self.assertGreater(knowledge_state.correct_count, 0)
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker integration."""
        mastery_tracker = MasteryTracker()
        lesson_id = "thai_week2_lesson9"
        
        assessment = {
            'accuracy': 0.92,
            'mastery_level': 'mastered',
            'total_exercises': 25,
        }
        
        update_mastery_tracker_2_9(assessment, mastery_tracker, lesson_id)
        
        self.assertIn(lesson_id, mastery_tracker.records)
        self.assertTrue(mastery_tracker.records[lesson_id].mastered)


class TestLesson29Integration(unittest.TestCase):
    """Integration test for complete learning flow."""
    
    def test_complete_learning_flow(self):
        """Test full flow."""
        # 1. Create lesson
        lesson = create_lesson_2_9()
        self.assertIsNotNone(lesson)
        
        # 2. Load examples
        examples = load_cluster_examples()
        self.assertGreater(len(examples), 0)
        
        # 3. Generate exercises
        exercises = generate_lesson_2_9_exercises()
        self.assertGreater(len(exercises), 0)
        
        # 4. Simulate practice (85%)
        responses = []
        for i, ex in enumerate(exercises[:20]):
            if i < 17:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        # 5. Assess
        assessment = assess_lesson_2_9_mastery(responses)
        self.assertEqual(assessment['accuracy'], 0.85)
        
        # 6. Update systems
        knowledge_state = KnowledgeState(lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_2_9(assessment, knowledge_state)
        update_mastery_tracker_2_9(assessment, mastery_tracker, lesson.id)
        
        # 7. Verify
        self.assertGreater(knowledge_state.correct_count, 0)
        self.assertIn(lesson.id, mastery_tracker.records)
        # 85% not mastered
        self.assertFalse(mastery_tracker.records[lesson.id].mastered)


if __name__ == '__main__':
    unittest.main()
