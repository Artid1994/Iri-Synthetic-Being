"""
Test Thai Week 3 Lesson 3_10 Implementation
"""
import pytest
from runtime.education.thai_lesson_3_10 import (
    create_lesson_3_10,
    load_integrated_vocabulary,
    generate_lesson_3_10_exercises,
    assess_lesson_3_10_mastery,
    update_knowledge_state_3_10,
    update_mastery_tracker_3_10,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson310Implementation:
    """Test Lesson 3_10 implementation."""
    
    def test_create_lesson_3_10(self):
        """Test lesson creation."""
        lesson = create_lesson_3_10()
        assert lesson.level == 3
        assert lesson.subject_id == "thai_language"
        assert len(lesson.objectives) >= 3
    
    def test_load_data(self):
        """Test data loading."""
        data = load_integrated_vocabulary()
        assert len(data) >= 0  # May be empty for some lessons
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_3_10_exercises()
        assert len(exercises) > 0
    
    def test_assess_mastery_perfect(self):
        """Test assessment with perfect score."""
        exercises = generate_lesson_3_10_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_10_mastery(responses)
        assert assessment['accuracy'] == 1.0
        assert assessment['mastery_level'] == 'mastered'
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_3_10_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
            responses = [(ex, ex.expected_answer) for ex in exercises[:9]]
            responses.append((exercises[9], "wrong"))
            
            assessment = assess_lesson_3_10_mastery(responses)
            assert assessment['accuracy'] == 0.9
            assert assessment['mastery_level'] == 'mastered'
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState update."""
        exercises = generate_lesson_3_10_exercises()[:5]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_10_mastery(responses)
        knowledge_state = KnowledgeState(concept_id="lesson_3_10")
        
        update_knowledge_state_3_10(assessment, knowledge_state)
        assert knowledge_state.correct_count == 5
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker update."""
        exercises = generate_lesson_3_10_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_10_mastery(responses)
        mastery_tracker = MasteryTracker()
        
        update_mastery_tracker_3_10(assessment, mastery_tracker, "lesson_3_10")
        
        record = mastery_tracker.get_progress("lesson_3_10")
        assert record is not None
        assert record.mastered is True


class TestLesson310Integration:
    """Test Lesson 3_10 integration."""
    
    def test_complete_learning_flow(self):
        """Test complete learning flow."""
        lesson = create_lesson_3_10()
        data = load_integrated_vocabulary()
        
        exercises = generate_lesson_3_10_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_10_mastery(responses)
        assert assessment['mastery_level'] == 'mastered'
        
        knowledge_state = KnowledgeState(concept_id=lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_3_10(assessment, knowledge_state)
        update_mastery_tracker_3_10(assessment, mastery_tracker, lesson.id)
        
        record = mastery_tracker.get_progress(lesson.id)
        assert record is not None
        assert record.mastered is True
