"""
Test Thai Week 4 Curriculum
"""
import pytest
from runtime.education.thai_week4_curriculum import create_week4_lessons
from runtime.education.thai_language_data import ThaiLanguageData


class TestThaiWeek4Curriculum:
    """Test Week 4 curriculum structure."""
    
    def test_lesson_count(self):
        """Test that Week 4 has 10 lessons."""
        thai_data = ThaiLanguageData()
        lessons = create_week4_lessons(thai_data)
        assert len(lessons) == 10
    
    def test_lesson_level(self):
        """Test that all Week 4 lessons are level 4."""
        thai_data = ThaiLanguageData()
        lessons = create_week4_lessons(thai_data)
        
        for lesson in lessons:
            assert lesson.level == 4
    
    def test_lesson_subject(self):
        """Test that all lessons belong to thai_language subject."""
        thai_data = ThaiLanguageData()
        lessons = create_week4_lessons(thai_data)
        
        for lesson in lessons:
            assert lesson.subject_id == "thai_language"
    
    def test_lesson_titles(self):
        """Test that all lessons have Thai and English titles."""
        thai_data = ThaiLanguageData()
        lessons = create_week4_lessons(thai_data)
        
        for lesson in lessons:
            assert len(lesson.title) > 0
            assert '(' in lesson.title and ')' in lesson.title
    
    def test_lesson_objectives(self):
        """Test that all lessons have objectives."""
        thai_data = ThaiLanguageData()
        lessons = create_week4_lessons(thai_data)
        
        for lesson in lessons:
            assert len(lesson.objectives) >= 3
    
    def test_lesson_prerequisites(self):
        """Test prerequisite chain."""
        thai_data = ThaiLanguageData()
        lessons = create_week4_lessons(thai_data)
        
        # First lesson has no prerequisites within Week 4
        assert lessons[0].prerequisites == []
        
        # Subsequent lessons depend on previous
        for i in range(1, len(lessons)):
            assert len(lessons[i].prerequisites) == 1
            assert lessons[i].prerequisites[0] == lessons[i-1].id
    
    def test_lesson_ids_unique(self):
        """Test that all lesson IDs are unique."""
        thai_data = ThaiLanguageData()
        lessons = create_week4_lessons(thai_data)
        
        ids = [lesson.id for lesson in lessons]
        assert len(ids) == len(set(ids))
    
    def test_progression_topics(self):
        """Test that lessons follow grammar progression."""
        thai_data = ThaiLanguageData()
        lessons = create_week4_lessons(thai_data)
        
        titles = [lesson.title for lesson in lessons]
        
        # Check key topics appear in order
        assert any('Basic Sentence' in t or 'โครงสร้างประโยค' in t for t in titles[:2])
        assert any('Integrated' in t or 'บูรณาการ' in t for t in titles[-1:])
