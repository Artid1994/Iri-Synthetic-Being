"""
Test Thai Week 2 Curriculum
"""
import unittest
from runtime.education.thai_week2_curriculum import create_week2_lessons
from runtime.education.thai_language_data import ThaiLanguageData


class TestThaiWeek2Curriculum(unittest.TestCase):
    
    def setUp(self):
        self.thai_data = ThaiLanguageData()
        self.lessons = create_week2_lessons(self.thai_data)
    
    def test_lesson_count(self):
        """Test that Week 2 has 10 lessons."""
        self.assertEqual(len(self.lessons), 10)
    
    def test_lesson_ids_unique(self):
        """Test that all lesson IDs are unique."""
        lesson_ids = [lesson.id for lesson in self.lessons]
        self.assertEqual(len(lesson_ids), len(set(lesson_ids)))
    
    def test_lesson_prerequisites(self):
        """Test that lessons have correct prerequisite chain."""
        # First lesson has no prerequisites
        self.assertEqual(len(self.lessons[0].prerequisites), 0)
        
        # Each subsequent lesson requires previous
        for i in range(1, len(self.lessons)):
            self.assertIn(self.lessons[i-1].id, self.lessons[i].prerequisites)
    
    def test_lesson_level(self):
        """Test that all Week 2 lessons are level 2."""
        for lesson in self.lessons:
            self.assertEqual(lesson.level, 2)
    
    def test_lesson_subject(self):
        """Test that all lessons belong to thai_language."""
        for lesson in self.lessons:
            self.assertEqual(lesson.subject_id, "thai_language")
    
    def test_lesson_titles(self):
        """Test that lessons have Thai titles."""
        expected_thai_words = [
            'พยัญชนะ', 'สระ', 'พยางค์', 'ท้าย', 'เป็น',
            'เสียง', 'วรรณยุกต์', 'นำ', 'กลุ่ม', 'อ่าน'
        ]
        
        all_titles = ' '.join([lesson.title for lesson in self.lessons])
        
        # Check that Thai terms appear
        found_count = sum(1 for word in expected_thai_words if word in all_titles)
        self.assertGreater(found_count, 5)
    
    def test_lesson_objectives(self):
        """Test that all lessons have objectives."""
        for lesson in self.lessons:
            self.assertGreater(len(lesson.objectives), 0)
            self.assertLessEqual(len(lesson.objectives), 5)
    
    def test_progression_topics(self):
        """Test that lessons cover expected phonological topics."""
        topics = ' '.join([lesson.content for lesson in self.lessons])
        
        # Check key concepts are covered
        self.assertIn('IPA', topics)
        self.assertIn('consonant', topics.lower())
        self.assertIn('vowel', topics.lower())
        self.assertIn('tone', topics.lower())
        self.assertIn('live', topics.lower())


if __name__ == '__main__':
    unittest.main()
