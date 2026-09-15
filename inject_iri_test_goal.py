import json
import time
from pathlib import Path

goals_path = Path("03_Hippocampus/goals.json")

# 1. โหลดข้อมูลเป้าหมายเดิม
with open(goals_path, "r", encoding="utf-8") as f:
    goals = json.load(f)

# 2. สร้างเป้าหมายใหม่สำหรับทดสอบกล้ามเนื้อ Cerebellum (WRITE_FILE)
test_goal = {
    "id": "test_c4_op",
    "title": "Generate automated journal on debian screen check",
    "description": "Iri writes a local sensory file down to the logs directory when triggered.",
    "priority": "medium",  # เริ่มจาก medium เพื่อให้กลไก Plasticity ปรับเป็น high เองตอนสแกนเจอคำว่า debian หรือ screen
    "status": "pending",
    "created_at": time.time(),
    "updated_at": time.time(),
    "subtasks": [
        {
            "id": "sub_c4_01",
            "title": "Create Curiosity Reflection Log",
            "type": "file_operation",
            "command": "WRITE_FILE:logs/iri_curiosity_journal.txt:--- IRI SYNTHETIC BEING JOURNAL ---\nStatus: Active and Living inside Debian 13.\nPerception State: Core loop execution success.\nPlasticity: Synaptic weight updated according to Boss Artid's screen activity.",
            "estimated_duration": 5,
            "status": "pending",
            "safety_checks": ["DIRECTIVE_1", "DIRECTIVE_2"]
        }
    ]
}

# 3. แทรกไว้บนสุดของคิวงาน
goals.insert(0, test_goal)

# 4. บันทึกคืนลงไฟล์
with open(goals_path, "w", encoding="utf-8") as f:
    json.dump(goals, f, ensure_ascii=False, indent=2)

print("[Injection] Successfully injected Cerebellum Test Goal into goals.json!")
