# Module Execution Entry Point Pattern

## Context
When running Python GUI modules directly via `python -m <module_name>` (e.g. `python -m ui.app`), Python imports the module definitions and executes top-level code. If no `if __name__ == "__main__":` block or `main()` launcher exists, Python exits immediately with returncode 0 without launching the window or starting the GUI event loop (`mainloop()`).

## Symptoms
- Executing `./.venv/bin/python -m ui.app` returns instantly with exit code 0.
- No window appears, and no errors or warnings are logged.
- Importing the class works in interactive shells, but CLI invocation fails silently.

## Root Cause
The module defines application classes (e.g. `AE01MApp(tk.Tk)`) but lacks an explicit entrypoint to instantiate the application and invoke `app.mainloop()`.

## Standard Fix Pattern
Always ensure modules intended for direct CLI execution define a standard entrypoint:

```python
def main():
    app = AE01MApp()
    app.mainloop()

if __name__ == "__main__":
    main()
```

## Diagnosis Workflow
1. Check file tail: inspect the bottom lines of the module for `if __name__ == "__main__":`.
2. Inspect legacy/backup versions: check `archive/` or previous git revisions for prior `main()` patterns.
3. Test inline invocation: run `python -c "from ui.app import AE01MApp; app = AE01MApp(); app.mainloop()"` to verify if the class itself runs when `mainloop()` is called.
