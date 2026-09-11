#!/usr/bin/env python3
"""
Test Thai Intent Variations
Test all variations of system status queries.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "03_Hippocampus"))
sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))

from skills import get_text_analyzer

print("=" * 70)
print("Thai Intent Mapping - Variation Test")
print("=" * 70)
print()

analyzer = get_text_analyzer()

# Test all variations
test_inputs = [
    "ตรวจสภาพ เครื่อง",
    "ตรวจสภาพเครื่อง",
    "ตรวจสภาพ",
    "สภาพเครื่อง",
    "ตรวจสอบระบบ",
    "ตรวจระบบ",
    "ระบบเป็นไงบ้าง",
    "สถานะระบบ",
    "สถานะเครื่อง",
    "รายงานระบบ",
    "รายงานผล",
    "วิเคราะห์ ระบบ",
    "ตรวจดู ระบบ"
]

print(f"Testing {len(test_inputs)} input variations:\n")

success_count = 0
fail_count = 0

for text in test_inputs:
    skill_cmd = analyzer.extract_skill_commands(text)
    
    if skill_cmd:
        status = "✓"
        success_count += 1
        result = f"{skill_cmd['skill']}.{skill_cmd['method']}"
    else:
        status = "✗"
        fail_count += 1
        result = "NOT MAPPED"
    
    print(f"{status} '{text}'")
    print(f"   → {result}")
    print()

print("=" * 70)
print(f"Results: {success_count} success, {fail_count} failed")
print("=" * 70)

if fail_count == 0:
    print("✓ ALL TESTS PASSED")
    sys.exit(0)
else:
    print(f"✗ {fail_count} tests failed")
    sys.exit(1)
