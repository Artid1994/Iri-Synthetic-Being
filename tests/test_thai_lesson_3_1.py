"""
Test Thai Week 3 Lesson 3.1 Implementation
"""
import pytest
from runtime.education.thai_lesson_3_1 import (
    create_lesson_3_1,
    load_single_syllable_vocabulary,
    generate_lesson_3_1_exercises,
    assess_lesson_3_1_mastery,
    update_knowledge_state_3_1,
    update_mastery_tracker_3_1,
)
from runtime.education.knowledge_state import KnowledgeState
from runtime.education.mastery_tracker import MasteryTracker


class TestLesson31Implementation:
    """Test Lesson 3.1 implementation."""
    
    def test_create_lesson_3_1(self):
        """Test lesson creation."""
        lesson = create_lesson_3_1()
        assert lesson.level == 3
        assert lesson.subject_id == "thai_language"
        assert len(lesson.objectives) >= 3
        assert "Single-Syllable" in lesson.title or "พยางค์เดียว" in lesson.title
    
    def test_load_single_syllable_vocabulary(self):
        """Test vocabulary loading."""
        words = load_single_syllable_vocabulary()
        assert len(words) > 0
        
        # Check structure
        for word in words:
            assert 'word' in word
            assert 'ipa' in word
            assert 'meaning' in word
            assert 'category' in word
            assert 'tone' in word
    
    def test_generate_exercises(self):
        """Test exercise generation."""
        exercises = generate_lesson_3_1_exercises()
        assert len(exercises) > 0
        
        # Check exercise types
        questions = [ex.question for ex in exercises]
        assert any('Meaning' in q for q in questions)
        assert any('IPA' in q for q in questions)
    
    def test_exercise_verification(self):
        """Test exercise answer verification."""
        exercises = generate_lesson_3_1_exercises()
        
        # Test correct answer
        ex = exercises[0]
        assert ex.verify(ex.expected_answer)
        
        # Test incorrect answer
        assert not ex.verify("wrong_answer")
    
    def test_assess_mastery_perfect(self):
        """Test assessment with perfect score."""
        exercises = generate_lesson_3_1_exercises()[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_1_mastery(responses)
        assert assessment['accuracy'] == 1.0
        assert assessment['mastery_level'] == 'mastered'
        assert assessment['correct'] == 10
    
    def test_assess_mastery_90_percent(self):
        """Test assessment with 90% score."""
        exercises = generate_lesson_3_1_exercises()[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises[:9]]
        responses.append((exercises[9], "wrong"))
        
        assessment = assess_lesson_3_1_mastery(responses)
        assert assessment['accuracy'] == 0.9
        assert assessment['mastery_level'] == 'mastered'
    
    def test_error_classification(self):
        """Test error pattern classification."""
        exercises = generate_lesson_3_1_exercises()[:10]
        
        # Introduce errors
        responses = []
        for i, ex in enumerate(exercises):
            if i < 7:
                responses.append((ex, ex.expected_answer))
            else:
                responses.append((ex, "wrong"))
        
        assessment = assess_lesson_3_1_mastery(responses)
        assert len(assessment['error_patterns']) > 0
    
    def test_knowledge_state_update(self):
        """Test KnowledgeState update."""
        exercises = generate_lesson_3_1_exercises()[:5]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_1_mastery(responses)
        knowledge_state = KnowledgeState(concept_id="lesson_3_1")
        
        update_knowledge_state_3_1(assessment, knowledge_state)
        assert knowledge_state.correct_count == 5
        assert knowledge_state.incorrect_count == 0
    
    def test_mastery_tracker_update(self):
        """Test MasteryTracker update."""
        exercises = generate_lesson_3_1_exercises()[:10]
        responses = [(ex, ex.expected_answer) for ex in exercises]
        
        assessment = assess_lesson_3_1_mastery(responses)
        mastery_tracker = MasteryTracker()
        
        update_mastery_tracker_3_1(assessment, mastery_tracker, "lesson_3_1")
        
        record = mastery_tracker.get_progress("lesson_3_1")
        assert record is not None
        assert record.mastered is True


class TestLesson31Integration:
    """Test Lesson 3.1 integration."""
    
    def test_complete_learning_flow(self):
        """Test complete learning flow."""
        # Create lesson
        lesson = create_lesson_3_1()
        assert lesson is not None
        
        # Load vocabulary
        words = load_single_syllable_vocabulary()
        assert len(words) > 0
        
        # Generate exercises
        exercises = generate_lesson_3_1_exercises()
        assert len(exercises) > 0
        
        # Simulate perfect performance
        responses = [(ex, ex.expected_answer) for ex in exercises[:10]]
        
        # Assess mastery
        assessment = assess_lesson_3_1_mastery(responses)
        assert assessment['mastery_level'] == 'mastered'
        
        # Update tracking
        knowledge_state = KnowledgeState(concept_id=lesson.id)
        mastery_tracker = MasteryTracker()
        
        update_knowledge_state_3_1(assessment, knowledge_state)
        update_mastery_tracker_3_1(assessment, mastery_tracker, lesson.id)
        
        # Verify final state
        total = knowledge_state.correct_count + knowledge_state.incorrect_count
        accuracy = knowledge_state.correct_count / total if total > 0 else 0.0
        assert accuracy >= 0.90
        assert mastery_tracker.get_progress(lesson.id).mastered is True
