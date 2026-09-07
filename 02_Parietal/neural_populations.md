---
brain_region: parietal
lobe: parietal
region: parietal
tags:
  - parietal
  - neurons
  - substrate
title: Parietal Neural Populations
description: Leaky Integrate-and-Fire neurons, node vectors, and state tensors
---

# Parietal Neural Populations

Implements biological-grade Leaky Integrate-and-Fire (LIF) dynamics, membrane potentials, and population spikes.

## Neural Signal Pathways
- Anchored to [[02_Parietal/README|Parietal Lobe Subsystem]]
- Receives projections from [[02_Parietal/spatial_substrate|Spatial Neural Substrate]]
- Transmits spike vectors across [[02_Parietal/synaptic_matrix|Synaptic Matrix]]
- Modulates somatic state fed back into [[00_BrainStem/README|BrainStem Subsystem]]
- Interconnects with [[04_Cerebellum/learning_loop|Cerebellar Learning Loop]] for sensorimotor calibration
