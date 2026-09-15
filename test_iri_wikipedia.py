import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "03_Hippocampus"))
sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))

try:
    from tools.wikipedia_tool import WikipediaTool
    from nlp_thai_lexicon import ThaiLexicon
    
    print("=============================================")
    print("🤖 IRI - INTEGRATED LINGUISTIC LEARNING TEST")
    print("=============================================")
    
    # 1. ให้สมองน้อยลากสายเน็ตดึงข้อมูลจาก Wikipedia สดๆ 
    wiki_th = WikipediaTool(lang="th")
    print("[1/3] Scrapping Thai linguistic stream from Wikipedia...")
    th_results = wiki_th.search("ปัญญาประดิษฐ์", limit=1)
    
    if th_results and len(th_results) > 0:
        target_title = th_results[0]['title']
        full_content = wiki_th.get_content(target_title, max_chars=3000)
        print(f"      ✓ Retrieved content for: {target_title} ({len(full_content)} characters)")
        
        # 2. ส่งข้อมูลที่ดึงได้ เข้าไประบบย่อยคำศัพท์ในฝั่งความจำ
        print("\n[2/3] Passing text stream into Wernicke's Area (ThaiLexicon)...")
        lexicon = ThaiLexicon()
        learning_report = lexicon.learn_vocabulary_from_text(full_content, topic_context=target_title)
        
        # 3. ตรวจสอบผลลัพธ์คลังศัพท์เด่นที่เด็กน้อยไอริแกนคัดกรองได้ค้างไว้บน RAM
        print("\n[3/3] Displaying Top Learned English Keywords from Thai Article:")
        for idx, word in enumerate(learning_report.get("english_keywords", [])):
            print(f"      [{idx+1}] {word}")
            
    print("=============================================")

except Exception as e:
    print(f"❌ Error during integrated flow: {e}")
