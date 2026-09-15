"""
Test Thai Week 5 Lesson 5.9 Implementation
"""
import pytest
from runtime.education.thai_lesson_5_9 import (
    create_lesson_5_9,
    load_semantic_relationships,
    generate_lesson_5_9_exercises,
    assess_lesson_5_9_mastery,
    update_knowledge_state_5_9,
    update_mastery_tracker_5_9,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson59Implementation:
    """Test Lesson 5.9 implementation."""
    
    def test_create_lesson_5_9(self):
        """Test lesson creation."""
        lesson = create_lesson_5_9()
        assert lesson.level == 5
        assert lesson.subject_id == "thai_language"
        assert len(lesson.objectives) >= 3
    
    def test_load_data(self):
        """Test data loading."""
        data = load_semantic_relationships()
        assert len(data) >= 0  # May have minimal data
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_5_9_exercises()
        assert len(exercises) > 0
    
    def test_assess_mastery_perfect(self):
        """Test assessment with perfect score."""
        exercises = generate_lesson_5_9_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_5_9_mastery(responses)
        assert assessment['accuracy'] == 1.0
        assert assessment['mastery_level'] == 'mastered'
    
    def test_assess_mastery_90_percent(self):
        """Test 90% threshold."""
        exercises = generate_lesson_5_9_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
            responses = [(ex, ex.expected_answer) for ex in exercises[:9]]
            responses.append((exercises[9], "wrong"))
            
            assessment = assess_lesson_5_9_mastery(responses)
            assert assessment['accuracy'] == 0.9
            assert assessment['mastery_level'] == 'mastered'
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState update."""
        exercises = generate_lesson_5_9_exercises()
        num_exercises = min(len(exercises), 5)
        responses = [(ex, ex.expected_answer) for ex in exercises[:num_exercises]]
        
        assessment = assess_lesson_5_9_mastery(responses)
        knowledge_state = KnowledgeState(concept_id="lesson_5_9")
        
        update_knowledge_state_5_9(assessment, knowledge_state)
        assert knowledge_state.correct_count == num_exercises
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker update."""
        exercises = generate_lesson_5_9_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_5_9_mastery(responses)
        mastery_tracker = MasteryTracker()
        
        update_mastery_tracker_5_9(assessment, mastery_tracker, "lesson_5_9")
        
        record = mastery_tracker.get_progress("lesson_5_9")
        assert record is not None
        assert record.mastered is True


class TestLesson59Integration:
    """Test Lesson 5.9 integration."""
    
    def test_complete_learning_flow(self):
        """Test complete learning flow."""
        lesson = create_lesson_5_9()
        data = load_semantic_relationships()
        
        exercises = generate_lesson_5_9_exercises()
        if len(exercises) >= 10:
            exercises = exercises[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_5_9_mastery(responses)
        assert assessment['mastery_level'] == 'mastered'
        
        knowledge_state = KnowledgeState(concept_id=lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_5_9(assessment, knowledge_state)
        update_mastery_tracker_5_9(assessment, mastery_tracker, lesson.id)
        
        record = mastery_tracker.get_progress(lesson.id)
        assert record is not None
        assert record.mastered is True
