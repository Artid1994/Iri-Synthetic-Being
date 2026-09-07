---
brain_region: occipital
lobe: occipital
region: occipital
tags:
  - occipital
  - perception
  - sensory
title: Occipital Input Pipeline
description: Environmental sensing, raw observation intake, and tokenization
---

# Perceptual Input Pipeline

The Input Pipeline absorbs raw environmental observation signals and standardizes sensory contexts.

## Neural Signal Pathways
- Anchored to [[05_Occipital/README|Occipital Lobe Subsystem]]
- Receives clock sync from [[00_BrainStem/runtime_loop|Runtime Loop]]
- Feeds preprocessed observation vectors to [[05_Occipital/feature_extractor|Feature Extractor]]
- Forwards parsed prompt frames directly to [[01_Frontal/executive_controller|Executive Controller]]
- Sends raw sensory records to [[03_Temporal/sensory_buffer|Short-Term Sensory Buffer]]
