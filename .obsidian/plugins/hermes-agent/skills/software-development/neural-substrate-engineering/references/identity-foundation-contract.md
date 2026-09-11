# Identity Foundation Consolidation & Lifecycle Contract

Guidelines for consolidating Identity and SelfModel subsystems without scope creep or speculative architectural claims.

## Core Architectural Boundary

Identity and SelfModel are deterministic software state machines tracking stages, experience counters, and metric indicators:

```text
Identity != Role
Identity != Purpose
Identity != LLM
Identity != Memory
Identity != Brain
SelfModel != Consciousness
```

Never claim consciousness, sentience, subjective experience, or real self-awareness.

## The Identity Lifecycle Contract

In AE01M / The Transcending Form, the Phase 6 completion criterion requires:

```text
exist → accumulate experience → maintain continuity → update representation
```

### Component Roles & Ownership

1. `Identity` (`runtime/identity.py`):
   - Owns `IdentityState` (`stage`, `experience`, `identity_level`, `created_at`).
   - Restricts stage transitions to sequential steps along `VALID_STAGES`: `NEWBORN -> INFANT -> LEARNING AGENT -> DEVELOPING PERSONA -> MATURE AGENT`.
   - Rejects negative experience additions and invalid non-sequential stage jumps.

2. `IdentityContinuity` (`runtime/identity_continuity.py`):
   - Owns `IdentityContinuityState` (frozen snapshot record).
   - Records transitions via immutable snapshots (`snapshot_count`, `last_stage`, `last_experience`).
   - Produces detached, immutable snapshots so history is preserved across subsequent state mutations.

3. `IdentityRepresentation` (`runtime/identity_representation.py`):
   - Provides a frozen, detached view of structured memory (`episodic: tuple[str, ...]`, `semantic: tuple[str, ...]`).
   - Constructed via `from_structured_memory(memory.snapshot())`.
   - Immutable tuples ensure that future mutations to `Memory` cannot retroactively alter an existing representation instance.

4. `SelfModel` (`runtime/self_model.py`):
   - Owns `SelfModelState` (`self_awareness`, `self_knowledge`, `goals`, `beliefs`, `self_history`).
   - Updates awareness and knowledge deltas with numeric clamping bounded strictly to `[0.0, 1.0]`.
   - Records discrete history events as strings.

5. `Development` (`runtime/development.py`):
   - Orchestrates experience synchronization from accepted learning candidate evaluations.
   - Evaluates developmental criteria policies against collected `DevelopmentCriteriaEvidence`.

## Testing Pattern

Validate the entire lifecycle end-to-end with deterministic behavioral tests (see `tests/test_identity_foundation.py`):
- Stage transitions must be strictly sequential.
- Negative experience must raise `ValueError`.
- Snapshots returned by `IdentityContinuity` and `IdentityRepresentation` must be copy-isolated and immune to subsequent source mutations.
- Numeric metrics in `SelfModel` must clamp cleanly at 0.0 and 1.0.
- `Development.sync()` and `evaluate_stage()` must operate cleanly with mock learning/prediction evaluations without modifying production code.
