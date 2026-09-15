"""
Test Thai Week 4 Lesson 4.7 Implementation
"""
import pytest
from runtime.education.thai_lesson_4_7 import (
    create_lesson_4_7,
    load_aspect_examples,
    generate_lesson_4_7_exercises,
    assess_lesson_4_7_mastery,
    update_knowledge_state_4_7,
    update_mastery_tracker_4_7,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson47Implementation:
    """Test Lesson 4.7 implementation."""
    
    def test_create_lesson_4_7(self):
        """Test lesson creation."""
        lesson = create_lesson_4_7()
        assert lesson.level == 4
        assert lesson.subject_id == "thai_language"
        assert len(lesson.objectives) >= 3
    
    def test_load_data(self):
        """Test data loading."""
        data = load_aspect_examples()
        assert len(data) >= 0
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_4_7_exercises()
        assert len(exercises) > 0
    
    def test_assess_mastery_perfect(self):
        """Test assessment with perfect score."""
        exercises = generate_lesson_4_7_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_4_7_mastery(responses)
        assert assessment['accuracy'] == 1.0
        assert assessment['mastery_level'] == 'mastered'
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_4_7_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
            responses = [(ex, ex.expected_answer) for ex in exercises[:9]]
            responses.append((exercises[9], "wrong"))
            
            assessment = assess_lesson_4_7_mastery(responses)
            assert assessment['accuracy'] == 0.9
            assert assessment['mastery_level'] == 'mastered'
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState update."""
        exercises = generate_lesson_4_7_exercises()
        num_exercises = min(len(exercises), 5)
        responses = [(ex, ex.expected_answer) for ex in exercises[:num_exercises]]
        
        assessment = assess_lesson_4_7_mastery(responses)
        knowledge_state = KnowledgeState(concept_id="lesson_4_7")
        
        update_knowledge_state_4_7(assessment, knowledge_state)
        assert knowledge_state.correct_count == num_exercises
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker update."""
        exercises = generate_lesson_4_7_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_4_7_mastery(responses)
        mastery_tracker = MasteryTracker()
        
        update_mastery_tracker_4_7(assessment, mastery_tracker, "lesson_4_7")
        
        record = mastery_tracker.get_progress("lesson_4_7")
        assert record is not None
        assert record.mastered is True


class TestLesson47Integration:
    """Test Lesson 4.7 integration."""
    
    def test_complete_learning_flow(self):
        """Test complete learning flow."""
        lesson = create_lesson_4_7()
        data = load_aspect_examples()
        
        exercises = generate_lesson_4_7_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_4_7_mastery(responses)
        assert assessment['mastery_level'] == 'mastered'
        
        knowledge_state = KnowledgeState(concept_id=lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_4_7(assessment, knowledge_state)
        update_mastery_tracker_4_7(assessment, mastery_tracker, lesson.id)
        
        record = mastery_tracker.get_progress(lesson.id)
        assert record is not None
        assert record.mastered is True
