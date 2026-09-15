"""
Thai Language Week 2 Curriculum
Phonological Foundation: From Graphemes to Pronunciation

Simplified implementation following existing Week 1 pattern.
Uses Lesson structure without separate Exercise class.
"""
from runtime.education import Subject, Lesson
from runtime.education.thai_language_data import ThaiLanguageData
from typing import List


def create_week2_lessons(thai_data: ThaiLanguageData) -> List[Lesson]:
    """
    Create Week 2 lessons: Phonological Foundation
    10 lessons covering pronunciation, tones, and reading
    """
    lessons = []
    
    # 2.1: Consonant Pronunciation (Mid Class)
    lesson_2_1 = Lesson(
        subject_id="thai_language",
        level=2,
        title="การออกเสียงพยัญชนะ (Consonant Pronunciation)",
        objectives=[
            "Understand IPA transcription for mid-class consonants",
            "Recognize phonological features (place, manner, voicing)",
            "Distinguish aspirated vs unaspirated consonants",
        ],
        content="Mid-class consonants (ก จ ฎ ฏ ด ต บ ป อ) with IPA and phonological features",
        prerequisites=[],  # Requires Week 1 completion
    )
    lessons.append(lesson_2_1)
    
    # 2.2: Vowel Pronunciation
    lesson_2_2 = Lesson(
        subject_id="thai_language",
        level=2,
        title="การออกเสียงสระ (Vowel Pronunciation)",
        objectives=[
            "Learn IPA for Thai vowels",
            "Distinguish short vs long vowels",
            "Recognize vowel position (leading, above, below, trailing)",
        ],
        content="Thai vowel system: 9 short + 9 long + diphthongs with IPA",
        prerequisites=[lesson_2_1.id],
    )
    lessons.append(lesson_2_2)
    
    # 2.3: CV Combinations
    lesson_2_3 = Lesson(
        subject_id="thai_language",
        level=2,
        title="พยางค์เปิด (Open Syllables: CV)",
        objectives=[
            "Combine consonants and vowels",
            "Read simple CV syllables",
            "Apply parser to verify pronunciation",
        ],
        content="Simple CV syllables: กา, กิ, ตา, ดี, บู with full IPA transcription",
        prerequisites=[lesson_2_2.id],
    )
    lessons.append(lesson_2_3)
    
    # 2.4: Final Consonants
    lesson_2_4 = Lesson(
        subject_id="thai_language",
        level=2,
        title="พยัญชนะท้าย (Final Consonants)",
        objectives=[
            "Understand final consonant neutralization",
            "Distinguish sonorant vs stop finals",
            "Read CVC syllables correctly",
        ],
        content="Final consonants: 8 phonetic finals, neutralization rules, CVC structure",
        prerequisites=[lesson_2_3.id],
    )
    lessons.append(lesson_2_4)
    
    # 2.5: Live/Dead Syllables
    lesson_2_5 = Lesson(
        subject_id="thai_language",
        level=2,
        title="พยางค์เป็น-ตาย (Live vs Dead Syllables)",
        objectives=[
            "Classify syllables as live or dead",
            "Apply classification rules correctly",
            "Understand importance for tone rules",
        ],
        content="Live/dead classification: long vowel OR sonorant final = live; short vowel + stop = dead",
        prerequisites=[lesson_2_4.id],
    )
    lessons.append(lesson_2_5)
    
    # 2.6: Five Tones
    lesson_2_6 = Lesson(
        subject_id="thai_language",
        level=2,
        title="เสียงวรรณยุกต์ (The Five Tones)",
        objectives=[
            "Recognize all 5 Thai tones",
            "Understand tone contours",
            "Distinguish tones perceptually",
        ],
        content="Five tones: mid (0), low (1), falling (2), high (3), rising (4) with Chao notation",
        prerequisites=[lesson_2_5.id],
    )
    lessons.append(lesson_2_6)
    
    # 2.7: Tone Marks
    lesson_2_7 = Lesson(
        subject_id="thai_language",
        level=2,
        title="วรรณยุกต์ (Tone Marks and Rules)",
        objectives=[
            "Learn tone mark effects (◌่ ◌้ ◌๊ ◌๋)",
            "Apply tone rules by consonant class",
            "Calculate tone from orthography",
        ],
        content="Tone rules: consonant class + live/dead + tone mark → tone number",
        prerequisites=[lesson_2_6.id],
    )
    lessons.append(lesson_2_7)
    
    # 2.8: Leading ห/อ
    lesson_2_8 = Lesson(
        subject_id="thai_language",
        level=2,
        title="ห/อนำ (Leading ห/อ Modification)",
        objectives=[
            "Understand leading ห + sonorant → high class",
            "Recognize silent leading letters",
            "Apply modification in tone calculation",
        ],
        content="Leading ห before sonorants (ง น ม ย ร ล ว) changes effective class to high",
        prerequisites=[lesson_2_7.id],
    )
    lessons.append(lesson_2_8)
    
    # 2.9: Initial Clusters
    lesson_2_9 = Lesson(
        subject_id="thai_language",
        level=2,
        title="กลุ่มพยัญชนะต้น (Initial Clusters)",
        objectives=[
            "Pronounce consonant clusters",
            "Recognize valid cluster patterns",
            "Read cluster syllables fluently",
        ],
        content="Valid clusters: stop + liquid (กร กล ปล ขว etc.) with pronunciation rules",
        prerequisites=[lesson_2_8.id],
    )
    lessons.append(lesson_2_9)
    
    # 2.10: Integrated Reading
    lesson_2_10 = Lesson(
        subject_id="thai_language",
        level=2,
        title="อ่านรวม (Integrated Reading)",
        objectives=[
            "Apply all Week 2 concepts",
            "Read varied syllable types",
            "Achieve 80%+ pronunciation accuracy",
        ],
        content="Mixed syllables covering all phonological patterns from Week 2",
        prerequisites=[lesson_2_9.id],
    )
    lessons.append(lesson_2_10)
    
    return lessons
