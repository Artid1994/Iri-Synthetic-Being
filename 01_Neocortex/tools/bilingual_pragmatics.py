"""
Bilingual Pragmatic Parser - Advanced intent & context handling
Handles Thai-English code-switching, slang, particles, and modal phrasing.
"""

import re
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass


@dataclass
class ParsedIntent:
    """Parsed intent with cleaned text and metadata."""
    intent_type: str  # 'question', 'command', 'statement', 'greeting', 'casual'
    clean_text: str  # Cleaned, normalized text
    original_text: str
    language: str  # 'th', 'en', 'mixed'
    formality: str  # 'formal', 'casual', 'polite'
    keywords: List[str]
    entities: Dict[str, str]
    confidence: float


class BilingualPragmaticParser:
    """Advanced parser for Thai-English code-switching and pragmatics."""
    
    def __init__(self):
        # Thai sentence-final particles
        self.th_particles = {
            'ครับ': 'polite_male',
            'ค่ะ': 'polite_female',
            'คะ': 'polite_female_question',
            'นะ': 'casual_softener',
            'เลย': 'emphasis',
            'จ้า': 'cute_casual',
            'จ๊ะ': 'cute_casual',
            'เน้อ': 'casual_softener',
            'วะ': 'very_casual',
            'สิ': 'imperative_softener'
        }
        
        # Thai-English common code-switches
        self.code_switch_patterns = {
            'check': 'ตรวจสอบ',
            'status': 'สถานะ',
            'system': 'ระบบ',
            'memory': 'หน่วยความจำ',
            'help': 'ช่วย',
            'update': 'อัปเดต',
            'search': 'ค้นหา',
            'show': 'แสดง',
            'list': 'รายการ'
        }
        
        # Intent keywords
        self.intent_keywords = {
            'question': ['ไหม', 'อะไร', 'ยังไง', 'ที่ไหน', 'เมื่อไหร่', 'ทำไม', 'what', 'how', 'where', 'when', 'why', 'who'],
            'command': ['ช่วย', 'ทำ', 'เริ่ม', 'หยุด', 'เปิด', 'ปิด', 'ลบ', 'แก้', 'check', 'start', 'stop', 'delete', 'fix', 'run'],
            'greeting': ['สวัสดี', 'หวัดดี', 'ว่าไง', 'hello', 'hi', 'hey'],
            'status': ['สถานะ', 'เป็นอย่างไร', 'เป็นไง', 'status', 'how are you'],
        }
    
    def parse(self, text: str) -> ParsedIntent:
        """
        Parse input text with bilingual pragmatic understanding.
        Returns structured intent with cleaned text.
        """
        original = text
        
        # Detect language
        language = self._detect_language(text)
        
        # Extract and remove particles
        text, formality = self._extract_particles(text)
        
        # Normalize code-switching
        text = self._normalize_code_switching(text)
        
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Classify intent
        intent_type = self._classify_intent(text)
        
        # Extract keywords and entities
        keywords = self._extract_keywords(text)
        entities = self._extract_entities(text)
        
        # Calculate confidence
        confidence = self._calculate_confidence(text, intent_type)
        
        return ParsedIntent(
            intent_type=intent_type,
            clean_text=text,
            original_text=original,
            language=language,
            formality=formality,
            keywords=keywords,
            entities=entities,
            confidence=confidence
        )
    
    def _detect_language(self, text: str) -> str:
        """Detect primary language: 'th', 'en', or 'mixed'."""
        thai_chars = sum(1 for c in text if '\u0e00' <= c <= '\u0e7f')
        english_chars = sum(1 for c in text if c.isalpha() and c.isascii())
        
        if thai_chars == 0 and english_chars > 0:
            return 'en'
        elif english_chars == 0 and thai_chars > 0:
            return 'th'
        else:
            return 'mixed'
    
    def _extract_particles(self, text: str) -> Tuple[str, str]:
        """Extract Thai particles and determine formality."""
        formality = 'neutral'
        
        for particle, style in self.th_particles.items():
            if text.endswith(particle):
                text = text[:-len(particle)].strip()
                
                if 'polite' in style:
                    formality = 'polite'
                elif 'casual' in style:
                    formality = 'casual'
                
                break
        
        return text, formality
    
    def _normalize_code_switching(self, text: str) -> str:
        """Normalize Thai-English code-switching to standard forms."""
        # Keep English technical terms, normalize common switches
        for en, th in self.code_switch_patterns.items():
            # Replace only whole words
            text = re.sub(r'\b' + en + r'\b', en, text, flags=re.IGNORECASE)
        
        return text
    
    def _classify_intent(self, text: str) -> str:
        """Classify intent type based on keywords and structure."""
        text_lower = text.lower()
        
        # Check for greetings
        if any(kw in text_lower for kw in self.intent_keywords['greeting']):
            return 'greeting'
        
        # Check for questions (Thai: ends with ไหม, มั้ย, or question words)
        if text.endswith('ไหม') or text.endswith('มั้ย') or text.endswith('?'):
            return 'question'
        
        if any(kw in text_lower for kw in self.intent_keywords['question']):
            return 'question'
        
        # Check for commands
        if any(kw in text_lower for kw in self.intent_keywords['command']):
            return 'command'
        
        # Check for status queries
        if any(kw in text_lower for kw in self.intent_keywords['status']):
            return 'status'
        
        # Default: statement
        return 'statement'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Simple word extraction (can be enhanced with NLP)
        words = text.split()
        
        # Filter out particles and common words
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'และ', 'ที่', 'นี้', 'นั้น'}
        keywords = [w for w in words if len(w) > 2 and w.lower() not in stopwords]
        
        return keywords[:5]  # Top 5 keywords
    
    def _extract_entities(self, text: str) -> Dict[str, str]:
        """Extract named entities (simple pattern-based)."""
        entities = {}
        
        # System components
        if re.search(r'(system|ระบบ)', text, re.IGNORECASE):
            entities['component'] = 'system'
        
        if re.search(r'(memory|หน่วยความจำ)', text, re.IGNORECASE):
            entities['component'] = 'memory'
        
        # Numbers
        numbers = re.findall(r'\d+', text)
        if numbers:
            entities['number'] = numbers[0]
        
        return entities
    
    def _calculate_confidence(self, text: str, intent_type: str) -> float:
        """Calculate parsing confidence score."""
        confidence = 0.8  # Base confidence
        
        # Boost for clear intent markers
        if intent_type in ['greeting', 'command', 'question']:
            confidence += 0.1
        
        # Reduce for very short text
        if len(text) < 5:
            confidence -= 0.2
        
        return min(max(confidence, 0.5), 1.0)
