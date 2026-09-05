# AE01M / THE_TRANSCENDING_FORM
# Master Development Plan — v1

สถานะฐาน:
- Git branch: `checkpoint/130-tests-pass`
- Baseline commit: `a2cf53f`
- Working tree ปัจจุบันมีงาน Learning และ UI/Memory ที่ยังไม่ commit
- แผนนี้ใช้ baseline และโครงสร้าง source ที่ตรวจพบเป็นฐาน
- สิ่งที่ยังไม่ได้ตรวจ implementation จะไม่ถือว่าเสร็จ

---

## 1. เป้าหมายหลัก

พัฒนา AE01M เป็นระบบ cognitive architecture ที่มีโครงสร้างภายในสำหรับ:

`Brain → Neural State → Memory → Identity/Self Model → Cognition → Learning → Research → Autonomy`

โดยหลักสำคัญคือสร้าง “กลไก” ให้ระบบสามารถพัฒนาได้จากประสบการณ์ แทนการ hard-code พฤติกรรมทั้งหมดไว้ล่วงหน้า

LLM เป็น cognitive component / inference component ไม่ใช่ตัว Brain ทั้งหมด

---

## 2. Development Principle

ทุก Phase ต้องใช้หลัก:

`INSPECT → PLAN → IMPLEMENT → TEST → REVIEW → FIX → VERIFY → CHECKPOINT`

Hermes ต้อง:

1. ตรวจ source จริงก่อนแก้
2. คำนวณเส้นทางที่สั้นที่สุดที่ยังถูกต้อง
3. ใช้ context และ token เท่าที่จำเป็น
4. reuse mechanism ที่มีอยู่ก่อนสร้างของใหม่
5. ไม่สร้าง abstraction ซ้ำ
6. ไม่แก้ไฟล์นอก Phase
7. ไม่ข้าม Phase
8. ต้องมี test/verification
9. ต้อง checkpoint เมื่อ Phase เสร็จ
10. หยุดเมื่อ completion criteria ของ Phase ผ่าน

Optimization target:

`Shortest Correct Plan + Minimum Necessary Tokens + Minimum Necessary Actions`

โดย:

`Correctness > Safety > Requirements > Architecture > Verification > Minimal Actions > Token Efficiency`

---

# PHASE 0 — PROJECT RECONNAISSANCE

สถานะ: `[BASELINE / PARTIALLY COMPLETED]`

สิ่งที่ยืนยันแล้ว:

- `brain/`
- `regions/`
- `runtime/`
- `tests/`
- `docs/`
- `research/`
- `server.py`
- `AGENTS.md`
- `PROJECT_MAP.md`
- `PROJECT_PLAN.md`

พบ subsystem จำนวนมากแล้ว เช่น:

- Brain
- Memory
- Identity
- Self Model
- Learning
- Research
- Autonomous Loop
- Goal / Intention
- Prediction
- Reflection
- Safety
- Embodiment
- UI
- inference backends

### Completion Criteria

ต้องสามารถระบุได้ว่า:

- subsystem แต่ละตัวอยู่ที่ใด
- dependency หลักคืออะไร
- subsystem ใดเป็น foundation
- subsystem ใดเป็น higher-level behavior
- งานใด committed
- งานใด uncommitted
- งานใดเป็น planned
- งานใด implementation ยังไม่ครบ

---

# PHASE 1 — ARCHITECTURE MAP

สถานะ: `[PLANNED]`

สร้าง architectural map ของ AE01M โดยแบ่งอย่างน้อยเป็น:

`Foundation`
→ Brain / Node / Neural substrate

`Cognitive State`
→ internal state / working state / self model

`Memory`
→ episodic / semantic / graph / consolidation / recall

`Identity`
→ identity / continuity / representation

`Cognition`
→ cognitive loop / prediction / reflection / reasoning

`Learning`
→ learning / exercise / verification / feedback

`Research`
→ research loop / numerical research / web research

`Agency`
→ goal / intention / action / autonomous loop

`Interface`
→ UI / server / external interaction

### Completion Criteria

มี dependency graph ที่บอกได้ว่า component ไหนควรพึ่ง component ไหน และไม่มีการนำ higher-level behavior ไปเป็น foundation โดยไม่มีเหตุผล

---

# PHASE 2 — BRAIN / NODE FOUNDATION

สถานะ: `[INCOMPLETE]`

Source ที่ยืนยันแล้ว:

```text
brain/brain.py
brain/neuron.py
brain/population.py

regions/hippocampus.py
regions/motor_cortex.py

config/anatomy_settings.py
```

Neural substrate ที่มีอยู่แล้วประกอบด้วย:

- LIF neuron
- membrane state
- leak
- threshold
- reset
- vectorized NumPy state
- neuron population
- lazy chunk allocation
- brain regions

แต่จากการตรวจ source ก่อนหน้า:

**ยังไม่พบ neural synapse / neural connection mechanism ใน `brain/` หรือ `regions/`**

และต้องไม่ใช้ `MemoryEdge` แทน neural connection เพราะเป็นคนละ abstraction

### งาน Phase นี้

ตรวจและกำหนด foundation ของ:

`Node → Neuron → Population → Region → Brain`

จากนั้นกำหนด:

`Connection / Synapse`

โดยไม่สร้าง duplicate Node abstraction หาก architecture ปัจจุบันมี abstraction ที่เหมาะสมอยู่แล้ว

### Completion Criteria

- Node/neuron foundation มี representation ที่ชัดเจน
- Population ทำงานได้
- Region ทำงานได้
- Brain รวม region ได้
- neural connection mechanism ถูกกำหนดและทดสอบ
- neural state สามารถเปลี่ยนจาก input/activity ได้
- ไม่มีการใช้ Memory Graph เป็น neural graph แทนกัน
- regression tests ผ่าน

---

# PHASE 3 — NEURAL CONNECTION / SYNAPSE

สถานะ: `[PLANNED]`

เป้าหมาย:

`Neuron A → Synapse → Neuron B`

ต้องกำหนดอย่างน้อย:

- connection representation
- weight
- signal propagation
- activation/spike propagation
- connection ownership
- scalability constraints

ยังไม่กำหนด plasticity จนกว่า basic connection mechanism จะทำงานถูกต้อง

### Completion Criteria

สามารถสร้าง connection และพิสูจน์การส่ง signal ระหว่าง neural components ได้ด้วย deterministic tests

---

# PHASE 4 — NEURAL STATE & PLASTICITY

สถานะ: `[PLANNED]`

แยกจาก basic connection

เป้าหมาย:

- neural state
- activation history
- adaptation
- plasticity mechanism
- state persistence หากจำเป็น

หลัก:

Plasticity ต้องเกิดจาก mechanism/rules และ experience ไม่ใช่ hard-coded memory association

### Completion Criteria

มี test ที่พิสูจน์ว่า neural state สามารถเปลี่ยนตาม experience/activity ได้อย่างถูกต้อง

---

# PHASE 5 — BRAIN ↔ MEMORY

สถานะ: `[PARTIALLY IMPLEMENTED]`

Memory subsystem ที่มีอยู่แล้วประกอบด้วย:

- `runtime/memory.py`
- `runtime/memory_graph.py`
- `runtime/associative_recall.py`
- `runtime/memory_consolidation.py`
- `runtime/association_index.py`
- `runtime/semantic_index.py`
- `runtime/recall_index.py`

Brain มี hippocampus และ memory synchronization อยู่แล้วบางส่วน

### เป้าหมาย

กำหนด boundary ให้ชัดเจน:

`Brain neural substrate`

ไม่เท่ากับ

`Memory representation`

แต่ทั้งสองระบบสามารถเชื่อมกันผ่าน defined interface

### Completion Criteria

- memory สามารถเข้าสู่ brain pipeline
- brain state ไม่ถูกใช้แทน memory storage โดยไม่มี abstraction
- memory graph และ neural connection ไม่ปะปนกัน
- synchronization มี deterministic tests

---

# PHASE 6 — IDENTITY FOUNDATION

สถานะ: `[EXISTING / NEED ARCHITECTURAL CONSOLIDATION]`

Source ที่มี:

```text
runtime/identity.py
runtime/identity_continuity.py
runtime/identity_representation.py
runtime/self_model.py
runtime/cognitive_context.py
runtime/development.py
```

องค์ประกอบที่มีอยู่แล้ว:

- identity stage
- experience
- identity level
- identity continuity
- self-awareness
- self-knowledge
- goals
- beliefs
- self-history

### เป้าหมาย

ทำให้ Identity เป็น stateful subsystem ที่เชื่อมกับ experience และ memory อย่างชัดเจน โดยไม่ให้ Identity กลายเป็นเพียง static label

### Completion Criteria

Identity state สามารถ:

`exist → accumulate experience → maintain continuity → update representation`

และมี regression tests ครบ

---

# PHASE 7 — ROLE / PURPOSE / BOUNDARY

สถานะ: `[PLANNED]`

กำหนดแยกจาก Identity:

`Who am I?`
→ Identity

`What am I doing?`
→ Role

`Why am I doing it?`
→ Purpose / Goal

`What am I allowed to do?`
→ Boundary / Safety

ไม่ควรรวมทั้งหมดเป็น object เดียวโดยไม่มีเหตุผล

### Completion Criteria

มี contract ที่ชัดเจนระหว่าง:

Identity
Role
Purpose
Goal
Intention
Safety Boundary

---

# PHASE 8 — BRAIN ↔ COGNITIVE CORE

สถานะ: `[PLANNED]`

เชื่อม:

`Brain`
→ `Cognitive Context`
→ `Cognitive Loop`
→ `Inference`
→ `Memory`
→ `Self Model`

Source สำคัญที่มีอยู่แล้ว:

```text
runtime/cognitive_context.py
runtime/cognitive_loop.py
runtime/cognitive_engine.py
runtime/gemma_cognitive_engine.py
runtime/runtime.py
```

### Completion Criteria

Cognitive system สามารถอ่าน state จาก foundation และส่งผลกลับเข้าสู่ state/memory pipeline โดยมี boundary ชัดเจน

---

# PHASE 9 — LEARNING

สถานะ: `[IN PROGRESS — DO NOT OVERWRITE]`

Working tree ปัจจุบันมี Learning files จำนวนมาก เช่น:

```text
runtime/learning.py
runtime/self_directed_learning.py
runtime/learning_task.py
runtime/learning_practice.py
runtime/learning_exercise.py
runtime/learning_exercise_generator.py
runtime/learning_exercise_runner.py
runtime/learning_exercise_verifier.py
runtime/learning_verification.py
...
```

และมี tests ที่เกี่ยวข้องจำนวนมาก

งานเหล่านี้เป็น **uncommitted development** ณ จุดที่ตรวจล่าสุด

Hermes ห้าม:

- ลบทิ้ง
- rewrite โดยไม่ตรวจ
- reset working tree
- commit รวมโดยอัตโนมัติ
- นำงานนี้ไปปะปนกับ Brain Foundation โดยไม่มี dependency ที่พิสูจน์แล้ว

### เป้าหมาย

Learning ต้องสามารถ:

`Experience → Practice → Evaluation → Feedback → Update`

และต้องมี verification mechanism

### Completion Criteria

Learning subsystem ผ่าน tests ของตัวเองและ integration กับ Memory/Identity/Cognition โดยไม่ทำลาย baseline

---

# PHASE 10 — RESEARCH

สถานะ: `[EXISTING / NEED VALIDATION]`

Source ที่มี:

```text
runtime/research_loop.py
runtime/research_learning.py
runtime/research_prompt.py
runtime/research_proposal.py
runtime/numerical_research.py
runtime/web_research.py

research/THE_QUANTUM_MEASUREMENT_PROBLEM.md
```

### เป้าหมาย

สร้าง research mechanism ที่:

`Question → Hypothesis/Proposal → Evidence → Experiment/Calculation → Evaluation → Record`

โดยไม่ถือว่าผลจาก LLM เป็นหลักฐานโดยอัตโนมัติ

### Completion Criteria

Research สามารถสร้างและตรวจสอบ research cycle ได้โดยมี evidence trail

---

# PHASE 11 — AUTONOMOUS COGNITIVE LOOP

สถานะ: `[EXISTING / NEED INTEGRATION VALIDATION]`

Source ที่มี:

```text
runtime/autonomous_controller.py
runtime/autonomous_loop.py
runtime/autonomous_runner.py
runtime/autonomous_step.py
runtime/autonomous_learning.py
runtime/autonomous_policy_gate.py
runtime/autonomous_gate.py
```

### เป้าหมาย

รวม foundation ทั้งหมด:

`Observe`
→ `Interpret`
→ `Recall`
→ `Think`
→ `Decide`
→ `Act`
→ `Observe Result`
→ `Learn`
→ `Update State`

### Completion Criteria

มี closed-loop test ที่พิสูจน์ lifecycle โดยไม่ต้องพึ่งพาพฤติกรรมที่ hard-code เฉพาะกรณีทดสอบ

---

# PHASE 12 — HERMES ↔ CODEX ENGINEERING SYSTEM

สถานะ: `[PLANNED]`

แยกออกจาก AE01M cognitive architecture

Hermes:

`Operator / Executor`

Codex:

`Engineering Reasoning / Review`

Project Gateway:

`Boundary + Context + Permission + Validation`

Git:

`Checkpoint / Recovery / Audit`

### Hermes Loop

```text
PLAN
↓
INSPECT
↓
IMPLEMENT
↓
TEST
↓
REVIEW
↓
FIX
↓
VERIFY
↓
CHECKPOINT
↓
NEXT PHASE
```

Hermes ต้องทำงานภายใน:

```text
/home/artid1994/Projects/THE_TRANSCENDING_FORM
```

และไม่ควรได้รับสิทธิ์ระบบที่ไม่จำเป็นต่อ project development

---

# PHASE 13 — CONTROLLED AUTONOMOUS DEVELOPMENT

สถานะ: `[FUTURE]`

เมื่อ Phase 0–12 ผ่านแล้ว:

Hermes สามารถรับ Master Plan แล้วทำงานแบบ phase-by-phase ได้เอง

เงื่อนไข:

- อ่าน current state
- เลือก task ที่สั้นที่สุดที่ถูกต้อง
- จำกัด context
- แก้เฉพาะ scope
- test
- review
- checkpoint
- รายงานผล
- ไป Phase ถัดไปเฉพาะเมื่อ completion criteria ผ่าน

หาก verification ไม่ผ่าน:

`STOP → DIAGNOSE → FIX → VERIFY`

ไม่ใช่:

`FAIL → CONTINUE`

---

# 3. Current Working Tree Rule

ณ baseline นี้ working tree มีงานที่ยังไม่ commit

ดังนั้นก่อนเริ่ม autonomous development ต้องมี decision อย่างใดอย่างหนึ่ง:

1. commit งานที่ต้องการเก็บ
2. stash งานที่ยังไม่พร้อม
3. แยก branch สำหรับงาน Learning
4. ทิ้งเฉพาะสิ่งที่ยืนยันแล้วว่าไม่ต้องการ

Hermes ห้ามตัดสินใจลบงานโดยเดา

---

# 4. Phase Dependency

Dependency หลัก:

```text
PHASE 0
  ↓
PHASE 1
  ↓
PHASE 2
  ↓
PHASE 3
  ↓
PHASE 4
  ↓
PHASE 5
  ↓
PHASE 6
  ↓
PHASE 7
  ↓
PHASE 8
  ↓
PHASE 9
  ↓
PHASE 10
  ↓
PHASE 11
  ↓
PHASE 12
  ↓
PHASE 13
```

แต่ Phase ที่มี implementation อยู่แล้ว เช่น Memory, Identity, Learning, Research และ Autonomy จะถูกนำมา “ตรวจและ consolidate” ตาม dependency จริง ไม่ใช่เขียนใหม่ทั้งหมด

---

# 5. Global Definition of Done

Project ไม่ถือว่า Phase ใดเสร็จเพียงเพราะ code รันได้

ต้องผ่าน:

```text
Implementation
+
Unit Tests
+
Integration Tests
+
Regression Tests
+
Architecture Check
+
No Known Hidden Failure
+
Checkpoint
```

และต้องสามารถอธิบายได้ว่า:

- ทำอะไร
- ทำไมต้องทำ
- dependency คืออะไร
- test อะไร
- ผลเป็นอย่างไร
- มีข้อจำกัดอะไร

---

# 6. Hermes Optimization Contract

Hermes ต้องพยายามลด:

- จำนวนไฟล์ที่อ่าน
- จำนวนบรรทัดที่อ่าน
- จำนวนคำสั่ง
- จำนวน test ที่ไม่เกี่ยวข้อง
- จำนวน Codex calls
- จำนวน context ที่ส่งให้ Codex
- จำนวนการแก้ไข
- จำนวนรอบ retry

แต่ต้องไม่ลด:

- correctness
- safety
- required verification
- architectural integrity

เป้าหมายคือ:

`Minimum Necessary Work`

ไม่ใช่:

`Minimum Work Regardless of Correctness`

---

# 7. Immediate Next Step

ยังไม่เริ่ม Phase 2 ทันที

สิ่งแรกคือจัดการสถานะ:

`a2cf53f = Clean Baseline`

กับ

`Working Tree = Active Uncommitted Development`

โดยเฉพาะ Learning subsystem

หลังจากสถานะนี้ถูกจัดการแล้ว จึงให้ Hermes เริ่มจาก Phase ที่ถูกต้องตาม dependency
และห้ามถือว่า Learning ที่อยู่ใน working tree เป็น baseline จนกว่าจะผ่านการตรวจและ checkpoint