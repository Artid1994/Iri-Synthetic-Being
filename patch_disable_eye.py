import re
from pathlib import Path

file_path = Path("01_Neocortex/autonomous_loop.py")
backup_path = Path("01_Neocortex/autonomous_loop.py.patch_disable_eye.bak")

# 1. อ่านไฟล์และทำข้อมูลสำรอง
text = file_path.read_text(encoding="utf-8")
backup_path.write_text(text, encoding="utf-8")
print("[Disable Eye] Backup created at:", backup_path)

# 2. ค้นหาจุดเงื่อนไขการกะพริบตาในลูป run_cycle แล้วแปลงตรรกะเป็น False เพื่อปิดสัญญาน
old_loop_trigger = "if current_state == CircadianState.ACTIVE and iteration % 30 == 1:"
new_loop_trigger = "if False: # 🔴 ปิดระบบประสาทตาชั่วคราวตามคำสั่งเจ้านาย"

if old_loop_trigger in text:
    text = text.replace(old_loop_trigger, new_loop_trigger, 1)
    print("[Disable Eye] ✓ Sensory loop has been safely commented out and deactivated.")
else:
    print("[Disable Eye] ❌ Error: Sensory loop trigger line not found!")

# 3. เขียนไฟล์ที่ปรับแต่งเรียบร้อยแล้วกลับลงระบบ
file_path.write_text(text, encoding="utf-8")
print("[Disable Eye] Process Complete. Eye module is now offline.")
