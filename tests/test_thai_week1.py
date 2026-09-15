import unittest

from runtime.education.thai_language_data import ThaiLanguageData
from runtime.education.thai_curriculum import (
    create_thai_subject,
    create_week1_lessons,
    create_exercises_for_lesson,
    initialize_thai_curriculum,
)
from runtime.education import Subject, SubjectType


class TestThaiLanguageData(unittest.TestCase):
    def setUp(self):
        self.thai_data = ThaiLanguageData()
    
    def test_load_consonants(self):
        """Test that consonant data loads correctly."""
        consonants = self.thai_data.consonants
        
        self.assertGreater(len(consonants), 40)  # At least 40 consonants
        
        # Check first consonant structure
        first = consonants[0]
        self.assertIn('char', first)
        self.assertIn('name', first)
        self.assertIn('class', first)
        self.assertIn('sound', first)
    
    def test_consonant_classes(self):
        """Test consonant class filtering."""
        low_class = self.thai_data.get_consonants_by_class('low')
        mid_class = self.thai_data.get_consonants_by_class('mid')
        high_class = self.thai_data.get_consonants_by_class('high')
        
        # Thai has 24 low, 9 mid, 11 high (excluding obsolete)
        self.assertGreater(len(low_class), 20)
        self.assertEqual(len(mid_class), 9)
        self.assertGreaterEqual(len(high_class), 10)  # Allow exactly 10
        
        # Verify ก is mid class
        ko_kai = self.thai_data.get_consonant('ก')
        self.assertEqual(ko_kai['class'], 'mid')
        self.assertEqual(ko_kai['name'], 'ko kai')
    
    def test_load_vowels(self):
        """Test that vowel data loads correctly."""
        vowels = self.thai_data.vowels
        
        self.assertGreater(len(vowels), 25)  # At least 25 vowel forms
        
        # Check structure
        first = vowels[0]
        self.assertIn('form', first)
        self.assertIn('name', first)
        self.assertIn('sound', first)
        self.assertIn('length', first)
    
    def test_load_tones(self):
        """Test that tone data loads correctly."""
        tones = self.thai_data.tones
        
        self.assertIn('tones', tones)
        self.assertIn('tone_marks', tones)
        self.assertIn('tone_rules', tones)
        
        # Check 5 tones
        self.assertEqual(len(tones['tones']), 5)
        
        # Check 4 tone marks
        self.assertEqual(len(tones['tone_marks']), 4)


class TestThaiCurriculum(unittest.TestCase):
    def test_create_thai_subject(self):
        """Test Thai subject creation."""
        subject = create_thai_subject()
        
        self.assertIsInstance(subject, Subject)
        self.assertEqual(subject.id, "thai_language")
        self.assertEqual(subject.subject_type, SubjectType.LANGUAGE)
        self.assertIn("ภาษาไทย", subject.name)
    
    def test_create_week1_lessons(self):
        """Test Week 1 lesson creation."""
        thai_data = ThaiLanguageData()
        lessons = create_week1_lessons(thai_data)
        
        # Week 1 has 10 lessons
        self.assertEqual(len(lessons), 10)
        
        # Check first lesson
        lesson1 = lessons[0]
        self.assertEqual(lesson1.subject_id, "thai_language")
        self.assertEqual(lesson1.level, 1)
        self.assertIn("Low Class Consonants", lesson1.title)
        self.assertGreater(len(lesson1.objectives), 0)
        
        # Check prerequisite chain
        lesson2 = lessons[1]
        self.assertIn(lesson1.id, lesson2.prerequisites)
    
    def test_lesson_prerequisite_chain(self):
        """Test that lessons form proper prerequisite chain."""
        thai_data = ThaiLanguageData()
        lessons = create_week1_lessons(thai_data)
        
        # Lesson 1 has no prerequisites
        self.assertEqual(len(lessons[0].prerequisites), 0)
        
        # Each subsequent lesson depends on previous
        for i in range(1, len(lessons)):
            self.assertEqual(len(lessons[i].prerequisites), 1)
            self.assertEqual(lessons[i].prerequisites[0], lessons[i-1].id)
    
    def test_create_exercises(self):
        """Test exercise generation for lessons."""
        thai_data = ThaiLanguageData()
        lessons = create_week1_lessons(thai_data)
        
        # Test exercise generation for first lesson
        exercises = create_exercises_for_lesson(lessons[0], thai_data)
        
        self.assertGreater(len(exercises), 0)
        
        # Check exercise structure
        ex = exercises[0]
        self.assertTrue(ex.question)
        self.assertTrue(ex.expected_answer)
        self.assertIn(ex.verification_type, {"EXACT", "NUMERICAL"})
    
    def test_initialize_curriculum(self):
        """Test complete curriculum initialization."""
        curriculum, thai_data = initialize_thai_curriculum()
        
        # Check subject added
        self.assertIn("thai_language", curriculum.subjects)
        
        # Check all 10 lessons added
        thai_lessons = [l for l in curriculum.lessons.values() if l.subject_id == "thai_language"]
        self.assertEqual(len(thai_lessons), 10)
        
        # Check can get first lesson
        next_lesson = curriculum.get_next_lesson("thai_language")
        self.assertIsNotNone(next_lesson)
        self.assertEqual(next_lesson.level, 1)


class TestThaiWeek1Integration(unittest.TestCase):
    def test_complete_week1_flow(self):
        """Test complete Week 1 learning flow."""
        from runtime.education import LearningSession, EducationPersistence
        from runtime.memory import Memory
        from runtime.self_model import SelfModel
        from runtime.identity import Identity
        from runtime.education import MasteryTracker
        import tempfile
        from pathlib import Path
        
        # Initialize curriculum
        curriculum, thai_data = initialize_thai_curriculum()
        
        # Setup learning session with persistence
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = EducationPersistence(storage_dir=Path(tmpdir))
            
            # Important: Use curriculum's own mastery tracker
            curriculum.mastery_tracker.set_persistence(persistence)
            
            session = LearningSession(
                mastery_tracker=curriculum.mastery_tracker,
                memory=Memory(),
                self_model=SelfModel(),
                identity=Identity(),
                persistence=persistence,
            )
            
            # Get first lesson
            lesson1 = curriculum.get_next_lesson("thai_language")
            self.assertIsNotNone(lesson1)
            
            # Create exercises
            exercises = create_exercises_for_lesson(lesson1, thai_data)
            self.assertGreater(len(exercises), 0)
            
            # Conduct session (without answers = perfect score)
            result = session.conduct_session(lesson1, exercises)
            
            # Verify result
            self.assertTrue(result.mastered)
            self.assertTrue(result.assessment_result.passed)
            self.assertEqual(result.exercises_attempted, len(exercises))
            
            # Verify persistence
            loaded_records = persistence.load_mastery_records()
            self.assertIn(lesson1.id, loaded_records)
            
            # Verify mastery recorded in tracker
            self.assertTrue(curriculum.mastery_tracker.is_mastered(lesson1.id))
            
            # Verify next lesson available
            lesson2 = curriculum.get_next_lesson("thai_language")
            self.assertIsNotNone(lesson2)
            # After mastering lesson 1, should get lesson 2 (different lesson)
            self.assertNotEqual(lesson2.title, lesson1.title)


if __name__ == "__main__":
    unittest.main()
