import re
from pathlib import Path

file_path = Path("01_Neocortex/autonomous_loop.py")
backup_path = Path("01_Neocortex/autonomous_loop.py.patch_eye.bak")

# 1. อ่านไฟล์เดิมและสำรองข้อมูล
text = file_path.read_text(encoding="utf-8")
backup_path.write_text(text, encoding="utf-8")
print("[Patch] Backup created at:", backup_path)

# 2. แก้ไขจุดที่ 1: แทรกตัวแปรสแกนตาใน __init__ (ชิ้นงาน 1.1)
init_target = "self.knowledge_base = self._load_knowledge_base()"
init_patch = (
    "self.knowledge_base = self._load_knowledge_base()\n        \n"
    "        # 🟢 Embedded Visual Cortex - Sensory Input\n"
    "        import importlib\n"
    "        visual_module = importlib.import_module(\"02_VisualCortex.screen_eye\")\n"
    "        self.screen_eye = visual_module.ScreenEye(ocr_scale=0.5, fast_mode=True)"
)

if init_target in text:
    text = text.replace(init_target, init_patch, 1)
    print("[Patch] Step 1.1: Visual initialization patched successfully.")
else:
    print("[Patch] ❌ Warning: Init target not found!")

# 3. แก้ไขจุดที่ 2: แทรกคำสั่งตากระพริบสแกนจอในลูป run_cycle (ชิ้นงาน 1.2)
loop_target = "logger.info(f\"[Cycle {iteration}] State: {current_state.value.upper()} (T+{time_in_state:.1f}s)\")"
loop_patch = (
    "logger.info(f\"[Cycle {iteration}] State: {current_state.value.upper()} (T+{time_in_state:.1f}s)\")\n            \n"
    "            # 🟢 Sensory Processing Loop: Eye blinks every 30s during ACTIVE state to conserve CPU\n"
    "            if current_state == CircadianState.ACTIVE and iteration % 30 == 1:\n"
    "                logger.info(\"[Sensory] Iri is acquiring screen context via OCR...\")\n"
    "                try:\n"
    "                    screen_elements = self.screen_eye.read_screen_text()\n"
    "                    # Bind recent words stream into temporary memory vector layer\n"
    "                    self.context.learned_facts.append({\n"
    "                        'topic': 'Visual Perception',\n"
    "                        'summary': f'Observed screen changes with {len(screen_elements)} text items.',\n"
    "                        'timestamp': time.time(),\n"
    "                        'source': 'visual_sensory'\n"
    "                    })\n"
    "                except Exception as e:\n"
    "                    logger.warning(f\"[Sensory] Visual acquisition failed: {e}\")"
)

if loop_target in text:
    text = text.replace(loop_target, loop_patch, 1)
    print("[Patch] Step 1.2: Visual loop execution patched successfully.")
else:
    print("[Patch] ❌ Warning: Loop target not found!")

# 4. เขียนไฟล์ที่แก้ไขแล้วกลับลงไป
file_path.write_text(text, encoding="utf-8")
print("[Patch] Complete. Ready for Verification Test.")
