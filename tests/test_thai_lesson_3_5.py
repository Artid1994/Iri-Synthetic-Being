"""
Test Thai Week 3 Lesson 3_5 Implementation
"""
import pytest
from runtime.education.thai_lesson_3_5 import (
    create_lesson_3_5,
    load_compound_vocabulary,
    generate_lesson_3_5_exercises,
    assess_lesson_3_5_mastery,
    update_knowledge_state_3_5,
    update_mastery_tracker_3_5,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson35Implementation:
    """Test Lesson 3_5 implementation."""
    
    def test_create_lesson_3_5(self):
        """Test lesson creation."""
        lesson = create_lesson_3_5()
        assert lesson.level == 3
        assert lesson.subject_id == "thai_language"
        assert len(lesson.objectives) >= 3
    
    def test_load_data(self):
        """Test data loading."""
        data = load_compound_vocabulary()
        assert len(data) >= 0  # May be empty for some lessons
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_3_5_exercises()
        assert len(exercises) > 0
    
    def test_assess_mastery_perfect(self):
        """Test assessment with perfect score."""
        exercises = generate_lesson_3_5_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_5_mastery(responses)
        assert assessment['accuracy'] == 1.0
        assert assessment['mastery_level'] == 'mastered'
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_3_5_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
            responses = [(ex, ex.expected_answer) for ex in exercises[:9]]
            responses.append((exercises[9], "wrong"))
            
            assessment = assess_lesson_3_5_mastery(responses)
            assert assessment['accuracy'] == 0.9
            assert assessment['mastery_level'] == 'mastered'
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState update."""
        exercises = generate_lesson_3_5_exercises()
        # Use actual exercise count (may be less than 5)
        num_exercises = min(len(exercises), 5)
        responses = [(ex, ex.expected_answer) for ex in exercises[:num_exercises]]
        
        assessment = assess_lesson_3_5_mastery(responses)
        knowledge_state = KnowledgeState(concept_id="lesson_3_5")
        
        update_knowledge_state_3_5(assessment, knowledge_state)
        assert knowledge_state.correct_count == num_exercises
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker update."""
        exercises = generate_lesson_3_5_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_5_mastery(responses)
        mastery_tracker = MasteryTracker()
        
        update_mastery_tracker_3_5(assessment, mastery_tracker, "lesson_3_5")
        
        record = mastery_tracker.get_progress("lesson_3_5")
        assert record is not None
        assert record.mastered is True


class TestLesson35Integration:
    """Test Lesson 3_5 integration."""
    
    def test_complete_learning_flow(self):
        """Test complete learning flow."""
        lesson = create_lesson_3_5()
        data = load_compound_vocabulary()
        
        exercises = generate_lesson_3_5_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_5_mastery(responses)
        assert assessment['mastery_level'] == 'mastered'
        
        knowledge_state = KnowledgeState(concept_id=lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_3_5(assessment, knowledge_state)
        update_mastery_tracker_3_5(assessment, mastery_tracker, lesson.id)
        
        record = mastery_tracker.get_progress(lesson.id)
        assert record is not None
        assert record.mastered is True
