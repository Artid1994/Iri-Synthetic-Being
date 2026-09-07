# Controlled Autonomous Development & Phase Consolidation Protocol

Guidelines and execution pattern for Phase 12 (Hermes <-> Codex Collaboration) and Phase 13 (Controlled Autonomous Development) across autonomous architecture milestones.

## Role Separation
- **Hermes**: `Operator / Executor`. Performs local file inspection, localized patches, test runs, and Git tree inspection within repo boundaries.
- **Codex**: `Engineering Reasoning / Review`. Provides advisory analysis, invariant checking, and code reviews; advice is non-authoritative and requires local empirical verification.
- **Project Gateway**: Enforces filesystem boundaries, access permissions, and scope constraints.
- **Git**: Provides checkpoints, recovery, and audit logs. Never commit or push without explicit user command.

## Development Loop
1. `PLAN`: Calculate the smallest valid change satisfying the current phase criteria.
2. `INSPECT`: Read only relevant lines/symbols; avoid project-wide scans.
3. `IMPLEMENT`: Apply minimal localized edits (`patch`/`write_file`).
4. `TEST`: Run focused unit tests first.
5. `REVIEW`: Review diff against architectural boundaries.
6. `FIX`: On failure, follow `STOP -> DIAGNOSE -> FIX -> VERIFY` (never `FAIL -> CONTINUE`).
7. `VERIFY`: Run relevant integration tests and full regression with documented exclusions.
8. `CHECKPOINT`: Verify `git status`, `git diff --check`, and compile sanity. Await explicit user authorization before creating commits.
9. `NEXT PHASE`: Advance only after completion criteria are satisfied and recorded.

## Checkpoint Preparation & Selective Staging
- When preparing an authorized milestone checkpoint:
  - Classify files into `KEEP`, `INVESTIGATE`, and `REMOVE`.
  - Check whether UI or extraneous tooling files (e.g. editor files like `.obsidian/` or frontend styling) should be separated from core architecture commits.
  - Stage only the reviewed and approved files using targeted `git add <file1> <file2> ...`.
  - Always verify `git diff --cached --check` and `git status --short` before final commit.
