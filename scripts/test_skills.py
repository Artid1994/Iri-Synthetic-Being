#!/usr/bin/env python3
"""
Test Iri Skills Integration
Quick test of system inspector and text analyzer skills.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "03_Hippocampus"))
sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))

from skills import get_system_inspector, get_text_analyzer

print("=== Testing Iri Skills ===\n")

# Test 1: System Inspector
print("1. System Inspector Test")
print("-" * 60)
inspector = get_system_inspector()
inspection = inspector.inspect_all()
report = inspector.format_report(inspection)
print(report)
print("\n")

# Test 2: Text Analyzer
print("2. Text Analyzer Test")
print("-" * 60)
analyzer = get_text_analyzer()

test_commands = [
    "วิเคราะห์ โปรเจกต์",
    "ตรวจสอบ ระบบ",
    "แสดง Git",
]

for cmd in test_commands:
    analysis = analyzer.analyze(cmd)
    skill_cmd = analyzer.extract_skill_commands(cmd)
    
    print(f"Command: '{cmd}'")
    print(f"  Action: {analysis['action']['thai']} → {analysis['action']['english']}")
    print(f"  Target: {analysis['target']['thai']} → {analysis['target']['english']}")
    
    if skill_cmd:
        print(f"  ✓ Mapped to: {skill_cmd['skill']}.{skill_cmd['method']}")
    else:
        print("  ✗ No skill mapping")
    print()

print("=" * 60)
print("✓ All tests completed")
