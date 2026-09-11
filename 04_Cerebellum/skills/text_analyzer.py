#!/usr/bin/env python3
"""
Text Analyzer Skill
Autonomous Thai text analysis using PyThaiNLP lexicon and Thai-NER.
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "03_Hippocampus"))

from nlp_thai_lexicon import get_thai_lexicon


class TextAnalyzer:
    """Analyze Thai text for entities, intent, and sentiment."""
    
    def __init__(self):
        self.lexicon = get_thai_lexicon()
        
        # Command mappings (Thai → English action)
        self.command_map = {
            "วิเคราะห์": "analyze",
            "ตรวจสอบ": "check",
            "ตรวจ": "check",
            "ตรวจสภาพ": "inspect",
            "ตรวจดู": "inspect",
            "แสดง": "show",
            "ค้นหา": "search",
            "เปิด": "open",
            "ปิด": "close",
            "เริ่ม": "start",
            "หยุด": "stop",
            "บันทึก": "save",
            "ลบ": "delete",
            "สร้าง": "create",
            "แก้ไข": "edit",
            "รายงาน": "report",
            "สถานะ": "status",
            "สภาพ": "status"
        }
        
        # Target mappings (Thai → English)
        self.target_map = {
            "โปรเจกต์": "project",
            "ระบบ": "system",
            "เครื่อง": "machine",
            "คอมพิวเตอร์": "computer",
            "ไฟล์": "file",
            "ข้อมูล": "data",
            "หน่วยความจำ": "memory",
            "CPU": "cpu",
            "ดิสก์": "disk",
            "Git": "git",
            "โค้ด": "code",
            "ผล": "result"
        }
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze Thai text and extract structured information.
        Returns action, target, entities, and confidence.
        """
        # Use lexicon for basic intent extraction
        intent = self.lexicon.extract_intent(text)
        
        # Translate action to English
        action_thai = intent.get('action', 'unknown')
        action_english = self.command_map.get(action_thai, action_thai)
        
        # Translate target to English
        target_thai = intent.get('target', '')
        target_english = self.target_map.get(target_thai, target_thai)
        
        # Enhanced analysis
        result = {
            "text": text,
            "expanded_text": intent.get('expanded_text', text),
            "action": {
                "thai": action_thai,
                "english": action_english
            },
            "target": {
                "thai": target_thai,
                "english": target_english
            },
            "entities": intent.get('entities', {}),
            "confidence": intent.get('confidence', 0.0),
            "is_command": action_english != 'unknown' and intent.get('confidence', 0) > 0.5,
            "is_question": self._is_question(text),
            "sentiment": self._analyze_sentiment(text)
        }
        
        return result
    
    def _is_question(self, text: str) -> bool:
        """Detect if text is a question."""
        question_markers = [
            '?', 'ไหม', 'หรือ', 'อะไร', 'ทำไม', 'อย่างไร', 
            'เมื่อไหร่', 'ที่ไหน', 'ใคร', 'เท่าไร'
        ]
        return any(marker in text for marker in question_markers)
    
    def _analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis."""
        # Positive indicators
        positive_words = ['ดี', 'เยี่ยม', 'สุดยอด', 'ชอบ', 'รัก', 'สวย', 'เก่ง', 'ขอบคุณ']
        # Negative indicators
        negative_words = ['แย่', 'เสีย', 'ไม่ดี', 'ไม่ชอบ', 'เกลียด', 'ผิด', 'เสียใจ', 'ขอโทษ']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def extract_skill_commands(self, text: str) -> Optional[Dict[str, str]]:
        """
        Extract skill command from Thai text.
        Returns None if not a skill command, or dict with skill name and parameters.
        """
        # Handle compound phrases first (before tokenization)
        compound_mappings = {
            'ตรวจสภาพเครื่อง': {'skill': 'system_inspector', 'method': 'inspect_system'},
            'ตรวจสภาพ เครื่อง': {'skill': 'system_inspector', 'method': 'inspect_system'},
            'สภาพเครื่อง': {'skill': 'system_inspector', 'method': 'inspect_system'},
            'ตรวจสอบระบบ': {'skill': 'system_inspector', 'method': 'inspect_all'},
            'ตรวจระบบ': {'skill': 'system_inspector', 'method': 'inspect_all'},
            'ตรวจดูระบบ': {'skill': 'system_inspector', 'method': 'inspect_all'},
            'ตรวจดู ระบบ': {'skill': 'system_inspector', 'method': 'inspect_all'},
            'ระบบเป็นไงบ้าง': {'skill': 'system_inspector', 'method': 'inspect_all'},
            'ระบบเป็นยังไงบ้าง': {'skill': 'system_inspector', 'method': 'inspect_all'},
            'สถานะระบบ': {'skill': 'system_inspector', 'method': 'inspect_all'},
            'สถานะเครื่อง': {'skill': 'system_inspector', 'method': 'inspect_system'},
            'รายงานระบบ': {'skill': 'system_inspector', 'method': 'inspect_all'},
            'รายงานผล': {'skill': 'system_inspector', 'method': 'inspect_all'},
            'ตรวจสภาพ': {'skill': 'system_inspector', 'method': 'inspect_system'},
        }
        
        # Check for compound phrases
        text_normalized = text.replace(' ', '')  # Remove spaces for compound matching
        for phrase, mapping in compound_mappings.items():
            phrase_normalized = phrase.replace(' ', '')
            if phrase_normalized in text_normalized:
                return mapping
        
        # Fall back to tokenized analysis
        analysis = self.analyze(text)
        
        if not analysis['is_command']:
            return None
        
        action = analysis['action']['english']
        target = analysis['target']['english']
        
        # Map to specific skills
        skill_mappings = {
            ('analyze', 'project'): {'skill': 'system_inspector', 'method': 'inspect_project'},
            ('check', 'project'): {'skill': 'system_inspector', 'method': 'inspect_project'},
            ('inspect', 'project'): {'skill': 'system_inspector', 'method': 'inspect_project'},
            ('analyze', 'system'): {'skill': 'system_inspector', 'method': 'inspect_all'},
            ('check', 'system'): {'skill': 'system_inspector', 'method': 'inspect_system'},
            ('inspect', 'system'): {'skill': 'system_inspector', 'method': 'inspect_system'},
            ('inspect', 'machine'): {'skill': 'system_inspector', 'method': 'inspect_system'},
            ('check', 'machine'): {'skill': 'system_inspector', 'method': 'inspect_system'},
            ('status', 'system'): {'skill': 'system_inspector', 'method': 'inspect_all'},
            ('status', 'machine'): {'skill': 'system_inspector', 'method': 'inspect_system'},
            ('report', 'system'): {'skill': 'system_inspector', 'method': 'inspect_all'},
            ('report', 'result'): {'skill': 'system_inspector', 'method': 'inspect_all'},
            ('show', 'git'): {'skill': 'system_inspector', 'method': 'inspect_git'},
            ('check', 'git'): {'skill': 'system_inspector', 'method': 'inspect_git'},
        }
        
        key = (action, target)
        if key in skill_mappings:
            return skill_mappings[key]
        
        # Default to full inspection if action matches but target is unknown
        if action in ['analyze', 'check', 'inspect', 'status', 'report']:
            return {'skill': 'system_inspector', 'method': 'inspect_all'}
        
        return None
    
    def format_analysis_report(self, analysis: Dict) -> str:
        """Format analysis results as Thai text report."""
        lines = []
        lines.append("=" * 60)
        lines.append("รายงานการวิเคราะห์ข้อความ (Text Analysis Report)")
        lines.append("=" * 60)
        lines.append(f"ข้อความ: {analysis['text']}")
        lines.append("")
        
        lines.append(f"🎯 Action: {analysis['action']['thai']} ({analysis['action']['english']})")
        if analysis['target']['thai']:
            lines.append(f"🎯 Target: {analysis['target']['thai']} ({analysis['target']['english']})")
        lines.append(f"💯 Confidence: {analysis['confidence']:.2%}")
        lines.append("")
        
        lines.append(f"📝 Type:")
        lines.append(f"  Command: {'Yes' if analysis['is_command'] else 'No'}")
        lines.append(f"  Question: {'Yes' if analysis['is_question'] else 'No'}")
        lines.append(f"  Sentiment: {analysis['sentiment']}")
        lines.append("")
        
        if analysis['entities']:
            lines.append("🔍 Entities:")
            for entity_type, entity_list in analysis['entities'].items():
                if entity_list:
                    lines.append(f"  {entity_type}: {', '.join(entity_list)}")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


# Standalone execution for testing
if __name__ == "__main__":
    analyzer = TextAnalyzer()
    
    test_cases = [
        "วิเคราะห์โปรเจกต์",
        "ตรวจสภาพเครื่อง",
        "แสดง สถานะ Git",
        "ตรวจสอบ ระบบ ทั้งหมด",
        "เปิด ไฟ ห้องนอน"
    ]
    
    print("=== Text Analyzer Skill Test ===\n")
    for text in test_cases:
        analysis = analyzer.analyze(text)
        print(f"Text: '{text}'")
        print(f"  Action: {analysis['action']['thai']} → {analysis['action']['english']}")
        print(f"  Target: {analysis['target']['thai']} → {analysis['target']['english']}")
        print(f"  Is Command: {analysis['is_command']}")
        print(f"  Confidence: {analysis['confidence']:.2%}")
        
        skill_cmd = analyzer.extract_skill_commands(text)
        if skill_cmd:
            print(f"  → Skill: {skill_cmd['skill']}.{skill_cmd['method']}")
        print()
