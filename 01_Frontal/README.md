---
brain_region: frontal
lobe: frontal
region: frontal
tags:
  - frontal
  - cognition
  - reasoning
  - gemma
title: Frontal Lobe Subsystem
description: Cognitive Engine, Reasoning, Gemma 3 Trigger, Reflection, Goal Formulation
---

# 01_Frontal — Cognitive Engine & Reasoning

## Overview
The Frontal Lobe orchestrates higher-order cognitive processing, prompt construction, decision-making, hypothesis generation, and goal formulation.

## Key Components & Responsibilities
- **Cognitive Engine**: `runtime/cognitive_engine.py`, `runtime/gemma_cognitive_engine.py`
- **Inference Boundary**: Local LLM backend abstraction (Gemma 3 1B IT Q4_K_M) via `runtime/llama_cpp_inference.py` and `runtime/ae01m_cognitive_factory.py`
- **Cognitive Loop & Trigger**: `runtime/cognitive_loop.py`
- **Reflection & Prediction**: `runtime/reflection.py`, `runtime/prediction.py`
- **Goal & Intention Management**: `runtime/goal.py`, `runtime/intention.py`

## Neural Connectivity & Cross-Region Pathways
- Clock pulse and execution constraints from [[00_BrainStem/README|00_BrainStem (Authority & Loop)]]
- Somatotopic feedback and neural firing state from [[02_Parietal/README|02_Parietal (Neural Substrate)]]
- Working memory recall, associative lookup, and episodic retrieval from [[03_Temporal/README|03_Temporal (Memory Systems)]]
- Plan evaluation and action candidate dispatch to [[04_Cerebellum/README|04_Cerebellum (Action Engine)]]
- Perceptual context intake and salient feature analysis from [[05_Occipital/README|05_Occipital (Perception)]]
- Central network topography: [[BRAIN_ATLAS_MAP]]
