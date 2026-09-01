# Development Guide

คู่มือการพัฒนาโครงการ THE_TRANSCENDING_FORM / AE01M

เอกสารนี้อธิบายแนวทางการพัฒนา ตรวจสอบ และทดสอบระบบตามสถานะปัจจุบันของโครงการ

---

## 1. Project Goal

เป้าหมายของโครงการคือการพัฒนาโครงสร้างพื้นฐานของ AI Cognitive Architecture สำหรับ AE01M

ในสถานะปัจจุบัน ระบบอยู่ในขั้นตอนการพัฒนา software architecture และ numerical research prototype

การทดลองและผลลัพธ์ที่ได้จาก numerical simulation ไม่ถือเป็นการพิสูจน์ว่า AI มี consciousness และไม่ถือเป็น physical discovery

---

## 2. Development Principles

การพัฒนาต้องยึดหลัก:

* ทำทีละ checkpoint
* การเปลี่ยนแปลงต้องตรวจสอบได้
* ทุก feature ต้องมี test ที่เหมาะสม
* หลีกเลี่ยงการเปลี่ยนแปลงหลายระบบพร้อมกันโดยไม่จำเป็น
* ไม่อ้างความสามารถที่ยังไม่ได้ทดสอบจริง
* ใช้ Git เพื่อให้สามารถย้อนกลับการเปลี่ยนแปลงได้
* เมื่อเกิด regression ต้องหยุดและตรวจสอบก่อนทำงานต่อ

---

## 3. Main Runtime Structure

โครงการมีส่วนประกอบสำคัญที่เกี่ยวข้องกับ cognitive runtime และ research system

ส่วนของ numerical research ที่พัฒนาในปัจจุบันประกอบด้วย:

```text
runtime/
├── numerical_engine.py
├── numerical_research.py
├── research_history.py
├── research_prompt.py
├── research_proposal.py
└── research_loop.py
```

ชื่อและโครงสร้างจริงของ repository เป็นแหล่งอ้างอิงหลักเมื่อมีการเปลี่ยนแปลงโค้ด

---

## 4. Numerical Research System

Numerical Research System ใช้ Python เป็นส่วนควบคุมการทดลองเชิงตัวเลข

Pipeline หลัก:

```text
Research Summary
→ AI Proposal
→ Proposal Parsing
→ Model Validation
→ Numerical Evaluation
→ Result
→ History
```

AI มีหน้าที่เสนอ hypothesis และ candidate model

Python มีหน้าที่ตรวจสอบ proposal และคำนวณ numerical result

---

## 5. Supported Research Models

ระบบรองรับ candidate models ที่กำหนดไว้เท่านั้น

ปัจจุบันมี:

```text
Exponential model
Linear model
```

หาก AI เสนอ model ที่ไม่อยู่ในรายการ ระบบต้อง reject proposal

ตัวอย่าง:

```text
status = REJECTED
error = UNSUPPORTED_MODEL
```

การจำกัด model เป็นส่วนหนึ่งของ safety boundary ของ research system

---

## 6. AI Proposal Boundary

AI ต้องส่ง proposal ในรูปแบบที่กำหนด

รูปแบบหลัก:

```text
Hypothesis: <testable hypothesis>
Model Proposal: Exponential model OR Linear model
```

Python จะ parse และ validate ข้อมูลก่อนทำ numerical evaluation

AI ไม่ได้ส่ง arbitrary executable code ให้ Python

ดังนั้น research system ไม่ได้ออกแบบให้ AI สร้างและสั่ง execute code โดยตรง

---

## 7. Research Prompt

`runtime/research_prompt.py` ทำหน้าที่สร้าง prompt สำหรับ research cycle

Prompt ประกอบด้วยข้อมูลจาก research summary เช่น:

* hypothesis
* objective
* best model
* exponential error
* linear error

Research cycle ถัดไปสามารถได้รับผลจาก cycle ก่อนหน้าในรูปแบบ:

```text
Previous result:
Model: <model>
Error: <error>
Status: <status>
```

ข้อมูลนี้ถูกส่งผ่าน:

```text
ResearchLoop
→ NumericalResearch
→ ResearchPrompt
→ AI
```

---

## 8. Research Loop

`runtime/research_loop.py` ทำหน้าที่ควบคุม research cycle หลายรอบ

Pipeline:

```text
Cycle 1
→ Result
→ Previous Result
→ Cycle 2
→ Result
→ Previous Result
→ Cycle 3
→ ...
```

จำนวน cycles สามารถกำหนดผ่าน `max_cycles`

ResearchLoop จะหยุดเมื่อพบสถานะ:

```text
FAILED
ERROR
REJECTED
```

โดยเฉพาะกรณี `REJECTED` เช่น `UNSUPPORTED_MODEL` จะไม่ดำเนินการต่อเป็น cycle ใหม่

---

## 9. Research History

`ExperimentHistory` ใช้บันทึกผล research ที่สำเร็จ

ระบบรองรับ:

* การบันทึกแต่ละ research cycle
* experiment ID
* หลาย research cycles
* save/load history
* การตรวจสอบผลย้อนหลัง

ผลที่ไม่สำเร็จหรือถูก reject ไม่ควรถูกบันทึกเป็น successful research result

---

## 10. Two-Machine Ollama Setup

ระบบสามารถแยก Python runtime และ Ollama ออกจากกันคนละเครื่องได้

โครงสร้างที่ทดสอบแล้ว:

```text
Machine 2
Python Research Runtime
        │
        │ Network
        ▼
Machine 1
Ollama
        │
        ▼
qwen2.5:0.5b
```

ในการทดสอบจริง:

```text
status = COMPLETED
model  = exponential
error  = 0.021072181397545926
```

การทดสอบนี้ยืนยันเฉพาะการทำงานของ software/network pipeline ตาม environment ที่ทดสอบ ไม่ได้หมายความว่าระบบสามารถใช้ model ขนาดใดก็ได้โดยไม่มีข้อจำกัดด้านทรัพยากร

---

## 11. Testing

ก่อนยอมรับการเปลี่ยนแปลง ต้องรัน test ที่เกี่ยวข้องก่อน

สำหรับ ResearchLoop สามารถตรวจสอบ focused tests ได้

ผลที่ตรวจสอบแล้ว:

```text
4 passed, 28 deselected in 0.25s
```

และ full project regression:

```text
467 passed in 795.20s (0:13:15)
```

ตัวเลขเหล่านี้เป็นผลการทดสอบ ณ วันที่ 2026-09-01 และอาจเปลี่ยนเมื่อมีการเพิ่มหรือแก้ไข tests

---

## 12. Regression Protection

เมื่อแก้ไขระบบ:

1. ตรวจสอบไฟล์ที่เปลี่ยน
2. รัน test ที่เกี่ยวข้อง
3. ตรวจสอบ `git diff --check`
4. รัน full regression เมื่อเหมาะสม
5. ตรวจสอบ Git status
6. commit เฉพาะการเปลี่ยนแปลงที่ต้องการ

หาก test ล้มเหลว:

```text
STOP
→ Inspect failure
→ Fix
→ Re-test
→ Verify
```

ไม่ควรข้าม test failure เพื่อไป checkpoint ถัดไป

---

## 13. Git Workflow

ก่อนเริ่มงาน:

```bash
git status
```

หลังแก้ไข:

```bash
git diff --check
git status
```

ตรวจสอบ diff:

```bash
git diff
```

เพิ่มไฟล์ที่ต้องการ:

```bash
git add <file>
```

ตรวจสอบ staged changes:

```bash
git diff --cached --check
git diff --cached
```

จากนั้นจึง commit เมื่อการตรวจสอบผ่าน

ตัวอย่าง:

```bash
git commit -m "docs: update development guide"
```

ไม่ควรใช้:

```bash
git add .
```

โดยไม่ตรวจสอบ เพราะอาจนำไฟล์ที่ไม่เกี่ยวข้องเข้า commit

---

## 14. Checkpoint Workflow

การพัฒนาของโครงการแบ่งเป็น checkpoint เพื่อควบคุมความเสี่ยง

หลักการ:

```text
Implement
→ Test
→ Verify
→ Document
→ Commit
→ Next Checkpoint
```

หาก checkpoint ปัจจุบันยังไม่ผ่าน ไม่ควรถือว่า checkpoint เสร็จสมบูรณ์

---

## 15. Documentation

เอกสารสำคัญของโครงการประกอบด้วย:

```text
docs/
├── PROJECT_CHECKPOINTS.md
├── PROJECT_BUILD_LOG.md
├── RESEARCH_LOG.md
├── DEVELOPMENT_GUIDE.md
└── ARCHITECTURE.md
```

หน้าที่โดยสรุป:

`PROJECT_CHECKPOINTS.md`

ใช้ติดตามสถานะของ checkpoint

`PROJECT_BUILD_LOG.md`

ใช้บันทึกประวัติการพัฒนาและเหตุการณ์สำคัญ

`RESEARCH_LOG.md`

ใช้บันทึก research experiment และผลการทดสอบที่เกิดขึ้นจริง

`DEVELOPMENT_GUIDE.md`

ใช้เป็นคู่มือสำหรับการพัฒนาและตรวจสอบระบบ

`ARCHITECTURE.md`

ใช้บันทึกโครงสร้างและความสัมพันธ์ของ components

---

## 16. Research Safety Boundaries

ระบบ research ปัจจุบันต้องรักษาขอบเขตดังต่อไปนี้:

* AI เสนอ hypothesis/model
* Python ตรวจสอบ proposal
* Python เป็นผู้คำนวณ numerical metrics
* unsupported model ถูก reject
* AI ไม่ execute arbitrary code
* numerical simulation ไม่ถูกอ้างเป็น physical discovery
* ผลการทดลองสามารถตรวจสอบย้อนหลังได้

---

## 17. Scientific Limitations

Numerical Research System เป็น software simulation

ผลจากระบบจึงต้องตีความภายใน:

```text
mathematical model
+
parameters
+
numerical implementation
+
software environment
```

ไม่ควรสรุปจาก numerical result เพียงอย่างเดียวว่า:

* เกิดปรากฏการณ์ทางฟิสิกส์จริง
* มีการค้นพบทางฟิสิกส์ใหม่
* ผลสามารถใช้แทน laboratory experiment
* AI มี consciousness

ข้อสรุปดังกล่าวต้องมีหลักฐานเพิ่มเติมนอกเหนือจาก numerical prototype

---

## 18. Current Project Status

สถานะ ณ วันที่ 2026-09-01:

```text
CP0  — CP11  COMPLETED
CP12 — Research Cycle Integration COMPLETED
CP13 — Autonomous Research Loop COMPLETED
CP14 — Stability/Regression COMPLETED
CP15 — Final Documentation IN PROGRESS
CP16 — System Start Point NOT STARTED
```

CP13 มี research loop ที่รองรับหลาย cycles และ previous-result propagation

CP14 ผ่าน full project regression:

```text
467 passed
```

CP15 มุ่งตรวจสอบและจัดทำ documentation ให้สอดคล้องกับ implementation และผลการทดสอบจริง

---

## 19. Development Rule

เมื่อมีการแก้ไข implementation หรือ documentation ต้องตรวจสอบผลจริงก่อนสรุปว่าเสร็จ

หลักปฏิบัติ:

```text
Change
→ Verify
→ Test
→ Review
→ Document
→ Commit
```

ห้ามถือว่าระบบมีความสามารถใด ๆ เพียงเพราะมีโค้ดรองรับความสามารถนั้น จนกว่าจะมีการทดสอบหรือหลักฐานที่เหมาะสมรองรับ

---

## 20. Next Step

หลังจาก CP15 documentation ผ่านการตรวจสอบทั้งหมด:

```text
CP15
Final Documentation
        ↓
CP16
System Start Point
```

CP16 ยังไม่เริ่มจนกว่า documentation และ regression verification ที่เกี่ยวข้องจะเสร็จสมบูรณ์
