import re
from pathlib import Path

file_path = Path("01_Neocortex/autonomous_loop.py")
backup_path = Path("01_Neocortex/autonomous_loop.py.patch_plasticity.bak")

# 1. อ่านไฟล์และสำรองข้อมูลล็อตใหม่
text = file_path.read_text(encoding="utf-8")
backup_path.write_text(text, encoding="utf-8")
print("[Patch 3] Backup created at:", backup_path)

# 2. แก้ไขชิ้นงานที่ 3: ฝังฟังก์ชัน _apply_memory_plasticity เข้าไปในคลาส AutonomousLoop
class_target = "    def mark_interaction(self):"
plasticity_function = """    def _apply_memory_plasticity(self, visual_words: set):
        \"\"\"
        🧠 Local Memory Plasticity (Hebbian Update Rule)
        Adjusts target goal priority based on recent visual screen triggers without using LLM.
        \"\"\"
        if not visual_words:
            return
            
        from goal_engine import GoalPriority, GoalStatus
        active_goals = self.goal_engine.list_goals()
        boosted_count = 0
        
        for goal in active_goals:
            if goal.status in [GoalStatus.PENDING, GoalStatus.IN_PROGRESS]:
                goal_text = (goal.title + " " + goal.description).lower()
                
                # Check if user's current desktop context overlaps with the goal keywords
                # กฎการเรียนรู้ประสาทสัมผัส: ถ้ายิ่งตรงกับสิ่งที่เจ้านายทำบ่อยๆ เส้นประสาทจะแข็งแรงขึ้น
                matched_words = [word for word in visual_words if word in goal_text]
                
                if matched_words and goal.priority != GoalPriority.HIGH:
                    # อัปเกรดประจุความสำคัญบน RAM ทันทีตามประสบการณ์หน้าจอ
                    goal.priority = GoalPriority.HIGH
                    boosted_count += 1
                    
        if boosted_count > 0:
            logger.info(f"[Plasticity] 🧠 Synaptic adjustment: Boosted {boosted_count} goals linked to screen context.")
            self.goal_engine.save_goals()

    def mark_interaction(self):"""

if class_target in text:
    text = text.replace(class_target, plasticity_function, 1)
    print("[Patch 3] Step 3.1: Plasticity neural dynamic function embedded.")
else:
    print("[Patch 3] ❌ Error: Target function position missing!")

# 3. นำฟังก์ชันนี้ไปปลั๊กเข้ากับรอบลูปรับรู้พิกเซลทางสายตาที่เพิ่งทำเสร็จในงานที่ 2
loop_target = "self.knowledge_base.setdefault(\"learned_facts\", []).append(fact_entry)"
loop_patch = """self.knowledge_base.setdefault("learned_facts", []).append(fact_entry)
                        
                        # 🧠 กระตุ้นกลไกปรับเปลี่ยนสภาพสมอง (Plasticity Trigger) ทันทีที่มีการเปลี่ยนแปลง
                        self._apply_memory_plasticity(current_words)"""

if loop_target in text:
    text = text.replace(loop_target, loop_patch, 1)
    print("[Patch 3] Step 3.2: Linked sensory context stream to Memory Weight updates.")
else:
    print("[Patch 3] ❌ Error: Target loop injection block not found!")

# 4. เขียนไฟล์กลับ
file_path.write_text(text, encoding="utf-8")
print("[Patch 3] Done. Dynamic Plasticity Setup Complete.")
