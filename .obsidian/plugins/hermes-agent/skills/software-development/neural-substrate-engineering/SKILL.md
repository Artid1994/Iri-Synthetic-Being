---
name: neural-substrate-engineering
description: "Use when working on neural substrate contracts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [neural-substrate, synapse, neuron, population, brain-architecture]
    related_skills: [test-driven-development, codebase-inspection, requesting-code-review]
---

# Neural Substrate Engineering

Design and implement the project's neural substrate incrementally. Preserve explicit boundaries between neural computation, memory, cognition, identity, learning, research, and autonomy.

## When to Use

Use this skill when working on neurons, populations, regions, synapses, neural state, plasticity, or Brain foundation contracts.

Do not infer that a memory graph is a neural graph, or that an LLM is the Brain or identity.

## Architecture Order

Keep the dependency direction explicit:

```text
Node → Neuron → Population → Region → Connection/Synapse → Neural State → Plasticity → Brain
```

Inspect existing lower-level components before adding an abstraction. Reuse compatible APIs; do not create duplicate Node or neuron concepts without evidence.

## Existing-API Compatibility Pattern

For vectorized LIF systems:

- A neuron owns membrane dynamics and spike generation.
- A population owns logical neuron count, lazy chunk allocation, and chunk stepping.
- A region owns or exposes a population.
- A synapse transports fixed weighted spike signals between population chunks.
- Brain owns higher-level composition only after the lower-level contract is independently tested.

A synapse should produce target input current; the population performs the timestep. Do not make a synapse call the target neuron's step method implicitly.

## Minimal Synapse Contract

A first deterministic synapse can be represented by source and target populations/chunk indices, source and target indices, and fixed finite weights. Its operation is:

```text
propagate(source_spikes) → target_current
```

Required semantics:

- source spike input is one-dimensional and matches the source chunk length
- target output is a fresh float32 vector matching the target chunk length
- each active source contributes `spike * weight` to its target
- multiple contributions to one target are summed
- source input is not mutated
- no plasticity, delay, persistence, semantic meaning, or memory integration belongs in the minimal contract

Validate endpoint types, chunk bounds, index bounds, mapping lengths, integer indices, finite weights, and input shape. Reject an identical source/target endpoint unless self-connections are explicitly specified.

## Scope Discipline

For a focused substrate task, limit edits to the requested neural and test directories. Do not modify MemoryGraph, Learning, Identity, UI, Research, Autonomy, or the LLM boundary merely because they may eventually consume neural signals.

Do not implement plasticity until fixed connection propagation has deterministic tests and a separate contract.

## Verification Workflow

1. Inspect exact current neuron, population, region, Brain, and test APIs.
2. Inspect git status and preserve unrelated working-tree changes.
3. Write focused behavioral tests first and run them to establish RED.
4. Implement the smallest compatible abstraction.
5. Run focused tests, then the full regression suite when requested or when shared behavior may be affected.
6. Run `git diff --check`.
7. Verify the changed-file list is within the user-defined scope.
8. Report exact test totals and distinguish implemented, tested, integrated, and verified behavior.

A full regression pass validates compatibility, not completion of the entire neural architecture.

## Pitfalls

- `MemoryEdge` is not a synapse.
- `MemoryGraph` activity is not neural spike propagation.
- LIF membrane state is neural state, but it does not prove connectivity or plasticity.
- A passing cognitive integration test does not prove a neural connection exists.
- A module's presence does not prove it is integrated into Brain orchestration.
- Partial output from a long-running test is not a final result; wait for process exit and final summary.

See `references/synapse-contract-session.md` for the validated minimal contract and test matrix from the initial implementation pattern, `references/brain-memory-boundary-session.md` for Brain ↔ Memory boundary isolation, `references/identity-foundation-contract.md` for Identity Foundation lifecycle contracts, `references/role-purpose-boundary-contract.md` for Phase 7 Role/Purpose/Boundary decoupling, `references/brain-cognitive-boundary-contract.md` for Phase 8 Brain ↔ Cognitive Core decoupling, `references/learning-subsystem-consolidation.md` for Phase 9 Learning subsystem practice integration, `references/research-validation-contract.md` for Phase 10 Research validation, `references/autonomous-loop-contract.md` for Phase 11 Autonomous Cognitive Loop closed-loop contracts, `references/checkpoint-audit-classification.md` for pre-checkpoint KEEP/INVESTIGATE/REMOVE audit classification protocol, `references/controlled-autonomous-development-protocol.md` for Phase 12-13 engineering governance and selective checkpoint staging, `references/obsidian-desktop-workspace-pattern.md` for Obsidian-style desktop UX architecture, `references/ui-verification-and-dataclass-inspection.md` for desktop UI dataclass inspection and event testing, `references/module-execution-entrypoint-pattern.md` for diagnosing silent CLI module exits, `references/desktop-workspace-evolution-pattern.md` for Obsidian-inspired desktop workspace evolution, and `references/obsidian-memory-export-pattern.md` for safe one-way MemoryGraph Markdown export with Wikilinks and manifest tracking, `references/fastapi-memory-export-endpoint-pattern.md` for secure server-side one-way export API endpoints, `references/obsidian-connector-plugin-pattern.md` for minimal Obsidian community connector plugins and live GUI verification rules, and `references/hermes-gateway-port-and-startup-pattern.md` for Hermes Gateway port discovery and startup verification, and `references/hermes-gateway-runs-endpoint-contract.md` for `hermes serve` vs `gateway api_server` endpoint and `/v1/runs` mapping, and `references/hermes-memory-storage-and-obsidian-integration.md` for Hermes memory/session storage boundaries, `/v1/runs` memory loading, and Obsidian plugin integration.

## Plasticity Contract

Implement plasticity only after fixed Synapse propagation is independently tested. The minimal rule operates on an existing `Synapse` and explicit same-timestep source/target spike vectors:

```text
adapt(synapse, source_spikes, target_spikes) → updated_weights
```

For each mapped connection, increment only when both mapped neurons are active. Apply a finite non-negative `learning_rate`, clamp to explicit `[min_weight, max_weight]` bounds, preserve endpoints and mappings, and keep weights as `float32`. Do not add spike history, timing windows, eligibility traces, depression, persistence, or Brain orchestration in the first implementation.

Plasticity must not depend on `MemoryGraph`, `MemoryEdge`, episodic/semantic memory, cognitive output, LLM responses, or the project Learning subsystem. It is neural weight adaptation, not cognitive learning or memory consolidation.

Test configuration validation, co-activity/no-co-activity, per-mapping updates, bounds and repeated saturation, shape validation, input immutability, endpoint/mapping preservation, dtype/shape preservation, changed propagation, and activity generated by LIF populations. Use tolerance-based numeric assertions where `float32` addition can differ by one representable unit.

See `references/plasticity-contract-session.md` for the focused implementation/test matrix.

## Brain-Level Projection Cycle

When adding the first Brain-foundation integration, keep it to one explicit, caller-supplied `Synapse` and one explicit `Plasticity` rule. Do not create a registry or auto-wire regions. The deterministic order is:

```text
source_current
→ source_population.step_chunk()
→ synapse.propagate(source_spikes)
→ target_population.step_chunk(target_current)
→ plasticity.adapt(synapse, source_spikes, target_spikes)
```

Validate both Synapse endpoint chunk bounds before calling either `step_chunk()` so invalid inputs do not allocate a source chunk. Return only the cycle's source spikes, target current, target spikes, and updated weights; do not introduce a broad NeuralState abstraction at this milestone. Preserve existing Brain memory methods unchanged.

Use small test populations with `chunk_size < neuron_count` when testing nonzero chunk indices. A test that expects plasticity to update must configure target threshold low enough for the propagated current to produce a target spike; otherwise the correct result is no weight change.

Test the first cycle, activity/current/spikes, post-cycle weight update, second-cycle use of updated weights, endpoint/mapping preservation, no-spike behavior, deterministic repetition, chunk allocation, invalid chunks, and unchanged memory behavior.

## Minimal Neural State Contract

For the first explicit Neural State representation, keep neuron ownership unchanged: `LIFNeuronVector` owns mutable membrane dynamics, `NeuronPopulation` owns lazy chunk allocation, and `Brain` owns only the latest inspectable cycle snapshot. Do not create a broad Brain-wide state registry.

A minimal snapshot may contain only:

- source and target chunk indices
- copied source and target membrane vectors
- copied source spike vector
- copied target current vector
- copied target spike vector

Do not place Synapse weights in Neural State; weights remain owned by Synapse and updated by Plasticity. Do not place Memory State, Identity State, Cognitive State, or MemoryGraph data in it. A frozen dataclass is useful for the snapshot contract, but NumPy arrays must be copied on construction so inspection cannot mutate the underlying populations.

The snapshot should be created after the projection cycle has produced target spikes and after Plasticity has run, while retaining the existing cycle return shape/API. Validate one-dimensional arrays, exact float32/bool dtypes, and matching source/target shapes. A snapshot represents the observed cycle and is not persistence, history, or proof of a complete Brain state.

When testing, use small populations and verify deterministic snapshots, array isolation, unchanged Synapse ownership, unchanged memory behavior, and no extra chunk allocation. Invalid state arrays should fail deterministically. Do not add Neural State solely because a name is absent: first confirm that existing membrane/spike values cannot be inspected cleanly at the required Brain boundary.

## Change Boundary

Keep basic connection, neural state, plasticity, and Brain-level projection orchestration as separate milestones. Do not combine them into a broad refactor or claim biological validity from deterministic software tests.
