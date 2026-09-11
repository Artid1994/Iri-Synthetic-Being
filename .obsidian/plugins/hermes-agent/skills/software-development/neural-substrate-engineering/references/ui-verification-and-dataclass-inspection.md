# Obsidian-Style Desktop Workspace Testing & UI Verification

When evaluating desktop UI integration (e.g. Tkinter-based consoles modeled after Obsidian):

1. **Substrate Dataclass Type Safety**:
   - Substrate stats returned by `Brain.stats()` contain `PopulationStats` dataclasses, NOT dicts.
   - Access fields directly: `hipp.allocated_neurons`, not `hipp.get('allocated_neurons')`.
   - Always verify the return type of foundation models when wiring UI dashboard property inspectors.

2. **Tkinter Keyboard Bindings & Event Testing**:
   - Number key bindings: `<Control-Key-1>` through `<Control-Key-6>` or `<Control-1>` must be tested with both direct keyboard handler invocation and virtual events.
   - Text widget states: Always toggle `state="normal"` before programmatic text insertion and restore `state="disabled"` immediately after.

3. **Multi-Tab Layout Verification Without Display Server**:
   - Headless verification using virtual X/Tkinter loops:
     ```python
     app = AE01MApp()
     app.update()
     # verify winfo_ismapped() and geometry
     ```
   - Test each tab frame mapped state sequentially with `app._select_tab(tab_name)` and `app.update()`.
