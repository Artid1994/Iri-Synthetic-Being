import re
from pathlib import Path

file_path = Path("04_Cerebellum/tools/wikipedia_tool.py")
backup_path = Path("04_Cerebellum/tools/wikipedia_tool.py.network_fix.bak")

# 1. อ่านไฟล์และทำข้อมูลสำรอง
text = file_path.read_text(encoding="utf-8")
backup_path.write_text(text, encoding="utf-8")
print("[Network Fix] Backup created for wikipedia_tool.py")

# 2. ปรับปรุงตรรกะการเรียก urlopen ให้ระบุสิทธิ์ User-Agent ของระบบปิดไอริ
old_urlopen_block = """            url = f"{self.api_url}?{urllib.parse.urlencode(params)}"
            with urllib.request.urlopen(url, timeout=self.timeout) as response:"""

new_urlopen_block = """            url = f"{self.api_url}?{urllib.parse.urlencode(params)}"
            # 🟢 ปลดล็อกท่อเครือข่าย: ระบุหัวข้อสิทธิ์ User-Agent ตามกฎสากลของ MediaWiki API เพื่อไม่ให้โดนบล็อก
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'IriSyntheticBeing/1.0 (Contact: artid1994@debian)'}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as response:"""

if old_urlopen_block in text:
    # แทนที่จุดรันคำสั่งทั้งหมดในไฟล์ (มี 3 จุด: search, get_summary, get_content)
    text = text.replace(old_urlopen_block, new_urlopen_block)
    print("[Network Fix] ✓ Safe User-Agent headers injected to all MediaWiki API endpoints!")
else:
    print("[Network Fix] ❌ Error: Urlopen block target structure mismatch!")

# 3. เขียนไฟล์ที่ซ่อมแซมเรียบร้อยแล้วกลับลงระบบ
file_path.write_text(text, encoding="utf-8")
print("[Network Fix] Repair Process Complete.")
