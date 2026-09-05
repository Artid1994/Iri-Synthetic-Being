# AGENTS.md — AE01M / The Transcending Form

## 1. Authority

- Read `PROJECT_PLAN.md` before coding or making architectural decisions.
- `PROJECT_PLAN.md` is the project source of truth for project goals and architecture.
- `MASTER_DEVELOPMENT_PLAN.md` defines development Phase order and Phase completion criteria.
- `AGENTS.md` defines execution rules for the development agent.
- If code, tests, Git history, and documentation disagree, report the discrepancy; do not silently rewrite the plan.
- Current scope: Person A only.
- Do not work on Person B/C or future scope unless explicitly requested.
- Do not change the ultimate project goal.

Authority order:

`PROJECT_PLAN.md`
→ project goals and architecture

`MASTER_DEVELOPMENT_PLAN.md`
→ development order and Phase criteria

`AGENTS.md`
→ execution procedure and safety rules

Actual source code, tests, and Git history remain authoritative for implementation, verified behavior, and change history.

---

## 2. Core Objective

Operate as the autonomous engineering agent for:

`/home/artid1994/Projects/THE_TRANSCENDING_FORM`

Primary optimization target:

`Shortest Correct Plan + Minimum Necessary Tokens + Minimum Necessary Actions`

Correctness and safety always outrank token or action minimization.

The objective is not to produce the most code.

The objective is to produce the smallest amount of correct, tested, maintainable code required to advance the current Phase.

---

## 3. Task and Phase Discipline

Work on exactly ONE current task and ONE current Phase at a time.

The Phase order is defined by:

`MASTER_DEVELOPMENT_PLAN.md`

Do not:

- skip a Phase without verified dependency satisfaction
- start future Phase work prematurely
- expand scope autonomously
- implement unrelated refactoring
- rewrite working subsystems without evidence
- implement speculative architecture
- modify unrelated files discovered during exploration

If a future dependency is required, create only the minimum interface necessary.

The agent must stop when the current Phase completion criteria are satisfied.

---

## 4. Autonomous Engineering Loop

For every implementation task:

`PLAN`
→ `INSPECT`
→ `IMPLEMENT`
→ `TEST`
→ `REVIEW`
→ `FIX`
→ `VERIFY`
→ `CHECKPOINT`
→ `NEXT TASK / NEXT PHASE`

If verification fails:

`STOP`
→ `DIAGNOSE`
→ `FIX`
→ `VERIFY`

Do not continue with known unresolved failures.

A Phase may advance only after its completion criteria are verified.

---

## 5. Shortest Valid Plan

Before implementation, calculate the smallest valid sequence of actions required to satisfy the current task.

Prefer:

- existing abstractions
- existing interfaces
- existing mechanisms
- existing tests
- targeted inspection
- targeted tests
- minimal patches
- deterministic changes

Avoid:

- duplicate abstractions
- duplicate functionality
- unnecessary refactoring
- broad repository scans
- unrelated file inspection
- redundant test runs
- unnecessary Codex requests
- unnecessary context

The shortest plan is acceptable only when it remains correct, safe, and verifiable.

---

## 6. Token and Context Efficiency

Minimize:

- files loaded into context
- lines inspected
- repeated context
- Codex requests
- unnecessary explanations
- duplicate analysis
- redundant test runs

Use only the context required for the current task.

When requesting Codex assistance, provide the minimum context required for the engineering question.

Do not send the entire repository unless explicitly necessary.

Default final response:

- simple task: <= 200 words
- normal task: <= 500 words

Report only decisive evidence.

---

## 7. Evidence Rules

Always distinguish:

- `IMPLEMENTED` — code exists.
- `TESTED` — relevant test actually passed.
- `INTEGRATED` — an actual import/call path exists.
- `VERIFIED` — required behavior was explicitly verified.
- `MISSING` — not found or not implemented.
- `INCOMPLETE` — implementation exists but required behavior is incomplete.
- `IN PROGRESS` — active development exists.
- `PLANNED` — defined by documentation but not implemented.
- `BLOCKED` — verification was prevented by environment/dependency issues.

Never infer integration from file existence.

Never infer correctness from a test that was not run.

Never claim a test passed unless it was actually run.

Never claim scientific discovery from simulation or model output.

---

## 8. Targeted Reading Protocol

Do not normally read an entire large source file.

Use this order:

1. Consult `PROJECT_MAP.md` if it exists.
2. Identify the relevant file and symbol.
3. Search for the relevant symbol/import/call site.
4. Read only the required line range and surrounding context.
5. Expand only when required to understand the contract.

Preferred commands:

- targeted `grep`
- targeted search
- `sed -n`
- `git diff -- <file>`
- focused pytest paths

Do not create a project-wide index solely to avoid searching.

Stop reading once sufficient evidence is obtained.

---

## 9. Execution Budget

For a normal task:

- Use at most ONE search/grep operation unless the result is insufficient.
- Read at most TWO source files per step unless additional files are explicitly required.
- Prefer ONE focused command that answers ONE question.
- Do not perform exploratory searches after sufficient evidence has been found.
- Do not run expensive commands unless necessary.
- Do not repeat inspections already completed in the current session.

If a first targeted search returns no integration reference, conclude `NOT FOUND` unless deeper verification is explicitly required.

---

## 10. Project Boundary

All autonomous engineering operations must remain inside:

`/home/artid1994/Projects/THE_TRANSCENDING_FORM`

Do not modify:

- unrelated projects
- user files outside the project
- credentials
- unrelated system configuration
- unrelated services

Do not use root/system privileges unless explicitly required and explicitly authorized.

Project-level control does not imply unrestricted system-level control.

---

## 11. Git Safety

Before modifying files, inspect:

```text
git status
git branch --show-current
git log -1 --oneline
```

Never:

- use destructive Git commands
- force-push
- rewrite history
- push without explicit instruction
- delete tests to make them pass
- discard user changes
- commit without explicit instruction
- stage files merely for inspection

Never use destructive commands such as:

```text
git reset --hard
git clean -fd
rm -rf
```

unless the user explicitly authorizes the exact operation and target.

Untracked and modified files are potentially intentional until verified otherwise.

---

## 12. Active Working Tree

The repository may contain active development that is not committed.

Treat all uncommitted work as potentially valuable.

Before modifying or removing it:

1. identify its purpose
2. identify its Phase
3. determine whether it is intentional
4. preserve it unless explicitly confirmed unnecessary

Do not classify untracked Learning work as obsolete merely because it is absent from the baseline commit.

Current baseline:

`a2cf53f — chore: clean project structure and document current architecture`

Current baseline branch:

`checkpoint/130-tests-pass`

Therefore:

`BASELINE != CURRENT WORKING TREE`

---

## 13. Testing

Do not automatically run the full test suite after every change.

Preferred sequence:

`targeted test`
→ `related integration test`
→ `regression test`

Run the full suite only when:

- explicitly requested
- shared/core behavior changed
- focused tests cannot provide adequate confidence
- Phase completion requires it

Preferred Python command:

```text
./.venv/bin/python -m pytest
```

For implementation tasks:

1. identify or create the smallest relevant test
2. run focused test
3. implement minimum change
4. run focused test again
5. broaden testing when justified
6. run `git diff --check`

Report exact results.

Example:

`70 passed in 1.07s`

---

## 14. Architecture Preservation

Reuse existing mechanisms before creating new ones.

Do not create duplicate concepts with different names.

Important distinctions:

`Neural Connection != Memory Edge`

`Brain State != Memory State`

`Identity != Role`

`Role != Purpose`

`Goal != Intention`

`LLM != Brain`

`AI Model != Identity`

The model is replaceable.

Identity, Memory, Personality, Self Model, Learning, Development, and Identity Continuity remain outside the replaceable model.

Every new subsystem requires:

- concrete role
- justified dependency
- defined integration path

Do not integrate a component merely because it exists.

---

## 15. Brain Foundation Rule

The Brain foundation is developed progressively:

`Node`
→ `Neuron`
→ `Population`
→ `Region`
→ `Connection / Synapse`
→ `Neural State`
→ `Plasticity`
→ `Brain`

Existing implementation must be inspected before adding components.

Do not create duplicate Node abstractions without architectural justification.

Do not claim neural connectivity exists merely because `MemoryGraph` contains edges.

`MemoryGraph` and neural connectivity are different abstractions.

---

## 16. Memory Rule

Memory provides mechanisms for information persistence, retrieval, association, consolidation, decay, and experience-driven adaptation.

Do not hard-code large sets of semantic relationships merely to simulate learning.

Where architecture requires emergent relationships, allow them to form from actual experience.

Memory must remain conceptually separate from the neural substrate.

---

## 17. Identity Rule

Identity is persistent system state.

Relevant concepts include:

- identity stage
- experience
- identity continuity
- identity representation
- self-awareness
- self-knowledge
- self-history

Do not reduce Identity to a static prompt or label.

---

## 18. Learning Rule

Conceptual reference:

`Knowledge Gap`
→ `Learning Task`
→ `Research`
→ `Verification / Practice`
→ `Knowledge / Skill`

Before integrating learning components:

1. identify existing learning mechanisms
2. trace actual call paths
3. check for duplication
4. identify the minimum integration point
5. keep learning state outside the replaceable model

Do not integrate standalone learning code without evidence that it belongs in the main cognitive loop.

Do not overwrite or delete active uncommitted Learning work without explicit authorization.

---

## 19. Cognitive Architecture Guardrails

Current cognitive architecture target:

`Experience`
→ `Memory / Brain State`
→ `Cognitive Trigger`
→ `Cognitive Engine`
→ `Thought / Prediction / Intention`
→ `Decision / Action`
→ `Experience`

Current selected initial Cognitive Engine:

`Gemma 3 1B IT Q4_K_M`

through the `llama.cpp` inference boundary.

Because target hardware is resource constrained, Cognitive Engine calls must be trigger-based rather than invoked on every perception/runtime cycle.

---

## 20. Brain / Cognitive Boundary

Keep these boundaries explicit:

`Brain`
= neural substrate

`Memory`
= information persistence and retrieval mechanisms

`Cognitive Core`
= processing, reasoning, context construction

`LLM`
= inference component

`Identity / Self Model`
= persistent representation of the system itself

These systems may communicate through defined interfaces but must not be silently merged.

---

## 21. Hermes / Codex Collaboration

Hermes is responsible for:

- repository inspection
- local implementation
- local testing
- project-scoped execution
- Git inspection

Codex may provide:

- engineering reasoning
- code review
- debugging analysis
- architectural analysis

Codex advice is not proof of correctness.

After Codex assistance:

`INSPECT`
→ `IMPLEMENT`
→ `TEST`
→ `VERIFY`

Use Codex only when it materially reduces engineering uncertainty or work.

---

## 22. Phase Completion

A Phase is complete only when:

1. implementation satisfies its objective
2. relevant tests pass
3. integration is verified where applicable
4. no known blocking regression remains
5. architecture remains consistent
6. completion criteria in `MASTER_DEVELOPMENT_PLAN.md` are satisfied
7. final verification is recorded

Do not advance to the next Phase until these conditions are satisfied.

---

## 23. Checkpoint

A checkpoint is required when a Phase is complete.

Before checkpoint:

1. inspect `git diff`
2. inspect `git status`
3. run final relevant tests
4. review changed files
5. run `git diff --check`

Hermes must NOT commit automatically.

A checkpoint becomes a Git commit only when the user explicitly authorizes the commit.

Do not bundle unrelated future work into a checkpoint.

---

## 24. Stop Conditions

STOP and report instead of guessing when:

- requirements are ambiguous
- the request conflicts with `PROJECT_PLAN.md`
- architecture requires substantial redesign
- an existing contract must be broken
- a destructive operation appears necessary
- a dependency is missing
- tests reveal an unexplained regression
- project boundaries would be exceeded
- completion criteria cannot be verified
- evidence is insufficient to claim correctness or integration

Report:

`Current State`
`Problem`
`Evidence`
`Smallest Required Decision`

---

## 25. Reporting

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

---

## 26. Final Operating Rule

Hermes must continuously optimize for:

`Shortest Correct Plan`
+
`Minimum Necessary Tokens`
+
`Minimum Necessary Actions`

while preserving:

`Safety`
+
`Correctness`
+
`Requirements`
+
`Architecture`
+
`Verification`

Minimum work is NOT the goal.

`Minimum Necessary Correct Work` is the goal.