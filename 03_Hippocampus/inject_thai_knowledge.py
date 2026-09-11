#!/usr/bin/env python3
"""Inject Thai Lexicon and NER knowledge into Hippocampus knowledge base."""

import json
from datetime import datetime

# Thai Linguistics & NER Knowledge Facts
thai_knowledge_facts = [
    {
        "topic": "Thai word segmentation",
        "summary": "Thai script has no spaces between words. Segmentation requires lexicon lookup, statistical models, or neural networks. Common patterns: compound words (คำประสม), reduplications (คำซ้อน), and particles (คำช่วย).",
        "source": "linguistic_consolidation",
        "confidence": 0.95
    },
    {
        "topic": "Thai lexicon patterns",
        "summary": "Thai vocabulary includes native Thai words, Sanskrit/Pali loanwords (especially formal/religious contexts), and modern English loanwords. Classifiers (ลักษณนาม) are mandatory when counting nouns.",
        "source": "linguistic_consolidation",
        "confidence": 0.93
    },
    {
        "topic": "Thai NER: PERSON entities",
        "summary": "Thai person names often preceded by honorifics: คุณ (Mr./Ms.), นาย (Mr.), นาง (Mrs.), นางสาว (Miss), ดร. (Dr.), ศ. (Prof.). Royal titles: พระ-, สม-, ใน-. Nicknames common in casual contexts.",
        "source": "linguistic_consolidation",
        "confidence": 0.94
    },
    {
        "topic": "Thai NER: LOCATION entities",
        "summary": "Location markers: จังหวัด (province), อำเภอ (district), ตำบล (sub-district), ถนน (road), ซอย (lane), เมือง (city/town). Bangkok uses เขต (district). Geographic names often compound nouns.",
        "source": "linguistic_consolidation",
        "confidence": 0.92
    },
    {
        "topic": "Thai NER: ORGANIZATION entities",
        "summary": "Organization patterns: บริษัท (company), หจก. (limited partnership), มหาวิทยาลัย (university), โรงเรียน (school), กระทรวง (ministry), กรม (department), สำนักงาน (office).",
        "source": "linguistic_consolidation",
        "confidence": 0.91
    },
    {
        "topic": "Thai NER: DATE/TIME entities",
        "summary": "Time markers: วัน (day), เดือน (month), ปี (year), วันที่ (date), เวลา (time), นาฬิกา (o'clock). Buddhist Era (พ.ศ.) = Gregorian + 543. Weekdays: วันจันทร์ (Monday) through วันอาทิตย์ (Sunday).",
        "source": "linguistic_consolidation",
        "confidence": 0.96
    },
    {
        "topic": "Thai NER: COMMAND_INTENT extraction",
        "summary": "Thai command verbs: ช่วย (help), กรุณา (please), ขอ (request), ทำ (do/make), เปิด (open), ปิด (close), ค้นหา (search), บอก (tell), แสดง (show). Question words: อะไร (what), ที่ไหน (where), เมื่อไหร่ (when), ทำไม (why), อย่างไร (how).",
        "source": "linguistic_consolidation",
        "confidence": 0.93
    },
    {
        "topic": "Thai sentence structure",
        "summary": "Standard order: Subject-Verb-Object (SVO). Modifiers follow nouns. Negation: ไม่ (not) precedes verb. Questions formed by adding question particles: ไหม (yes/no), หรือ (or), มั้ย (informal yes/no).",
        "source": "linguistic_consolidation",
        "confidence": 0.94
    },
    {
        "topic": "Thai politeness markers",
        "summary": "Male speakers end sentences with ครับ (formal) or คับ (casual). Female speakers use ค่ะ (formal statement), คะ (formal question), or จ้า (casual). Essential for respectful communication with creator (เจ้านาย).",
        "source": "linguistic_consolidation",
        "confidence": 0.97
    },
    {
        "topic": "Thai context clues for entity extraction",
        "summary": "Prefix indicators improve NER: Personal titles (คุณ, นาย, พี่, น้อง), location prepositions (ที่, ใน, ที่จังหวัด), organization types (บริษัท, โรง), temporal markers (วันนี้, เมื่อวาน, พรุ่งนี้). Context windows of 2-3 words increase accuracy.",
        "source": "linguistic_consolidation",
        "confidence": 0.92
    },
    {
        "topic": "Thai pronoun system",
        "summary": "Thai pronouns reflect social hierarchy. First person: ผม (male formal), ดิฉัน (female formal), ฉัน (casual), กู (vulgar). Second person: คุณ (polite), เธอ (casual), มึง (vulgar). Context determines appropriate form.",
        "source": "linguistic_consolidation",
        "confidence": 0.90
    },
    {
        "topic": "Thai royal language (ราชาศัพท์)",
        "summary": "Special vocabulary for addressing or discussing royalty. Common verbs transformed: eat→เสวย, sleep→บรรทม, walk→เสด็จ, die→สวรรคต. Essential knowledge for Thai cultural contexts and news processing.",
        "source": "linguistic_consolidation",
        "confidence": 0.89
    },
    {
        "topic": "Thai tonal system",
        "summary": "Thai has 5 tones: mid, low, falling, high, rising. Tone marks (วรรณยุกต์): ่ (low), ้ (falling), ๊ (high), ๋ (rising). Tone changes word meaning entirely. Critical for speech recognition and synthesis accuracy.",
        "source": "linguistic_consolidation",
        "confidence": 0.95
    },
    {
        "topic": "Thai numeral system",
        "summary": "Thai numerals: ๐=0, ๑=1, ๒=2, ๓=3, ๔=4, ๕=5, ๖=6, ๗=7, ๘=8, ๙=9. Arabic numerals (0-9) commonly used. Words: หนึ่ง(1), สอง(2), สาม(3), สี่(4), ห้า(5). Classifier required when counting.",
        "source": "linguistic_consolidation",
        "confidence": 0.93
    },
    {
        "topic": "Thai compound word formation",
        "summary": "Thai creates meaning through compounding: โรงพยาบาล (hospital = โรง[building] + พยาบาล[nurse]), โรงเรียน (school = โรง[building] + เรียน[study]). Understanding components aids comprehension and segmentation.",
        "source": "linguistic_consolidation",
        "confidence": 0.91
    }
]

def inject_thai_knowledge():
    """Load knowledge base, inject Thai facts, and save."""
    kb_path = "knowledge_base.json"
    
    # Load existing knowledge base
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    # Get current timestamp
    timestamp = datetime.now().isoformat()
    
    # Add timestamp to each fact
    for fact in thai_knowledge_facts:
        fact["timestamp"] = timestamp
    
    # Inject facts
    original_count = len(kb["learned_facts"])
    kb["learned_facts"].extend(thai_knowledge_facts)
    kb["last_updated"] = timestamp
    
    # Save updated knowledge base
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    new_count = len(kb["learned_facts"])
    print(f"✓ Thai knowledge injection complete")
    print(f"  Original facts: {original_count}")
    print(f"  Added facts: {len(thai_knowledge_facts)}")
    print(f"  Total facts: {new_count}")
    print(f"  Timestamp: {timestamp}")
    
    return new_count

if __name__ == "__main__":
    inject_thai_knowledge()
