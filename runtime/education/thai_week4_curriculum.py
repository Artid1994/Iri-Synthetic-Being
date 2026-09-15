"""
Thai Language Week 4 Curriculum
Sentence Foundation: From Words to Sentences

Week 4 focuses on building sentence understanding after establishing
vocabulary foundation in Week 3.
"""
from runtime.education import Lesson
from runtime.education.thai_language_data import ThaiLanguageData
from typing import List


def create_week4_lessons(thai_data: ThaiLanguageData) -> List[Lesson]:
    """
    Create Week 4 lessons: Sentence Foundation
    10 lessons covering basic grammar and sentence understanding
    """
    lessons = []
    
    # 4.1: Basic Sentence Structure
    lesson_4_1 = Lesson(
        subject_id="thai_language",
        level=4,
        title="โครงสร้างประโยคพื้นฐาน (Basic Sentence Structure)",
        objectives=[
            "Recognize Subject-Verb-Object (SVO) word order",
            "Identify subject, verb, and object in simple sentences",
            "Understand Thai word order patterns",
            "Read and comprehend basic sentences",
        ],
        content="Thai basic sentence structure: SVO word order",
        prerequisites=[],  # Requires Week 3 completion
    )
    lessons.append(lesson_4_1)
    
    # 4.2: Grammatical Roles
    lesson_4_2 = Lesson(
        subject_id="thai_language",
        level=4,
        title="การระบุบทบาททางไวยากรณ์ (Grammatical Roles)",
        objectives=[
            "Identify subject, verb, and object in sentences",
            "Understand grammatical role functions",
            "Distinguish between different sentence components",
            "Apply role analysis to sentence comprehension",
        ],
        content="Grammatical roles: Subject, Verb, Object identification",
        prerequisites=[lesson_4_1.id],
    )
    lessons.append(lesson_4_2)
    
    # 4.3: Negation
    lesson_4_3 = Lesson(
        subject_id="thai_language",
        level=4,
        title="การปฏิเสธ (Negation)",
        objectives=[
            "Use ไม่ (mai) for negation",
            "Understand negation word order (NEG + Verb)",
            "Form negative sentences",
            "Distinguish affirmative vs negative meaning",
        ],
        content="Thai negation: ไม่ + Verb pattern",
        prerequisites=[lesson_4_2.id],
    )
    lessons.append(lesson_4_3)
    
    # 4.4: Yes-No Questions
    lesson_4_4 = Lesson(
        subject_id="thai_language",
        level=4,
        title="คำถามแบบใช่-ไม่ใช่ (Yes-No Questions)",
        objectives=[
            "Form yes-no questions with ไหม",
            "Understand question particle placement (sentence-final)",
            "Distinguish statements from questions",
            "Comprehend question meaning",
        ],
        content="Yes-no questions: Statement + ไหม",
        prerequisites=[lesson_4_3.id],
    )
    lessons.append(lesson_4_4)
    
    # 4.5: Wh-Questions
    lesson_4_5 = Lesson(
        subject_id="thai_language",
        level=4,
        title="คำถาม wh- (Wh-Questions)",
        objectives=[
            "Use question words: อะไร (what), ที่ไหน (where), ทำไม (why)",
            "Understand in-situ wh-word placement",
            "Form and comprehend wh-questions",
            "Answer wh-questions appropriately",
        ],
        content="Wh-questions: in-situ question word placement",
        prerequisites=[lesson_4_4.id],
    )
    lessons.append(lesson_4_5)
    
    # 4.6: Thai Word Order
    lesson_4_6 = Lesson(
        subject_id="thai_language",
        level=4,
        title="ลำดับคำในภาษาไทย (Thai Word Order)",
        objectives=[
            "Master SVO basic word order",
            "Understand noun-adjective order (N-Adj)",
            "Apply word order rules consistently",
            "Recognize word order deviations",
        ],
        content="Thai word order: SVO sentences, Noun-Adjective modification",
        prerequisites=[lesson_4_5.id],
    )
    lessons.append(lesson_4_6)
    
    # 4.7: Tense and Aspect Markers
    lesson_4_7 = Lesson(
        subject_id="thai_language",
        level=4,
        title="เครื่องหมายกาลและลักษณะ (Tense and Aspect Markers)",
        objectives=[
            "Use แล้ว (perfective/completed)",
            "Use กำลัง (progressive/ongoing)",
            "Use จะ (future/intentional)",
            "Understand time reference in Thai",
        ],
        content="Thai aspect markers: แล้ว, กำลัง, จะ",
        prerequisites=[lesson_4_6.id],
    )
    lessons.append(lesson_4_7)
    
    # 4.8: Context-Dependent Meaning
    lesson_4_8 = Lesson(
        subject_id="thai_language",
        level=4,
        title="ความหมายตามบริบท (Context-Dependent Meaning)",
        objectives=[
            "Understand context-dependent interpretation",
            "Use context clues for disambiguation",
            "Recognize implicit information",
            "Apply contextual reasoning",
        ],
        content="Context-dependent interpretation in Thai sentences",
        prerequisites=[lesson_4_7.id],
    )
    lessons.append(lesson_4_8)
    
    # 4.9: Sentence Analysis
    lesson_4_9 = Lesson(
        subject_id="thai_language",
        level=4,
        title="การวิเคราะห์ประโยค (Sentence Analysis)",
        objectives=[
            "Analyze complete sentence structure",
            "Identify all grammatical components",
            "Explain WHY sentences have their meaning",
            "Apply integrated grammatical knowledge",
        ],
        content="Complete sentence analysis: structure, roles, word order, meaning",
        prerequisites=[lesson_4_8.id],
    )
    lessons.append(lesson_4_9)
    
    # 4.10: Integrated Sentence Understanding
    lesson_4_10 = Lesson(
        subject_id="thai_language",
        level=4,
        title="ความเข้าใจประโยคแบบบูรณาการ (Integrated Sentence Understanding)",
        objectives=[
            "Demonstrate Week 4 sentence mastery",
            "Read and comprehend varied sentence types",
            "Apply all grammatical patterns",
            "Integrate phonology + vocabulary + grammar",
        ],
        content="Final integration: Weeks 2-4 combined (sound → word → sentence → meaning)",
        prerequisites=[lesson_4_9.id],
    )
    lessons.append(lesson_4_10)
    
    return lessons
