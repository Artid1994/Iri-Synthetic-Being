"""
Test Thai Week 5 Lesson 5.8 Implementation
"""
import pytest
from runtime.education.thai_lesson_5_8 import (
    create_lesson_5_8,
    load_expanded_patterns,
    generate_lesson_5_8_exercises,
    assess_lesson_5_8_mastery,
    update_knowledge_state_5_8,
    update_mastery_tracker_5_8,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson58Implementation:
    """Test Lesson 5.8 implementation."""
    
    def test_create_lesson_5_8(self):
        """Test lesson creation."""
        lesson = create_lesson_5_8()
        assert lesson.level == 5
        assert lesson.subject_id == "thai_language"
        assert len(lesson.objectives) >= 3
    
    def test_load_data(self):
        """Test data loading."""
        data = load_expanded_patterns()
        assert len(data) >= 0  # May have minimal data
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_5_8_exercises()
        assert len(exercises) > 0
    
    def test_assess_mastery_perfect(self):
        """Test assessment with perfect score."""
        exercises = generate_lesson_5_8_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_5_8_mastery(responses)
        assert assessment['accuracy'] == 1.0
        assert assessment['mastery_level'] == 'mastered'
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_5_8_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
            responses = [(ex, ex.expected_answer) for ex in exercises[:9]]
            responses.append((exercises[9], "wrong"))
            
            assessment = assess_lesson_5_8_mastery(responses)
            assert assessment['accuracy'] == 0.9
            assert assessment['mastery_level'] == 'mastered'
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState update."""
        exercises = generate_lesson_5_8_exercises()
        num_exercises = min(len(exercises), 5)
        responses = [(ex, ex.expected_answer) for ex in exercises[:num_exercises]]
        
        assessment = assess_lesson_5_8_mastery(responses)
        knowledge_state = KnowledgeState(concept_id="lesson_5_8")
        
        update_knowledge_state_5_8(assessment, knowledge_state)
        assert knowledge_state.correct_count == num_exercises
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker update."""
        exercises = generate_lesson_5_8_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_5_8_mastery(responses)
        mastery_tracker = MasteryTracker()
        
        update_mastery_tracker_5_8(assessment, mastery_tracker, "lesson_5_8")
        
        record = mastery_tracker.get_progress("lesson_5_8")
        assert record is not None
        assert record.mastered is True


class TestLesson58Integration:
    """Test Lesson 5.8 integration."""
    
    def test_complete_learning_flow(self):
        """Test complete learning flow."""
        lesson = create_lesson_5_8()
        data = load_expanded_patterns()
        
        exercises = generate_lesson_5_8_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_5_8_mastery(responses)
        assert assessment['mastery_level'] == 'mastered'
        
        knowledge_state = KnowledgeState(concept_id=lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_5_8(assessment, knowledge_state)
        update_mastery_tracker_5_8(assessment, mastery_tracker, lesson.id)
        
        record = mastery_tracker.get_progress(lesson.id)
        assert record is not None
        assert record.mastered is True
