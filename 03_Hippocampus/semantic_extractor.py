#!/usr/bin/env python3
"""
Semantic Knowledge Extractor for AE01M
Extracts structured semantic facts from natural language teaching statements.
"""
import re
from typing import List, Dict, Optional
from datetime import datetime


class SemanticFact:
    """Represents a single extracted semantic fact."""
    
    def __init__(self, subject: str, predicate: str, object_: str, context: str = ""):
        self.subject = subject
        self.predicate = predicate
        self.object = object_
        self.context = context
        self.learned_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'subject': self.subject,
            'predicate': self.predicate,
            'object': self.object,
            'context': self.context,
            'learned_at': self.learned_at
        }
    
    def to_markdown(self) -> str:
        """Format as markdown for storage."""
        md = f"**{self.subject}** {self.predicate} **{self.object}**"
        if self.context:
            md += f"\n\n_{self.context}_"
        return md


class SemanticExtractor:
    """Extract structured semantic knowledge from natural language."""
    
    def __init__(self):
        # Thai teaching patterns (MORE SPECIFIC PATTERNS FIRST)
        self.thai_patterns = [
            # "ชื่อของ X คือ Y" (name of X is Y) - MUST come before general คือ
            (r'ชื่อของ\s*(.+?)\s*คือ\s*(.+?)(?:\s|$|\.)', 'ชื่อคือ', 'naming'),
            # "X คือ Y" (X is Y)
            (r'(.+?)\s*คือ\s*(.+?)(?:\s|$|\.)', 'คือ', 'definition'),
            # "X ชอบ Y" (X likes Y)
            (r'(.+?)\s*ชอบ\s*(.+?)(?:\s|$|\.)', 'ชอบ', 'preference'),
            # "X อาศัยอยู่ Y" (X lives in Y)
            (r'(.+?)\s*อาศัยอยู่\s*(.+?)(?:\s|$|\.)', 'อาศัยอยู่', 'location'),
            # "X ออกหา Y" (X goes out to find Y)
            (r'(.+?)\s*ออกหา\s*(.+?)(?:\s|$|\.)', 'ออกหา', 'action'),
            # "X นอนบน Y" (X sleeps on Y)
            (r'(.+?)\s*นอนบน\s*(.+?)(?:\s|$|\.)', 'นอนบน', 'location'),
        ]
        
        # English teaching patterns
        self.english_patterns = [
            # "X is Y"
            (r'(.+?)\s+is\s+(.+?)(?:\s|$|\.)', 'is', 'definition'),
            # "X lives in Y"
            (r'(.+?)\s+lives?\s+in\s+(.+?)(?:\s|$|\.)', 'lives in', 'location'),
            # "X likes Y"
            (r'(.+?)\s+likes?\s+(.+?)(?:\s|$|\.)', 'likes', 'preference'),
        ]
    
    def extract_facts(self, text: str) -> List[SemanticFact]:
        """Extract semantic facts from teaching text."""
        facts = []
        
        # Try Thai patterns
        for pattern, predicate, fact_type in self.thai_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) >= 2:
                    subject = match.group(1).strip()
                    obj = match.group(2).strip()
                    
                    # For naming patterns, swap: the name IS the entity, not the thing being named
                    if fact_type == 'naming':
                        subject, obj = obj, subject
                    
                    # Clean up subjects and objects
                    subject = self._clean_entity(subject)
                    obj = self._clean_entity(obj)
                    
                    if subject and obj and len(subject) < 100 and len(obj) < 200:
                        facts.append(SemanticFact(subject, predicate, obj, context=text[:200]))
        
        # Try English patterns
        for pattern, predicate, fact_type in self.english_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) >= 2:
                    subject = match.group(1).strip()
                    obj = match.group(2).strip()
                    
                    subject = self._clean_entity(subject)
                    obj = self._clean_entity(obj)
                    
                    if subject and obj and len(subject) < 100 and len(obj) < 200:
                        facts.append(SemanticFact(subject, predicate, obj, context=text[:200]))
        
        return facts
    
    def _clean_entity(self, entity: str) -> str:
        """Clean and normalize extracted entity."""
        # Remove quotes
        entity = re.sub(r'["\']', '', entity)
        # Remove excessive whitespace
        entity = re.sub(r'\s+', ' ', entity)
        # Remove trailing punctuation
        entity = entity.rstrip('.,!?')
        return entity.strip()
    
    def is_teaching_statement(self, text: str) -> bool:
        """Check if text appears to be teaching new information."""
        teaching_markers_thai = [
            'คือ', 'จำไว้', 'จดจำ', 'เรียนรู้', 'รู้ไว้',
            'ชื่อ', 'นี้คือ', 'สอน', 'บอก'
        ]
        teaching_markers_english = [
            'is', 'called', 'named', 'remember', 'learn',
            'teach', 'this is', 'that is'
        ]
        
        text_lower = text.lower()
        return (
            any(marker in text for marker in teaching_markers_thai) or
            any(marker in text_lower for marker in teaching_markers_english)
        )


if __name__ == "__main__":
    # Test extraction
    extractor = SemanticExtractor()
    
    test_text = """ชื่อของสิ่งนี้คือ ลูม่า
ลูม่าคือสัตว์สมมติที่ชอบนอนบนต้นไม้ตอนกลางวัน
และออกหาอาหารในเวลากลางคืน"""
    
    facts = extractor.extract_facts(test_text)
    print(f"Extracted {len(facts)} facts:")
    for fact in facts:
        print(f"  - {fact.subject} {fact.predicate} {fact.object}")
