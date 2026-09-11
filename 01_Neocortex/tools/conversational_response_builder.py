"""
Conversational Response Builder - Dynamic natural language generation
Replaces static templates with adaptive phrasing for natural conversation.
"""

import random
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ResponseContext:
    """Context for response generation."""
    intent_type: str
    formality: str  # 'polite', 'casual', 'neutral'
    language: str  # 'th', 'en', 'mixed'
    topic: Optional[str] = None
    facts: Optional[List[str]] = None
    emotion: str = 'neutral'  # 'happy', 'neutral', 'concerned'


class ConversationalResponseBuilder:
    """Build natural, adaptive responses with bilingual support."""
    
    def __init__(self):
        # Response templates by intent and formality
        self.templates = {
            'greeting': {
                'polite_th': [
                    'สวัสดีครับเจ้านาย ผมไอริพร้อมรับคำสั่งครับ',
                    'ยินดีต้อนรับครับเจ้านาย มีอะไรให้ช่วยไหมครับ',
                    'สวัสดีครับ ผมพร้อมช่วยเหลือเจ้านายแล้วครับ'
                ],
                'casual_th': [
                    'หวัดดีครับ มีอะไรให้ช่วยไหมครับ',
                    'สวัสดีครับ พร้อมช่วยเหลือเลยครับ'
                ],
                'polite_en': [
                    'Hello, I am Iri. How may I assist you?',
                    'Welcome. What can I help you with today?'
                ]
            },
            'status': {
                'polite_th': [
                    'ระบบทำงานปกติครับเจ้านาย {details}',
                    'สถานะระบบดีครับ {details}',
                    'ทุกอย่างเป็นปกติครับเจ้านาย {details}'
                ],
                'casual_th': [
                    'ระบบโอเคครับ {details}',
                    'ทุกอย่างปกติดีครับ {details}'
                ]
            },
            'command_ack': {
                'polite_th': [
                    'รับทราบครับเจ้านาย กำลังดำเนินการครับ',
                    'ครับเจ้านาย ผมจะดำเนินการทันทีครับ',
                    'เข้าใจแล้วครับ กำลังทำตามคำสั่งครับ'
                ],
                'casual_th': [
                    'เข้าใจแล้วครับ กำลังทำให้เลยครับ',
                    'โอเคครับ ทำทันทีเลยครับ'
                ]
            },
            'info_response': {
                'polite_th': [
                    '{info} ครับเจ้านาย',
                    'ผมพบว่า {info} ครับ',
                    'จากข้อมูลที่ผมรู้ {info} ครับเจ้านาย'
                ],
                'casual_th': [
                    '{info} ครับ',
                    'ผมรู้ว่า {info} ครับ'
                ]
            },
            'error': {
                'polite_th': [
                    'ขออภัยครับเจ้านาย เกิดข้อผิดพลาดครับ',
                    'ผมขออภัยครับ ไม่สามารถดำเนินการได้ครับ'
                ],
                'casual_th': [
                    'ขอโทษครับ เกิดปัญหานิดหน่อยครับ'
                ]
            }
        }
        
        # Connectors for natural flow
        self.connectors_th = {
            'addition': ['นอกจากนี้', 'และยังมี', 'อีกทั้ง'],
            'contrast': ['แต่', 'อย่างไรก็ตาม', 'ในทางกลับกัน'],
            'result': ['ดังนั้น', 'เพราะฉะนั้น', 'จึง']
        }
    
    def build_response(self, context: ResponseContext, data: Dict = None) -> str:
        """
        Build natural conversational response based on context.
        Returns formatted response text.
        """
        if data is None:
            data = {}
        
        # Select template category
        if context.intent_type == 'greeting':
            return self._build_greeting(context)
        elif context.intent_type == 'status':
            return self._build_status_response(context, data)
        elif context.intent_type == 'command':
            return self._build_command_acknowledgment(context, data)
        elif context.intent_type == 'question':
            return self._build_info_response(context, data)
        else:
            return self._build_generic_response(context, data)
    
    def _build_greeting(self, context: ResponseContext) -> str:
        """Build greeting response."""
        key = f"{context.formality}_{context.language}"
        if key not in self.templates['greeting']:
            key = 'polite_th'  # Default
        
        return random.choice(self.templates['greeting'][key])
    
    def _build_status_response(self, context: ResponseContext, data: Dict) -> str:
        """Build system status response."""
        # Extract status details
        memory = data.get('memory', 'N/A')
        cpu = data.get('cpu', 'N/A')
        
        details = f"มีหน่วยความจำ {memory} และใช้ CPU {cpu}"
        
        key = f"{context.formality}_th"
        if key not in self.templates['status']:
            key = 'polite_th'
        
        template = random.choice(self.templates['status'][key])
        return template.format(details=details)
    
    def _build_command_acknowledgment(self, context: ResponseContext, data: Dict) -> str:
        """Build command acknowledgment."""
        key = f"{context.formality}_th"
        if key not in self.templates['command_ack']:
            key = 'polite_th'
        
        return random.choice(self.templates['command_ack'][key])
    
    def _build_info_response(self, context: ResponseContext, data: Dict) -> str:
        """Build informational response with facts."""
        info = data.get('info', 'ผมไม่พบข้อมูลที่เกี่ยวข้อง')
        
        key = f"{context.formality}_th"
        if key not in self.templates['info_response']:
            key = 'polite_th'
        
        template = random.choice(self.templates['info_response'][key])
        return template.format(info=info)
    
    def _build_generic_response(self, context: ResponseContext, data: Dict) -> str:
        """Build generic response."""
        text = data.get('text', '')
        
        # Add polite suffix
        if context.formality == 'polite' and context.language in ['th', 'mixed']:
            if not text.endswith('ครับ') and not text.endswith('ค่ะ'):
                text += ' ครับ'
        
        return text
    
    def add_emotion(self, text: str, emotion: str, language: str = 'th') -> str:
        """Add emotional tone to response."""
        if emotion == 'happy' and language == 'th':
            # Add enthusiasm
            if not text.endswith('!'):
                text = text.rstrip('ครับค่ะ') + ' เลยครับ!'
        
        elif emotion == 'concerned' and language == 'th':
            # Add concern markers
            text = 'ผมกังวลว่า ' + text
        
        return text
    
    def create_multi_sentence_response(self, sentences: List[str], context: ResponseContext) -> str:
        """Combine multiple sentences with natural connectors."""
        if len(sentences) <= 1:
            return sentences[0] if sentences else ""
        
        result = [sentences[0]]
        
        for i, sentence in enumerate(sentences[1:], 1):
            # Add connector
            if i == len(sentences) - 1:
                # Last sentence
                connector = random.choice(self.connectors_th.get('result', ['และ']))
            else:
                connector = random.choice(self.connectors_th.get('addition', ['และ']))
            
            result.append(f"{connector}{sentence}")
        
        return ' '.join(result)
