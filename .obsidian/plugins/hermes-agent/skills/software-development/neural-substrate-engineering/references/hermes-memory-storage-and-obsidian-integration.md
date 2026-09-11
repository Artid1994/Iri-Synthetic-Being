# Hermes Memory and History Storage & Obsidian Integration Pattern

## Overview
This reference documents the exact storage boundaries, runtime initialization flow, and integration semantics between Hermes CLI / Gateway and the Obsidian Hermes Plugin.

## 1. Storage Layout and Formats
- **Terminal Session History & Transcripts:**
  - `~/.hermes/state.db` (SQLite 3 with WAL journal): Contains `sessions` (metadata, token counts, timestamps, cwd) and `messages` (role, content, tool_calls, reasoning_details) tables with FTS5 search index (`messages_fts`).
  - `~/.hermes/runtime/active_sessions.json`: Live session registry.
  - `~/.hermes/sessions/request_dump_*.json`: Raw API prompt/response logs.
  - `~/.hermes/.hermes_history`: Terminal prompt_toolkit input history (plaintext).
- **Persistent Memory:**
  - `~/.hermes/memories/USER.md`: User profile memory (markdown, separated by bare `§` lines).
  - `~/.hermes/memories/MEMORY.md`: Agent persistent memory cards (markdown, separated by bare `§` lines).
  - `~/.hermes/skills/*/SKILL.md`: Procedural memory and operational skills.

## 2. Memory Loading Flow
- **Components:**
  - `agent/agent_init.py`: Initializes `MemoryStore` during `AIAgent.__init__`.
  - `tools/memory_tool.py` (`MemoryStore.load_from_disk()`): Reads `USER.md` and `MEMORY.md`, sanitizes entries against injection threat patterns, and freezes `_system_prompt_snapshot`.
  - `agent/system_prompt.py` (`build_system_prompt_parts()`): Injects formatted memory blocks into the agent volatile system prompt block before each turn.
- **Trigger Points:**
  - Loaded once on agent startup/turn initialization.
  - Re-read from disk on session restore or prompt refresh (`rebuild_system_prompt()`).

## 3. Gateway / API Runs & Obsidian Plugin Behavior
- **API Server & `/v1/runs`:**
  - `gateway/platforms/api_server_runs.py` and `gateway/platforms/api_server.py` (`_create_agent`) spin up standard `AIAgent` instances using `run_agent.py`.
  - Unless disabled in `config.yaml`, built-in memory is active and loaded for all gateway runs.
- **Obsidian Hermes Plugin (`.obsidian/plugins/hermes-agent/main.js`):**
  - **Storage Isolation:** The plugin stores its UI conversation tree locally inside the Obsidian vault (`.obsidian/plugins/hermes-agent/history.json`). It does not directly read or write `~/.hermes/state.db`.
  - **Session IDs:** When dispatching a run, the plugin creates an isolated session ID (`obs-${Date.now()}-${uuid}`). Existing terminal CLI sessions cannot be directly resumed or attached to from Obsidian.
  - **Memory Injection:** Obsidian sessions dispatched to `/v1/runs` automatically inherit `MEMORY.md` and `USER.md` from the Hermes backend system prompt builder. A custom system prompt is **not** necessary to expose persistent memory to the agent.

## 4. Safe Read-Only Integration Rules
- **Do not modify or duplicate `state.db` or `~/.hermes/memories/` files.**
- For model execution: Rely on native Gateway `/v1/runs` injection; no extra prompt configuration needed.
- For user inspection in Obsidian note explorer: Use a read-only filesystem symlink (`ln -s ~/.hermes/memories/MEMORY.md <vault>/Hermes_Memory.md`) or the one-way deterministic exporter pattern (`runtime/obsidian_exporter.py`).
