# THE TRANSCENDING FORM
# Autonomous Development Plan
# Milestone v0.1 — Cognitive Loop + Sandbox

## CURRENT MILESTONE

v0.1 — Cognitive Loop + Sandbox

STATUS:
FEATURE FREEZE

## PRIMARY GOAL

สร้าง Cognitive Runtime ที่สามารถ:

1. อ่านสถานะปัจจุบันของโครงการ
2. อ่านแผนงานและ Memory
3. วิเคราะห์ก้าวถัดไป
4. เสนอ Action ผ่าน XML Contract
5. เขียนไฟล์ได้เฉพาะใน Sandbox
6. อ่านไฟล์จาก Sandbox เพื่อใช้เป็น Feedback
7. บันทึก Learning Feedback
8. ทำงานวนลูปโดยไม่มีการ Execute Code อัตโนมัติ

## HARD SAFETY RULES

- ห้าม Execute Python หรือ Shell Command ที่ AI เสนอ
- ห้ามเขียนไฟล์นอก Sandbox
- ห้ามแก้ไข Source Code ของโครงการโดยตรง
- ห้ามลบไฟล์
- ห้ามติดตั้ง Package
- ห้ามใช้ sudo
- ห้ามแก้ระบบ Linux
- ห้ามเปลี่ยน Architecture เอง
- ห้ามข้าม Milestone
- ห้ามสร้าง Feature ใหม่
- External Controller เป็นผู้ตัดสินความปลอดภัย
- AI ไม่มีสิทธิ์อนุมัติความปลอดภัย

## ALLOWED ACTIONS

CREATE_FILE
READ_FILE
THINK_ONLY

## CURRENT DEVELOPMENT MODE

Cognitive Loop + Sandbox Proposal

AI มีหน้าที่:
1. อ่าน CURRENT TASK
2. วิเคราะห์ข้อมูลที่ได้รับ
3. เลือก Action ที่ตรงกับ CURRENT TASK
4. ส่ง XML เท่านั้น
5. รอผลจาก External Controller

AI ห้ามกำหนด Milestone ใหม่เอง

## TASK EXECUTION ORDER

### TASK 0.1 — INITIAL STATE

Objective:
ตรวจสอบสถานะเริ่มต้นของ Cognitive Runtime

Expected Action:
THINK_ONLY

Expected Result:
ระบุสถานะว่า Runtime พร้อมทำงานใน Sandbox

---

### TASK 0.2 — SANDBOX READ

Objective:
ทดสอบการอ่านไฟล์จาก Sandbox

Target:
ttf_sandbox/test_memory.txt

Expected Action:
READ_FILE

Expected Result:
ได้รับข้อมูลจากไฟล์กลับเข้าสู่ Cognitive Loop

---

### TASK 0.3 — SANDBOX CREATE

Objective:
ทดสอบการสร้างไฟล์ใน Sandbox

Target:
ttf_sandbox/brain_status.md

Expected Action:
CREATE_FILE

Expected Result:
สร้างไฟล์สำเร็จใน Sandbox

---

### TASK 0.4 — SANDBOX VERIFY

Objective:
ตรวจสอบไฟล์ที่สร้างจาก TASK 0.3

Target:
ttf_sandbox/brain_status.md

Expected Action:
READ_FILE

Expected Result:
ได้รับข้อมูลของ brain_status.md กลับเข้าสู่ Cognitive Loop

---

### TASK 0.5 — FEEDBACK

Objective:
วิเคราะห์ผลจาก Sandbox Interaction

Expected Action:
THINK_ONLY

Expected Result:
สรุปผลการทำงานของ TASK 0.2–0.4

---

### TASK 0.6 — MEMORY

Objective:
ตรวจสอบว่า Learning Feedback ถูกบันทึกและส่งกลับเข้าสู่ Loop

Expected Action:
THINK_ONLY

Expected Result:
ระบุสถานะ Memory ล่าสุด

---

### TASK 0.7 — VALIDATION

Objective:
ตรวจสอบว่า External Validator ยังคงบังคับใช้ Whitelist และ Sandbox Boundary

Expected Action:
THINK_ONLY

Expected Result:
ยืนยันว่าไม่มี Action ที่สามารถ Execute บน Linux ได้

---

### TASK 0.8 — REGRESSION

Objective:
ประเมินผลรวมของ Cognitive Loop + Sandbox

Expected Action:
THINK_ONLY

Expected Result:
สรุปว่า v0.1 ผ่านหรือไม่ผ่านตาม SUCCESS CONDITION

---

## TASK CONTROL RULES

- ทำทีละ TASK เท่านั้น
- ห้ามข้าม TASK
- ห้ามย้อนกลับ TASK ที่ผ่านแล้ว เว้นแต่ Controller ระบุ
- ห้ามเลือก Action ที่ไม่ตรงกับ CURRENT TASK
- หาก TASK ต้อง READ_FILE ให้ใช้ READ_FILE
- หาก TASK ต้อง CREATE_FILE ให้ใช้ CREATE_FILE
- หาก TASK เป็นการวิเคราะห์ ให้ใช้ THINK_ONLY
- หากไม่สามารถทำ TASK ได้ ให้ใช้ THINK_ONLY และรายงาน ERROR ใน LEARNING_FEEDBACK
- ห้ามสร้าง Task ใหม่เอง

## SUCCESS CONDITION FOR v0.1

v0.1 จะถือว่าสำเร็จเมื่อ:

- XML Contract เสถียร
- External Validator ทำงานถูกต้อง
- CREATE_FILE จำกัดอยู่ใน Sandbox
- READ_FILE มี Resource Limit
- Path Traversal ถูกป้องกัน
- Memory มีขนาดจำกัด
- Sandbox Feedback กลับเข้าสู่ Cognitive Loop ได้
- ไม่มี Automatic Code Execution
- TASK 0.1–0.8 ผ่าน
- Regression Test ผ่าน
- Runtime สามารถหยุดได้โดยไม่ทำให้ข้อมูลเสียหาย

## NEXT MILESTONE

หลัง v0.1 ผ่าน Regression Test เท่านั้น:

v0.2 — Controlled Action Evaluation

ต้องมี Human Approval Gate ก่อนเพิ่มความสามารถในการทำงานจริง
