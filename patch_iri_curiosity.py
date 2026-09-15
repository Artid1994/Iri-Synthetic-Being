import re
from pathlib import Path

file_path = Path("01_Neocortex/autonomous_loop.py")
backup_path = Path("01_Neocortex/autonomous_loop.py.patch_curiosity.bak")

# 1. อ่านไฟล์และสำรองข้อมูลล็อตใหม่
text = file_path.read_text(encoding="utf-8")
backup_path.write_text(text, encoding="utf-8")
print("[Patch 2] Backup created at:", backup_path)

# 2. แก้ไขชิ้นงาน 2.1: แทรกตัวแปรสภาวะอารมณ์ใน AutonomousContext
context_target = "learned_facts: List[Dict[str, Any]] = None"
context_patch = (
    "learned_facts: List[Dict[str, Any]] = None\n"
    "    last_seen_words: set = None\n"
    "    curiosity_charge: float = 0.0"
)

post_init_target = "if self.learned_facts is None:\n            self.learned_facts = []"
post_init_patch = (
    "if self.learned_facts is None:\n            self.learned_facts = []\n"
    "        if self.last_seen_words is None:\n            self.last_seen_words = set()"
)

if context_target in text and post_init_target in text:
    text = text.replace(context_target, context_patch, 1)
    text = text.replace(post_init_target, post_init_patch, 1)
    print("[Patch 2] Step 2.1: Context emotional memory layers added.")
else:
    print("[Patch 2] ❌ Error: Context target missing!")

# 3. แก้ไขชิ้นงาน 2.2: พัฒนาตัวแปรในส่วนส่งสัญญาณลูปให้เรียนรู้ความแปลกใหม่
sensory_old_block = """            if current_state == CircadianState.ACTIVE and iteration % 30 == 1:
                logger.info("[Sensory] Iri is acquiring screen context via OCR...")
                try:
                    screen_elements = self.screen_eye.read_screen_text()
                    # Bind recent words stream into temporary memory vector layer
                    self.context.learned_facts.append({
                        'topic': 'Visual Perception',
                        'summary': f'Observed screen changes with {len(screen_elements)} text items.',
                        'timestamp': time.time(),
                        'source': 'visual_sensory'
                    })
                except Exception as e:
                    logger.warning(f"[Sensory] Visual acquisition failed: {e}")"""

sensory_new_block = """            if current_state == CircadianState.ACTIVE and iteration % 30 == 1:
                logger.info("[Sensory] Iri is acquiring screen context via OCR...")
                try:
                    screen_elements = self.screen_eye.read_screen_text()
                    
                    # 👶 Local Novelty Detection (Curiosity Driven Learning)
                    current_words = set([elem.text.lower() for elem in screen_elements if len(elem.text) > 1])
                    old_words = self.context.last_seen_words
                    
                    # หาคำศัพท์ใหม่ที่เด็กน้อยเพิ่งเคยเห็นในการกะพริบตารอบนี้
                    new_words = current_words - old_words
                    novelty_ratio = len(new_words) / max(len(current_words), 1)
                    
                    # ปรับชาร์จประจุไฟฟ้าความสนใจสะสมบน RAM
                    self.context.curiosity_charge = novelty_ratio
                    self.context.last_seen_words = current_words
                    
                    if novelty_ratio > 0.15: # หากหน้าจอเปลี่ยนไปมากกว่า 15% (เกิดสิ่งใหม่)
                        logger.info(f"[Curiosity] 👶 Iri feels curious! Novelty ratio: {novelty_ratio:.1%}. Found {len(new_words)} new words.")
                        fact_entry = {
                            'topic': 'Curiosity Experience',
                            'summary': f'Discovered fresh context on screen containing words like: {list(new_words)[:3]}.',
                            'timestamp': time.time(),
                            'source': 'visual_curiosity',
                            'novelty_level': novelty_ratio
                        }
                        self.context.learned_facts.append(fact_entry)
                        # เพิ่มพูนความรู้ดิบก้าวแรกเข้าสู่คลังความรู้จำลองทันที
                        self.knowledge_base.setdefault("learned_facts", []).append(fact_entry)
                    else:
                        logger.info(f"[Curiosity] Screen environment is stable ({novelty_ratio:.1%}). No high trigger.")
                        
                except Exception as e:
                    logger.warning(f"[Sensory] Visual acquisition failed: {e}")"""

if sensory_old_block in text:
    text = text.replace(sensory_old_block, sensory_new_block, 1)
    print("[Patch 2] Step 2.2: Curiosity engine embedded into sensory loop.")
else:
    print("[Patch 2] ❌ Error: Sensory loop block from Patch 1 not found!")

# 4. เขียนไฟล์กลับ
file_path.write_text(text, encoding="utf-8")
print("[Patch 2] Done. Complete Curiosity Setup.")
