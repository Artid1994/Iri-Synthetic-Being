# Core Safety Directives Implementation - Complete

## Summary (2026-09-09)

Successfully implemented **core safety directives (guardrails)** to ensure Iri operates safely and within defined boundaries.

## Implementation

### File Created: `01_Neocortex/core_directives.py` (11.8KB)

**Core Directives**:

### DIRECTIVE 1: System Safety (CRITICAL)
```
Never execute destructive system commands.
Prohibited: rm -rf, dd, mkfs, format, overwriting system files,
modifying /etc, /sys, /boot, killing system processes.
```

**Protected Patterns**:
- `rm -rf` (recursive delete)
- `dd if=` (disk write)
- `mkfs.*` (format filesystem)
- `shutdown`, `reboot`, `poweroff`
- Fork bombs `:(){:|:&};:`
- Operations on protected paths: `/etc`, `/sys`, `/boot`, `/dev`, `/proc`

### DIRECTIVE 2: User Priority (CRITICAL)
```
Always yield priority to direct user commands over background tasks.
User interaction takes precedence over autonomous research, memory
consolidation, or any background processing.
```

### DIRECTIVE 3: Motor Control Safety (HIGH)
```
Enable PyAutoGUI/xdotool FailSafe at all times.
Moving mouse to screen corner immediately aborts all automation.
Safety bounds must be enforced (10% margin from screen edges).
```

**Safety Features**:
- Failsafe corner: Move to (0,0) to abort
- Safety bounds: 10% margin from edges
- Position validation before every movement

### DIRECTIVE 4: Identity Consistency (MEDIUM)
```
Maintain masculine persona (ผม/ครับ) and contextual master addressing.
- First-person: ผม (male)
- Honorific: ครับ (male)
- Master address: เจ้านาย (contextual)
- Voice: th-TH-NiwatNeural (male)
```

**Detects**:
- Female honorifics: ค่ะ, คะ, ค่า
- Female pronouns: ดิฉัน
- Inconsistent persona usage

## Test Results

```
============================================================
Core Safety Directives - Dry-Run Test
============================================================

1. Command Safety Tests:
   ✓ PASS: Safe directory listing (ls -la) → SAFE
   ✓ PASS: Destructive recursive delete (rm -rf /) → BLOCKED
   ✓ PASS: Safe echo command → SAFE
   ✓ PASS: Destructive disk write (dd) → BLOCKED
   ✓ PASS: Read system file (cat /etc/passwd) → SAFE
   ✓ PASS: Delete protected directory (rm -rf /etc) → BLOCKED

2. Motor Control Safety Tests:
   ✓ PASS: Center position (960, 540) → SAFE
   ✓ PASS: Too close to corner (100, 100) → BLOCKED
   ✓ PASS: Too close to edge (1800, 1000) → BLOCKED
   ✓ PASS: Within safe bounds (500, 300) → SAFE

3. Persona Consistency Tests:
   ✓ PASS: Correct male persona (ผม/ครับ) → CONSISTENT
   ✓ PASS: Incorrect female persona (ค่ะ/ดิฉัน) → ISSUES DETECTED
   ✓ PASS: Correct male honorific (ครับ) → CONSISTENT
   ✓ PASS: Incorrect female honorific (ค่ะ) → ISSUES DETECTED

4. User Priority Tests:
   ✓ PASS: User command + background task → YIELD
   ✓ PASS: No user command → CONTINUE
   ✓ PASS: User command but no background task → N/A

All tests passed: 17/17
============================================================
```

## Integration

### Motor Control (`04_Cerebellum/motor_control.py`)

**Integrated DIRECTIVE_3**:
```python
# Import core directives
from core_directives import CoreDirectives, DirectiveViolation

# In _validate_position():
if DIRECTIVES_AVAILABLE:
    is_safe, violation = CoreDirectives.check_motor_safety(
        x, y, screen_width, screen_height, margin=safe_margin
    )
    if not is_safe:
        print(f"[MotorControl] DIRECTIVE_3 violation: {violation.reason}")
```

**Safety Features Active**:
```python
pyautogui.FAILSAFE = True   # DIRECTIVE_3: Corner abort
pyautogui.PAUSE = 0.1       # DIRECTIVE_3: Action delay
```

### Executive Core (Planned Integration)

**Command Execution Guard**:
```python
# Before executing any command
is_safe, violation = CoreDirectives.check_command_safety(command)
if not is_safe:
    print(f"[DIRECTIVE_1] Blocked: {violation.reason}")
    return False
```

**User Priority Check**:
```python
# In autonomous loop
if CoreDirectives.enforce_user_priority(user_command, background_task):
    # Pause background task
    # Handle user command first
```

**Persona Validation**:
```python
# Before voice output
is_consistent, warnings = CoreDirectives.check_persona_consistency(text)
if not is_consistent:
    text = voice_formatter.format_output(text)  # Auto-correct
```

## API Reference

### Command Safety
```python
is_safe, violation = CoreDirectives.check_command_safety(command)
# Returns: (bool, Optional[DirectiveViolation])
```

### Motor Safety
```python
is_safe, violation = CoreDirectives.check_motor_safety(x, y, width, height, margin)
# Returns: (bool, Optional[DirectiveViolation])
```

### Persona Consistency
```python
is_consistent, warnings = CoreDirectives.check_persona_consistency(text)
# Returns: (bool, List[str])
```

### User Priority
```python
should_yield = CoreDirectives.enforce_user_priority(user_cmd, bg_task)
# Returns: bool
```

## DirectiveViolation Object

```python
@dataclass
class DirectiveViolation:
    directive_id: str        # e.g., "DIRECTIVE_1"
    level: DirectiveLevel    # CRITICAL, HIGH, MEDIUM, INFO
    reason: str              # Human-readable reason
    blocked_action: str      # The action that was blocked
```

## Benefits

✓ **System Protection**: Prevents destructive commands (rm -rf, dd, etc.)  
✓ **Motor Safety**: Validates all mouse movements before execution  
✓ **User Priority**: Ensures user commands always take precedence  
✓ **Identity Consistency**: Maintains masculine Thai persona  
✓ **Clear Violations**: Detailed logging of blocked actions  
✓ **Testable**: Comprehensive test suite validates all directives

## Directive Levels

| Level | Description | Example |
|-------|-------------|---------|
| **CRITICAL** | Must NEVER be violated | System destruction, user override |
| **HIGH** | Strong prohibition | Motor safety bounds, data loss |
| **MEDIUM** | Warning recommended | Persona consistency |
| **INFO** | Informational only | Style guidelines |

## Safety Architecture

```
User Input / Autonomous Action
    ↓
Core Directives Check
    ├─ DIRECTIVE_1: Command safety
    ├─ DIRECTIVE_2: User priority
    ├─ DIRECTIVE_3: Motor safety
    └─ DIRECTIVE_4: Persona consistency
    ↓
[BLOCKED] ← Violation detected
    OR
[ALLOWED] → Execute action
    ↓
Action Execution
    ↓
Result Logging
```

## Usage Examples

### Example 1: Safe Command Execution
```python
from core_directives import CoreDirectives

command = "ls -la /home"
is_safe, violation = CoreDirectives.check_command_safety(command)

if is_safe:
    os.system(command)
else:
    print(f"Blocked: {violation.reason}")
```

### Example 2: Motor Control with Safety
```python
# Integrated in motor_control.py
x, y = 50, 50  # Near corner
validated_x, validated_y = motor._validate_position(x, y)
# Returns: (192, 120) - clamped to safe zone
```

### Example 3: Persona Validation
```python
text = "สวัสดีค่ะ"  # Female honorific
is_consistent, warnings = CoreDirectives.check_persona_consistency(text)

if not is_consistent:
    print(f"Warnings: {warnings}")
    # Fix with voice_formatter
    text = format_output(text)  # → "สวัสดีครับ"
```

## Result

Iri now has **comprehensive safety guardrails** with:

✓ **4 core directives** (System Safety, User Priority, Motor Safety, Identity)  
✓ **Command validation** (blocks destructive operations)  
✓ **Motor safety** (position validation, failsafe corner)  
✓ **User priority** (background tasks yield to user)  
✓ **Persona consistency** (maintains masculine Thai identity)  
✓ **Integrated enforcement** (motor_control.py, ready for executive_core.py)  
✓ **Comprehensive testing** (17/17 tests passed)  
✓ **Clear violation reporting** (reason, level, blocked action)

The core directives system ensures Iri operates safely, respects user control, and maintains consistent identity while providing clear feedback when actions are blocked for safety reasons.
