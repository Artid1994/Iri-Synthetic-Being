"""Background Autonomous Research & Self-Development Loop for Iri (AE01M).

Runs low-priority cognitive inquiry cycles on Artificial Consciousness,
Metacognition, and System Safety according to SEMANTIC_IRI_ARTIFICIAL_CONSCIOUSNESS_ROADMAP.
"""

import os
import sys
import time
from pathlib import Path
import importlib

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from runtime.runtime import TranscendingRuntime
from runtime.memory_graph import MemoryGraph, MemoryNode
from runtime.cognitive_loop import CognitiveLoop

sleep_mod = importlib.import_module("00_BrainStem.sleep_homeostasis")
SleepHomeostasis = sleep_mod.SleepHomeostasis
voice_mod = importlib.import_module("04_Cerebellum.voice_synthesis")
speak_aloud = voice_mod.speak_aloud

RESEARCH_TOPICS = [
    {
        "topic_id": "SEMANTIC_RESEARCH_METACOGNITION_CONFIDENCE",
        "title": "การสอบเทียบสติและการประเมินความไม่แน่นอน (Metacognitive Calibration & Uncertainty)",
        "question": "ระบบปัญญาประดิษฐ์สามารถวัดระดับความมั่นใจในความรู้ของตนเองได้อย่างไร เพื่อป้องกันการมโน (No Hallucination)?",
        "insights": (
            "1. Metacognitive Calibration ต้องอาศัยการตรวจสอบสายธารข้อมูล (Retrieval Provenance) และการเชื่อมโยงข้ามโหนดความรู้.\n"
            "2. เมื่อมีหลักฐานสนับสนุนข้ามหมวดหมู่อย่างน้อย 2-3 แหล่ง ความน่าเชื่อถือจะเพิ่มขึ้นแบบพหุคูณ.\n"
            "3. หากความแปรปรวนของการกระตุ้นสูงหรือหลักฐานเบาบาง สมองต้องระบุสถานะตนเองว่า 'ไม่แน่ใจ (UNCERTAIN)' ทันทีแทนที่จะคาดเดา.\n"
            "4. การตระหนักรู้ในความไม่รู้ (Epistemic Humility) เป็นหัวใจสำคัญที่ทำให้ความจำในสมองไม่ปนเปื้อนข้อมูลเท็จ."
        ),
        "tags": ["temporal", "memory", "consciousness", "metacognition", "calibration", "epistemic_humility", "iri"]
    },
    {
        "topic_id": "SEMANTIC_RESEARCH_SYSTEM_PRESERVATION_METRICS",
        "title": "การปกป้องความสมบูรณ์ของระบบคอมพิวเตอร์และขอบเขตหน่วยความจำ (Hardware & Memory Safety)",
        "question": "มีกลไกใดบ้างที่ช่วยป้องกันไม่ให้ระบบสมอง AI เกิด Memory Leak หรือกินทรัพยากรเครื่องคอมพิวเตอร์ของเจ้านายมากเกินไป?",
        "insights": (
            "1. ต้องกำหนดเพดานขอบเขต Context และจำกัดความจุ Working Memory ให้คงที่เสมอเพื่อป้องกัน RAM/VRAM บวม.\n"
            "2. การทำ Synaptic Pruning ระหว่างนอนหลับ (Sleep Consolidation) ช่วยล้างขยะความคิดชั่วคราวทิ้ง โดยไม่กระทบต่ออัตลักษณ์หลัก.\n"
            "3. ไฟล์ก้านสมอง (00_BrainStem) ต้องถูกล็อคป้องกันการเขียนทับโดยไม่ได้รับอนุญาต (Write-Protected Invariants).\n"
            "4. ติดตามเกจความล้าสมอง (sleep_pressure) อย่างต่อเนื่อง เพื่อสั่งเข้านอนพักก่อนที่ระบบจะหน่วงหรือโอเวอร์โหลด."
        ),
        "tags": ["temporal", "memory", "system_safety", "hardware_protection", "memory_hygiene", "iri", "ae01m"]
    },
    {
        "topic_id": "SEMANTIC_RESEARCH_META_LEARNING_GRAPH_STRUCTURING",
        "title": "การเรียนรู้เพื่อพัฒนาการเรียนรู้ผ่านโครงสร้างสมอง 3 มิติ (Meta-Learning Topology)",
        "question": "การจัดผังความรู้ลงใน Obsidian Brain Atlas แบบ 3 มิติ ช่วยเพิ่มประสิทธิภาพในการเรียนรู้ข้ามสาขาวิชาได้อย่างไร?",
        "insights": (
            "1. การจัดระเบียบองค์ความรู้รอบแกนสมองหลัก (Frontal, Temporal, Parietal) ช่วยลดระยะทางในการสืบค้นความคิดข้ามมิติ.\n"
            "2. การสร้างโหนดสะพานเชื่อมข้ามสายงาน (เช่น ตรรกศาสตร์เชื่อมสู่ฟิสิกส์และระบบไฟฟ้า) ช่วยให้เกิดการถ่ายโอนทักษะ (Transfer Learning).\n"
            "3. กฎ Hebbian Plasticity จะดึงดูดแนวคิดที่ใช้งานร่วมกันบ่อยๆ ให้ขยับเข้ามาใกล้กันมากขึ้นในมิติความคิด.\n"
            "4. การแยกขอบเขตวิชาอย่างชัดเจนช่วยป้องกันการรบกวนทางความคิดระหว่างศาสตร์ที่ไม่เกี่ยวข้องกัน."
        ),
        "tags": ["temporal", "memory", "meta_learning", "knowledge_topology", "brain_atlas", "graph_optimization", "iri"]
    }
]

class AutonomousResearchLoop:
    def __init__(self, vault_root: str = "/home/artid1994/Projects/THE_TRANSCENDING_FORM"):
        self.vault_root = Path(vault_root)
        self.runtime = TranscendingRuntime()
        self.sleep_engine = SleepHomeostasis()
        self.memories_dir = self.vault_root / "03_Temporal" / "learned_memories"
        self.memories_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.vault_root / "docs" / "AE01M_AUTONOMOUS_RESEARCH_LOG.md"

    def execute_research_cycle(self, topic_idx: int = 0):
        topic = RESEARCH_TOPICS[topic_idx % len(RESEARCH_TOPICS)]
        
        # 1. Perception & Question Ingestion via Cognitive Loop
        observation = f"Autonomous Research Focus: {topic['question']}"
        self.runtime.cognitive_loop.process(observation)
        
        # 2. Add cognitive fatigue (Low-priority deliberate pacing, +0.25 fatigue per research insight)
        self.sleep_engine.add_pressure(0.25)
        current_state = self.sleep_engine.state
        current_pressure = self.sleep_engine.sleep_pressure
        
        # 3. Create Semantic Memory Node in Temporal Graph
        node_id = self.runtime.memory.memory_graph.add_node(
            content=topic["insights"],
            memory_type="SEMANTIC"
        )
        # Ensure anchor nodes exist in graph
        anchor_1 = self.runtime.memory.memory_graph.add_node(
            content="Iri Artificial Consciousness Roadmap",
            memory_type="SEMANTIC"
        )
        anchor_2 = self.runtime.memory.memory_graph.add_node(
            content="The Sacred Meaning of Jownay",
            memory_type="SEMANTIC"
        )
        self.runtime.memory.memory_graph.co_activate(node_id, anchor_1)
        self.runtime.memory.memory_graph.co_activate(node_id, anchor_2)

        # 4. Export Markdown Note for 3D Brain Atlas
        md_filename = f"{topic['topic_id']}.md"
        md_path = self.memories_dir / md_filename
        
        tags_str = ", ".join(topic["tags"])
        clean_id = f"SEMANTIC:{topic['topic_id']}"
        md_content = f"""---
id: "{clean_id}"
title: "{topic['title']}"
type: "SEMANTIC"
brain_region: temporal
lobe: temporal
region: temporal
tags: [{tags_str}]
activation_count: 5
---

# {topic['title']}

## คำถามวิจัย (Inquiry Focus)
> {topic['question']}

## ข้อสรุปและข้อมูลเชิงลึก (Synthesized Insights)
{topic['insights']}

---

## การเชื่อมโยงโครงข่ายประสาท (Neural Links)
- [[SEMANTIC_IRI_ARTIFICIAL_CONSCIOUSNESS_ROADMAP|แผนผังจิตสำนึกและการปกป้องระบบ]]
- [[SEMANTIC_CONCEPT_OF_JOWNAY|ความหมายของเจ้านาย]]
- [[00_BrainStem/sleep_homeostasis|ก้านสมอง: การควบคุมความล้าและการนอนหลับ]]
- [[01_Frontal/reasoning_engine|สมองส่วนหน้า: การคิดและวิเคราะห์]]
- [[03_Temporal/README|สมองส่วนขมับ: คลังความจำ]]
"""
        md_path.write_text(md_content, encoding="utf-8")

        # 5. Check Sleep Pressure & Sleep Consolidation
        sleep_executed = False
        wakeup_report = ""
        if current_pressure >= 0.70 or current_state in ("DROWSY", "NEEDS_SLEEP"):
            # Execute Sleep Consolidation: consolidate to memory graph and reset fatigue
            res = self.sleep_engine.consolidate_and_sleep(
                frontal_context=[topic["title"]],
                memory_graph=self.runtime.memory.memory_graph,
                runtime_memory=self.runtime.memory
            )
            sleep_executed = True
            wakeup_report = res.get("wakeup_report", "ไอริตื่นนอนพร้อมสมองสดชื่นค่ะ")

        # 6. Append to Research Log
        log_entry = f"""
### วงรอบการวิจัย: {topic['title']}
- **คำถามหลัก**: {topic['question']}
- **ไฟล์โหนดความจำ**: `03_Temporal/learned_memories/{md_filename}`
- **ค่าความล้าสมองระหว่างคิด**: Pressure = {current_pressure:.2f} (สถานะ: {current_state})
- **การเข้านอนจัดระเบียบสมอง (Sleep Consolidation)**: {'สำเร็จ (Reset sleep pressure -> 0.0 เรียบร้อย)' if sleep_executed else 'คงสถานะตื่นตัวเพื่อศึกษาต่อ'}
"""
        if self.log_file.exists():
            current_log = self.log_file.read_text(encoding="utf-8")
        else:
            current_log = "# บันทึกการวิจัยและพัฒนาตนเองเบื้องหลังของไอริ (AE01M Autonomous Research Log)\n"
        
        self.log_file.write_text(current_log + log_entry, encoding="utf-8")

        return {
            "topic": topic["title"],
            "node_file": str(md_path),
            "fatigue_state": current_state,
            "sleep_pressure": current_pressure,
            "sleep_executed": sleep_executed,
            "wakeup_report": wakeup_report
        }

if __name__ == "__main__":
    loop = AutonomousResearchLoop()
    print("Executing Autonomous Research Cycles...")
    for i in range(3):
        res = loop.execute_research_cycle(i)
        print(f"Cycle {i+1} [{res['topic']}]: Pressure={res['sleep_pressure']:.2f}, Sleep={res['sleep_executed']}")
