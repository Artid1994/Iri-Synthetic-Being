# Pre-Checkpoint Consolidation Classification Protocol

When preparing a repository with substantial uncommitted and untracked development for its first authorized Git checkpoint (e.g. after multi-phase roadmap completion):

## Classification Taxonomy

1. **KEEP**:
   - Production modules implementing verified roadmap phases.
   - Foundation boundaries and contracts (`BrainMemoryBridge`, `AgencyContract`, `CognitiveContext`).
   - Unit, contract, and integration tests confirming those modules.
   - Master development plans and execution rules (`MASTER_DEVELOPMENT_PLAN.md`, `AGENTS.md`).

2. **INVESTIGATE**:
   - Pre-existing uncommitted changes made prior to the current roadmap phase (e.g. UI panels, dashboard updates). Verify whether they are intentional non-breaking additions to bundle or if they belong in a dedicated UI checkpoint.
   - Untracked deleted files (e.g. `runtime/code_reviewer.py`). Confirm whether deletion was deliberate cleanup or an unintentional working-tree discrepancy.

3. **REMOVE**:
   - IDE, editor, and OS-generated metadata directories (e.g. `.obsidian/`, `.DS_Store`, `.idea/`).
   - Ensure these are added to `.gitignore` rather than committed into source history.

## Audit Workflow

- Never run destructive commands (`git clean -fd`, `git reset --hard`) during an audit.
- Confirm full test suite passes before proposing checkpoint boundaries.
- Present classified lists (KEEP, INVESTIGATE, REMOVE) clearly before requesting user commit authorization.
