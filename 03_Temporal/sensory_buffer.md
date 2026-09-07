---
brain_region: temporal
lobe: temporal
region: temporal
tags:
  - temporal
  - sensory
  - buffer
title: Temporal Short-Term Sensory Buffer
description: High-throughput transient queue for incoming perceptual frames
---

# Short-Term Sensory Buffer

Holds raw incoming experiences transiently before hippocampal filtering and memory graph consolidation.

## Neural Signal Pathways
- Anchored to [[03_Temporal/README|Temporal Lobe Subsystem]]
- Receives immediate observation stream from [[05_Occipital/input_pipeline|Perceptual Input Pipeline]]
- Buffers frames for consolidation into [[03_Temporal/hippocampus_bridge|Hippocampus Bridge]]
- Exposes working window to [[01_Frontal/executive_controller|Executive Controller]]
- Synchronized under the heartbeat of [[00_BrainStem/runtime_loop|Runtime Loop]]
