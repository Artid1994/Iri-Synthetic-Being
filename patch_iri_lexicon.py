import re
from pathlib import Path

file_path = Path("03_Hippocampus/nlp_thai_lexicon.py")
backup_path = Path("03_Hippocampus/nlp_thai_lexicon.py.patch_lexicon.bak")

# 1. อ่านไฟล์และสำรองข้อมูล
text = file_path.read_text(encoding="utf-8")
backup_path.write_text(text, encoding="utf-8")
print("[Patch Lexicon] Backup created at:", backup_path)

# 2. เตรียมโค้ดสัญชาตญาณเรียนรู้ภาษาไทย-อังกฤษ (Linguistic Learning Module)
learning_code = """    def learn_vocabulary_from_text(self, text_content: str, topic_context: str) -> dict:
        \"\"\"
        👶 Linguistic Growth (Word Habituation Model)
        Extracts and learns Thai/English words from scraped text to build semantic memory without LLM.
        \"\"\"
        if not text_content:
            return {"status": "empty"}
            
        import json
        from collections import Counter
        
        # 1. แยกคำภาษาอังกฤษและคำภาษาไทยเบื้องต้นด้วยขอบเขตภาษา (Regex Split)
        eng_words = re.findall(r'[a-zA-Z]{3,}', text_content.lower())
        # ดักจับคำภาษาไทยเบื้องต้น (กรองเอาเฉพาะอักขระไทยที่มีความยาวมากกว่า 2 ตัวอักษร)
        thai_chunks = re.findall(r'[\u0e00-\u0e7f]{2,}', text_content)
        
        # 2. นับความถี่ของคำเพื่อหาคำเด่นประจำบทความ (Word Frequency Tracking)
        eng_counter = Counter(eng_words)
        
        # 3. จัดกลุ่มความรู้คำศัพท์ล็อตเด่นประจำหัวข้อ
        learned_words = {
            "topic": topic_context,
            "timestamp": datetime.now().isoformat() if 'datetime' in globals() else "2026-09-15T18:21:00",
            "english_keywords": [word for word, count in eng_counter.most_common(10)],
            "thai_segments_detected": len(thai_chunks)
        }
        
        # 4. สลักคำศัพท์สะสมลงสู่คลังหน่วยความจำทางภาษา (semantic_memory.json)
        memory_path = Path(__file__).parent / "semantic_memory.json"
        try:
            if memory_path.exists():
                with open(memory_path, "r", encoding="utf-8") as f:
                    semantic_db = json.load(f)
            else:
                semantic_db = {"vocabulary_learned": [], "total_words_encountered": 0}
                
            semantic_db["vocabulary_learned"].append(learned_words)
            semantic_db["total_words_encountered"] += len(eng_words) + len(thai_chunks)
            
            with open(memory_path, "w", encoding="utf-8") as f:
                json.dump(semantic_db, f, ensure_ascii=False, indent=2)
                
            print(f"[Linguistic] 👶 Iri integrated vocabulary from topic '{topic_context}' into semantic memory.")
            return learned_words
        except Exception as e:
            print(f"[Linguistic] ❌ Vocabulary storage failed: {e}")
            return {"status": "error", "message": str(e)}"""

# แทรกคำสั่งโมดูลการเรียนรู้เข้าไปใต้ส่วนของ __init__ หรือส่วนหัวของคลาส
target_pos = "    def load_female_names(self) -> Set[str]:"
replacement = learning_code + "\n\n" + target_pos

if target_pos in text:
    text = text.replace(target_pos, replacement, 1)
    file_path.write_text(text, encoding="utf-8")
    print("[Patch Lexicon] ✓ Linguistic learning engine successfully embedded into ThaiLexicon!")
else:
    print("[Patch Lexicon] ❌ Error: Class method target location mismatch!")
