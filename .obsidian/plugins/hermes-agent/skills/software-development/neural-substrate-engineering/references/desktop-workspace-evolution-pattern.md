# Desktop Workspace Evolution Pattern: Obsidian-Inspired Cognitive Shell

When evolving an existing AI cognitive architecture or scientific project into a desktop application inspired by Obsidian (or similar workspace-oriented desktop apps):

## Core Design Principle
The desktop workspace must remain a presentation/control shell around the core engine, NOT a replacement for the underlying cognitive architecture or data model.

1. **Independent Product & Source Code**: Never use Obsidian as a runtime dependency or copy its proprietary source code/assets. Re-implement workspace primitives natively using existing GUI frameworks (e.g. Tkinter, Qt).
2. **Distinct Product Identity**: Visual design should be informed by the productive workflow (three-column layout, command palettes, markdown/canvas workspaces), but branded and architected specifically for the project.
3. **Strict Boundary**: Core subsystems (Brain, Memory, Identity, Learning, Research, Safety) communicate with the UI purely via detached state snapshots or adapter interfaces (e.g. `RuntimeSnapshot`). The UI never directly manipulates private substrate internals.

## Architectural Layers
```text
Project Core Subsystems (Neural, Memory, Agency, Learning, Safety)
   ↓ (read snapshots / dispatch safe actions)
UI State / Workspace Adapter (RuntimeSnapshot, CommandRegistry)
   ↓ (binds state & dispatch)
Desktop Workspace Shell (Top Command Bar, Left Nav, Central Workspace, Right Inspector, Status Bar)
```

## Progressive Capabilities Roadmap
1. **Audit & Scope Mapping**: Inventory existing GUI capabilities vs target workspace features before coding.
2. **Paned / Split View Workspace**: Replace fixed frame containers with split panes (e.g. `ttk.PanedWindow`) allowing simultaneous side-by-side or stacked views (e.g. Chat alongside Memory Graph).
3. **Vault / File Navigator**: Provide lightweight project file browsing in the sidebar for docs and research logs.
4. **Command Palette (`Ctrl+P` / `Ctrl+K`)**: Register modal actions (run exercise, sync memory, switch tabs) without cluttering the screen.
5. **Interactive Context / Backlinks**: Connect node/item selections in graphs or notes to live property inspectors.
