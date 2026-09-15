"""
Thai Language Week 3 Curriculum
Vocabulary Foundation: From Words to Meaning

Week 3 focuses on building vocabulary knowledge after establishing
phonological foundation in Week 2.
"""
from runtime.education import Lesson
from runtime.education.thai_language_data import ThaiLanguageData
from typing import List


def create_week3_lessons(thai_data: ThaiLanguageData) -> List[Lesson]:
    """
    Create Week 3 lessons: Vocabulary Foundation
    10 lessons covering vocabulary, word reading, and meaning
    """
    lessons = []
    
    # 3.1: Single-Syllable Vocabulary
    lesson_3_1 = Lesson(
        subject_id="thai_language",
        level=3,
        title="คำพยางค์เดียว (Single-Syllable Vocabulary)",
        objectives=[
            "Read and recognize 10+ single-syllable words",
            "Connect orthography → pronunciation → meaning",
            "Distinguish words by tone contrast",
            "Apply Week 2 phonology to real vocabulary",
        ],
        content="Common single-syllable Thai words with pronunciation and meaning",
        prerequisites=[],  # Requires Week 2 completion
    )
    lessons.append(lesson_3_1)
    
    # 3.2: Two-Syllable Vocabulary
    lesson_3_2 = Lesson(
        subject_id="thai_language",
        level=3,
        title="คำสองพยางค์ (Two-Syllable Vocabulary)",
        objectives=[
            "Read and recognize two-syllable words",
            "Identify syllable boundaries in words",
            "Apply tone rules to each syllable independently",
            "Connect multi-syllable pronunciation to meaning",
        ],
        content="Common two-syllable Thai words with syllable boundaries",
        prerequisites=[lesson_3_1.id],
    )
    lessons.append(lesson_3_2)
    
    # 3.3: Word Categories
    lesson_3_3 = Lesson(
        subject_id="thai_language",
        level=3,
        title="ประเภทคำ (Word Categories)",
        objectives=[
            "Classify words as noun, verb, or adjective",
            "Understand basic Thai word categories",
            "Recognize category from meaning and usage",
            "Build categorical vocabulary knowledge",
        ],
        content="Thai word categories: nouns, verbs, adjectives",
        prerequisites=[lesson_3_2.id],
    )
    lessons.append(lesson_3_3)
    
    # 3.4: Tone Contrast in Vocabulary
    lesson_3_4 = Lesson(
        subject_id="thai_language",
        level=3,
        title="ความแตกต่างของเสียงวรรณยุกต์ (Tone Contrast)",
        objectives=[
            "Recognize minimal pairs differing only in tone",
            "Understand that tone changes meaning",
            "Distinguish words by tone alone",
            "Apply precise tone identification to vocabulary",
        ],
        content="Tone is lexical: same segments + different tone = different meaning",
        prerequisites=[lesson_3_3.id],
    )
    lessons.append(lesson_3_4)
    
    # 3.5: Compound Words
    lesson_3_5 = Lesson(
        subject_id="thai_language",
        level=3,
        title="คำประสม (Compound Words)",
        objectives=[
            "Recognize compound words (two meaningful parts)",
            "Understand compound formation patterns",
            "Decompose compounds into components",
            "Derive compound meaning from parts",
        ],
        content="Thai compound words: ทำงาน (work), ครอบครัว (family), หนังสือ (book)",
        prerequisites=[lesson_3_4.id],
    )
    lessons.append(lesson_3_5)
    
    # 3.6: Common Phrases
    lesson_3_6 = Lesson(
        subject_id="thai_language",
        level=3,
        title="วลีที่ใช้บ่อย (Common Phrases)",
        objectives=[
            "Read and recognize common Thai phrases",
            "Understand phrase meaning and usage",
            "Learn greetings and polite expressions",
            "Apply phonology to multi-word phrases",
        ],
        content="Common phrases: สวัสดี (hello), ขอบคุณ (thank you)",
        prerequisites=[lesson_3_5.id],
    )
    lessons.append(lesson_3_6)
    
    # 3.7: High-Frequency Vocabulary
    lesson_3_7 = Lesson(
        subject_id="thai_language",
        level=3,
        title="คำที่ใช้บ่อย (High-Frequency Vocabulary)",
        objectives=[
            "Master the most frequent Thai words",
            "Develop automatic recognition of common words",
            "Build vocabulary fluency",
            "Understand frequency-based learning",
        ],
        content="High-frequency vocabulary for maximum reading utility",
        prerequisites=[lesson_3_6.id],
    )
    lessons.append(lesson_3_7)
    
    # 3.8: Contextual Reading
    lesson_3_8 = Lesson(
        subject_id="thai_language",
        level=3,
        title="การอ่านตามบริบท (Contextual Reading)",
        objectives=[
            "Read words in meaningful context",
            "Use context to support comprehension",
            "Understand word relationships in phrases",
            "Apply vocabulary knowledge contextually",
        ],
        content="Reading vocabulary in context: simple phrases and word combinations",
        prerequisites=[lesson_3_7.id],
    )
    lessons.append(lesson_3_8)
    
    # 3.9: Reading Fluency Practice
    lesson_3_9 = Lesson(
        subject_id="thai_language",
        level=3,
        title="การอ่านคล่อง (Reading Fluency)",
        objectives=[
            "Develop automatic word recognition",
            "Read vocabulary without conscious decoding",
            "Increase reading speed and confidence",
            "Consolidate Week 3 vocabulary knowledge",
        ],
        content="Practice rapid recognition of learned vocabulary",
        prerequisites=[lesson_3_8.id],
    )
    lessons.append(lesson_3_9)
    
    # 3.10: Integrated Vocabulary & Reading
    lesson_3_10 = Lesson(
        subject_id="thai_language",
        level=3,
        title="การอ่านแบบบูรณาการ (Integrated Vocabulary Reading)",
        objectives=[
            "Demonstrate mastery of Week 3 vocabulary",
            "Apply phonology + vocabulary together",
            "Read and comprehend words and phrases",
            "Integrate pronunciation, meaning, and context",
        ],
        content="Final integration: Week 2 phonology + Week 3 vocabulary = reading comprehension",
        prerequisites=[lesson_3_9.id],
    )
    lessons.append(lesson_3_10)
    
    return lessons
