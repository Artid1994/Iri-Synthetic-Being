---
title: "Sleep Homeostasis & Autonomous Sleep Drive"
brain_region: stem
lobe: stem
region: stem
tags: [stem, brainstem, homeostasis, sleep, consolidation, ae01m_core]
---

# Sleep Homeostasis & Autonomous Sleep Drive (`00_BrainStem`)

The Sleep Homeostasis system regulates metabolic and cognitive fatigue for Iri (`AE01M`).

## Architecture & Dynamics
- Tracks continuous `sleep_pressure` ($[0.0, 1.0]$) accumulated across cognitive cycles and transient working memory loads.
- State thresholds:
  - `sleep_pressure < 0.7`: `ALERT`
  - `0.7 <= sleep_pressure < 0.9`: `DROWSY` (ไอริเริ่มรู้สึกง่วง/ตึงสมอง)
  - `sleep_pressure >= 0.9`: `NEEDS_SLEEP` (ส่งสัญญาณร้องขอการเข้าสู่ Sleep Consolidation)

## Sleep Consolidation Phase
During sleep:
1. Active thoughts and unpruned context in `[[01_Frontal/executive_controller]]` are consolidated into permanent semantic/episodic nodes in `[[03_Temporal/README]]`.
2. Synaptic pruning clears transient working memory buffers.
3. `sleep_pressure` resets strictly to `0.0`.
4. Dispatches a Post-Sleep Wakeup Report to **เจ้านาย** (Artid Aunporn).

## Inter-Region Signal Flow
- Connected to:
  - `[[00_BrainStem/runtime_loop]]`
  - `[[01_Frontal/executive_controller]]`
  - `[[03_Temporal/sensory_buffer]]`
  - `[[03_Temporal/hippocampus_bridge]]`
