---
brain_region: stem
lobe: stem
region: stem
tags:
  - stem
  - brainstem
  - architecture
  - runtime
title: Brain Stem Subsystem
description: Authority, Rules, Core Runtime Loop, Process Guard, Heartbeat
---

# 00_BrainStem — Authority, Rules & Core Loop

## Overview
The Brain Stem is the foundational operational core of AE01M / The Transcending Form. It coordinates life-support functions, safety gates, execution contracts, and the central runtime clock loop.

## Key Components & Responsibilities
- **Authority & Rules**: [[AGENTS]], [[PROJECT_PLAN]], [[MASTER_DEVELOPMENT_PLAN]]
- **Runtime Loop**: `runtime/runtime.py`, `runtime/autonomous_loop.py`
- **Safety Gate & Process Guard**: `runtime/autonomous_gate.py`, `runtime/process_guard.py`
- **Heartbeat & Telemetry**: `runtime/heartbeat.py`, `runtime/heartbeat_storage.py`

## Neural Connectivity & Cross-Region Pathways
- Ascending arousal and cycle dispatch to [[01_Frontal/README|01_Frontal (Cognitive Engine)]]
- Somatic state anchoring and neuromuscular gating to [[02_Parietal/README|02_Parietal (Neural Substrate)]]
- Persistence, checkpointing, and trace logging to [[03_Temporal/README|03_Temporal (Memory Graph)]]
- Autonomous learning coordination and motor verification to [[04_Cerebellum/README|04_Cerebellum (Action Engine)]]
- Environmental sensory reception arbitration to [[05_Occipital/README|05_Occipital (Perception)]]
- Global structural wiring map: [[BRAIN_ATLAS_MAP]]
