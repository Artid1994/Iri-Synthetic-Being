import unittest

from runtime.education import (
    Subject,
    SubjectType,
    Lesson,
    Assessment,
    AssessmentResult,
    MasteryTracker,
    MasteryRecord,
    Curriculum,
)


class TestSubject(unittest.TestCase):
    def test_subject_creation(self):
        subject = Subject(
            id="thai",
            name="Thai Language",
            subject_type=SubjectType.LANGUAGE,
            description="Thai language fundamentals",
        )
        
        self.assertEqual(subject.id, "thai")
        self.assertEqual(subject.name, "Thai Language")
        self.assertEqual(subject.subject_type, SubjectType.LANGUAGE)
    
    def test_subject_requires_id(self):
        with self.assertRaises(ValueError):
            Subject(id="", name="Test", subject_type=SubjectType.LANGUAGE)


class TestLesson(unittest.TestCase):
    def test_lesson_creation(self):
        lesson = Lesson(
            subject_id="thai",
            level=1,
            title="Thai Vowels",
            objectives=["Learn 32 Thai vowels", "Recognize vowel forms"],
        )
        
        self.assertEqual(lesson.subject_id, "thai")
        self.assertEqual(lesson.level, 1)
        self.assertEqual(lesson.title, "Thai Vowels")
        self.assertEqual(len(lesson.objectives), 2)
        self.assertTrue(lesson.id)  # Auto-generated
    
    def test_lesson_requires_objectives(self):
        with self.assertRaises(ValueError):
            Lesson(
                subject_id="thai",
                level=1,
                title="Test",
                objectives=[],
            )
    
    def test_lesson_level_must_be_positive(self):
        with self.assertRaises(ValueError):
            Lesson(
                subject_id="thai",
                level=0,
                title="Test",
                objectives=["obj1"],
            )


class TestAssessment(unittest.TestCase):
    def test_assessment_passed(self):
        assessment = Assessment()
        result = assessment.evaluate(
            correct_count=9,
            total_count=10,
            attempts=1,
        )
        
        self.assertTrue(result.passed)
        self.assertEqual(result.score, 0.9)
        self.assertIn("MASTERED", result.feedback)
    
    def test_assessment_not_passed(self):
        assessment = Assessment()
        result = assessment.evaluate(
            correct_count=5,
            total_count=10,
            attempts=1,
        )
        
        self.assertFalse(result.passed)
        self.assertEqual(result.score, 0.5)
        self.assertIn("NOT_YET_MASTERED", result.feedback)
    
    def test_assessment_requires_remediation(self):
        assessment = Assessment()
        result = assessment.evaluate(
            correct_count=6,
            total_count=10,
            attempts=3,
        )
        
        self.assertFalse(result.passed)
        self.assertIn("REMEDIATION_REQUIRED", result.feedback)
    
    def test_assessment_mastery_threshold(self):
        assessment = Assessment()
        
        # Exactly at threshold (80%)
        result = assessment.evaluate(8, 10, 1)
        self.assertTrue(result.passed)
        
        # Just below threshold
        result = assessment.evaluate(7, 10, 1)
        self.assertFalse(result.passed)


class TestMasteryTracker(unittest.TestCase):
    def test_mastery_tracker_initial_state(self):
        tracker = MasteryTracker()
        
        self.assertFalse(tracker.is_mastered("lesson1"))
        self.assertIsNone(tracker.get_progress("lesson1"))
    
    def test_mastery_tracker_records_attempt(self):
        tracker = MasteryTracker()
        
        record = tracker.record_attempt("lesson1", 0.9)
        
        self.assertEqual(record.lesson_id, "lesson1")
        self.assertEqual(record.mastery_score, 0.9)
        self.assertEqual(record.attempts, 1)
        self.assertTrue(record.mastered)
        self.assertTrue(tracker.is_mastered("lesson1"))
    
    def test_mastery_tracker_weighted_average(self):
        tracker = MasteryTracker()
        
        # First attempt: 50%
        tracker.record_attempt("lesson1", 0.5)
        record1 = tracker.get_progress("lesson1")
        self.assertEqual(record1.mastery_score, 0.5)
        
        # Second attempt: 100% -> weighted average
        # 0.7 * 1.0 + 0.3 * 0.5 = 0.85
        tracker.record_attempt("lesson1", 1.0)
        record2 = tracker.get_progress("lesson1")
        self.assertAlmostEqual(record2.mastery_score, 0.85, places=2)
        self.assertEqual(record2.attempts, 2)
        self.assertTrue(record2.mastered)
    
    def test_mastery_tracker_prerequisites(self):
        tracker = MasteryTracker()
        
        # No prerequisites met
        self.assertTrue(tracker.prerequisites_met([]))
        
        # Prerequisites not mastered
        self.assertFalse(tracker.prerequisites_met(["lesson1", "lesson2"]))
        
        # Master prerequisites
        tracker.record_attempt("lesson1", 0.9)
        tracker.record_attempt("lesson2", 0.85)
        
        # Now prerequisites met
        self.assertTrue(tracker.prerequisites_met(["lesson1", "lesson2"]))


class TestCurriculum(unittest.TestCase):
    def test_curriculum_add_subject(self):
        curriculum = Curriculum()
        subject = Subject(
            id="thai",
            name="Thai Language",
            subject_type=SubjectType.LANGUAGE,
        )
        
        curriculum.add_subject(subject)
        
        self.assertIn("thai", curriculum.subjects)
        self.assertEqual(curriculum.get_subject_by_id("thai"), subject)
    
    def test_curriculum_add_lesson(self):
        curriculum = Curriculum()
        subject = Subject(
            id="thai",
            name="Thai Language",
            subject_type=SubjectType.LANGUAGE,
        )
        curriculum.add_subject(subject)
        
        lesson = Lesson(
            subject_id="thai",
            level=1,
            title="Test Lesson",
            objectives=["Learn something"],
        )
        
        curriculum.add_lesson(lesson)
        
        self.assertIn(lesson.id, curriculum.lessons)
        self.assertEqual(curriculum.get_lesson_by_id(lesson.id), lesson)
    
    def test_curriculum_rejects_lesson_without_subject(self):
        curriculum = Curriculum()
        lesson = Lesson(
            subject_id="nonexistent",
            level=1,
            title="Test",
            objectives=["obj"],
        )
        
        with self.assertRaises(ValueError):
            curriculum.add_lesson(lesson)
    
    def test_curriculum_get_next_lesson(self):
        curriculum = Curriculum()
        
        # Add subject
        subject = Subject(
            id="thai",
            name="Thai Language",
            subject_type=SubjectType.LANGUAGE,
        )
        curriculum.add_subject(subject)
        
        # Add lessons
        lesson1 = Lesson(
            subject_id="thai",
            level=1,
            title="Lesson 1",
            objectives=["obj1"],
        )
        lesson2 = Lesson(
            subject_id="thai",
            level=2,
            title="Lesson 2",
            objectives=["obj2"],
            prerequisites=[lesson1.id],
        )
        
        curriculum.add_lesson(lesson1)
        curriculum.add_lesson(lesson2)
        
        # Should get lesson1 first (lowest level, no prerequisites)
        next_lesson = curriculum.get_next_lesson("thai")
        self.assertEqual(next_lesson.id, lesson1.id)
        
        # Master lesson1
        curriculum.mastery_tracker.record_attempt(lesson1.id, 0.9)
        
        # Now should get lesson2
        next_lesson = curriculum.get_next_lesson("thai")
        self.assertEqual(next_lesson.id, lesson2.id)
        
        # Master lesson2
        curriculum.mastery_tracker.record_attempt(lesson2.id, 0.85)
        
        # No more lessons
        next_lesson = curriculum.get_next_lesson("thai")
        self.assertIsNone(next_lesson)
    
    def test_curriculum_respects_prerequisites(self):
        curriculum = Curriculum()
        
        subject = Subject(
            id="thai",
            name="Thai",
            subject_type=SubjectType.LANGUAGE,
        )
        curriculum.add_subject(subject)
        
        lesson1 = Lesson(
            subject_id="thai",
            level=1,
            title="L1",
            objectives=["o1"],
        )
        lesson2 = Lesson(
            subject_id="thai",
            level=1,
            title="L2",
            objectives=["o2"],
            prerequisites=[lesson1.id],
        )
        
        curriculum.add_lesson(lesson1)
        curriculum.add_lesson(lesson2)
        
        # Without mastering lesson1, should get lesson1
        next_lesson = curriculum.get_next_lesson("thai")
        self.assertEqual(next_lesson.id, lesson1.id)
        
        # Even if we try again, should still get lesson1 (prerequisite not met)
        next_lesson = curriculum.get_next_lesson("thai")
        self.assertEqual(next_lesson.id, lesson1.id)


if __name__ == "__main__":
    unittest.main()
