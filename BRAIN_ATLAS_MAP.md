---
brain_region: stem
title: Brain Atlas Map — Functional Neural Pathways
description: Mapping of the 6 core functional regions and neural pathways for Obsidian Brain Atlas
---

# Brain Atlas Map — Functional Neural Pathways

This document integrates the AE01M Blank-Slate Cognitive Architecture with the Obsidian Brain Atlas plugin. It describes the 6 core functional brain regions, their architectural responsibilities, and the directional signal pathways connecting them.

```
       [05_Occipital] (Perception / Sensory Input)
              │
              ▼
       [01_Frontal] ◄──────────────► [03_Temporal]
  (Cognitive Engine / Gemma 3)     (Blank Slate Memory / Graph)
              │                               ▲
              ▼                               │
       [02_Parietal]                          │
  (Neural Substrate: LIF / Synapse / Plasticity)
              │
              ▼
       [04_Cerebellum] ─── Feedback ──────────┘
  (Action Dispatcher / Autonomous Loop / Verification)
              ▲
              │
       [00_BrainStem]
  (Authority, Safety Gate, Heartbeat Runtime Loop)
```

---

## 1. Regional Breakdown & Mappings

| Directory | Region Key (`brain_region`) | Subsystem Function | Key Files / Interfaces |
|---|---|---|---|
| `00_BrainStem/` | `stem` | Authority, Safety Policies, Core Runtime Loop, Heartbeat | `AGENTS.md`, `runtime/runtime.py`, `runtime/autonomous_gate.py` |
| `01_Frontal/` | `frontal` | Cognitive Engine, Gemma 3 1B Inference Boundary, Reasoning, Goals | `runtime/gemma_cognitive_engine.py`, `runtime/cognitive_loop.py`, `runtime/goal.py` |
| `02_Parietal/` | `parietal` | Neural Substrate, LIF Neurons, Synaptic Arrays, Plasticity Interface | `brain/neuron.py`, `brain/synapse.py`, `brain/plasticity.py`, `brain/population.py` |
| `03_Temporal/` | `temporal` | Blank-Slate Short-Term Buffer, Memory Graph, Associative Indices | `runtime/memory.py`, `runtime/memory_graph.py`, `regions/hippocampus.py` |
| `04_Cerebellum/` | `cerebellum` | Autonomous Learning Loop, Action Dispatcher, Motor & Pytest Verification | `runtime/learning.py`, `runtime/action.py`, `runtime/autonomous_runner.py`, `tests/` |
| `05_Occipital/` | `occipital` | Sensory Perception, Observation Ingestion, Multimodal Adapters | `runtime/perception.py`, `runtime/sensor.py`, `runtime/world_observation.py` |

---

## 2. Functional Neural Pathways

1. **Perception Ingestion (`05_Occipital` -> `01_Frontal`)**:
   Sensory observations and environmental payloads enter through Occipital handlers and are structured for cognitive evaluation.
2. **Cognitive Reasoning & Deliberation (`01_Frontal` <-> `03_Temporal`)**:
   The Gemma 3 inference engine consults working memory and the blank-slate memory graph to evaluate context and deliberate on actions.
3. **Somatic & Substrate Projection (`01_Frontal` -> `02_Parietal`)**:
   Cognitive impulses project activations into the LIF neural populations and synaptic matrices within the Parietal layer.
4. **Action Dispatch & Motor Coordination (`02_Parietal` -> `04_Cerebellum`)**:
   Neural activations translate into concrete actions dispatched via the Cerebellum.
5. **Feedback & Plasticity Adaptation (`04_Cerebellum` -> `03_Temporal` / `02_Parietal`)**:
   Execution outcomes generate experiences that update memory graphs and tune synaptic weights via plasticity rules.
6. **Regulatory Oversight (`00_BrainStem` -> All Regions)**:
   The BrainStem maintains the clock cycle, heartbeat telemetry, and enforces safety gate approval boundaries across all regional operations.
