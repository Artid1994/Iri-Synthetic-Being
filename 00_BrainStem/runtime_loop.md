---
brain_region: stem
lobe: stem
region: stem
tags:
  - stem
  - runtime
  - scheduler
title: BrainStem Core Loop & Clock
description: Master tick generator and cognitive state orchestrator
---

# Master Clock & Runtime Loop

The Master Runtime Loop coordinates continuous autonomic cognitive pacing across all lobes.

## Neural Signal Pathways
- Receives arousal signals and safety constraints from [[00_BrainStem/README|BrainStem Subsystem]]
- Directs autonomic pacing into [[00_BrainStem/safety_gate|Safety Gate]]
- Synchronizes sensory cycle sampling with [[05_Occipital/input_pipeline|Perceptual Input Pipeline]]
- Triggers executive action evaluation in [[01_Frontal/executive_controller|Executive Controller]]
- Emits clock ticks to [[04_Cerebellum/action_dispatcher|Action Dispatcher]]
- Bridges to global topology: [[BRAIN_ATLAS_MAP]]
