---
brain_region: temporal
lobe: temporal
region: temporal
tags:
  - temporal
  - memory
  - graph
  - hippocampus
title: Temporal Lobe Subsystem
description: Blank-Slate Memory Architecture, Working Memory, Episodic/Semantic Graph, Hippocampus
---

# 03_Temporal — Memory Systems & Graph Structures

## Overview
The Temporal Lobe manages memory retention, associative recall, and knowledge graphing. In Phase 1 Foundation, this layer initializes as a **Blank-Slate** (zero pre-existing long-term memories or knowledge nodes), maintaining full interface readiness for learning.

## Key Components & Responsibilities
- **Memory Subsystem**: `runtime/memory.py` (working memory, short-term buffer)
- **Memory Graph Interface**: `runtime/memory_graph.py` (`MemoryGraph`, `MemoryNode`, `MemoryEdge`)
- **Associative Recall & Indexing**: `runtime/associative_recall.py`, `runtime/semantic_index.py`
- **Hippocampal Processing**: `regions/hippocampus.py`, `runtime/brain_memory_bridge.py`
- **Consolidation**: `runtime/memory_consolidation.py`

## Neural Connectivity & Cross-Region Pathways
- State checkpointing and safety logging to [[00_BrainStem/README|00_BrainStem (Authority & Loop)]]
- Semantic lookup and episodic context provisioning for [[01_Frontal/README|01_Frontal (Cognitive Engine)]]
- Synaptic trace recording and plasticity persistence with [[02_Parietal/README|02_Parietal (Neural Substrate)]]
- Skill acquisition feedback and sequence recall for [[04_Cerebellum/README|04_Cerebellum (Action Engine)]]
- Sensory episode binding and perceptual feature association from [[05_Occipital/README|05_Occipital (Perception)]]
- Global structural wiring map: [[BRAIN_ATLAS_MAP]]
