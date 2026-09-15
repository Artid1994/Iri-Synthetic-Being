"""
Thai Language Week 5 Curriculum
Practical Communication: From Sentences to Conversation

Week 5 focuses on practical Thai structures after establishing
sentence foundation in Week 4.
"""
from runtime.education import Lesson
from runtime.education.thai_language_data import ThaiLanguageData
from typing import List


def create_week5_lessons(thai_data: ThaiLanguageData) -> List[Lesson]:
    """
    Create Week 5 lessons: Practical Communication
    10 lessons covering classifiers, serial verbs, and conversational structures
    """
    lessons = []
    
    # 5.1: Classifiers
    lesson_5_1 = Lesson(
        subject_id="thai_language",
        level=5,
        title="ลักษณนาม (Classifiers)",
        objectives=[
            "Understand the classifier system in Thai",
            "Recognize common classifiers",
            "Match classifiers to appropriate nouns",
            "Apply classifiers in counting contexts",
        ],
        content="Thai classifier system: Required for counting and specifying nouns",
        prerequisites=[],  # Requires Week 4 completion
    )
    lessons.append(lesson_5_1)
    
    # 5.2: Counting with Classifiers
    lesson_5_2 = Lesson(
        subject_id="thai_language",
        level=5,
        title="การนับด้วยลักษณนาม (Counting with Classifiers)",
        objectives=[
            "Form quantity expressions",
            "Count objects using appropriate classifiers",
            "Understand word order in quantity expressions",
            "Apply classifiers to real counting situations",
        ],
        content="Counting pattern: NOUN + NUMBER + CLASSIFIER",
        prerequisites=[lesson_5_1.id],
    )
    lessons.append(lesson_5_2)
    
    # 5.3: Serial Verbs
    lesson_5_3 = Lesson(
        subject_id="thai_language",
        level=5,
        title="กริยาอนุกรม (Serial Verbs)",
        objectives=[
            "Understand serial verb constructions",
            "Form verb sequences without conjunctions",
            "Recognize sequential, manner, and purpose patterns",
            "Apply serial verbs in sentence formation",
        ],
        content="Serial verbs: Multiple verbs in sequence, no conjunction",
        prerequisites=[lesson_5_2.id],
    )
    lessons.append(lesson_5_3)
    
    # 5.4: Location Expressions
    lesson_5_4 = Lesson(
        subject_id="thai_language",
        level=5,
        title="การแสดงตำแหน่งที่ (Location Expressions)",
        objectives=[
            "Use อยู่ for location expressions",
            "Form location sentences",
            "Understand locative structures",
            "Apply location expressions in context",
        ],
        content="Location pattern: อยู่ + LOCATION",
        prerequisites=[lesson_5_3.id],
    )
    lessons.append(lesson_5_4)
    
    # 5.5: Possession
    lesson_5_5 = Lesson(
        subject_id="thai_language",
        level=5,
        title="การแสดงความเป็นเจ้าของ (Possession)",
        objectives=[
            "Use มี for possession",
            "Form possession sentences",
            "Understand possessive structures",
            "Apply possession in practical contexts",
        ],
        content="Possession pattern: Subject + มี + Object",
        prerequisites=[lesson_5_4.id],
    )
    lessons.append(lesson_5_5)
    
    # 5.6: Want/Desire
    lesson_5_6 = Lesson(
        subject_id="thai_language",
        level=5,
        title="การแสดงความต้องการ (Want/Desire)",
        objectives=[
            "Use อยาก for expressing desire",
            "Form desire sentences",
            "Understand want/desire structures",
            "Apply desire expressions in practical contexts",
        ],
        content="Want/desire pattern: Subject + อยาก + Verb",
        prerequisites=[lesson_5_5.id],
    )
    lessons.append(lesson_5_6)
    
    # 5.7: Ability
    lesson_5_7 = Lesson(
        subject_id="thai_language",
        level=5,
        title="การแสดงความสามารถ (Ability)",
        objectives=[
            "Use ได้ for expressing ability",
            "Form ability sentences",
            "Understand can/ability structures",
            "Apply ability expressions correctly",
        ],
        content="Ability pattern: Verb + ได้",
        prerequisites=[lesson_5_6.id],
    )
    lessons.append(lesson_5_7)
    
    # 5.8: Expanded Sentence Patterns
    lesson_5_8 = Lesson(
        subject_id="thai_language",
        level=5,
        title="รูปแบบประโยคขยาย (Expanded Sentence Patterns)",
        objectives=[
            "Combine multiple grammatical elements",
            "Form complex sentences",
            "Integrate classifiers, serial verbs, and modifiers",
            "Apply expanded patterns in context",
        ],
        content="Expanded patterns: S-V-O-LOC, S-VERB-VERB, S-V-NUM-CL-O",
        prerequisites=[lesson_5_7.id],
    )
    lessons.append(lesson_5_8)
    
    # 5.9: Semantic Relationships
    lesson_5_9 = Lesson(
        subject_id="thai_language",
        level=5,
        title="ความสัมพันธ์เชิงความหมาย (Semantic Relationships)",
        objectives=[
            "Recognize time-sequence relationships",
            "Understand word-to-word semantic connections",
            "Identify sentence-to-sentence relationships",
            "Apply WHY reasoning to semantic patterns",
        ],
        content="Semantic relationships: time sequence, word connections, sentence relationships",
        prerequisites=[lesson_5_8.id],
    )
    lessons.append(lesson_5_9)
    
    # 5.10: Self-Directed Learning Strategies
    lesson_5_10 = Lesson(
        subject_id="thai_language",
        level=5,
        title="กลยุทธ์การเรียนรู้ด้วยตนเอง (Self-Directed Learning Strategies)",
        objectives=[
            "Identify knowledge gaps in Thai understanding",
            "Formulate learning questions",
            "Recognize when to seek examples vs practice",
            "Apply self-assessment to learning progress",
        ],
        content="Learning strategies: Gap identification, question formation, evidence seeking, practice, self-assessment",
        prerequisites=[lesson_5_9.id],
    )
    lessons.append(lesson_5_10)
    
    return lessons
