---
brain_region: parietal
lobe: parietal
region: parietal
tags:
  - parietal
  - neural
  - substrate
  - plasticity
title: Parietal Lobe Subsystem
description: Neural Substrate, Spiking Neurons, Synaptic Connectivity, Plasticity Interface
---

# 02_Parietal — Neural Substrate & Structural Dynamics

## Overview
The Parietal Lobe models somatic structure, spatial representation, and foundational neural substrate primitives (LIF neurons, synaptic weight matrices, and plasticity rules).

## Key Components & Responsibilities
- **Neuron Substrate**: `brain/neuron.py` (`LIFNeuronVector`, membrane dynamics, leak, threshold)
- **Neural Population & State**: `brain/population.py`, `brain/neural_state.py`
- **Synaptic Connectivity**: `brain/synapse.py` (`Synapse` weight matrices, transmission)
- **Plasticity Interface**: `brain/plasticity.py` (`Plasticity` STDP / Hebbian adaptation)
- **Brain Integration**: `brain/brain.py` (orchestrating neural regions and somatic state)

## Neural Connectivity & Cross-Region Pathways
- Neuromodulatory tone and baseline regulation from [[00_BrainStem/README|00_BrainStem (Authority & Loop)]]
- Top-down executive modulation and attention focus from [[01_Frontal/README|01_Frontal (Cognitive Engine)]]
- Synaptic consolidation and hippocampal trace binding to [[03_Temporal/README|03_Temporal (Memory Systems)]]
- Sensorimotor forward model predictions and motor adjustments with [[04_Cerebellum/README|04_Cerebellum (Action Engine)]]
- Primary spatial coordinates and retinotopic projections from [[05_Occipital/README|05_Occipital (Perception)]]
- Global structural wiring map: [[BRAIN_ATLAS_MAP]]
