"""
Test Thai Week 5 Curriculum
"""
import pytest
from runtime.education.thai_week5_curriculum import create_week5_lessons
from runtime.education.thai_language_data import ThaiLanguageData


class TestThaiWeek5Curriculum:
    """Test Week 5 curriculum structure."""
    
    def test_lesson_count(self):
        """Test that Week 5 has 10 lessons."""
        thai_data = ThaiLanguageData()
        lessons = create_week5_lessons(thai_data)
        assert len(lessons) == 10
    
    def test_lesson_level(self):
        """Test that all Week 5 lessons are level 5."""
        thai_data = ThaiLanguageData()
        lessons = create_week5_lessons(thai_data)
        
        for lesson in lessons:
            assert lesson.level == 5
    
    def test_lesson_subject(self):
        """Test that all lessons belong to thai_language subject."""
        thai_data = ThaiLanguageData()
        lessons = create_week5_lessons(thai_data)
        
        for lesson in lessons:
            assert lesson.subject_id == "thai_language"
    
    def test_lesson_titles(self):
        """Test that all lessons have Thai and English titles."""
        thai_data = ThaiLanguageData()
        lessons = create_week5_lessons(thai_data)
        
        for lesson in lessons:
            assert len(lesson.title) > 0
            assert '(' in lesson.title and ')' in lesson.title
    
    def test_lesson_objectives(self):
        """Test that all lessons have objectives."""
        thai_data = ThaiLanguageData()
        lessons = create_week5_lessons(thai_data)
        
        for lesson in lessons:
            assert len(lesson.objectives) >= 3
    
    def test_lesson_prerequisites(self):
        """Test prerequisite chain."""
        thai_data = ThaiLanguageData()
        lessons = create_week5_lessons(thai_data)
        
        # First lesson has no prerequisites within Week 5
        assert lessons[0].prerequisites == []
        
        # Subsequent lessons depend on previous
        for i in range(1, len(lessons)):
            assert len(lessons[i].prerequisites) == 1
            assert lessons[i].prerequisites[0] == lessons[i-1].id
    
    def test_lesson_ids_unique(self):
        """Test that all lesson IDs are unique."""
        thai_data = ThaiLanguageData()
        lessons = create_week5_lessons(thai_data)
        
        ids = [lesson.id for lesson in lessons]
        assert len(ids) == len(set(ids))
    
    def test_progression_topics(self):
        """Test that lessons follow practical communication progression."""
        thai_data = ThaiLanguageData()
        lessons = create_week5_lessons(thai_data)
        
        titles = [lesson.title for lesson in lessons]
        
        # Check key topics appear
        assert any('Classifiers' in t or 'ลักษณนาม' in t for t in titles[:2])
        assert any('Self-Directed' in t or 'การเรียนรู้ด้วยตนเอง' in t for t in titles[-1:])
