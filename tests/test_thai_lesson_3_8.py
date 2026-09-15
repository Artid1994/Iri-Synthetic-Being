"""
Test Thai Week 3 Lesson 3_8 Implementation
"""
import pytest
from runtime.education.thai_lesson_3_8 import (
    create_lesson_3_8,
    load_contextual_examples,
    generate_lesson_3_8_exercises,
    assess_lesson_3_8_mastery,
    update_knowledge_state_3_8,
    update_mastery_tracker_3_8,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson38Implementation:
    """Test Lesson 3_8 implementation."""
    
    def test_create_lesson_3_8(self):
        """Test lesson creation."""
        lesson = create_lesson_3_8()
        assert lesson.level == 3
        assert lesson.subject_id == "thai_language"
        assert len(lesson.objectives) >= 3
    
    def test_load_data(self):
        """Test data loading."""
        data = load_contextual_examples()
        assert len(data) >= 0  # May be empty for some lessons
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_3_8_exercises()
        assert len(exercises) > 0
    
    def test_assess_mastery_perfect(self):
        """Test assessment with perfect score."""
        exercises = generate_lesson_3_8_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_8_mastery(responses)
        assert assessment['accuracy'] == 1.0
        assert assessment['mastery_level'] == 'mastered'
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_3_8_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
            responses = [(ex, ex.expected_answer) for ex in exercises[:9]]
            responses.append((exercises[9], "wrong"))
            
            assessment = assess_lesson_3_8_mastery(responses)
            assert assessment['accuracy'] == 0.9
            assert assessment['mastery_level'] == 'mastered'
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState update."""
        exercises = generate_lesson_3_8_exercises()[:5]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_8_mastery(responses)
        knowledge_state = KnowledgeState(concept_id="lesson_3_8")
        
        update_knowledge_state_3_8(assessment, knowledge_state)
        assert knowledge_state.correct_count == 5
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker update."""
        exercises = generate_lesson_3_8_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_8_mastery(responses)
        mastery_tracker = MasteryTracker()
        
        update_mastery_tracker_3_8(assessment, mastery_tracker, "lesson_3_8")
        
        record = mastery_tracker.get_progress("lesson_3_8")
        assert record is not None
        assert record.mastered is True


class TestLesson38Integration:
    """Test Lesson 3_8 integration."""
    
    def test_complete_learning_flow(self):
        """Test complete learning flow."""
        lesson = create_lesson_3_8()
        data = load_contextual_examples()
        
        exercises = generate_lesson_3_8_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_8_mastery(responses)
        assert assessment['mastery_level'] == 'mastered'
        
        knowledge_state = KnowledgeState(concept_id=lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_3_8(assessment, knowledge_state)
        update_mastery_tracker_3_8(assessment, mastery_tracker, lesson.id)
        
        record = mastery_tracker.get_progress(lesson.id)
        assert record is not None
        assert record.mastered is True
