# Architecture

โครงสร้างสถาปัตยกรรมปัจจุบันของโครงการ THE_TRANSCENDING_FORM / AE01M

เอกสารนี้อธิบาย components และ data flow ที่มีหลักฐานจาก implementation และการทดสอบของโครงการในปัจจุบัน

---

## 1. Architecture Overview

ระบบแบ่งหน้าที่หลักออกเป็น:

```text
AI / Ollama
      │
      ▼
Research Prompt
      │
      ▼
Research Proposal
      │
      ▼
Validation
      │
      ▼
Numerical Research
      │
      ▼
Numerical Engine
      │
      ▼
Research Result
      │
      ▼
Experiment History
```

สำหรับ research loop หลายรอบ:

```text
Research Result
      │
      ▼
Previous Result
      │
      ▼
Next Research Cycle
```

---

## 2. Main Components

Components ที่เกี่ยวข้องกับ Numerical Research System:

```text
runtime/
├── numerical_engine.py
├── numerical_research.py
├── research_history.py
├── research_prompt.py
├── research_proposal.py
└── research_loop.py
```

แต่ละ component มีหน้าที่แตกต่างกันและควรรักษาขอบเขตความรับผิดชอบของตัวเอง

---

## 3. NumericalEngine

`NumericalEngine` เป็นส่วนที่ทำหน้าที่ numerical computation

หน้าที่หลักที่มีการทดสอบ:

* สร้าง numerical experiment
* คำนวณ coherence
* คำนวณ probability
* ตรวจ probability normalization
* รองรับ coupling parameter
* ทำ parameter sweep
* ประเมิน candidate model
* คำนวณ error

ระบบ numerical ปัจจุบันเป็น prototype ที่ใช้ NumPy

ขอบเขตที่ทดสอบอยู่ในปัจจุบันรองรับระบบขนาดเล็ก เช่น 1–2 qubits

---

## 4. ResearchPrompt

`ResearchPrompt` ทำหน้าที่สร้าง prompt สำหรับ AI research proposal

ข้อมูลที่สามารถส่งเข้า prompt ได้แก่:

* hypothesis
* objective
* best model
* exponential error
* linear error
* previous result

รูปแบบหลักของ proposal:

```text
Hypothesis: <testable hypothesis>
Model Proposal: Exponential model OR Linear model
```

ResearchPrompt ไม่ได้ทำหน้าที่ execute code

---

## 5. ResearchProposal

`ResearchProposal` ทำหน้าที่ parse และตรวจสอบ output จาก AI

ระบบกำหนดรูปแบบ proposal อย่างชัดเจน:

```text
Hypothesis:
Model Proposal:
```

เฉพาะ model ที่อยู่ใน whitelist เท่านั้นที่สามารถผ่าน validation ได้

ปัจจุบัน:

```text
Exponential model
Linear model
```

หาก AI เสนอ model ที่ไม่รองรับ ระบบจะ reject proposal

ตัวอย่างผล:

```text
status = REJECTED
error = UNSUPPORTED_MODEL
```

---

## 6. NumericalResearch

`NumericalResearch` เป็นตัวประสาน research cycle

ลำดับการทำงาน:

```text
Create Research Summary
        ↓
Build Research Prompt
        ↓
Call AI / Ollama
        ↓
Parse AI Proposal
        ↓
Validate Proposal
        ↓
Numerical Evaluation
        ↓
Return Result
        ↓
Record Successful Result
```

หากผลไม่ใช่ `COMPLETED` จะไม่ถูกบันทึกเป็น successful research result ใน ExperimentHistory

---

## 7. ResearchLoop

`ResearchLoop` ทำหน้าที่ควบคุม research cycle หลายรอบ

ลำดับ:

```text
Cycle 1
   ↓
Result 1
   ↓
Previous Result
   ↓
Cycle 2
   ↓
Result 2
   ↓
Previous Result
   ↓
Cycle N
```

จำนวนรอบกำหนดผ่าน `max_cycles`

ResearchLoop จะหยุดเมื่อได้รับสถานะ:

```text
FAILED
ERROR
REJECTED
```

ดังนั้น error หรือ rejected proposal จะไม่ทำให้ loop ดำเนินต่อโดยไม่มีการตรวจสอบ

---

## 8. Previous Result Flow

ผลจาก cycle ก่อนหน้าถูกส่งต่อไปยัง cycle ถัดไป

Data flow:

```text
ResearchLoop
      ↓
NumericalResearch
      ↓
ResearchPrompt
      ↓
AI
```

ข้อมูล previous result ที่ส่งต่อประกอบด้วย:

```text
Model
Error
Status
```

ตัวอย่างข้อมูลที่ตรวจสอบจริง:

```text
Model: exponential
Error: 0.021072181397545926
Status: COMPLETED
```

กลไกนี้ทำให้ research cycle ถัดไปมีข้อมูลจากผลก่อนหน้าเป็น context

---

## 9. ExperimentHistory

`ExperimentHistory` ทำหน้าที่เก็บ research results

รองรับ:

* experiment ID
* hypothesis
* model
* parameters
* result
* หลาย research cycles
* save/load history

Research result ที่มีสถานะ `COMPLETED` ถูกบันทึกเพื่อให้สามารถตรวจสอบย้อนหลังได้

ผล `REJECTED` จาก unsupported model ไม่ถูกบันทึกเป็น successful result

---

## 10. AI / Ollama Boundary

ระบบสามารถใช้ Ollama เป็น AI inference backend

สถาปัตยกรรมที่ทดสอบ:

```text
Machine 2
Python Runtime
      │
      │ Network
      ▼
Machine 1
Ollama
      │
      ▼
qwen2.5:0.5b
```

AI ส่งกลับ research proposal ตาม format ที่กำหนด

Python เป็นผู้ควบคุม validation และ numerical evaluation

AI ไม่ได้ส่ง arbitrary executable code ให้ Python

---

## 11. Two-Machine Data Flow

Research cycle ที่ทดสอบจริง:

```text
Machine 2
│
├── Research Summary
│
├── Research Prompt
│
├── Network Request
│
▼
Machine 1
│
├── Ollama
│
└── qwen2.5:0.5b
│
▼
AI Proposal
│
▼
Machine 2
│
├── Proposal Parsing
├── Model Validation
├── Numerical Evaluation
└── Research Result
```

ผลการทดสอบจริง:

```text
status = COMPLETED
model  = exponential
error  = 0.021072181397545926
```

---

## 12. Research Data Flow

ภาพรวมของ numerical research:

```text
Research Input
      ↓
Numerical Experiment
      ↓
Research Summary
      ↓
AI Proposal
      ↓
Proposal Parser
      ↓
Model Validation
      ↓
Numerical Model Evaluation
      ↓
Error Measurement
      ↓
Research Result
      ↓
Experiment History
```

หาก proposal ไม่ผ่าน validation:

```text
AI Proposal
      ↓
Validation
      ↓
REJECTED
      ↓
Stop
```

---

## 13. Model Evaluation

Candidate models ถูกประเมินด้วย numerical metrics

ผลจาก prototype ที่ตรวจสอบแล้ว:

```text
Exponential error = 0.021072181397545926
Linear error      = 0.2777777777777778
Best model        = exponential
```

ผลนี้หมายถึง exponential model มี error ต่ำกว่า linear model ภายใต้ experiment และ parameters ของ prototype ที่ใช้ทดสอบ

ไม่ได้หมายความว่า exponential model ได้รับการพิสูจน์ว่าเป็นคำอธิบายทางฟิสิกส์ที่ถูกต้อง

---

## 14. Safety Boundary

Architecture ปัจจุบันกำหนด boundary ระหว่าง AI และ numerical runtime:

```text
AI
│
├── Hypothesis
└── Candidate Model
        │
        ▼
Python
│
├── Parse
├── Validate
├── Calculate
└── Record
```

Python ไม่ควรรับ arbitrary executable code จาก AI เพื่อ execute โดยตรง

ระบบจึงจำกัด AI output ให้อยู่ใน structured proposal

---

## 15. Failure Handling

Failure สามารถเกิดขึ้นได้จากหลายจุด เช่น:

```text
AI / Network
      ↓
Inference Failure
      ↓
Research Failure
```

หรือ:

```text
AI Proposal
      ↓
Invalid / Unsupported
      ↓
REJECTED
```

ResearchLoop จะหยุดเมื่อได้รับ:

```text
FAILED
ERROR
REJECTED
```

นอกจากนี้ระบบ AutonomousRunner มี failure limit และ circuit breaker สำหรับการหยุด task หลังเกิด failure ตามเงื่อนไขที่กำหนด

---

## 16. Testing Architecture

ระบบใช้ automated tests เพื่อตรวจสอบ components และ integration

การตรวจสอบที่ทำแล้วครอบคลุม:

* numerical research
* research history
* multi-cycle research
* previous-result propagation
* rejected proposal
* network failure
* timeout
* malformed response
* autonomous runner failure handling
* regression

Full regression ที่ตรวจสอบล่าสุด:

```text
467 passed in 795.20s (0:13:15)
```

Focused ResearchLoop tests:

```text
4 passed, 28 deselected in 0.25s
```

---

## 17. Main Runtime Boundary

Numerical Research System เป็นส่วนหนึ่งของ repository แต่ `NumericalResearch` และ `ResearchLoop` ไม่ควรถูกตีความว่าเป็น main autonomous cognitive loop ของ `TranscendingRuntime`

การวิจัยเชิงตัวเลขเป็น research subsystem ที่มีขอบเขตของตัวเอง

ดังนั้น:

```text
Transcending Runtime
        │
        └── Research Subsystem
              │
              ├── NumericalResearch
              ├── ResearchLoop
              └── ExperimentHistory
```

เป็นการอธิบายขอบเขตของ subsystem ไม่ใช่การอ้างว่า ResearchLoop ถูกเชื่อมเป็น autonomous loop หลักของ runtime แล้ว

---

## 18. Current Architecture Status

สถานะปัจจุบัน:

```text
Numerical Engine              IMPLEMENTED
Research Proposal             IMPLEMENTED
Research Prompt               IMPLEMENTED
Research History              IMPLEMENTED
Numerical Research            IMPLEMENTED
Research Loop                 IMPLEMENTED
Previous Result Propagation   VERIFIED
Two-Machine Ollama            VERIFIED
Regression Tests              VERIFIED
```

ระบบเหล่านี้เป็น software components ที่มี implementation และการทดสอบตามขอบเขตที่ระบุ

---

## 19. Scientific Boundary

Architecture นี้เป็น architecture ของ software numerical research prototype

ยังไม่มีหลักฐานจาก architecture นี้สำหรับ:

* physical experiment
* laboratory validation
* physical discovery
* proof of consciousness
* proof of AI consciousness

Numerical result ต้องตีความภายใต้:

```text
Model
+
Parameters
+
Implementation
+
Numerical Method
+
Software Environment
```

---

## 20. Current Project Position

ณ วันที่ 2026-09-01:

```text
CP12 — Research Cycle Integration   COMPLETED
CP13 — Autonomous Research Loop     COMPLETED
CP14 — Stability / Regression       COMPLETED
CP15 — Final Documentation          IN PROGRESS
CP16 — System Start Point           NOT STARTED
```

CP15 มีเป้าหมายให้ documentation สอดคล้องกับ implementation และผลการทดสอบจริง

หลัง CP15 เสร็จจึงพิจารณาเข้าสู่ CP16

---

## 21. Architecture Development Rule

เมื่อ architecture เปลี่ยนจากการแก้ implementation:

```text
Implementation Change
        ↓
Test
        ↓
Verify
        ↓
Update Architecture
        ↓
Commit
```

Documentation ต้องไม่อ้างความสามารถที่ยังไม่ได้รับการตรวจสอบ

หาก implementation และ documentation ไม่ตรงกัน ต้องตรวจสอบ implementation และ test result ก่อนแก้ documentation

---

## 22. Future Expansion Boundary

ส่วนประกอบในเอกสารนี้ไม่ได้หมายความว่าความสามารถในอนาคตถูก implement แล้ว

ความสามารถใหม่ เช่น:

* research model ใหม่
* numerical method ใหม่
* cognitive subsystem ใหม่
* autonomous behavior ใหม่
* physical experiment integration

ต้องถูกเพิ่มผ่าน implementation, testing และ checkpoint แยกต่างหาก

จนกว่าจะมีการทดสอบจริง ให้ถือว่าเป็น future work ไม่ใช่ current capability
