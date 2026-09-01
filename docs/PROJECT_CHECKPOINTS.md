# TTF Project Checkpoints

เอกสารนี้ใช้ติดตามตำแหน่งปัจจุบันของโครงการ
เพื่อป้องกันการหลงทาง ลืมงาน หรือข้ามขั้นตอนสำคัญ

---

## เป้าหมายหลัก

สร้าง Numerical Research System สำหรับศึกษา:

- quantum coherence
- environmental coupling
- decoherence
- candidate mathematical models

ระบบต้องสามารถ:

AI เสนอ hypothesis/model
→ Python ตรวจสอบ
→ Python คำนวณ
→ เปรียบเทียบผล
→ บันทึกประวัติ
→ AI วิเคราะห์ผล
→ ทดลองรอบถัดไป

ข้อจำกัดสำคัญ:

- AI ไม่ execute arbitrary code
- Python เป็นผู้คำนวณและวัด metric
- ห้ามอ้าง simulation เป็น physical discovery
- ทุก milestone ต้องย้อนกลับได้ด้วย Git

---

# Checkpoint Roadmap

## CP0 — Project Baseline

สถานะ: ✅ COMPLETED

เป้าหมาย:
มี TTF project และ Git checkpoint ที่ย้อนกลับได้

---

## CP1 — Remote Ollama

สถานะ: ✅ COMPLETED

สิ่งที่ยืนยัน:
- เครื่อง 2 สามารถใช้ Python เชื่อม Ollama เครื่อง 1
- `qwen2.5:0.5b` ทำงานผ่าน remote host

Git:
`14d4218`

---

## CP2 — Experiment Contract

สถานะ: ✅ COMPLETED

สร้าง:
- `Experiment`
- `ExperimentResult`

---

## CP3 — Numerical Engine

สถานะ: ✅ COMPLETED

รองรับ:
- 1–2 qubit
- coupling
- coherence
- probability normalization
- parameter sweep

---

## CP4 — Model Comparison

สถานะ: ✅ COMPLETED

เปรียบเทียบ:
- exponential model
- linear model

Python คำนวณ error และเลือก `best_model`

---

## CP5 — Independent Reference Dynamics

สถานะ: ✅ COMPLETED

เพิ่ม reference dynamics ที่แยกจาก candidate model

วัตถุประสงค์:
ป้องกัน self-confirming simulation

---

## CP6 — Research Summary

สถานะ: ✅ COMPLETED

Python สามารถสร้าง summary สำหรับ AI:

- hypothesis
- objective
- best_model
- model errors

---

## CP7 — AI Research Proposal

สถานะ: ✅ COMPLETED

สร้าง:
- `ResearchPrompt`
- `ResearchProposal`

รองรับ:
- parse hypothesis
- parse model proposal
- model validation
- model key

AI ไม่ส่ง executable code ให้ Python

---

## CP8 — Model Evaluation Gate

สถานะ: ✅ COMPLETED

Python สามารถ:
- reject unsupported model
- dispatch supported model
- evaluate model
- คำนวณ error กับ reference dynamics

---

## CP9 — NumericalResearch 1-Cycle

สถานะ: ✅ COMPLETED

Pipeline:

Research Summary
→ AI
→ ResearchProposal
→ Validation
→ Numerical Evaluation

ทดสอบด้วย FakeAI:

`13 passed`

Cycle จริงบนเครื่อง 2:

`status = COMPLETED`

`model = exponential`

`error = 0.021072181397545926`

หมายเหตุ:
ยังไม่ได้ทดสอบ NumericalResearch แบบครบ cycle ผ่าน Ollama ล่าสุด เพราะเครื่อง 1 ปิดอยู่

Git checkpoint ล่าสุด:
`4e942de`

---

# CURRENT POSITION

## CP10 — Experiment History

สถานะ: ✅ COMPLETED

สิ่งที่ยืนยัน:
- record() ✅
- timestamp ✅
- experiment_id ✅
- record_result() ✅
- NumericalResearch → History ✅
- JSON save() ✅
- JSON load() ✅
- persistence test ✅
- research tests: `19 passed`

ต้องทำ:

- บันทึก hypothesis
- model
- parameters
- metrics
- error
- status
- timestamp
- ผลของแต่ละ research cycle

ต้องทำก่อน autonomous multi-cycle

---

## CP11 — Real 2-Machine Research Cycle

สถานะ: ✅ COMPLETED

หลักฐาน:
- เครื่อง 2 → เครื่อง 1 Ollama ✅
- `qwen2.5:0.5b` inference จริง ✅
- Research Proposal parsing ✅
- Model validation ✅
- Numerical evaluation ✅
- Result: `COMPLETED`
- Error: `0.021072181397545926`

เงื่อนไข:
- เครื่อง 1 เปิด
- Ollama ทำงาน
- เครื่อง 2 ติดต่อ Ollama ได้

Pipeline:

เครื่อง 2 Python
→ network
→ เครื่อง 1 Ollama
→ AI proposal
→ เครื่อง 2 Python evaluation

---

## CP12 — Research Cycle Integration

สถานะ: ✅ COMPLETED

รวมระบบ:

Research History
+ NumericalResearch
+ AI Proposal
+ Numerical Evaluation

สิ่งที่ยืนยัน:
- NumericalResearch บันทึกผลลง ExperimentHistory
- รองรับหลาย research cycles
- History แยก experiment_id ของแต่ละ cycle
- History save/load รักษาข้อมูลหลาย cycles
- failed proposal ไม่ถูกบันทึกเป็นผลสำเร็จ

---

## CP13 — Autonomous Research Loop

สถานะ: ✅ COMPLETED

สร้าง:
- `runtime/research_loop.py`

ระบบทำงาน:

cycle
→ research summary
→ AI proposal
→ validation
→ numerical evaluation
→ history
→ previous result
→ next cycle

สิ่งที่ยืนยัน:
- ส่งผลของ cycle ก่อนหน้าเข้า cycle ถัดไป
- `previous_result` ถูกส่งเข้า ResearchPrompt จริง
- รองรับหลาย cycles
- หยุดเมื่อ `FAILED`
- หยุดเมื่อ `ERROR`
- หยุดเมื่อ `REJECTED`
- ไม่บันทึกผล `REJECTED` ลง History

การทดสอบจริง:
- 2 cycles ทำงานสำเร็จ
- cycle ถัดไปได้รับผลของ cycle ก่อนหน้า
- unsupported model ทำให้ loop หยุดที่ cycle แรก
- history_entries = 0 สำหรับ rejected proposal

Git:
`110306e`

---

## CP14 — Stability / Regression

สถานะ: ✅ COMPLETED

ตรวจสอบ:
- research tests
- existing AE01M tests
- invalid AI output
- unsupported model
- network failure
- Ollama timeout
- malformed Ollama response
- AutonomousRunner failure limit
- legacy test collection

เพิ่ม:
- `pytest.ini`
- ย้าย legacy tests ไป `tests/legacy/`

Full regression:

`467 passed in 795.20s (0:13:15)`

ไม่พบ test failure ใน regression ล่าสุด

---

## CP15 — Final Documentation

สถานะ: ⬜ IN PROGRESS

เป้าหมาย:

สร้าง/อัปเดต:

- `PROJECT_BUILD_LOG.md`
- `PROJECT_CHECKPOINTS.md`
- `RESEARCH_LOG.md`
- `DEVELOPMENT_GUIDE.md`
- `ARCHITECTURE.md`

---

## CP16 — System Start Point

สถานะ: ⬜ TODO

สร้างแฟ้มสำหรับจุดเริ่มระบบ เช่น:

`docs/START_HERE.md`
