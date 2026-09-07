# Phase 10 Research Validation Contract

## Architecture
Phase 10 consolidates the scientific research execution loop:
```text
Question → Hypothesis/Proposal → Evidence → Experiment/Calculation → Evaluation → Record
```

Key invariants:
- **No Unconditional Acceptance**: AI model proposals are parsed via `ResearchProposal.parse()` with strict constraints.
- **Empirical/Dynamical Calculation**: Evaluates hypotheses against reference dynamical benchmarks (e.g. quantum decoherence models in `NumericalResearch`).
- **Deterministic Error Gating**: Acceptance is governed by explicit numerical tolerance thresholds.
- **Persistent Evidence Trail**: All accepted and rejected iterations maintain structured history records with timestamps and metrics.
- **Separation from Substrate**: Research operates strictly on calculations and strings; it has no direct connection to neural membrane voltages or synaptic weights.
- **Safety Gate**: Research retrieval passes through `ResearchSafetyGate` before reaching candidate learning.
