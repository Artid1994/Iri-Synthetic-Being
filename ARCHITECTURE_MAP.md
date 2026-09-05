# ARCHITECTURE_MAP.md — AE01M / The Transcending Form
# Architectural Layering, Dependency Matrix, and Subsystem Boundaries

## 1. Architectural Precedence and Layer Hierarchy

The AE01M system strictly enforces a unidirectional tiered architecture. Lower tiers have zero awareness of higher tiers. Higher tiers interact with lower tiers exclusively via defined contracts and immutable snapshots.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Tier 7: User Interface                     │
│               ui/ (App, MemoryPanel, Helpers)                  │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                   Tier 6: Autonomous & Agency                   │
│ runtime/ (AutonomousRunner, AutonomousStep, PolicyGate)         │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│              Tier 5: Cognition, Learning & Speech               │
│ runtime/ (CognitiveLoop, GemmaCognitiveEngine, Learning, Voice) │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│            Tier 4: Identity, Prediction & Reflection            │
│ runtime/ (Identity, SelfModel, Personality, Development, Pred)  │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│               Tier 3: Symbolic & Semantic Memory                │
│ runtime/ (Memory, MemoryGraph, RecallIndex, WorkingMemory)      │
└────────────────────────────────┬────────────────────────────────┘
                                 │ (via BrainMemoryBridge)
┌────────────────────────────────▼────────────────────────────────┐
│                  Tier 2: Foundation Substrate                   │
│ brain/ (Brain, NeuronPopulation, LIFNeuron, Synapse, Plasticity)│
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│               Tier 1: Configuration & Settings                  │
│ config/ (AnatomySettings, NeuronParameters, RegionParameters)   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Subsystem Boundaries and Invariants

### Tier 1: Configuration (`config/`)
- Pure dataclasses and declarative configuration parameters.
- Zero dependencies on `brain/`, `runtime/`, or `ui/`.

### Tier 2: Biological & Foundation Substrate (`brain/`)
- Components: `Neuron`, `NeuronPopulation`, `Brain`, `Synapse`, `Plasticity`, `NeuralState`.
- Rules:
  - Numerical arrays are float32/int32 NumPy structures.
  - Zero imports from `runtime/` or `ui/`.
  - Pure biophysical spiking model (LIF), chunk allocation, synaptic transmission, and Hebbian plasticity.
  - Synapse connectivity graphs are completely distinct from symbolic semantic memory graphs.

### Tier 3: Memory Systems (`runtime/memory*.py`, `runtime/memory_graph*.py`)
- Components: Episodic memory, Semantic knowledge, Association indices, Memory Graph (nodes and edges), Working memory.
- Bridge (`BrainMemoryBridge`):
  - Mediates synchronization between symbolic memory events and biological substrate allocations (e.g. hippocampus activation).
  - Snapshot isolation: operations return copies or frozen records; brain/synapse arrays are never directly exposed or mutated by memory index operations.

### Tier 4: Identity, Prediction & Development
- Components: `Identity`, `IdentityContinuity`, `SelfModel`, `Personality`, `Development`, `Prediction`.
- Rules:
  - Tracks developmental trajectory (starting newborn Person A).
  - Evaluates action consequences and maintains continuity across cycles.
  - Generates immutable `CognitiveContext` representations for reasoning.

### Tier 5: Cognition & Learning
- Components: `CognitiveLoop`, `GemmaCognitiveEngine`, `Learning`, `AutonomousLearning`, `ResearchLearning`.
- Rules:
  - Consumes `CognitiveContext` snapshot; strictly forbidden from mutating neural weights or substrate directly.
  - Issues decisions (`BodyCommand`, `RespondAction`) subject to safety gates.

### Tier 6: Autonomous Agency & Safety
- Components: `AutonomousRunner`, `AutonomousLoopController`, `SafetyPolicy`, `ResourceGuard`.
- Rules:
  - Enforces safety policy gating prior to physical/virtual actuator execution.
  - Manages cooling cycles, memory pressure, and task queues.

### Tier 7: Interface & Obsidian Integration
- Components: `ui/`, `runtime/obsidian_exporter.py`.
- Rules:
  - Observes and exports runtime state to Obsidian vault or visualization dashboards.
  - UI activation events must be driven by genuine backend telemetry (`MemoryActivationEvent`), never synthetic or decorative simulation.

---

## 3. Boundary Verification Matrix

| Boundary Contract | Enforcing Test Suite | Status |
| :--- | :--- | :--- |
| Brain ↔ Cognitive Substrate Isolation | `tests/test_brain_cognitive_boundary.py` | `VERIFIED` |
| Brain ↔ Memory Substrate Isolation | `tests/test_brain_memory_boundary.py` | `VERIFIED` |
| Role, Purpose & Agency Boundaries | `tests/test_role_purpose_boundary.py` | `VERIFIED` |
| Memory Graph Lifecycle Integrity | `tests/test_memory_graph_integration.py` | `VERIFIED` |
| Substrate Spiking & Synapse Weights | `tests/test_synapse.py`, `tests/test_plasticity.py` | `VERIFIED` |
