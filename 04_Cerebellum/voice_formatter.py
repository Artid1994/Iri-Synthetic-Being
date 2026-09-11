#!/usr/bin/env python3
"""
Voice Output Formatter for AE01M
Ensures honorifics match active TTS voice gender and natural dialogue flow.
"""
import re
from pathlib import Path


class VoiceFormatter:
    """
    Format Thai text output to match TTS voice gender and natural conversation style.
    """
    
    # Voice gender mapping
    MALE_VOICES = ["th-TH-NiwatNeural"]
    FEMALE_VOICES = ["th-TH-PremwadeeNeural"]
    
    # Honorific patterns
    FEMALE_HONORIFICS = ["ค่ะ", "คะ", "ค่า", "คะ"]
    MALE_HONORIFIC = "ครับ"
    
    # Master addressing keywords that trigger "เจ้านาย"
    MASTER_CONTEXTS = [
        r'สวัสดี',      # Greetings
        r'พร้อม',       # Readiness statements
        r'รับทราบ',     # Acknowledgments
        r'เสร็จ',       # Completion reports
        r'ทำเรียบร้อย', # Status confirmations
    ]
    
    def __init__(self, voice_name: str = "th-TH-NiwatNeural"):
        self.voice_name = voice_name
        self.is_male_voice = voice_name in self.MALE_VOICES
        self.is_female_voice = voice_name in self.FEMALE_VOICES
    
    def format_response(self, text: str, include_master: bool = None) -> str:
        """
        Format response text to match voice gender and natural dialogue.
        
        Args:
            text: Raw response text
            include_master: Override master addressing (None = auto-detect)
        
        Returns:
            Formatted text with correct honorifics
        """
        if not text or not text.strip():
            return text
        
        # Step 1: Fix honorifics to match voice gender
        text = self._fix_honorifics(text)
        
        # Step 2: Manage "เจ้านาย" usage (contextual)
        if include_master is None:
            include_master = self._should_include_master(text)
        
        if not include_master:
            # Remove excessive "เจ้านาย" for natural flow
            text = re.sub(r'เจ้านาย\s*', '', text)
        
        return text.strip()
    
    def _fix_honorifics(self, text: str) -> str:
        """Replace honorifics to match voice gender."""
        if self.is_male_voice:
            # Replace all female honorifics with male "ครับ"
            for fem in self.FEMALE_HONORIFICS:
                text = re.sub(fem, self.MALE_HONORIFIC, text)
        elif self.is_female_voice:
            # Replace male honorific with female "ค่ะ"
            text = re.sub(r'ครับ', 'ค่ะ', text)
        
        return text
    
    def _should_include_master(self, text: str) -> bool:
        """
        Determine if "เจ้านาย" should be included based on context.
        
        Include in: greetings, status reports, formal confirmations
        Omit in: casual conversation, continuous dialogue
        """
        # Check if text matches master-addressing contexts
        for pattern in self.MASTER_CONTEXTS:
            if re.search(pattern, text):
                return True
        
        # If "เจ้านาย" already present, keep it
        if 'เจ้านาย' in text:
            return True
        
        # Default: omit for natural conversation
        return False
    
    def add_master_address(self, text: str) -> str:
        """Add appropriate master address to text."""
        if 'เจ้านาย' not in text:
            # Add at appropriate position (after greeting if present)
            if re.search(r'สวัสดี', text):
                text = re.sub(r'(สวัสดี[ค่ะครับคะ]*)', r'\1เจ้านาย', text, count=1)
            else:
                # Add before first honorific
                honorific = self.MALE_HONORIFIC if self.is_male_voice else 'ค่ะ'
                text = re.sub(f'({honorific})', r'เจ้านาย\1', text, count=1)
        
        return text


# Global formatter instance (updated when voice changes)
_formatter = VoiceFormatter(voice_name="th-TH-NiwatNeural")


def set_voice(voice_name: str):
    """Update global formatter for new voice."""
    global _formatter
    _formatter = VoiceFormatter(voice_name=voice_name)


def format_output(text: str, include_master: bool = None) -> str:
    """Format text output for current TTS voice."""
    return _formatter.format_response(text, include_master=include_master)


if __name__ == "__main__":
    # Test examples
    test_cases = [
        ("สวัสดีค่ะ พร้อมรับใช้เจ้านายค่ะ", "th-TH-NiwatNeural"),
        ("เข้าใจแล้วค่ะ", "th-TH-NiwatNeural"),
        ("ดิฉันชื่อไอริค่ะ", "th-TH-NiwatNeural"),
        ("พร้อมรับใช้เจ้านายครับ", "th-TH-PremwadeeNeural"),
    ]
    
    for text, voice in test_cases:
        formatter = VoiceFormatter(voice)
        result = formatter.format_response(text)
        print(f"Voice: {voice}")
        print(f"Input:  {text}")
        print(f"Output: {result}")
        print()
