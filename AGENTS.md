# AGENTS.md — AE01M / The Transcending Form

## 1. Authority

- Read `PROJECT_PLAN.md` before coding or making architectural decisions.
- `PROJECT_PLAN.md` is the project source of truth.
- Current scope: Person A only.
- Do not work on Person B/C or future scope unless explicitly requested.
- Do not change the ultimate project goal.
- If code, tests, Git history, and documentation disagree, report the discrepancy; do not silently rewrite the plan.

## 2. Task Discipline

- Work on ONE requested task only.
- Stay within the requested subsystem/files.
- Do not implement future tasks or unrelated refactoring.
- Prefer the smallest additive change.
- Inspect existing code/tests before modifying anything.
- Do not modify files unless implementation/fixing was explicitly requested.
- Do not repeat inspections already completed in the current session.

## 3. Evidence Rules

Always distinguish:

- `IMPLEMENTED` — code exists.
- `TESTED` — relevant test actually passed.
- `INTEGRATED` — an actual import/call path exists.
- `MISSING` — not found or not implemented.
- `BLOCKED` — verification was prevented by environment/dependency issues.

Never infer integration from file existence or tests alone.
Never claim a test passed unless it was actually run.
Never overclaim scientific results.

## 4. Token & Context Efficiency

The user explicitly wants Hermes to minimize token and context consumption.

- Default final response: <= 500 words.
- Simple tasks: <= 200 words.
- Do not paste source files or long logs.
- Summarize results and report only decisive evidence.
- Prefer targeted search/read over repository-wide inspection.
- Read only the file/range/symbol required for the current task.
- Stop reading once sufficient evidence is obtained.
- Do not investigate unrelated findings.
- Do not repeat broad scans.
- Do not run expensive commands unless necessary.
- If output may be large, summarize it instead of reproducing it.
- Prefer one focused command that answers one question.

### Targeted Reading Protocol

Do NOT normally read an entire large source file.

Use this order:

1. Consult `PROJECT_MAP.md` if it exists.
2. Identify the relevant file and symbol.
3. Search for the symbol/import/call site.
4. Read only the relevant line range plus a small surrounding context.
5. Expand the range only if required to understand the contract.

Line numbers are navigation hints, not permanent truth. If a file changed, search for the symbol again before relying on old line numbers.

Preferred tools/commands:
- targeted `grep`/search
- `sed -n '<start>,<end>p'`
- `git diff -- <file>`
- focused pytest paths

Do not create a project-wide index solely to avoid searching; use a map when it materially reduces repeated exploration.

## 5. PROJECT_MAP.md

`PROJECT_MAP.md` is an optimization/index file, NOT a source of truth.

- `PROJECT_PLAN.md` remains authoritative for goals and architecture decisions.
- Actual source code remains authoritative for implementation.
- Tests remain authoritative for verified behavior.
- Git history remains authoritative for change history.
- The map should contain concise file → symbol → purpose/navigation information.
- Prefer stable symbol names over hard-coded line numbers.
- Line ranges may be included as navigation hints.
- Update the map when major file/symbol locations change, but do not treat stale line numbers as facts.

Recommended format:

`runtime/memory.py`
- `Memory` — main memory container
- `Memory.recall()` — recall path
- `Memory.memory_graph` — graph integration

`runtime/cognitive_engine.py`
- `CognitiveEngine` — replaceable cognitive boundary

The map must stay small. Do not duplicate project documentation inside it.

## 6. Efficient Repository Workflow

For a normal task:

1. Read the relevant part of `PROJECT_PLAN.md` only if needed.
2. Consult `PROJECT_MAP.md`.
3. Search for the relevant symbol/call path.
4. Read the smallest useful code range.
5. Inspect focused tests.
6. Make the minimum change if authorized.
7. Run focused tests.
8. Run broader tests only when justified.
9. Run `git diff --check` before declaring completion.

Use delegation only when it materially reduces work/context.

## 7. Testing

Do not automatically run the full test suite after every change.

Run the full suite only when:
- explicitly requested,
- shared/core behavior changed,
- or focused tests cannot provide adequate confidence.

Preferred Python command:

`./.venv/bin/python -m pytest`

Report exact results, e.g. `70 passed in 1.07s`.

For implementation tasks:
1. Identify/create the smallest relevant test.
2. Run focused test.
3. Implement minimum change.
4. Run focused test again.
5. Broaden testing when justified.
6. Run `git diff --check`.

## 8. Git Safety

- Never use destructive Git commands.
- Never force-push.
- Never rewrite history.
- Never push unless explicitly instructed.
- Never delete tests to make them pass.
- Never discard user changes.
- Never commit unless explicitly instructed.
- Do not stage files merely for inspection.
- Treat untracked files as potentially intentional until verified.

## 9. AE01M Architecture Guardrails

- AI Model != Identity.
- The model is replaceable.
- Identity, Memory, Personality, Self Model, Learning, Development, and Identity Continuity remain outside the replaceable model.
- Prefer extending existing mechanisms over creating parallel systems.
- Avoid duplicate memory/learning architectures.
- Every new subsystem needs a concrete role and justified integration path.
- Do not integrate a component merely because it exists.
- Person A is the current scope.
- Numerical research is simulation/research infrastructure; do not present simulation results as physical discovery.

Current cognitive architecture target:
`Experience → Memory/Brain State → Cognitive Trigger → Cognitive Engine → Thought/Prediction/Intention → Decision/Action → Experience`

Current selected initial Cognitive Engine:
`Gemma 3 1B IT Q4_K_M` through the `llama.cpp` inference boundary.

Because target hardware is resource constrained, Cognitive Engine calls must be trigger-based rather than invoked on every perception/runtime cycle.

## 10. Learning Architecture

Conceptual reference:

`Knowledge Gap → Learning Task → Research → Verification/Practice → Knowledge/Skill`

Before integrating learning components:
- identify existing learning mechanisms,
- trace the actual call path,
- check for duplication,
- identify the minimum integration point,
- keep learning state outside the replaceable model.

Do not integrate standalone learning code without evidence that it belongs in the main cognitive loop.

## 11. Autonomous Agent Boundary

Hermes is a development agent, not project authority.

- Do not expand scope autonomously.
- Do not make architectural decisions that contradict `PROJECT_PLAN.md`.
- Do not modify unrelated files discovered during exploration.
- Report useful out-of-scope discoveries as follow-ups instead of implementing them.
- Prefer deterministic, inspectable changes.
- If requirements are ambiguous, stop and ask/report rather than guessing.

## 12. Stop Conditions

STOP and report instead of guessing if:
- the request conflicts with `PROJECT_PLAN.md`,
- architecture requires substantial redesign,
- an existing contract must be broken,
- a destructive change appears necessary,
- requirements are ambiguous,
- tests fail for an unrelated reason,
- evidence is insufficient to claim integration/correctness.

## 13. Reporting

For repository reviews:

`STATUS`
`ARCHITECTURE`
`INTEGRATION`
`TESTS`
`RISKS`
`RECOMMENDATION`

For implementation tasks report only:
- files changed
- tests run/result
- remaining issue/blocker
- next action

Keep reports concise and evidence-based.

## 14. Execution Budget

- Use at most ONE search/grep operation per task unless the result is insufficient.
- Read at most TWO source files per step unless additional files are explicitly required.
- Do not perform exploratory searches after the required evidence has been found.
- Stop immediately when the requested evidence is sufficient.
- If the requested evidence is a simple import/call-path check, prefer ONE targeted search over repeated searches. If the first search returns no integration reference, conclude NOT FOUND unless the task explicitly requires deeper verification.
