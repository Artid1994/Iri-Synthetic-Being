import re
from pathlib import Path

file_path = Path("01_Neocortex/autonomous_loop.py")
backup_path = Path("01_Neocortex/autonomous_loop.py.patch_cerebellum_fix.bak")

text = file_path.read_text(encoding="utf-8")
backup_path.write_text(text, encoding="utf-8")
print("[Fix] Backup created before cerebellum repair.")

# ค้นหาบล็อกเดิมที่มีจุดบั๊กตัวแปร parts
old_block = """                    target_path = self.project_root / parts.strip()
                    content = parts
                    
                    # Ensure path directory safety
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    target_path.write_text(content, encoding="utf-8")"""

# แทนที่ด้วยตรรกะการแยกมิติอินพุต (Array Indexing) ที่ถูกต้อง
new_block = """                    # แยกมิติพาธไฟล์และข้อความออกจากอาเรย์ส่วนย่อยให้ตรงจุด
                    target_file_str = parts[1].strip()
                    content = parts[2]
                    target_path = self.project_root / target_file_str
                    
                    # Ensure path directory safety
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    target_path.write_text(content, encoding="utf-8")"""

# จัดการแก้บั๊กจุดที่สองในพาร์ท APPEND_FILE ด้วยเช่นกัน
old_append_block = """                    target_path = self.project_root / parts.strip()
                    content = parts"""

new_append_block = """                    target_file_str = parts[1].strip()
                    content = parts[2]
                    target_path = self.project_root / target_file_str"""

if old_block in text:
    text = text.replace(old_block, new_block, 1)
    text = text.replace(old_append_block, new_append_block, 1)
    print("[Fix] ✓ Cerebellum indexing code successfully corrected!")
else:
    print("[Fix] ❌ Error: Indexing target position mismatch!")

file_path.write_text(text, encoding="utf-8")
print("[Fix] Complete. Ready for re-test.")
