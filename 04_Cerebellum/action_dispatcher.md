---
brain_region: cerebellum
lobe: cerebellum
region: cerebellum
tags:
  - cerebellum
  - action
  - motor
title: Cerebellum Action Dispatcher
description: Motor command translation, tool execution, and environment interaction
---

# Action Dispatcher

Converts frontal intentions into safe, bounded tool execution commands and motor events.

## Neural Signal Pathways
- Anchored to [[04_Cerebellum/README|Cerebellum Subsystem]]
- Receives action directives from [[01_Frontal/goal_formulator|Goal Formulator]] and [[01_Frontal/reasoning_engine|Reasoning Engine]]
- Bound by execution approval from [[00_BrainStem/safety_gate|Safety Gate]]
- Synchronized by ticks from [[00_BrainStem/runtime_loop|Runtime Loop]]
- Evaluated for calibration and error in [[04_Cerebellum/learning_loop|Cerebellar Learning Loop]]
- Writes action outcome telemetry to [[03_Temporal/hippocampus_bridge|Hippocampus Bridge]]
