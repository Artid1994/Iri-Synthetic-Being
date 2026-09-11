# Obsidian-Style Desktop Workspace Pattern for AE01M

When adapting or designing desktop GUI frontends (e.g. Tkinter) for autonomous cognitive architectures to match an Obsidian-like UX while preserving underlying backend models:

## Key Structural Components

1. **Top Command & Quick-Switcher Bar:**
   - Obsidian dark palette base (`#16161a`, `#1e1e24`, `#22222a`, `#30303c`).
   - Integrated quick-switcher entry (`Ctrl+K`) for commands/quick navigation.
   - Status chips (e.g., policy gate mode: `● HUMAN GATED`, manual sync triggers).

2. **Left Navigation Sidebar:**
   - Slim vertical ribbon or compact sidebar (`width: 220px`).
   - Clean iconography + tab titles (`Chat`, `Memory`, `Brain`, `Research`, `Learning`, `System`).
   - Direct hotkey accelerators (`Ctrl+1` through `Ctrl+6`).
   - Bottom state widgets (active developmental stage, cumulative cycles).

3. **Central Tabbed Editor Workspace:**
   - Top tab headers (`bg: #16161a`, active: `#22222a` with text highlight).
   - Swappable container frames (`grid(row=0, column=0, sticky='nsew')` / `grid_forget()`).
   - Embedded Chat workspace styled like an editor note with distinct user/agent tags.
   - Canvas-based Memory graph with force-directed relaxation and dynamic activity pulse animations.

4. **Right Context / Properties Inspector:**
   - Persistent property metadata (`Identity Stage`, `Self-Awareness`, `Active Goals`, `Memory counts`).
   - Safety boundary summary (active safety gates, resource bounds).

5. **Bottom Status Bar:**
   - Discrete status indicators (`Ready`, `Memory: OK`, `Safety: Active`).

## Non-Destructive GUI Refactoring Rule
- Never modify the underlying cognitive model or runtime interfaces for styling.
- Feed GUI views exclusively via isolated runtime snapshots (`runtime_snapshot.capture()`).
- Separate UI commits from core cognitive architecture checkpoints.
