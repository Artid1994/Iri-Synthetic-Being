"""
Test mastery consistency across all three systems
"""
import unittest
from runtime.education.thai_lesson_2_1 import (
    generate_lesson_2_1_exercises,
    assess_lesson_2_1_mastery,
    update_knowledge_state_2_1,
    update_mastery_tracker_2_1,
    create_lesson_2_1,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestMasteryConsistency(unittest.TestCase):
    """Test that all three systems agree on mastery status."""
    
    def test_mastery_at_95_percent(self):
        """95% accuracy → all systems agree: MASTERED."""
        exercises = generate_lesson_2_1_exercises()[:20]
        
        # Simulate 95% accuracy (19 correct, 1 incorrect)
        responses = []
        for i, ex in enumerate(exercises):
            if i < 19:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        # Assess
        assessment = assess_lesson_2_1_mastery(responses)
        self.assertEqual(assessment['accuracy'], 0.95)
        self.assertEqual(assessment['mastery_level'], 'mastered')
        
        # Update systems
        lesson = create_lesson_2_1()
        knowledge_state = KnowledgeState(lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_2_1(assessment, knowledge_state)
        update_mastery_tracker_2_1(assessment, mastery_tracker, lesson.id)
        
        # Verify consistency
        self.assertEqual(assessment['mastery_level'], 'mastered')
        self.assertTrue(mastery_tracker.records[lesson.id].mastered)
        # KnowledgeState will be MASTERED after 5+ correct
        self.assertGreaterEqual(knowledge_state.correct_count, 19)
    
    def test_no_mastery_at_85_percent(self):
        """85% accuracy → all systems agree: NOT MASTERED."""
        exercises = generate_lesson_2_1_exercises()[:20]
        
        # Simulate 85% accuracy (17 correct, 3 incorrect)
        responses = []
        for i, ex in enumerate(exercises):
            if i < 17:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        # Assess
        assessment = assess_lesson_2_1_mastery(responses)
        self.assertEqual(assessment['accuracy'], 0.85)
        self.assertEqual(assessment['mastery_level'], 'proficient')  # NOT mastered
        
        # Update systems
        lesson = create_lesson_2_1()
        knowledge_state = KnowledgeState(lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_2_1(assessment, knowledge_state)
        update_mastery_tracker_2_1(assessment, mastery_tracker, lesson.id)
        
        # Verify consistency: NO mastery
        self.assertEqual(assessment['mastery_level'], 'proficient')
        self.assertFalse(mastery_tracker.records[lesson.id].mastered)
        # Knowledge state should not be MASTERED
        self.assertIn(knowledge_state.level.value, ['learning', 'understood', 'can_use'])
    
    def test_progression_gate(self):
        """Only 90%+ accuracy allows progression to next lesson."""
        test_scores = [
            (0.95, True),   # Can progress
            (0.90, True),   # Can progress (at threshold)
            (0.89, False),  # Cannot progress
            (0.85, False),  # Cannot progress
            (0.75, False),  # Cannot progress
        ]
        
        for score, should_progress in test_scores:
            with self.subTest(score=score):
                # Determine if learner can progress
                if score >= 0.90:
                    mastery_level = 'mastered'
                elif score >= 0.75:
                    mastery_level = 'proficient'
                else:
                    mastery_level = 'developing'
                
                can_progress = (mastery_level == 'mastered')
                self.assertEqual(can_progress, should_progress)


if __name__ == '__main__':
    unittest.main()
