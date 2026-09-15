"""
Semantic Response Generator
Generates responses based on semantic understanding.

Uses semantic context from cognitive processing to generate appropriate responses.
"""
from __future__ import annotations
from typing import Optional, Dict, List


class SemanticResponseGenerator:
    """
    Generate responses using semantic understanding.
    
    Takes semantic context from cognitive processing and generates
    appropriate Thai responses based on understood meaning.
    """
    
    def __init__(self):
        self.response_templates = self._load_response_templates()
    
    def generate_response(
        self,
        semantic_context: Optional[str],
        user_input: str,
        cognitive_reasoning: str
    ) -> str:
        """
        Generate response based on semantic understanding.
        
        Args:
            semantic_context: Semantic understanding from bridge
            user_input: Original user input
            cognitive_reasoning: Reasoning from cognitive engine
            
        Returns:
            Response text (Thai if input was Thai, English otherwise)
        """
        if not semantic_context:
            # No semantic understanding, generic response
            return "I heard you."
        
        # Check if Thai input
        if 'Thai understood' in semantic_context:
            return self._generate_thai_response(semantic_context, user_input)
        else:
            return self._generate_english_response(semantic_context, user_input)
    
    def _generate_thai_response(self, semantic_context: str, user_input: str) -> str:
        """Generate Thai response based on semantic understanding."""
        
        # Extract understood words from context
        understood_words = self._extract_understood_words(semantic_context)
        
        # Pattern-based responses
        if 'สวัสดี' in understood_words:
            # Greeting detected
            if 'ครับ' in understood_words:
                return 'สวัสดี ครับ'
            elif 'ค่ะ' in understood_words:
                return 'สวัสดี ค่ะ'
            else:
                return 'สวัสดี'
        
        if 'ขอบคุณ' in understood_words:
            # Thanks detected
            if 'ครับ' in understood_words:
                return 'ยินดี ครับ'
            elif 'ค่ะ' in understood_words:
                return 'ยินดี ค่ะ'
            else:
                return 'ยินดี'
        
        # NEW: Answer questions meaningfully based on semantic understanding
        # Question pattern: คุณ ชื่อ อะไร (What is your name?)
        if 'ชื่อ' in understood_words and 'อะไร' in understood_words and 'คุณ' in understood_words:
            polite = 'ครับ' if 'ครับ' in understood_words else 'ค่ะ' if 'ค่ะ' in understood_words else ''
            # Answer with name
            if polite:
                return f'ผม ชื่อ ไอริ {polite}'
            return 'ผม ชื่อ ไอริ'
        
        # Question pattern: คุณ เป็น ใคร (Who are you?)
        if 'เป็น' in understood_words and ('ใคร' in user_input or 'อะไร' in understood_words):
            polite = 'ครับ' if 'ครับ' in understood_words else 'ค่ะ' if 'ค่ะ' in understood_words else ''
            # Answer with identity
            if 'คุณ' in understood_words:
                if polite:
                    return f'ผม ชื่อ ไอริ {polite}'
                return 'ผม ชื่อ ไอริ'
        
        # Question pattern: ไป ที่ไหน (Go where? / Where are you going?)
        if 'ไป' in understood_words and 'ที่ไหน' in understood_words:
            polite = 'ครับ' if 'ครับ' in understood_words else 'ค่ะ' if 'ค่ะ' in understood_words else ''
            # Context-dependent answer
            if 'คุณ' in understood_words:
                # Asking about IRI
                if polite:
                    return f'ผม อยู่ ที่นี่ {polite}'  # I'm staying here
                return 'ผม อยู่ ที่นี่'
            else:
                # General question - ask back or acknowledge
                if polite:
                    return f'คุณ จะ ไป ที่ไหน {polite}'
                return 'คุณ จะ ไป ที่ไหน'
        
        # Statement about liking/wanting
        if 'ชอบ' in understood_words or 'รัก' in understood_words:
            polite = 'ครับ' if 'ครับ' in understood_words else 'ค่ะ' if 'ค่ะ' in understood_words else ''
            # Acknowledge preference
            if polite:
                return f'ดี มาก {polite}'
            return 'ดี มาก'
        
        # Name introduction pattern
        if 'ชื่อ' in understood_words and ('ผม' in understood_words or 'ดิฉัน' in understood_words):
            polite = 'ครับ' if 'ครับ' in understood_words else 'ค่ะ' if 'ค่ะ' in understood_words else ''
            if polite:
                return f'ยินดี ที่ ได้ รู้จัก {polite}'
            return 'ยินดี ที่ ได้ รู้จัก'
        
        # Question detected but no specific pattern - acknowledge meaningfully
        if 'อะไร' in understood_words or 'ที่ไหน' in understood_words or 'ทำไม' in understood_words or 'ไหม' in understood_words:
            polite_marker = 'ครับ' if 'ครับ' in understood_words else 'ค่ะ' if 'ค่ะ' in understood_words else ''
            if polite_marker:
                return f'เข้าใจ คำถาม {polite_marker}'
            else:
                return 'เข้าใจ คำถาม'
        
        # General acknowledgment with politeness
        if 'ครับ' in understood_words:
            return 'เข้าใจ ครับ'
        elif 'ค่ะ' in understood_words:
            return 'เข้าใจ ค่ะ'
        else:
            return 'เข้าใจ'
    
    def _generate_english_response(self, semantic_context: str, user_input: str) -> str:
        """Generate English response."""
        # Check if semantic context indicates understanding
        if "understood" in semantic_context.lower():
            # Simple acknowledgment for understood input
            return "I understand."
        
        # Default acknowledgment
        return "I heard you."
    
    def _extract_understood_words(self, semantic_context: str) -> Dict[str, str]:
        """
        Extract understood words from semantic context.
        
        Returns dict mapping Thai word to meaning.
        """
        understood = {}
        
        if 'Thai understood:' in semantic_context:
            # Parse: "Thai understood: word1=meaning1, word2=meaning2 | ..."
            parts = semantic_context.split('Thai understood: ')
            if len(parts) > 1:
                word_section = parts[1].split(' | ')[0]
                word_pairs = word_section.split(', ')
                
                for pair in word_pairs:
                    if '=' in pair:
                        word, meaning = pair.split('=', 1)
                        understood[word.strip()] = meaning.strip()
        
        return understood
    
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load response templates (placeholder for future expansion)."""
        return {
            'greeting': ['สวัสดี', 'Hello'],
            'thanks': ['ยินดี', 'You\'re welcome'],
            'acknowledgment': ['เข้าใจ', 'I understand'],
        }
