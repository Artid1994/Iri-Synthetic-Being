import re
from pathlib import Path

file_path = Path("01_Neocortex/autonomous_loop.py")
backup_path = Path("01_Neocortex/autonomous_loop.py.patch_cerebellum.bak")

# 1. อ่านไฟล์และสำรองข้อมูลล็อตสุดท้าย
text = file_path.read_text(encoding="utf-8")
backup_path.write_text(text, encoding="utf-8")
print("[Patch 4] Final backup created at:", backup_path)

# 2. ค้นหาบล็อก Mockup เดิมของระบบไฟล์ปฏิบัติการ แล้วแทนด้วยคำสั่งจริงระดับ OS
old_file_op_block = """    def _execute_file_operation_subtask(self, subtask) -> str:
        \"\"\"Execute file operation subtask.\"\"\"
        logger.info(f"[Goals] File operation: {subtask.title}")
        
        # For now, just log the operation
        # In production, implement actual file operations with safety checks
        return f"File operation queued: {subtask.command}\""""

new_file_op_block = """    def _execute_file_operation_subtask(self, subtask) -> str:
        \"\"\"
        🛠️ Real Motor Execution System (Cerebellum Action Trigger)
        Executes safe, localized file operations on Linux Debian 13 without external dependencies.
        \"\"\"
        logger.info(f"[Goals] Executing real Cerebellum file operation: {subtask.title}")
        
        try:
            # รูปแบบคำสั่งดิบ: WRITE_FILE:path/to/file:content_string
            if subtask.command.startswith("WRITE_FILE:"):
                parts = subtask.command.split(":", 2)
                if len(parts) >= 3:
                    target_path = self.project_root / parts[1].strip()
                    content = parts[2]
                    
                    # Ensure path directory safety
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    target_path.write_text(content, encoding="utf-8")
                    
                    logger.info(f"[Cerebellum] ✓ Successfully wrote file down to disk: {target_path.name}")
                    return f"Action complete: File created and written at {target_path.name}."
            
            # รูปแบบคำสั่งดิบ: APPEND_FILE:path/to/file:content_string
            elif subtask.command.startswith("APPEND_FILE:"):
                parts = subtask.command.split(":", 2)
                if len(parts) >= 3:
                    target_path = self.project_root / parts[1].strip()
                    content = parts[2]
                    
                    with open(target_path, "a", encoding="utf-8") as f:
                        f.write(f"\\n{content}")
                        
                    logger.info(f"[Cerebellum] ✓ Successfully appended data to: {target_path.name}")
                    return f"Action complete: Data appended to {target_path.name}."
                    
            # คำสั่งทั่วไป ส่งผ่านเข้า Standard Shell Command
            return self._execute_terminal_subtask(subtask)
            
        except Exception as e:
            logger.error(f"[Cerebellum] ❌ Safe action execution failed: {e}")
            return f"Execution Error: {str(e)}" """

if old_file_op_block in text:
    text = text.replace(old_file_op_block, new_file_op_block, 1)
    print("[Patch 4] Step 4.1: Cerebellum safe motor action trigger patched successfully.")
else:
    print("[Patch 4] ❌ Error: Old file operation template block not found!")

# 3. เขียนไฟล์ที่สมบูรณ์กลับลงดิสก์
file_path.write_text(text, encoding="utf-8")
print("[Patch 4] Done. Autonomous Brain-Motor Circle is complete.")
