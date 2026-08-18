# AGENTS.md

## Authority
- Read `PROJECT_PLAN.md` before coding.
- `PROJECT_PLAN.md` is the project source of truth.
- Current scope: Person A only.
- Do not work on Person B.
- Do not change the ultimate project goal.

## Execution
- Work on ONE requested task only.
- Do not implement future tasks.
- Do not perform unrelated refactoring.
- Prefer the smallest additive change.
- Inspect existing code/tests before modifying anything.

## Test-First
1. Create or update a focused test.
2. Run the focused test.
3. Implement the minimum required change.
4. Run the focused test again.
5. Run the full test suite.
6. Run `git diff --check`.

## Git Safety
- Never use destructive Git commands.
- Never use force push.
- Never rewrite history.
- Never push unless explicitly instructed.
- Never delete existing tests to make them pass.
- Commit only when explicitly instructed.

## Stop Conditions
STOP and report instead of guessing if:
- the requested change conflicts with `PROJECT_PLAN.md`
- architecture must be substantially redesigned
- an existing contract must be broken
- a destructive change appears necessary
- requirements are ambiguous
- tests fail for an unrelated reason

## Output
Report only:
- files changed
- tests run/result
- remaining issue/blocker
- next action required

Do not expand scope.
