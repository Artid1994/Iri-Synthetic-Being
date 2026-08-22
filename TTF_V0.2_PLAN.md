# THE TRANSCENDING FORM
# Milestone v0.2 — Controlled Action Evaluation

## STATUS

DESIGN ONLY
v0.1 BASELINE LOCKED

## GOAL

เพิ่ม Human Approval Gate ระหว่าง Brain Engine
กับ External Controller โดยไม่ให้ Qwen สามารถอนุมัติ
Action ของตัวเองได้

## CORE FLOW

Qwen
  ↓
XML ACTION
  ↓
External Validator
  ↓
HUMAN APPROVAL GATE
  ↓
Controller
  ↓
Sandbox Action

## HARD RULES

- Qwen ไม่มีสิทธิ์อนุมัติ Action ของตัวเอง
- THINK_ONLY ไม่ต้อง Execute
- CREATE_FILE ต้องผ่าน Approval Gate
- READ_FILE ต้องผ่าน Validator
- ห้าม Execute Code
- ห้าม Shell Command
- ห้าม Python Execution
- ห้าม sudo
- ห้าม Package Installation
- ห้าม Delete
- ห้ามเขียนนอก Sandbox
- ห้ามแก้ Source Code โดยตรง
- ห้ามข้าม Milestone
- External Controller เป็นผู้มีอำนาจสูงสุด

## ACTION STATES

PROPOSED
VALIDATED
APPROVED
REJECTED
EXECUTED
FAILED

## APPROVAL RULE

AI สามารถสร้างได้เฉพาะ:

PROPOSED

Validator สามารถเปลี่ยนเป็น:

VALIDATED

มนุษย์เท่านั้นสามารถเปลี่ยนเป็น:

APPROVED
หรือ
REJECTED

## EXECUTION RULE

ห้ามเข้าสู่ EXECUTED หากไม่มี:

1. Valid XML
2. Allowed Action
3. Valid Sandbox Path
4. Resource Limit ผ่าน
5. Human Approval

## CURRENT SCOPE

ยังไม่เปิด Automatic Execution

v0.2 ระยะแรกเป็นการทดสอบ
Action Lifecycle และ Approval Gate เท่านั้น

## SUCCESS CONDITION

v0.2 จะถือว่าผ่านเมื่อ:

- Action Lifecycle ถูกต้อง
- Validator แยกจาก Approval Gate
- AI ไม่สามารถอนุมัติตัวเอง
- REJECTED Action ไม่ถูก Execute
- ไม่มี Approval = ไม่มี Execution
- Sandbox Boundary ยังคงทำงาน
- v0.1 Regression ไม่เสีย
