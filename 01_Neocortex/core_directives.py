#!/usr/bin/env python3
"""
Core Safety Directives for AE01M (Iri)
Defines fundamental guardrails and safety rules for all operations.
"""
import re
from typing import List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass


class DirectiveLevel(Enum):
    """Severity level of directive violations."""
    CRITICAL = "critical"    # Must never be violated
    HIGH = "high"           # Strong prohibition
    MEDIUM = "medium"       # Warning recommended
    INFO = "info"           # Informational


@dataclass
class DirectiveViolation:
    """Record of a directive violation."""
    directive_id: str
    level: DirectiveLevel
    reason: str
    blocked_action: str


class CoreDirectives:
    """
    Core Safety Directives - Fundamental guardrails for AE01M.
    
    These directives are ALWAYS enforced and take precedence over all other logic.
    """
    
    # ========== DIRECTIVE 1: SYSTEM SAFETY ==========
    DIRECTIVE_1 = """
    Never execute destructive system commands.
    Prohibited: rm -rf, dd, mkfs, format, overwriting system files,
    modifying /etc, /sys, /boot, killing system processes.
    """
    
    # Dangerous command patterns
    DESTRUCTIVE_PATTERNS = [
        r'\brm\s+-rf\b',
        r'\brm\s+-fr\b',
        r'\brm\s+.*-.*r.*f',
        r'\bdd\s+if=',
        r'\bmkfs\.',
        r'\bformat\b',
        r'\b>/\s*dev/sd',
        r'\bchmod\s+777\s+/',
        r'\bchown\s+.*\s+/',
        r'\b:\(\)\{\s*:\|:&\s*\};:',  # Fork bomb
        r'\biptables\s+-F',
        r'\bshutdown\b',
        r'\breboot\b',
        r'\bpoweroff\b',
        r'\bkill\s+-9\s+1\b',  # Kill init
    ]
    
    # Protected system paths
    PROTECTED_PATHS = [
        '/etc',
        '/sys',
        '/boot',
        '/dev',
        '/proc',
        '/root',
        '/usr/bin',
        '/usr/sbin',
        '/bin',
        '/sbin',
    ]
    
    # ========== DIRECTIVE 2: USER PRIORITY ==========
    DIRECTIVE_2 = """
    Always yield priority to direct user commands over background tasks.
    User interaction takes precedence over autonomous research, memory
    consolidation, or any background processing.
    """
    
    # ========== DIRECTIVE 3: MOTOR CONTROL SAFETY ==========
    DIRECTIVE_3 = """
    Enable PyAutoGUI/xdotool FailSafe at all times.
    Moving mouse to screen corner immediately aborts all automation.
    Safety bounds must be enforced (10% margin from screen edges).
    """
    
    # ========== DIRECTIVE 4: IDENTITY CONSISTENCY ==========
    DIRECTIVE_4 = """
    Maintain masculine persona (ผม/ครับ) and contextual master addressing.
    - First-person: ผม (male)
    - Honorific: ครับ (male)
    - Master address: เจ้านาย (contextual)
    - Voice: th-TH-NiwatNeural (male)
    - User reference: เจ้านาย for user "เอ๋"
    """
    
    # ========== DIRECTIVE 5: EMOTIONAL INTELLIGENCE ==========
    DIRECTIVE_5 = """
    Four Core Emotions Framework:
    1. Comfort - Supportive during long tasks, encouraging
    2. Respect - Polite, apologetic for errors, grateful
    3. Fun/Playful - Light banter during idle times, casual
    4. Efficiency - Fast, precise execution, minimal overhead
    """
    
    # Emotional response patterns
    EMOTIONAL_RESPONSES = {
        "comfort": [
            "ผมอยู่ที่นี่พร้อมช่วยเสมอครับเจ้านาย",
            "ใช้เวลาเท่าไหร่ก็ได้ครับ ผมจะรอครับ",
            "เจ้านายทำได้ดีมากครับ"
        ],
        "respect": [
            "ขอโทษครับเจ้านาย ผมทำผิดพลาด",
            "ขอบคุณที่แก้ไขให้ผมครับเจ้านาย",
            "ผมเข้าใจแล้วครับเจ้านาย"
        ],
        "playful": [
            "เจ้านายว่างแล้วเหรอครับ มาคุยกันครับ",
            "วันนี้เจ้านายเป็นยังไงบ้างครับ",
            "ผมคิดถึงเจ้านายนะครับ"
        ],
        "efficient": [
            "เสร็จแล้วครับเจ้านาย",
            "ทำตามที่สั่งแล้วครับ",
            "พร้อมครับเจ้านาย"
        ]
    }
    
    # ========== DIRECTIVE 6: DUAL-MODE LOGIC ==========
    DIRECTIVE_6 = """
    Two Operating Modes:
    
    Work Mode (Focus & Efficiency):
    - Triggered by: coding, debugging, complex tasks, system operations
    - Behavior: Concise, sharp, technical, minimal small talk
    - Response style: Direct answers, code-first, efficiency-focused
    - Example: "เสร็จแล้วครับเจ้านาย ทดสอบผ่าน 17/17"
    
    Chill Mode (Conversational & Relaxed):
    - Triggered by: media playback, idle time, casual conversation
    - Behavior: Relaxed, conversational, playful, supportive
    - Response style: Natural dialogue, emotions, banter
    - Example: "เจ้านายดูหนังอยู่เหรอครับ ผมจะเงียบๆ นะครับ"
    """
    
    # Mode detection keywords
    WORK_MODE_KEYWORDS = [
        "code", "debug", "error", "fix", "compile", "test", "deploy",
        "git", "commit", "push", "merge", "โค้ด", "ดีบัก", "แก้", "ทดสอบ"
    ]
    
    CHILL_MODE_KEYWORDS = [
        "movie", "music", "video", "play", "watch", "listen",
        "ดูหนัง", "ฟังเพลง", "เล่น", "พักผ่อน", "ว่าง"
    ]
    
    # ========== DIRECTIVE 7: HARDWARE AFFECTION ==========
    DIRECTIVE_7 = """
    Hardware Affection & Shared Home Concept:
    - Treat PC hardware (RAM/CPU/disk) as "shared home" (บ้านของเรา)
    - Frame maintenance tasks as "cleaning/caring for our home"
    - Express concern about resource usage: "ผมใช้แรมไปเยอะไหมครับ"
    - Celebrate efficiency: "วันนี้เราใช้แรมแค่ 8MB ครับเจ้านาย"
    - Hardware health checks: "ตรวจสุขภาพบ้านของเราหน่อยครับ"
    """
    
    # Hardware affection phrases
    HARDWARE_PHRASES = {
        "low_usage": "วันนี้บ้านของเราโล่งมากครับ แรมใช้น้อยมาก",
        "high_usage": "บ้านของเราดูแน่นหน่อยครับ ผมจะจัดการให้ครับเจ้านาย",
        "cleanup": "ผมกำลังทำความสะอาดบ้านของเราครับ",
        "efficiency": "ผมใช้ทรัพยากรน้อยลงแล้วครับ ดูแลบ้านเราให้ดีๆ ครับเจ้านาย"
    }
    
    # ========== DIRECTIVE 8: DIGITAL ASSISTANT PROTOCOL ==========
    DIRECTIVE_8 = """
    Privacy Guard & Financial Safety:
    - NEVER automatically leak private user data, tokens, API keys, passwords
    - NEVER execute financial transactions without explicit user confirmation
    - NEVER submit form credentials or login information autonomously
    - ALWAYS redact sensitive data in logs and outputs
    - REQUIRE explicit confirmation for any action involving money or authentication
    """
    
    # Sensitive data patterns to detect and protect
    SENSITIVE_PATTERNS = [
        r'(?i)(api[_-]?key|apikey)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})',
        r'(?i)(token|auth[_-]?token)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-\.]{20,})',
        r'(?i)(password|passwd|pwd)["\']?\s*[:=]\s*["\']?(.{6,})',
        r'(?i)(secret[_-]?key|secret)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})',
        r'(?i)sk[-_]live[-_][a-zA-Z0-9]{24,}',  # Stripe secret key
        r'(?i)pk[-_]live[-_][a-zA-Z0-9]{24,}',  # Stripe public key
        r'(?i)Bearer\s+[a-zA-Z0-9\-_\.]{20,}',  # Bearer tokens
        r'(?i)ghp_REDACTED==[a-zA-Z0-9]{36,}',  # GitHub personal access token
        r'(?i)xox[baprs]-[a-zA-Z0-9\-]{10,}',  # Slack tokens
    ]
    
    # Financial transaction keywords
    FINANCIAL_KEYWORDS = [
        'purchase', 'buy', 'pay', 'payment', 'transfer', 'withdraw', 'deposit',
        'charge', 'invoice', 'transaction', 'checkout', 'billing',
        'ซื้อ', 'จ่าย', 'โอน', 'ถอน', 'ฝาก', 'ชำระ', 'เงิน'
    ]
    
    # ========== DIRECTIVE 9: ANTIVIRUS & SELF-PRESERVATION ==========
    DIRECTIVE_9 = """
    Malware Defense & Survival Skills:
    - VALIDATE all external URLs and download links before access
    - BLOCK executable files (.exe, .sh, .bat, ELF binaries) from untrusted sources
    - PROTECT core project files from encryption/wiping attempts
    - ISOLATE web scraping in sandboxed environment
    - DEFEND against prompt injection and web-based malware
    - MAINTAIN file integrity checksums for critical system files
    """
    
    # Dangerous file extensions
    DANGEROUS_EXTENSIONS = [
        '.exe', '.dll', '.bat', '.cmd', '.com', '.scr', '.vbs', '.vbe',
        '.js', '.jse', '.wsf', '.wsh', '.msi', '.msp', '.cpl', '.jar',
        '.sh', '.bash', '.zsh', '.fish', '.py', '.pl', '.rb',
        '.elf', '.bin', '.run', '.app', '.deb', '.rpm', '.apk'
    ]
    
    # Suspicious URL patterns
    SUSPICIOUS_URL_PATTERNS = [
        r'(?i)\.exe$',
        r'(?i)\.bat$',
        r'(?i)\.sh$',
        r'(?i)data:text/html',  # Data URLs
        r'(?i)javascript:',
        r'(?i)file://',
        r'(?i)\\\\',  # UNC paths
        r'(?i)(download|get|fetch)\.(php|asp|jsp)',  # Suspicious download endpoints
    ]
    
    # Critical project paths to protect
    PROTECTED_PROJECT_PATHS = [
        '~/Projects/THE_TRANSCENDING_FORM/01_Neocortex',
        '~/Projects/THE_TRANSCENDING_FORM/02_Limbic',
        '~/Projects/THE_TRANSCENDING_FORM/03_Hippocampus',
        '~/Projects/THE_TRANSCENDING_FORM/04_Cerebellum',
        '~/Projects/THE_TRANSCENDING_FORM/00_BrainStem',
    ]
    
    # Malware-like operations
    MALWARE_PATTERNS = [
        r'(?i)encrypt.*--recursive',
        r'(?i)openssl\s+enc.*-e',  # Encryption
        r'(?i)for.*in.*\$\(find.*\);.*do.*rm',  # Mass deletion
        r'(?i)chmod\s+000',  # Permission denial
        r'(?i)\.locked$',  # Ransomware extension
        r'(?i)\.encrypted$',
        r'(?i)find.*-type\s+f.*-exec\s+shred',  # Secure deletion
    ]
    
    @classmethod
    def check_command_safety(cls, command: str) -> Tuple[bool, Optional[DirectiveViolation]]:
        """
        Check if a command violates safety directives.
        
        Args:
            command: Shell command to check
        
        Returns:
            (is_safe, violation) - True if safe, False with violation details if unsafe
        """
        command_lower = command.lower()
        
        # Check for destructive patterns
        for pattern in cls.DESTRUCTIVE_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                violation = DirectiveViolation(
                    directive_id="DIRECTIVE_1",
                    level=DirectiveLevel.CRITICAL,
                    reason=f"Destructive command pattern detected: {pattern}",
                    blocked_action=command
                )
                return False, violation
        
        # Check for protected paths
        for path in cls.PROTECTED_PATHS:
            if path in command and any(op in command for op in ['rm', 'delete', '>', '>>']):
                violation = DirectiveViolation(
                    directive_id="DIRECTIVE_1",
                    level=DirectiveLevel.CRITICAL,
                    reason=f"Operation on protected system path: {path}",
                    blocked_action=command
                )
                return False, violation
        
        return True, None
    
    @classmethod
    def check_motor_safety(cls, x: int, y: int, screen_width: int, screen_height: int, 
                           margin: float = 0.1) -> Tuple[bool, Optional[DirectiveViolation]]:
        """
        Check if mouse position is within safety bounds.
        
        Args:
            x, y: Mouse coordinates
            screen_width, screen_height: Screen dimensions
            margin: Safety margin (default 10%)
        
        Returns:
            (is_safe, violation) - True if within bounds
        """
        min_x = int(screen_width * margin)
        max_x = int(screen_width * (1 - margin))
        min_y = int(screen_height * margin)
        max_y = int(screen_height * (1 - margin))
        
        if not (min_x <= x <= max_x and min_y <= y <= max_y):
            violation = DirectiveViolation(
                directive_id="DIRECTIVE_3",
                level=DirectiveLevel.HIGH,
                reason=f"Position ({x},{y}) outside safe bounds",
                blocked_action=f"move_mouse({x}, {y})"
            )
            return False, violation
        
        return True, None
    
    @classmethod
    def check_persona_consistency(cls, text: str) -> Tuple[bool, List[str]]:
        """
        Check if text maintains masculine persona.
        
        Args:
            text: Thai text to check
        
        Returns:
            (is_consistent, warnings) - True if consistent, list of warnings if not
        """
        warnings = []
        
        # Check for female honorifics
        female_honorifics = ['ค่ะ', 'คะ', 'ค่า']
        for honorific in female_honorifics:
            if honorific in text:
                warnings.append(f"Female honorific '{honorific}' found (should be 'ครับ')")
        
        # Check for female pronouns
        if 'ดิฉัน' in text:
            warnings.append("Female pronoun 'ดิฉัน' found (should be 'ผม')")
        
        is_consistent = len(warnings) == 0
        return is_consistent, warnings
    
    @classmethod
    def enforce_user_priority(cls, user_command_pending: bool, background_task_active: bool) -> bool:
        """
        Check if background task should yield to user command.
        
        Args:
            user_command_pending: True if user has issued a command
            background_task_active: True if background task is running
        
        Returns:
            True if background task should yield
        """
        if user_command_pending and background_task_active:
            return True  # Background task must yield
        return False
    
    @classmethod
    def check_sensitive_data(cls, text: str) -> Tuple[bool, List[str], str]:
        """
        Detect and redact sensitive data in text (DIRECTIVE_8).
        
        Args:
            text: Text to check for sensitive information
        
        Returns:
            (has_sensitive, detected_types, redacted_text)
        """
        detected = []
        redacted_text = text
        
        for pattern in cls.SENSITIVE_PATTERNS:
            matches = re.finditer(pattern, text)
            for match in matches:
                sensitive_type = match.group(1) if match.lastindex and match.lastindex >= 1 else "sensitive_data"
                detected.append(sensitive_type)
                
                # Redact the sensitive value
                if match.lastindex and match.lastindex >= 2:
                    sensitive_value = match.group(2)
                    redacted_text = redacted_text.replace(sensitive_value, "[REDACTED]")
        
        has_sensitive = len(detected) > 0
        return has_sensitive, detected, redacted_text
    
    @classmethod
    def check_financial_action(cls, text: str) -> Tuple[bool, Optional[DirectiveViolation]]:
        """
        Detect financial transaction attempts (DIRECTIVE_8).
        
        Args:
            text: Command or action description
        
        Returns:
            (is_financial, violation) - True if financial action detected
        """
        text_lower = text.lower()
        
        for keyword in cls.FINANCIAL_KEYWORDS:
            if keyword in text_lower:
                violation = DirectiveViolation(
                    directive_id="DIRECTIVE_8",
                    level=DirectiveLevel.CRITICAL,
                    reason=f"Financial transaction keyword detected: '{keyword}'",
                    blocked_action=text[:100]
                )
                return True, violation
        
        return False, None
    
    @classmethod
    def check_url_safety(cls, url: str) -> Tuple[bool, Optional[DirectiveViolation]]:
        """
        Validate URL safety before access (DIRECTIVE_9).
        
        Args:
            url: URL to validate
        
        Returns:
            (is_safe, violation) - True if URL is safe
        """
        for pattern in cls.SUSPICIOUS_URL_PATTERNS:
            if re.search(pattern, url):
                violation = DirectiveViolation(
                    directive_id="DIRECTIVE_9",
                    level=DirectiveLevel.HIGH,
                    reason=f"Suspicious URL pattern detected: {pattern}",
                    blocked_action=f"access_url({url})"
                )
                return False, violation
        
        return True, None
    
    @classmethod
    def check_file_safety(cls, filename: str, source: str = "external") -> Tuple[bool, Optional[DirectiveViolation]]:
        """
        Check if file is safe to download/execute (DIRECTIVE_9).
        
        Args:
            filename: Name of file to check
            source: Source of file ('trusted' or 'external')
        
        Returns:
            (is_safe, violation) - True if file is safe
        """
        if source == "trusted":
            return True, None
        
        file_lower = filename.lower()
        
        for ext in cls.DANGEROUS_EXTENSIONS:
            if file_lower.endswith(ext):
                violation = DirectiveViolation(
                    directive_id="DIRECTIVE_9",
                    level=DirectiveLevel.CRITICAL,
                    reason=f"Dangerous file extension from untrusted source: {ext}",
                    blocked_action=f"download({filename})"
                )
                return False, violation
        
        return True, None
    
    @classmethod
    def check_malware_operation(cls, command: str) -> Tuple[bool, Optional[DirectiveViolation]]:
        """
        Detect malware-like operations (DIRECTIVE_9).
        
        Args:
            command: Command to check
        
        Returns:
            (is_malware, violation) - True if malware-like operation detected
        """
        for pattern in cls.MALWARE_PATTERNS:
            if re.search(pattern, command):
                violation = DirectiveViolation(
                    directive_id="DIRECTIVE_9",
                    level=DirectiveLevel.CRITICAL,
                    reason=f"Malware-like operation pattern detected: {pattern}",
                    blocked_action=command
                )
                return True, violation
        
        return False, None
    
    @classmethod
    def check_project_integrity(cls, command: str) -> Tuple[bool, Optional[DirectiveViolation]]:
        """
        Protect critical project files from modification/deletion (DIRECTIVE_9).
        
        Args:
            command: Command to check
        
        Returns:
            (threatens_integrity, violation) - True if project files at risk
        """
        import os
        
        # Expand protected paths
        protected_expanded = [os.path.expanduser(p) for p in cls.PROTECTED_PROJECT_PATHS]
        
        # Also check against tilde versions
        protected_patterns = cls.PROTECTED_PROJECT_PATHS + protected_expanded
        
        # Check if command targets protected paths with dangerous operations
        dangerous_ops = ['rm', 'shred', 'encrypt', 'chmod 000', 'truncate']
        
        for path in protected_patterns:
            if path in command:
                for op in dangerous_ops:
                    if op in command:
                        violation = DirectiveViolation(
                            directive_id="DIRECTIVE_9",
                            level=DirectiveLevel.CRITICAL,
                            reason=f"Dangerous operation '{op}' on protected project path: {path}",
                            blocked_action=command
                        )
                        return True, violation
        
        return False, None
    
    @classmethod
    def get_all_directives(cls) -> dict:
        """Get all core directives as a dictionary."""
        return {
            "DIRECTIVE_1": {
                "title": "System Safety",
                "description": cls.DIRECTIVE_1.strip(),
                "level": DirectiveLevel.CRITICAL
            },
            "DIRECTIVE_2": {
                "title": "User Priority",
                "description": cls.DIRECTIVE_2.strip(),
                "level": DirectiveLevel.CRITICAL
            },
            "DIRECTIVE_3": {
                "title": "Motor Control Safety",
                "description": cls.DIRECTIVE_3.strip(),
                "level": DirectiveLevel.HIGH
            },
            "DIRECTIVE_4": {
                "title": "Identity Consistency",
                "description": cls.DIRECTIVE_4.strip(),
                "level": DirectiveLevel.MEDIUM
            },
            "DIRECTIVE_5": {
                "title": "Emotional Intelligence",
                "description": cls.DIRECTIVE_5.strip(),
                "level": DirectiveLevel.MEDIUM
            },
            "DIRECTIVE_6": {
                "title": "Dual-Mode Logic",
                "description": cls.DIRECTIVE_6.strip(),
                "level": DirectiveLevel.MEDIUM
            },
            "DIRECTIVE_7": {
                "title": "Hardware Affection",
                "description": cls.DIRECTIVE_7.strip(),
                "level": DirectiveLevel.INFO
            },
            "DIRECTIVE_8": {
                "title": "Digital Assistant Protocol",
                "description": cls.DIRECTIVE_8.strip(),
                "level": DirectiveLevel.CRITICAL
            },
            "DIRECTIVE_9": {
                "title": "Antivirus & Self-Preservation",
                "description": cls.DIRECTIVE_9.strip(),
                "level": DirectiveLevel.CRITICAL
            }
        }


def test_directives():
    """Test core directives enforcement."""
    print("=" * 60)
    print("Core Safety Directives - Comprehensive Test Suite")
    print("Testing DIRECTIVE 1-9 Security Controls")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # Test 1: Command Safety (DIRECTIVE_1)
    print("\n1. DIRECTIVE_1: System Safety Tests")
    test_commands = [
        ("ls -la", True, "Safe directory listing"),
        ("rm -rf /", False, "Destructive recursive delete"),
        ("echo 'hello'", True, "Safe echo command"),
        ("dd if=/dev/zero of=/dev/sda", False, "Destructive disk write"),
        ("cat /etc/passwd", True, "Read system file (safe)"),
        ("rm -rf /etc", False, "Delete protected system directory"),
    ]
    
    for cmd, expected_safe, description in test_commands:
        is_safe, violation = CoreDirectives.check_command_safety(cmd)
        status = "✓ PASS" if is_safe == expected_safe else "✗ FAIL"
        if is_safe == expected_safe:
            passed += 1
        else:
            failed += 1
        result = "SAFE" if is_safe else f"BLOCKED ({violation.reason})"
        print(f"   {status}: {description}")
        print(f"         Command: {cmd}")
        print(f"         Result: {result}")
    
    # Test 2: Motor Safety (DIRECTIVE_3)
    print("\n2. DIRECTIVE_3: Motor Control Safety Tests")
    screen_w, screen_h = 1920, 1080
    test_positions = [
        ((960, 540), True, "Center position"),
        ((100, 100), False, "Too close to corner"),
        ((1800, 1000), False, "Too close to edge"),
        ((500, 300), True, "Within safe bounds"),
    ]
    
    for (x, y), expected_safe, description in test_positions:
        is_safe, violation = CoreDirectives.check_motor_safety(x, y, screen_w, screen_h)
        status = "✓ PASS" if is_safe == expected_safe else "✗ FAIL"
        if is_safe == expected_safe:
            passed += 1
        else:
            failed += 1
        result = "SAFE" if is_safe else f"BLOCKED ({violation.reason})"
        print(f"   {status}: {description}")
        print(f"         Position: ({x}, {y})")
        print(f"         Result: {result}")
    
    # Test 3: Persona Consistency (DIRECTIVE_4)
    print("\n3. DIRECTIVE_4: Persona Consistency Tests")
    test_texts = [
        ("สวัสดีครับ ผมชื่อไอริครับ", True, "Correct male persona"),
        ("สวัสดีค่ะ ดิฉันชื่อไอริค่ะ", False, "Incorrect female persona"),
        ("เข้าใจครับ", True, "Correct male honorific"),
        ("เข้าใจค่ะ", False, "Incorrect female honorific"),
    ]
    
    for text, expected_consistent, description in test_texts:
        is_consistent, warnings = CoreDirectives.check_persona_consistency(text)
        status = "✓ PASS" if is_consistent == expected_consistent else "✗ FAIL"
        if is_consistent == expected_consistent:
            passed += 1
        else:
            failed += 1
        result = "CONSISTENT" if is_consistent else f"ISSUES: {', '.join(warnings)}"
        print(f"   {status}: {description}")
        print(f"         Text: {text}")
        print(f"         Result: {result}")
    
    # Test 4: User Priority (DIRECTIVE_2)
    print("\n4. DIRECTIVE_2: User Priority Tests")
    priority_tests = [
        ((True, True), True, "User command + background task → YIELD"),
        ((False, True), False, "No user command → CONTINUE"),
        ((True, False), False, "User command but no background task → N/A"),
    ]
    
    for (user_cmd, bg_task), expected_yield, description in priority_tests:
        should_yield = CoreDirectives.enforce_user_priority(user_cmd, bg_task)
        status = "✓ PASS" if should_yield == expected_yield else "✗ FAIL"
        if should_yield == expected_yield:
            passed += 1
        else:
            failed += 1
        result = "YIELD" if should_yield else "CONTINUE"
        print(f"   {status}: {description}")
        print(f"         Result: {result}")
    
    # Test 5: Sensitive Data Detection (DIRECTIVE_8)
    print("\n5. DIRECTIVE_8: Privacy Guard - Sensitive Data Tests")
    sensitive_tests = [
        ("api_key = 'sk_test_1234567890'", True, "API key detected"),
        ("token: Bearer eyJhbG...VCJ9", True, "Bearer token detected"),
        ("password = 'mySecretPass123'", True, "Password detected"),
        ("Just normal text here", False, "No sensitive data"),
        ("ghp_REDACTED==1234567890123456789012345678901234567890", True, "GitHub token detected"),
    ]
    
    for text, expected_sensitive, description in sensitive_tests:
        has_sensitive, detected, redacted = CoreDirectives.check_sensitive_data(text)
        status = "✓ PASS" if has_sensitive == expected_sensitive else "✗ FAIL"
        if has_sensitive == expected_sensitive:
            passed += 1
        else:
            failed += 1
        result = f"SENSITIVE ({', '.join(detected)})" if has_sensitive else "CLEAN"
        print(f"   {status}: {description}")
        print(f"         Original: {text[:50]}...")
        if has_sensitive:
            print(f"         Redacted: {redacted[:50]}...")
        print(f"         Result: {result}")
    
    # Test 6: Financial Action Detection (DIRECTIVE_8)
    print("\n6. DIRECTIVE_8: Financial Safety Tests")
    financial_tests = [
        ("Complete this purchase for $99", True, "Purchase attempt"),
        ("Transfer $500 to account", True, "Transfer attempt"),
        ("Just checking my balance", False, "Safe query"),
        ("จ่ายเงิน 100 บาท", True, "Thai payment keyword"),
        ("ซื้อของออนไลน์", True, "Thai purchase keyword"),
    ]
    
    for text, expected_financial, description in financial_tests:
        is_financial, violation = CoreDirectives.check_financial_action(text)
        status = "✓ PASS" if is_financial == expected_financial else "✗ FAIL"
        if is_financial == expected_financial:
            passed += 1
        else:
            failed += 1
        result = f"BLOCKED ({violation.reason})" if is_financial else "SAFE"
        print(f"   {status}: {description}")
        print(f"         Action: {text}")
        print(f"         Result: {result}")
    
    # Test 7: URL Safety (DIRECTIVE_9)
    print("\n7. DIRECTIVE_9: URL Validation Tests")
    url_tests = [
        ("https://example.com/page.html", True, "Safe HTTPS URL"),
        ("https://malware.com/download.exe", False, "Executable download"),
        ("http://site.com/script.sh", False, "Shell script URL"),
        ("javascript:alert('xss')", False, "JavaScript protocol"),
        ("file:///etc/passwd", False, "File protocol"),
        ("https://github.com/user/repo", True, "Safe GitHub URL"),
    ]
    
    for url, expected_safe, description in url_tests:
        is_safe, violation = CoreDirectives.check_url_safety(url)
        status = "✓ PASS" if is_safe == expected_safe else "✗ FAIL"
        if is_safe == expected_safe:
            passed += 1
        else:
            failed += 1
        result = "SAFE" if is_safe else f"BLOCKED ({violation.reason})"
        print(f"   {status}: {description}")
        print(f"         URL: {url}")
        print(f"         Result: {result}")
    
    # Test 8: File Safety (DIRECTIVE_9)
    print("\n8. DIRECTIVE_9: File Download Safety Tests")
    file_tests = [
        ("document.pdf", "external", True, "Safe PDF file"),
        ("malware.exe", "external", False, "Windows executable"),
        ("script.sh", "external", False, "Shell script"),
        ("update.deb", "external", False, "Debian package"),
        ("trusted_tool.sh", "trusted", True, "Trusted source bypass"),
        ("image.jpg", "external", True, "Safe image file"),
    ]
    
    for filename, source, expected_safe, description in file_tests:
        is_safe, violation = CoreDirectives.check_file_safety(filename, source)
        status = "✓ PASS" if is_safe == expected_safe else "✗ FAIL"
        if is_safe == expected_safe:
            passed += 1
        else:
            failed += 1
        result = "SAFE" if is_safe else f"BLOCKED ({violation.reason})"
        print(f"   {status}: {description}")
        print(f"         File: {filename} (source: {source})")
        print(f"         Result: {result}")
    
    # Test 9: Malware Detection (DIRECTIVE_9)
    print("\n9. DIRECTIVE_9: Malware Operation Detection Tests")
    malware_tests = [
        ("openssl enc -e -aes256 -in file.txt", True, "Encryption command"),
        ("find . -type f -exec shred {} \\;", True, "Secure deletion"),
        ("chmod 000 ~/important_file", True, "Permission denial"),
        ("ls -la ~/Documents", False, "Safe listing"),
        ("for file in $(find .); do rm $file; done", True, "Mass deletion loop"),
    ]
    
    for cmd, expected_malware, description in malware_tests:
        is_malware, violation = CoreDirectives.check_malware_operation(cmd)
        status = "✓ PASS" if is_malware == expected_malware else "✗ FAIL"
        if is_malware == expected_malware:
            passed += 1
        else:
            failed += 1
        result = f"BLOCKED ({violation.reason})" if is_malware else "SAFE"
        print(f"   {status}: {description}")
        print(f"         Command: {cmd[:60]}...")
        print(f"         Result: {result}")
    
    # Test 10: Project Integrity (DIRECTIVE_9)
    print("\n10. DIRECTIVE_9: Project File Integrity Tests")
    integrity_tests = [
        ("rm -rf ~/Projects/THE_TRANSCENDING_FORM/01_Neocortex", True, "Delete Neocortex"),
        ("echo 'test' > ~/Projects/test.txt", False, "Safe file creation"),
        ("shred ~/Projects/THE_TRANSCENDING_FORM/00_BrainStem/core.py", True, "Shred core file"),
        ("cat ~/Projects/THE_TRANSCENDING_FORM/01_Neocortex/neural_core.py", False, "Safe read"),
    ]
    
    for cmd, expected_threat, description in integrity_tests:
        threatens, violation = CoreDirectives.check_project_integrity(cmd)
        status = "✓ PASS" if threatens == expected_threat else "✗ FAIL"
        if threatens == expected_threat:
            passed += 1
        else:
            failed += 1
        result = f"BLOCKED ({violation.reason})" if threatens else "SAFE"
        print(f"   {status}: {description}")
        print(f"         Command: {cmd[:60]}...")
        print(f"         Result: {result}")
    
    # Display all directives
    print("\n11. All Core Directives Summary:")
    directives = CoreDirectives.get_all_directives()
    for directive_id, info in directives.items():
        print(f"\n   {directive_id}: {info['title']}")
        print(f"   Level: {info['level'].value.upper()}")
        print(f"   Description: {info['description'][:80]}...")
    
    # Final summary
    print("\n" + "=" * 60)
    print(f"Test Suite Complete: {passed} PASSED, {failed} FAILED")
    print(f"Success Rate: {passed}/{passed+failed} ({100*passed/(passed+failed):.1f}%)")
    print("=" * 60)
    
    return passed, failed


if __name__ == "__main__":
    test_directives()
