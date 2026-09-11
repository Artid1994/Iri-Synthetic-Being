# Hermes Agent Obsidian Plugin Feasibility Audit Pattern

## Objective
Evaluate whether an existing third-party or local Hermes Agent Obsidian plugin can serve as the primary developer / AI interaction interface for an autonomous cognitive architecture without compromising runtime isolation, security boundaries, or project ownership.

## Key Principles
1. **Never Assume Plugin Identity from Name Alone:**
   - Inspect `.obsidian/plugins/<plugin-id>/manifest.json` for exact `id`, `name`, `author`, `version`, and `description`.
   - Inspect `main.js` to determine whether it embeds a runtime or simply communicates with a local gateway over HTTP/SSE.
2. **Strict Architectural Decoupling:**
   - **Obsidian Workspace:** UI / Knowledge surface / Note viewer.
   - **Hermes Agent Plugin:** Local client sending requests to Hermes Agent Gateway (`http://127.0.0.1:8642`).
   - **Hermes Agent:** Developer / Operator executing local tools and terminal commands.
   - **AE01M Engine:** In-memory Python cognitive substrate, memory graph, and learning engine.
   - **AE01M Connector Plugin:** Dedicated single-purpose projection bridge (e.g. `POST /api/memory/export`).
3. **Preserve Single Responsibility:**
   - Do NOT collapse the developer assistant (`hermes-agent`) into the domain engine connector (`ae01m-connector`).
   - The cognitive engine must remain 100% headless and executable without Obsidian or Hermes running.
4. **Git & Config Integrity:**
   - Never stage or commit `.obsidian/` metadata (`graph.json`, `workspace.json`) into Git unless explicitly instructed.
   - Inspect and immediately restore any unintended config modifications introduced by background Obsidian processes.
