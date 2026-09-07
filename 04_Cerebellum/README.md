---
brain_region: cerebellum
lobe: cerebellum
region: cerebellum
tags:
  - cerebellum
  - learning
  - motor
  - verification
title: Cerebellum Subsystem
description: Autonomous Learning Loop, Action Dispatcher, Motor Coordination, Automated Pytest Verification
---

# 04_Cerebellum — Learning Loops & Action Execution

## Overview
The Cerebellum automates rapid refinement, motor execution, action dispatching, error compensation, and empirical verification via automated test feedback loops.

## Key Components & Responsibilities
- **Autonomous Learning Loop**: `runtime/autonomous_learning.py`, `runtime/learning.py`
- **Action Dispatcher & Motor Control**: `runtime/action.py`, `runtime/action_mapper.py`, `regions/motor_cortex.py`
- **Autonomous Runner & Controller**: `runtime/autonomous_runner.py`, `runtime/autonomous_controller.py`
- **Verification Engine**: `runtime/learning_verification.py`, `tests/` automated test suites

## Neural Connectivity & Cross-Region Pathways
- Rhythm coordination and safety termination gates from [[00_BrainStem/README|00_BrainStem (Authority & Loop)]]
- Intent commands and formulated goals received from [[01_Frontal/README|01_Frontal (Cognitive Engine)]]
- Somatosensory efference copies and predictive models with [[02_Parietal/README|02_Parietal (Neural Substrate)]]
- Procedural skill consolidation and verification logging to [[03_Temporal/README|03_Temporal (Memory Systems)]]
- Visuomotor coordination and sensory-guided action loops with [[05_Occipital/README|05_Occipital (Perception)]]
- Global structural wiring map: [[BRAIN_ATLAS_MAP]]
