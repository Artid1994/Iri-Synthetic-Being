#!/usr/bin/env python3
"""
Test Iri Chat Skills Integration
Dry-run test of system inspection command.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "01_Neocortex"))
sys.path.insert(0, str(PROJECT_ROOT / "03_Hippocampus"))
sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))

from executive_core import KnowledgeGraph, Intent
from memory_store import HippocampusMemory
from core_directives import CoreDirectives
from nlp_thai_lexicon import get_thai_lexicon
from skills import get_system_inspector, get_text_analyzer

class IriChatTest:
    """Simplified IriChat for testing."""
    
    def __init__(self):
        self.thai_lexicon = get_thai_lexicon()
        self.system_inspector = get_system_inspector()
        self.text_analyzer = get_text_analyzer()
    
    def classify_input(self, user_input: str) -> Intent:
        """Classify user input intent."""
        # Check for system inspection keywords
        system_keywords = ['ตรวจสอบ', 'สถานะ', 'ระบบ', 'รายงาน', 'วิเคราะห์', 'ตรวจสภาพ']
        if any(keyword in user_input for keyword in system_keywords):
            skill_command = self.text_analyzer.extract_skill_commands(user_input)
            if skill_command:
                return Intent(
                    type='skill',
                    confidence=1.0,
                    entities=[skill_command['skill'], skill_command['method']]
                )
            return Intent(
                type='skill',
                confidence=0.9,
                entities=['system_inspector', 'inspect_all']
            )
        
        return Intent(type='statement', confidence=0.6, entities=[])
    
    def execute_skill(self, intent: Intent) -> str:
        """Execute skill command."""
        if len(intent.entities) < 2:
            return "ขออภัยครับเจ้านาย ระบุสกิลไม่ครบถ้วนครับ"
        
        skill_name = intent.entities[0]
        method_name = intent.entities[1]
        
        if skill_name == 'system_inspector' and method_name == 'inspect_all':
            inspection = self.system_inspector.inspect_all()
            report = self.system_inspector.format_report(inspection)
            return f"รับทราบคำสั่งครับเจ้านาย กำลังตรวจสอบระบบของไอริ...\n\n{report}"
        
        return "ยังไม่รองรับคำสั่งนี้ครับ"

# Test
print("=" * 70)
print("Iri Chat Skills Integration - Dry Run Test")
print("=" * 70)
print()

chat = IriChatTest()

test_input = "ตรวจสอบระบบของไอริ แล้วรายงานผลโดยสรุป"
print(f"User: {test_input}")
print()

intent = chat.classify_input(test_input)
print(f"Detected Intent: {intent.type}")
print(f"Confidence: {intent.confidence}")
print(f"Entities: {intent.entities}")
print()

if intent.type == 'skill':
    response = chat.execute_skill(intent)
    print(f"Iri Response:")
    print(response)
else:
    print("⚠️  Intent not recognized as skill command")

print()
print("=" * 70)
