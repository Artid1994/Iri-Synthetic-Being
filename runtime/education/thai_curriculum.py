"""
Thai Language Curriculum - Week 1: Grapheme Foundation
10 lessons covering consonant and vowel recognition
"""
from runtime.education import Subject, SubjectType, Lesson, Curriculum
from runtime.education.thai_language_data import ThaiLanguageData
from runtime.learning_exercise import LearningExercise
from typing import List


def create_thai_subject() -> Subject:
    """Create the Thai language subject."""
    return Subject(
        id="thai_language",
        name="ภาษาไทย (Thai Language)",
        subject_type=SubjectType.LANGUAGE,
        description="Complete Thai language mastery from graphemes to fluent communication"
    )


def create_week1_lessons(thai_data: ThaiLanguageData) -> List[Lesson]:
    """
    Create Week 1 lessons: Grapheme Recognition
    10 lessons covering all consonants, vowels, and tone marks
    """
    lessons = []
    
    # Lesson 1.1: Low Class Consonants (Part 1: 12 consonants)
    low_consonants_1 = thai_data.get_consonants_by_class('low')[:12]
    lesson_1_1 = Lesson(
        subject_id="thai_language",
        level=1,
        title="พยัญชนะกลุ่มต่ำ 1 (Low Class Consonants 1)",
        objectives=[
            f"Recognize and name {len(low_consonants_1)} low class consonants",
            "Distinguish low class from other classes",
            "Identify visual patterns",
        ],
        content=f"Low class consonants: {', '.join([c['char'] + ' (' + c['name'] + ')' for c in low_consonants_1])}",
    )
    lessons.append(lesson_1_1)
    
    # Lesson 1.2: Low Class Consonants (Part 2: remaining)
    low_consonants_2 = thai_data.get_consonants_by_class('low')[12:]
    lesson_1_2 = Lesson(
        subject_id="thai_language",
        level=1,
        title="พยัญชนะกลุ่มต่ำ 2 (Low Class Consonants 2)",
        objectives=[
            f"Recognize and name {len(low_consonants_2)} low class consonants",
            "Complete low class consonant mastery",
        ],
        content=f"Low class consonants: {', '.join([c['char'] + ' (' + c['name'] + ')' for c in low_consonants_2])}",
        prerequisites=[lesson_1_1.id],
    )
    lessons.append(lesson_1_2)
    
    # Lesson 1.3: Mid Class Consonants
    mid_consonants = thai_data.get_consonants_by_class('mid')
    lesson_1_3 = Lesson(
        subject_id="thai_language",
        level=1,
        title="พยัญชนะกลุ่มกลาง (Mid Class Consonants)",
        objectives=[
            f"Recognize and name {len(mid_consonants)} mid class consonants",
            "Understand mid class tone behavior",
        ],
        content=f"Mid class consonants: {', '.join([c['char'] + ' (' + c['name'] + ')' for c in mid_consonants])}",
        prerequisites=[lesson_1_2.id],
    )
    lessons.append(lesson_1_3)
    
    # Lesson 1.4: High Class Consonants
    high_consonants = thai_data.get_consonants_by_class('high')
    lesson_1_4 = Lesson(
        subject_id="thai_language",
        level=1,
        title="พยัญชนะกลุ่มสูง (High Class Consonants)",
        objectives=[
            f"Recognize and name {len(high_consonants)} high class consonants",
            "Distinguish high class from low/mid classes",
        ],
        content=f"High class consonants: {', '.join([c['char'] + ' (' + c['name'] + ')' for c in high_consonants])}",
        prerequisites=[lesson_1_3.id],
    )
    lessons.append(lesson_1_4)
    
    # Lesson 1.5: Consonant Class Review
    lesson_1_5 = Lesson(
        subject_id="thai_language",
        level=1,
        title="ทบทวนพยัญชนะ (Consonant Class Review)",
        objectives=[
            "Identify class of any consonant",
            "Distinguish similar shapes across classes",
            "Achieve 90%+ recognition accuracy",
        ],
        content="Comprehensive review of all 44 Thai consonants and their classes",
        prerequisites=[lesson_1_4.id],
    )
    lessons.append(lesson_1_5)
    
    # Lesson 1.6: Basic Vowels (Short Forms)
    short_vowels = [v for v in thai_data.vowels if v['length'] == 'short'][:10]
    lesson_1_6 = Lesson(
        subject_id="thai_language",
        level=1,
        title="สระสั้น (Short Vowels)",
        objectives=[
            f"Recognize {len(short_vowels)} short vowel forms",
            "Understand vowel position (above/below/leading/trailing)",
        ],
        content=f"Short vowels: {', '.join([v['form'] + ' (' + v['name'] + ')' for v in short_vowels])}",
        prerequisites=[lesson_1_5.id],
    )
    lessons.append(lesson_1_6)
    
    # Lesson 1.7: Long Vowels
    long_vowels = [v for v in thai_data.vowels if v['length'] == 'long'][:10]
    lesson_1_7 = Lesson(
        subject_id="thai_language",
        level=1,
        title="สระยาว (Long Vowels)",
        objectives=[
            f"Recognize {len(long_vowels)} long vowel forms",
            "Distinguish short vs long vowel pairs",
        ],
        content=f"Long vowels: {', '.join([v['form'] + ' (' + v['name'] + ')' for v in long_vowels])}",
        prerequisites=[lesson_1_6.id],
    )
    lessons.append(lesson_1_7)
    
    # Lesson 1.8: Complex Vowels
    complex_vowels = [v for v in thai_data.vowels if 'leading+' in v.get('position', '')]
    lesson_1_8 = Lesson(
        subject_id="thai_language",
        level=1,
        title="สระประสม (Complex Vowels)",
        objectives=[
            f"Recognize {len(complex_vowels)} complex vowel forms",
            "Understand multi-position vowels",
        ],
        content=f"Complex vowels: {', '.join([v['form'] + ' (' + v['name'] + ')' for v in complex_vowels])}",
        prerequisites=[lesson_1_7.id],
    )
    lessons.append(lesson_1_8)
    
    # Lesson 1.9: Tone Marks
    tone_marks = thai_data.tones['tone_marks']
    lesson_1_9 = Lesson(
        subject_id="thai_language",
        level=1,
        title="วรรณยุกต์ (Tone Marks)",
        objectives=[
            "Recognize 4 tone marks",
            "Understand tone mark names",
            "Identify tone marks on syllables",
        ],
        content=f"Tone marks: {', '.join([m['mark'] + ' (' + m['name'] + ')' for m in tone_marks])}",
        prerequisites=[lesson_1_8.id],
    )
    lessons.append(lesson_1_9)
    
    # Lesson 1.10: Complete Grapheme Mastery
    lesson_1_10 = Lesson(
        subject_id="thai_language",
        level=1,
        title="ทบทวนอักษรไทย (Complete Thai Grapheme Review)",
        objectives=[
            "Recognize any Thai consonant instantly",
            "Recognize any Thai vowel form instantly",
            "Identify tone marks accurately",
            "Achieve 95%+ speed and accuracy",
        ],
        content="Comprehensive review and mastery assessment of all Thai graphemes",
        prerequisites=[lesson_1_9.id],
    )
    lessons.append(lesson_1_10)
    
    return lessons


def create_exercises_for_lesson(lesson: Lesson, thai_data: ThaiLanguageData) -> List[LearningExercise]:
    """Generate practice exercises for a lesson."""
    exercises = []
    
    if "Low Class Consonants 1" in lesson.title:
        consonants = thai_data.get_consonants_by_class('low')[:12]
        for c in consonants[:5]:  # Sample exercises
            exercises.append(LearningExercise(
                question=f"What is the name of {c['char']}?",
                expected_answer=c['name'],
                verification_type="EXACT",
            ))
            exercises.append(LearningExercise(
                question=f"What class is {c['char']} ({c['name']})?",
                expected_answer="low",
                verification_type="EXACT",
            ))
    
    elif "Low Class Consonants 2" in lesson.title:
        consonants = thai_data.get_consonants_by_class('low')[12:]
        for c in consonants[:5]:
            exercises.append(LearningExercise(
                question=f"What is the name of {c['char']}?",
                expected_answer=c['name'],
                verification_type="EXACT",
            ))
    
    elif "Mid Class Consonants" in lesson.title:
        consonants = thai_data.get_consonants_by_class('mid')
        for c in consonants[:5]:
            exercises.append(LearningExercise(
                question=f"What is the name of {c['char']}?",
                expected_answer=c['name'],
                verification_type="EXACT",
            ))
            exercises.append(LearningExercise(
                question=f"What class is {c['char']}?",
                expected_answer="mid",
                verification_type="EXACT",
            ))
    
    elif "High Class Consonants" in lesson.title:
        consonants = thai_data.get_consonants_by_class('high')
        for c in consonants[:5]:
            exercises.append(LearningExercise(
                question=f"What is the name of {c['char']}?",
                expected_answer=c['name'],
                verification_type="EXACT",
            ))
            exercises.append(LearningExercise(
                question=f"What class is {c['char']}?",
                expected_answer="high",
                verification_type="EXACT",
            ))
    
    elif "Short Vowels" in lesson.title:
        vowels = [v for v in thai_data.vowels if v['length'] == 'short'][:10]
        for v in vowels[:5]:
            exercises.append(LearningExercise(
                question=f"What is the name of vowel {v['form']}?",
                expected_answer=v['name'],
                verification_type="EXACT",
            ))
    
    elif "Tone Marks" in lesson.title:
        marks = thai_data.tones['tone_marks']
        for m in marks:
            exercises.append(LearningExercise(
                question=f"What is the name of tone mark {m['mark']}?",
                expected_answer=m['name'],
                verification_type="EXACT",
            ))
    
    # If no exercises generated, create at least one placeholder
    if not exercises:
        exercises.append(LearningExercise(
            question="Review complete?",
            expected_answer="yes",
            verification_type="EXACT",
        ))
    
    return exercises


def initialize_thai_curriculum() -> tuple[Curriculum, ThaiLanguageData]:
    """Initialize complete Thai curriculum with Week 1 lessons."""
    thai_data = ThaiLanguageData()
    curriculum = Curriculum()
    
    # Add Thai subject
    subject = create_thai_subject()
    curriculum.add_subject(subject)
    
    # Add Week 1 lessons
    week1_lessons = create_week1_lessons(thai_data)
    for lesson in week1_lessons:
        curriculum.add_lesson(lesson)
    
    return curriculum, thai_data
