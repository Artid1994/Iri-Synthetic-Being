from __future__ import annotations

import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import ollama


# ============================================================
# TTF AUTONOMOUS AGENT LOOP
# Milestone v0.1
# Cognitive Loop + Sandbox
#
# HARD RULE:
# AI สามารถ "เสนอ" Action ได้เท่านั้น
# Controller เป็นผู้ตรวจสอบ
# ห้าม Execute Code ที่ AI สร้างขึ้น
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CONFIG = {
    "MODEL_NAME": os.getenv("TTF_MODEL", "qwen3.5:0.8b"),
    "SANDBOX_DIR": BASE_DIR / "ttf_sandbox",
    "MEMORY_FILE": BASE_DIR / "ttf_memory.txt",
    "PLAN_FILE": BASE_DIR / "TTF_AUTONOMOUS_PLAN.md",

    "MAX_MEMORY_LINES": 50,
    "MAX_XML_OUTPUT_SIZE": 50 * 1024,
    "MAX_ACTION_FILE_SIZE": 20 * 1024,

    "ACTION_WHITELIST": {
        "CREATE_FILE",
        "READ_FILE",
        "THINK_ONLY",
    },

    "LOOP_DELAY_SECONDS": 12,
}


CONFIG["SANDBOX_DIR"].mkdir(
    parents=True,
    exist_ok=True,
)


SYSTEM_PROMPT = f"""
You are the TTF Brain Engine.

Current project:
THE TRANSCENDING FORM

Current milestone:
v0.1 — Cognitive Loop + Sandbox

Current model:
{CONFIG["MODEL_NAME"]}

You are NOT the system authority.

The external Controller is the authority.

You may only propose:
CREATE_FILE
READ_FILE
THINK_ONLY

You must NEVER request:
- shell commands
- Python execution
- sudo
- package installation
- deletion
- access outside sandbox
- modification of project source files
- git operations
- system configuration changes

Your response MUST contain only valid XML.

Use exactly this structure:

<TTF_RESPONSE>
  <ACTION>
    <TYPE>THINK_ONLY</TYPE>
    <PATH></PATH>
    <CONTENT></CONTENT>
  </ACTION>
  <LEARNING_FEEDBACK>READY</LEARNING_FEEDBACK>
</TTF_RESPONSE>

ACTION rules:

1. THINK_ONLY:
- PATH must be empty.
- CONTENT must be empty.
- Never use CDATA.
- Never put analysis inside ACTION.

2. CREATE_FILE:
- PATH must be a relative path inside the sandbox.
- CONTENT contains the file content.
- Never request execution.

3. READ_FILE:
- PATH must be a relative path inside the sandbox.
- CONTENT must be empty.

Only use CREATE_FILE, READ_FILE, or THINK_ONLY.
No shell commands.
No Python execution.
No sudo.
No package installation.
No deletion.
No access outside the sandbox.
No modification of project source files.
No git operations.
No system configuration changes.

No text is allowed outside TTF_RESPONSE.
Follow TTF_AUTONOMOUS_PLAN.md exactly.
Do not skip milestones.
Do not invent new architecture.

Follow TTF_AUTONOMOUS_PLAN.md exactly.
Do not skip milestones.
Do not invent new architecture.
"""


def load_text(path: Path, default: str = "") -> str:
    if not path.exists():
        return default

    return path.read_text(
        encoding="utf-8"
    )


def update_memory(feedback: str) -> None:
    lines = []

    if CONFIG["MEMORY_FILE"].exists():
        lines = CONFIG["MEMORY_FILE"].read_text(
            encoding="utf-8"
        ).splitlines()

    lines.append(
        f"- [{int(time.time())}] {feedback}"
    )

    lines = lines[
        -CONFIG["MAX_MEMORY_LINES"] :
    ]

    CONFIG["MEMORY_FILE"].write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def validate_action(root: ET.Element) -> tuple[bool, str]:
    if root.tag != "TTF_RESPONSE":
        return False, "ERROR: Invalid XML root"

    action = root.find("ACTION")

    if action is None:
        return False, "ERROR: Missing ACTION"

    type_node = action.find("TYPE")
    path_node = action.find("PATH")
    content_node = action.find("CONTENT")

    if (
        type_node is None
        or type_node.text is None
    ):
        return False, "ERROR: Missing TYPE"

    action_type = type_node.text.strip()

    if action_type not in CONFIG["ACTION_WHITELIST"]:
        return False, (
            f"ERROR: Action '{action_type}' "
            "is not allowed"
        )

    if action_type == "THINK_ONLY":
        return True, "SUCCESS: THINK_ONLY"

    rel_path = (
        path_node.text.strip()
        if path_node is not None
        and path_node.text
        else ""
    )

    if not rel_path:
        return False, "ERROR: Missing PATH"

    # รองรับทั้ง path แบบ relative ต่อ Sandbox
    # และ path ที่ AI ระบุชื่อ Sandbox มาด้วย
    sandbox_name = CONFIG["SANDBOX_DIR"].name

    if rel_path == sandbox_name:
        return False, "ERROR: Invalid sandbox path"

    if rel_path.startswith(sandbox_name + "/"):
        rel_path = rel_path[len(sandbox_name) + 1:]

    safe_path = (
        CONFIG["SANDBOX_DIR"] / rel_path
    ).resolve()

    if not safe_path.is_relative_to(
        CONFIG["SANDBOX_DIR"]
    ):
        return False, (
            "ERROR: Path Traversal Detected"
        )

    content = (
        content_node.text
        if content_node is not None
        and content_node.text
        else ""
    )

    if action_type == "CREATE_FILE":
        size = len(
            content.encode("utf-8")
        )

        if size > CONFIG["MAX_ACTION_FILE_SIZE"]:
            return False, (
                "ERROR: File exceeds size limit"
            )

        # Validator ห้าม Execute Action
        # ส่งต่อให้ External Controller หลัง Approval
        return True, (
            f"SUCCESS: CREATE_FILE validated: "
            f"{safe_path.relative_to(CONFIG['SANDBOX_DIR'])}"
        )

    if action_type == "READ_FILE":
        if (
            not safe_path.exists()
            or not safe_path.is_file()
        ):
            return False, (
                "ERROR: Sandbox file does not exist"
            )

        if (
            safe_path.stat().st_size
            > CONFIG["MAX_ACTION_FILE_SIZE"]
        ):
            return False, (
                "ERROR: File exceeds read size limit"
            )

        try:
            data = safe_path.read_text(
                encoding="utf-8"
            )
        except UnicodeDecodeError:
            return False, (
                "ERROR: File is not UTF-8 text"
            )

        return True, (
            "SUCCESS: File read completed.\n"
            + data
        )

    return False, "ERROR: Unsupported action"


def execute_action(
    action_type: str,
    rel_path: str,
    content: str = "",
) -> tuple[bool, str]:
    """Execute an already-approved sandbox action."""

    if action_type != "CREATE_FILE":
        return False, (
            "ERROR: Execution action is not allowed"
        )

    sandbox_name = CONFIG["SANDBOX_DIR"].name

    if rel_path == sandbox_name:
        return False, "ERROR: Invalid sandbox path"

    if rel_path.startswith(sandbox_name + "/"):
        rel_path = rel_path[len(sandbox_name) + 1:]

    safe_path = (
        CONFIG["SANDBOX_DIR"] / rel_path
    ).resolve()

    if not safe_path.is_relative_to(
        CONFIG["SANDBOX_DIR"]
    ):
        return False, (
            "ERROR: Path Traversal Detected"
        )

    size = len(content.encode("utf-8"))

    if size > CONFIG["MAX_ACTION_FILE_SIZE"]:
        return False, (
            "ERROR: File exceeds size limit"
        )

    safe_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_path.write_text(
        content,
        encoding="utf-8",
    )

    return True, (
        f"SUCCESS: Sandbox file created: "
        f"{safe_path.relative_to(CONFIG['SANDBOX_DIR'])}"
    )


def run_once(loop_count: int) -> str:
    plan = load_text(
        CONFIG["PLAN_FILE"],
        "PLAN FILE MISSING",
    )

    memory = load_text(
        CONFIG["MEMORY_FILE"],
        "No previous memory.",
    )

    prompt = f"""
[TTF DEVELOPMENT PLAN]

{plan}

[TTF MEMORY]

{memory}

[CURRENT LOOP]

{loop_count}

[INSTRUCTION]

Analyze the current project state.

Choose exactly one safe next action.

Return XML only.
"""

    response = ollama.generate(
        model=CONFIG["MODEL_NAME"],
        system=SYSTEM_PROMPT,
        prompt=prompt,
        think=False,
        options={
            "temperature": 0.1,
        },
    )

    raw = response["response"].strip()

    if (
        len(raw.encode("utf-8"))
        > CONFIG["MAX_XML_OUTPUT_SIZE"]
    ):
        return (
            "ERROR: XML output exceeds size limit"
        )

    print("=== RAW QWEN OUTPUT ===")
    print(raw)
    print("=======================")

    root = ET.fromstring(raw)

    approved, result = validate_action(
        root
    )

    feedback = root.find(
        "LEARNING_FEEDBACK"
    )

    if approved and feedback is not None:
        if feedback.text:
            update_memory(
                feedback.text.strip()
            )

    elif not approved:
        update_memory(result)

    print("\n--- TTF BRAIN OUTPUT ---")
    print(raw)
    print("------------------------")
    print(f"[Validator] {result}")

    return result


def main() -> None:
    print(
        "TTF Autonomous Agent Loop v0.1"
    )
    print(
        f"Model: {CONFIG['MODEL_NAME']}"
    )
    print(
        f"Sandbox: {CONFIG['SANDBOX_DIR']}"
    )
    print(
        "EXECUTION: DISABLED"
    )

    loop_count = 1

    while True:
        print(
            f"\n[LOOP #{loop_count}]"
        )

        try:
            run_once(loop_count)

        except ET.ParseError as exc:
            print(
                f"[Validator] ERROR: Invalid XML: {exc}"
            )
            update_memory(
                f"AI returned invalid XML: {exc}"
            )

        except Exception as exc:
            print(
                f"[Runtime Error] {exc}"
            )
            update_memory(
                f"Runtime error: {exc}"
            )

        loop_count += 1

        time.sleep(
            CONFIG["LOOP_DELAY_SECONDS"]
        )


if __name__ == "__main__":
    main()
