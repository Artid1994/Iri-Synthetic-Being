# THE TRANSCENDING FORM — START HERE

เอกสารนี้คือจุดเริ่มต้นสำหรับผู้ที่ต้องการเข้าใจและทดลองใช้งานโครงการ THE TRANSCENDING FORM (TTF) / AE01M

---

## 1. โครงการนี้คืออะไร

THE TRANSCENDING FORM เป็นโครงการพัฒนาสถาปัตยกรรม AI แบบ Cognitive Architecture โดยมี AE01M เป็นระบบ AI ที่พัฒนาบน runtime และองค์ประกอบด้านความจำ การรับรู้ การคิด การเรียนรู้ ความปลอดภัย และ autonomous operation

โครงการยังอยู่ในระหว่างการพัฒนา

ระบบปัจจุบันควรถูกมองเป็น software research prototype ไม่ใช่หลักฐานว่า AI มี consciousness หรือความคิดแบบมนุษย์

---

## 2. จุดเริ่มต้นของระบบ

โครงการมี entry point หลักตามวัตถุประสงค์ดังนี้

### Interactive AE01M

ไฟล์:

    ae01m_chat.py

ใช้สำหรับการโต้ตอบกับ AE01M ผ่าน terminal

การทำงานโดยสรุป:

    ae01m_chat.py
        ↓
    TranscendingRuntime
        ↓
    runtime.cognitive.think()
        ↓
    ผลลัพธ์ AE01M

เริ่มใช้งาน:

    python3 ae01m_chat.py

โปรแกรมจะเปิด interactive prompt และรอข้อความจากผู้ใช้

พิมพ์:

    exit

เพื่อออกจากโปรแกรม

---

## 3. Autonomous Service

ไฟล์:

    tools/autonomous_service_launcher.py

ใช้สำหรับเริ่ม autonomous runtime service

การทำงานโดยสรุป:

    autonomous_service_launcher.py
        ↓
    TranscendingRuntime
        ↓
    enable_autonomous_mode()
        ↓
    start_safe_autonomous_runtime()
        ↓
    autonomous cycles

Service มีการจัดการ SIGTERM และ SIGINT เพื่อเรียก shutdown ของ runtime

เริ่มใช้งาน:

    python3 tools/autonomous_service_launcher.py

ควรใช้ด้วยความระมัดระวัง เนื่องจากเป็น autonomous execution loop ที่ทำงานต่อเนื่องจนกว่าจะได้รับคำสั่ง shutdown

---

## 4. TranscendingRuntime

ไฟล์หลัก:

    runtime/runtime.py

คลาสหลัก:

    TranscendingRuntime

หน้าที่คือเป็น runtime orchestration layer ของระบบ

ภายใน runtime มีองค์ประกอบ เช่น

- SystemMonitor
- Identity
- Memory
- Brain
- SafetyPolicy
- InternalStateManager
- Personality
- SelfModel
- Cognitive Engine
- AutonomousLoopController
- AutonomousRunner
- SafeRuntimeControl
- WebResearch
- ResearchSafetyGate
- ResearchLearning
- AutonomousLearning

`runtime/runtime.py` ไม่ใช่ executable entry point โดยตรง

โดยทั่วไปควรเข้าระบบผ่าน entry point เช่น

    ae01m_chat.py

หรือ

    tools/autonomous_service_launcher.py

---

## 5. TTF Agent Loop

ไฟล์:

    ttf_agent_loop.py

เป็น autonomous agent loop อีกชุดหนึ่งของโครงการ

มีฟังก์ชัน:

    main()

และสามารถทำงานเป็นโปรแกรมแยกได้:

    python3 ttf_agent_loop.py

อย่างไรก็ตาม จากโครงสร้างปัจจุบัน ไฟล์นี้ไม่ควรถูกตีความว่าเป็น entry point หลักของ `TranscendingRuntime`

ให้ถือว่าเป็น agent loop แยกจาก runtime entry point หลัก จนกว่าจะมีการเปลี่ยนแปลงสถาปัตยกรรมและตรวจสอบการเชื่อมต่อใหม่

---

## 6. การเชื่อมต่อ AI Model

ระบบ Cognitive Engine ปัจจุบันสามารถใช้ Ollama เป็น backend

โมเดลที่ runtime ตั้งค่าเริ่มต้นไว้ในปัจจุบันคือ:

    qwen2.5:0.5b

ในสถาปัตยกรรมแบบสองเครื่อง Ollama สามารถทำงานบนเครื่องหนึ่ง และ Python runtime ทำงานบนอีกเครื่องหนึ่งผ่านเครือข่าย

ก่อนใช้งานจริงควรตรวจสอบว่า Ollama server พร้อมใช้งาน

ตัวอย่าง:

    ollama list

หรือ ตรวจสอบ endpoint ของ Ollama ตาม configuration ที่ใช้งานอยู่

---

## 7. Research Subsystem

โครงการมี Numerical Research subsystem สำหรับการทดลองเชิงตัวเลข

องค์ประกอบสำคัญ:

    NumericalEngine
        ↓
    ResearchProposal
        ↓
    ResearchPrompt
        ↓
    NumericalResearch
        ↓
    ResearchLoop

ระบบนี้ใช้ AI เพื่อเสนอ hypothesis / candidate model และใช้ Python/NumPy ในการคำนวณและประเมินผล

ปัจจุบัน candidate model ที่รองรับ ได้แก่:

- Exponential model
- Linear model

ResearchLoop สามารถทำหลาย research cycles และส่งผลของ cycle ก่อนหน้าไปยัง cycle ถัดไป

ระบบจะหยุดเมื่อพบสถานะ:

    FAILED
    ERROR
    REJECTED

Numerical Research เป็น research subsystem แยกจาก autonomous loop หลักของ `TranscendingRuntime`

---

## 8. กฎสำคัญของการพัฒนา

ก่อนแก้ไขระบบควรตรวจสอบสถานะ Git:

    git status --short

หลังแก้ไขควรตรวจสอบ:

    git diff --check

และรัน test ที่เกี่ยวข้องก่อนยืนยันการเปลี่ยนแปลง

ห้ามถือว่าการเปลี่ยนแปลงทำงานถูกต้องจนกว่าจะมีผลการทดสอบยืนยัน

การเปลี่ยนแปลงที่สำคัญควรทำเป็น checkpoint ที่สามารถย้อนกลับได้

---

## 9. เอกสารสำคัญ

เอกสารสำหรับทำความเข้าใจโครงการ:

    README.md

สถาปัตยกรรม:

    docs/ARCHITECTURE.md

แนวทางพัฒนา:

    docs/DEVELOPMENT_GUIDE.md

ประวัติ checkpoint:

    docs/PROJECT_CHECKPOINTS.md

บันทึกการพัฒนา:

    docs/PROJECT_BUILD_LOG.md

บันทึก numerical research:

    docs/RESEARCH_LOG.md

เอกสารนี้:

    docs/START_HERE.md

---

## 10. ลำดับการอ่านที่แนะนำ

หากเพิ่งเข้ามาดูโครงการ ให้เริ่มตามลำดับ:

    1. README.md
    2. docs/START_HERE.md
    3. docs/ARCHITECTURE.md
    4. docs/DEVELOPMENT_GUIDE.md
    5. docs/PROJECT_CHECKPOINTS.md
    6. docs/PROJECT_BUILD_LOG.md
    7. docs/RESEARCH_LOG.md

จากนั้นจึงเข้าไปดู source code ที่เกี่ยวข้อง

---

## 11. คำสั่งตรวจสอบเบื้องต้น

ตรวจสอบสถานะ Git:

    git status --short

ตรวจสอบโครงสร้าง runtime:

    find runtime -maxdepth 2 -type f -name "*.py" -print | sort

ตรวจสอบ entry points:

    grep -nE 'if __name__|def main|TranscendingRuntime|AutonomousLoopController|AutonomousRunner' \
    ae01m_chat.py ttf_agent_loop.py runtime/runtime.py tools/autonomous_service_launcher.py

รัน test suite:

    pytest -q

---

## 12. สถานะปัจจุบัน

CP0–CP15 เสร็จสิ้นแล้ว

CP16 — System Start Point:

    IN PROGRESS

เป้าหมายของ CP16 คือสร้างจุดเริ่มต้นที่ชัดเจนสำหรับการเข้าใจและใช้งานโครงการ โดยไม่เปลี่ยนพฤติกรรมของ runtime หรือเพิ่มความสามารถใหม่โดยไม่จำเป็น

หลังจากตรวจสอบเอกสารและ entry points แล้ว จึงสามารถปิด CP16 และกำหนด checkpoint ถัดไปได้

---

## 13. ขอบเขตทางวิทยาศาสตร์

Numerical Research ในโครงการเป็นการทดลองและ validation เชิงตัวเลข

ผลจาก simulation ไม่ควรถูกตีความเป็นการค้นพบทางฟิสิกส์โดยตรง

AI มีหน้าที่เสนอ hypothesis หรือ candidate model ตามข้อจำกัดของระบบ

Python มีหน้าที่คำนวณและตรวจสอบผล

การทดลองเชิงตัวเลขไม่เท่ากับการพิสูจน์ว่าระบบมี consciousness หรือคุณสมบัติทางกายภาพจริง

---

## 14. หลักการสำคัญของโครงการ

พัฒนาจากระบบเล็กไปสู่ระบบที่ซับซ้อน

ทุกความสามารถใหม่ต้องตรวจสอบได้

ไม่ถือว่าผลลัพธ์ที่ยังไม่ได้ทดสอบเป็นข้อเท็จจริง

ไม่ผูก research prototype เข้ากับ autonomous runtime โดยไม่มีการตรวจสอบ

รักษาความสามารถในการย้อนกลับของการเปลี่ยนแปลง

และให้ความสำคัญกับความถูกต้องของระบบมากกว่าการเพิ่มความสามารถอย่างรวดเร็ว
