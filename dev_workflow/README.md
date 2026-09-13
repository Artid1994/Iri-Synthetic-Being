# IRI Development Multi-Agent Workflow Orchestrator v1.2

Development infrastructure for controlled, autonomous IRI development tasks.

**v1.2 Updates:**
- Real execution engine with inline script execution
- Actual test execution via terminal commands
- Git status and diff inspection
- Enhanced result structure (test_exit_code, commands_executed)
- Path validation and workspace isolation
- Direct Python exec for controlled script execution

**v1.1 Updates:**
- Real execution framework (HermesBuilder with execute_code integration ready)
- Context compaction implemented
- Enhanced reviewer with workspace inspection
- Automatic compaction when context threshold reached
- Improved state preservation during compaction

## Architecture

The orchestrator implements 5 logical agent roles:

### 1. Controller (WorkflowOrchestrator)
- Owns workflow state machine
- Enforces task goal and acceptance criteria
- Manages iteration lifecycle
- Prevents scope creep
- Never declares success without Final Gate evidence

### 2. Prompt + Token Auditor
- Reviews prompts before execution
- Estimates token costs (conservative heuristic: ~4 chars/token + 20% overhead)
- Removes redundant whitespace and context
- Enforces hard token budget
- Rejects prompts exceeding available budget

### 3. Hermes Builder (stub in v1)
- Executes repository work (in v1: placeholder for delegate_task integration)
- Returns structured results with evidence
- Does not control its own budget
- Tracks execution history

### 4. Independent Reviewer
- Reviews implementation independently
- Does not trust Hermes' completion claims
- Inspects repository directly (git diff, test results, changed files)
- Checks for: missing files, missing tests, acceptance criteria verification
- Returns PASS/FAIL with severity-classified findings

### 5. Final Quality Gate
- Verifies all conditions before DONE:
  - Reviewer passed
  - No critical/high findings
  - Token budget not exceeded
  - Context utilization safe
  - Iterations within limit
- Returns structured gate report

## Token Budget Control

**BudgetGovernor** enforces hard limits:

```
remaining = total_budget - used - reserved
```

Before execution:
1. Estimate required tokens
2. Reserve the amount (fails if insufficient)
3. Execute
4. Commit actual usage
5. Release unused reservation

**Guarantees:**
- Remaining budget never goes negative
- No silent budget expansion
- All token usage tracked
- Failed reservation prevents execution

## Context Control

**ContextGovernor** enforces context window limits:

### Thresholds
- SAFE: <70% utilization
- WARNING: 70-80%
- COMPACTION_REQUIRED: 80-90%
- HARD_STOP: >90%

Before execution:
1. Estimate context growth
2. Check projected utilization
3. If HARD_STOP or COMPACTION_REQUIRED → prevent execution
4. Track compaction events

**Guarantees:**
- Context cannot exceed hard limit
- Compaction triggers before critical levels
- Hard stop prevents execution beyond 90%

## Workflow State Machine

```
IDLE
  ↓
PLANNING
  ↓
PROMPT_AUDIT → (budget check) → BUDGET_STOP
  ↓
CONTEXT_CHECK → (context check) → CONTEXT_STOP
  ↓
EXECUTING
  ↓
TESTING
  ↓
REVIEWING
  ↓
  ├─ PASS → FINAL_GATE → DONE
  └─ FAIL → FIX_REQUIRED → (back to PROMPT_AUDIT)
  
Hard stops:
- BUDGET_STOP (budget exhausted)
- CONTEXT_STOP (context limit exceeded)
- ITERATION_STOP (max iterations reached)
- FAILED (unrecoverable error)
```

## Hard Stop Conditions

Workflow stops immediately when:
1. Token budget exhausted or insufficient for next iteration
2. Context utilization > 90% (HARD_STOP)
3. Max iterations reached
4. Max fix iterations reached
5. Repeated identical failures (future enhancement)

## Finding Severity

Reviewer findings are classified:

- **CRITICAL**: Must fix before PASS
- **HIGH**: Must fix before PASS
- **MEDIUM**: Fix if within scope/budget
- **LOW**: Record as technical debt
- **UNKNOWN**: Preserve; do not guess; fail-closed

## Usage

```python
from dev_workflow import WorkflowOrchestrator

orchestrator = WorkflowOrchestrator(
    task_id="task-001",
    goal="Add logging to Identity module",
    acceptance_criteria=[
        "All public methods log entry/exit",
        "Log level configurable",
        "Tests verify logging",
    ],
    total_token_budget=50000,
    context_limit=100000,
    max_iterations=5,
    max_fix_iterations=3,
)

# Execute workflow (v1: stub; v2: integrate delegate_task)
final_state = orchestrator.run()

# Get summary
print(orchestrator.get_summary())

# Save state for resume
from pathlib import Path
orchestrator.save_state(Path("logs/workflow_states/task-001.json"))
```

## Files

```
dev_workflow/
├── __init__.py          # Public API
├── state.py             # State machine and data structures
├── budget.py            # Token and context governors
├── agents.py            # Agent role implementations
├── orchestrator.py      # Main workflow controller
└── examples.py          # Usage examples

tests/
└── test_dev_workflow_orchestrator.py  # Comprehensive tests (35 tests)
```

## v1.1 Features

### Real Execution Framework
HermesBuilder now includes execution script generation and result parsing infrastructure. Ready for execute_code integration.

### Context Compaction
Automatic state compaction when context utilization reaches 80-90%:
- Preserves: goal, acceptance criteria, budget state, unresolved findings, recent iterations (last 2)
- Discards: redundant history, obsolete attempts, low-severity findings, excessive logs
- Updates context governor and state tracking

### Enhanced Review
IndependentReviewer with workspace-aware inspection capabilities.

### Compaction Workflow
```
Context 80-90% → COMPACTION_REQUIRED
↓
StateCompactor.compact()
↓
Update ContextGovernor
↓
Continue execution
```

## Tests

All critical properties verified:

**v1 Tests (35 tests):**
1. ✓ Token budget cannot be exceeded
2. ✓ Context limit cannot be exceeded
3. ✓ Reservation prevents execution when budget insufficient
4. ✓ Context warning/compaction/hard-stop thresholds work
5. ✓ Budget hard stop prevents execution
6. ✓ Context hard stop prevents execution
7. ✓ Max iterations prevents infinite loops
8. ✓ Reviewer can FAIL Hermes
9. ✓ FAIL produces minimal fix request
10. ✓ PASS reaches Final Gate
11. ✓ Final Gate requires reviewer evidence
12. ✓ Final Gate checks all conditions
13. ✓ No hidden retry bypasses accounting
14. ✓ State serialization works
15. ✓ No IRI runtime modification

**v1.1 Tests (8 additional tests):**
16. ✓ Compaction reduces state size
17. ✓ Compaction preserves critical findings
18. ✓ Compaction preserves budget state
19. ✓ Orchestrator compacts on threshold
20. ✓ Compaction updates state correctly
21. ✓ Builder executes and returns structured result
22. ✓ Builder tracks execution history
23. ✓ Workflow handles compaction integration

Run tests:
```bash
PYTHONPATH=. ./.venv/bin/python -m pytest tests/test_dev_workflow_orchestrator.py tests/test_dev_workflow_v1_1.py -v
```

Result: **43 passed in 0.37s**

## v1.1 Limitations

1. **Execution is inspection-only**: HermesBuilder framework is ready but returns inspection results only. Full implementation requires execute_code integration with actual task execution logic.

2. **Token estimation heuristic**: Uses ~4 chars/token + 20% overhead. More precise with actual tokenizer.

3. **Context estimation rough**: ~50% of token usage. More precise tracking possible with actual context measurement.

4. **Reviewer verification structural**: Checks files changed, tests run, but acceptance criteria verification still marks UNKNOWN in many cases.

5. **No automatic resume**: State is serializable and compaction preserves essentials, but resume from saved state not implemented.

6. **No parallel execution**: Single workflow at a time.

7. **Compaction is deterministic but simple**: Keeps last 2 iterations. More sophisticated strategies possible.

## What Changed from v1 → v1.1

### Added
- `dev_workflow/compaction.py`: StateCompactor for context reduction
- `tests/test_dev_workflow_v1_1.py`: 8 new tests for v1.1 features
- HermesBuilder execution framework (workspace_root parameter, script generation)
- IndependentReviewer workspace awareness
- WorkflowOrchestrator._compact_context() method
- Context compaction on COMPACTION_REQUIRED threshold
- ContextGovernor.compact(reduced_context) with actual context reduction

### Modified
- `dev_workflow/agents.py`: HermesBuilder real execution framework, enhanced reviewer
- `dev_workflow/budget.py`: ContextGovernor.compact() now updates context_used
- `dev_workflow/orchestrator.py`: Compaction integration, workspace_root support
- `dev_workflow/__init__.py`: v1.1 version, StateCompactor export
- `tests/test_dev_workflow_orchestrator.py`: Updated compaction test

### Execution Status

**v1.1 execution is INSPECTION-READY but not FULLY AUTONOMOUS:**

The HermesBuilder framework is in place:
- Script generation implemented
- Result parsing implemented  
- Workspace awareness implemented
- Token estimation implemented

However, `_execute_via_code()` currently returns inspection-only results rather than performing actual repository modifications.

**Why**: Full autonomous execution requires careful integration with the actual development task logic, which varies by task type. v1.1 provides the infrastructure; task-specific execution logic is delegated to future integration.

**This is intentional**: v1.1 establishes the control plane (budget, context, review, compaction) with execution hooks. Real task execution can now be added incrementally without redesigning the control architecture.

## Design Principles

1. **CLAIM ≠ EVIDENCE**: Agent saying "done" is not proof of completion
2. **Fail-closed on UNKNOWN**: When verification is impossible, fail rather than guess
3. **Budget is sacred**: Never silently exceed or expand token/context budgets
4. **Independent review**: Reviewer inspects repository, not just Hermes output
5. **Minimal fixes only**: Fix iterations target specific issues, not full rewrites
6. **State machine discipline**: Invalid transitions rejected
7. **Separation of concerns**: Development infrastructure stays separate from IRI cognitive architecture

## Future Enhancements (v2+)

1. Integrate `delegate_task` for actual Hermes execution
2. Implement context compaction with state preservation
3. Add automatic workflow resume from saved state
4. Integrate actual tokenizer for precise token counting
5. Add repository-specific acceptance criteria verifiers
6. Implement parallel workflow execution with locking
7. Add git operation automation (commit, push, branch)
8. Add webhook/notification on workflow completion
9. Track and prevent repeated identical failures
10. Add workflow visualization/dashboard

## No IRI Modification

This orchestrator is **development infrastructure only**.

It does NOT:
- Modify IRI's cognitive architecture
- Import from `runtime/`, `brain/`, or other IRI modules
- Add LLM dependencies to IRI
- Affect IRI's learning loops
- Modify IRI's memory or state

Verified: orchestrator modules can be imported without loading IRI runtime.
