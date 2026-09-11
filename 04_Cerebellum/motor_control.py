#!/usr/bin/env python3
"""
Motor Control Engine for AE01M (Cerebellum)
Provides mouse and keyboard automation for physical world interaction.
Integrated with Core Safety Directives (DIRECTIVE_3).
"""
import os
import sys
import time
import subprocess
from pathlib import Path
from typing import Tuple, Optional, List
from enum import Enum

# Import core safety directives
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "01_Neocortex"))
    from core_directives import CoreDirectives, DirectiveViolation
    DIRECTIVES_AVAILABLE = True
except ImportError:
    DIRECTIVES_AVAILABLE = False
    print("[MotorControl] WARNING: Core directives not available")

# PyAutoGUI for cross-platform automation
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    # Configure PyAutoGUI safety (DIRECTIVE_3)
    pyautogui.PAUSE = 0.1  # 100ms delay between actions
    pyautogui.FAILSAFE = True  # Move mouse to corner to abort
except ImportError:
    PYAUTOGUI_AVAILABLE = False


class MouseButton(Enum):
    """Mouse button types."""
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"


class MotorControl:
    """
    Motor control engine for mouse and keyboard automation.
    Provides safe, bounded control of desktop environment.
    """
    
    def __init__(self, enable_safety: bool = True):
        """
        Initialize motor control engine.
        
        Args:
            enable_safety: Enable failsafe corner interrupt
        """
        self.safety_enabled = enable_safety
        
        # Check available tools
        self.xdotool_available = self._check_command("xdotool")
        self.pyautogui_available = PYAUTOGUI_AVAILABLE
        
        if not self.xdotool_available and not self.pyautogui_available:
            raise RuntimeError("No automation tools available (xdotool or pyautogui)")
        
        # Get screen dimensions
        self.screen_width, self.screen_height = self._get_screen_size()
        
        # Safety bounds (10% margin from edges)
        self.safe_margin = 0.1
        self.min_x = int(self.screen_width * self.safe_margin)
        self.max_x = int(self.screen_width * (1 - self.safe_margin))
        self.min_y = int(self.screen_height * self.safe_margin)
        self.max_y = int(self.screen_height * (1 - self.safe_margin))
        
        print(f"[MotorControl] Initialized")
        print(f"[MotorControl] Screen: {self.screen_width}x{self.screen_height}")
        print(f"[MotorControl] Safe zone: ({self.min_x},{self.min_y}) to ({self.max_x},{self.max_y})")
        print(f"[MotorControl] Failsafe: {'ENABLED' if self.safety_enabled else 'DISABLED'}")
    
    def _check_command(self, command: str) -> bool:
        """Check if a command is available."""
        try:
            subprocess.run(["which", command], capture_output=True, check=True, timeout=2)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions."""
        if self.pyautogui_available:
            size = pyautogui.size()
            return size.width, size.height
        elif self.xdotool_available:
            try:
                result = subprocess.run(
                    ["xdotool", "getdisplaygeometry"],
                    capture_output=True, text=True, timeout=2
                )
                if result.returncode == 0:
                    width, height = result.stdout.strip().split()
                    return int(width), int(height)
            except Exception:
                pass
        
        # Fallback
        return 1920, 1080
    
    def _validate_position(self, x: int, y: int) -> Tuple[int, int]:
        """
        Validate and clamp position to safe bounds.
        Enforces DIRECTIVE_3: Motor Control Safety.
        """
        if not self.safety_enabled:
            return x, y
        
        # Check against core directives if available
        if DIRECTIVES_AVAILABLE:
            is_safe, violation = CoreDirectives.check_motor_safety(
                x, y, self.screen_width, self.screen_height, margin=self.safe_margin
            )
            if not is_safe:
                print(f"[MotorControl] DIRECTIVE_3 violation: {violation.reason}")
        
        # Clamp to safe bounds
        x = max(self.min_x, min(x, self.max_x))
        y = max(self.min_y, min(y, self.max_y))
        return x, y
    
    # ============ MOUSE CONTROL ============
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position."""
        if self.pyautogui_available:
            pos = pyautogui.position()
            return pos.x, pos.y
        elif self.xdotool_available:
            try:
                result = subprocess.run(
                    ["xdotool", "getmouselocation", "--shell"],
                    capture_output=True, text=True, timeout=2
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    x = int(lines[0].split('=')[1])
                    y = int(lines[1].split('=')[1])
                    return x, y
            except Exception:
                pass
        
        return 0, 0
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> bool:
        """
        Move mouse to position.
        
        Args:
            x: Target x coordinate
            y: Target y coordinate
            duration: Movement duration in seconds
        
        Returns:
            True if successful
        """
        # Validate position
        x, y = self._validate_position(x, y)
        
        try:
            if self.pyautogui_available:
                pyautogui.moveTo(x, y, duration=duration)
                return True
            elif self.xdotool_available:
                subprocess.run(
                    ["xdotool", "mousemove", str(x), str(y)],
                    timeout=2, check=True
                )
                return True
        except Exception as e:
            print(f"[MotorControl] Mouse move failed: {e}")
            return False
        
        return False
    
    def click(self, button: MouseButton = MouseButton.LEFT, clicks: int = 1) -> bool:
        """
        Click mouse button.
        
        Args:
            button: Mouse button to click
            clicks: Number of clicks
        
        Returns:
            True if successful
        """
        try:
            if self.pyautogui_available:
                pyautogui.click(button=button.value, clicks=clicks)
                return True
            elif self.xdotool_available:
                # Map button to xdotool button number
                button_map = {
                    MouseButton.LEFT: "1",
                    MouseButton.MIDDLE: "2",
                    MouseButton.RIGHT: "3"
                }
                button_num = button_map.get(button, "1")
                
                for _ in range(clicks):
                    subprocess.run(
                        ["xdotool", "click", button_num],
                        timeout=2, check=True
                    )
                    if clicks > 1:
                        time.sleep(0.1)
                return True
        except Exception as e:
            print(f"[MotorControl] Click failed: {e}")
            return False
        
        return False
    
    def scroll(self, amount: int) -> bool:
        """
        Scroll mouse wheel.
        
        Args:
            amount: Scroll amount (positive = up, negative = down)
        
        Returns:
            True if successful
        """
        try:
            if self.pyautogui_available:
                pyautogui.scroll(amount)
                return True
            elif self.xdotool_available:
                # xdotool: button 4 = scroll up, button 5 = scroll down
                button = "4" if amount > 0 else "5"
                count = abs(amount)
                
                for _ in range(count):
                    subprocess.run(
                        ["xdotool", "click", button],
                        timeout=2, check=True
                    )
                    time.sleep(0.05)
                return True
        except Exception as e:
            print(f"[MotorControl] Scroll failed: {e}")
            return False
        
        return False
    
    # ============ KEYBOARD CONTROL ============
    
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """
        Type text with keyboard.
        
        Args:
            text: Text to type
            interval: Delay between keystrokes (seconds)
        
        Returns:
            True if successful
        """
        try:
            if self.pyautogui_available:
                pyautogui.write(text, interval=interval)
                return True
            elif self.xdotool_available:
                # xdotool type with delay
                delay_ms = int(interval * 1000)
                subprocess.run(
                    ["xdotool", "type", "--delay", str(delay_ms), text],
                    timeout=len(text) * interval + 5, check=True
                )
                return True
        except Exception as e:
            print(f"[MotorControl] Type text failed: {e}")
            return False
        
        return False
    
    def press_key(self, key: str) -> bool:
        """
        Press a key.
        
        Args:
            key: Key name (e.g., 'enter', 'tab', 'ctrl')
        
        Returns:
            True if successful
        """
        try:
            if self.pyautogui_available:
                pyautogui.press(key)
                return True
            elif self.xdotool_available:
                subprocess.run(
                    ["xdotool", "key", key],
                    timeout=2, check=True
                )
                return True
        except Exception as e:
            print(f"[MotorControl] Press key failed: {e}")
            return False
        
        return False
    
    def hotkey(self, *keys: str) -> bool:
        """
        Press key combination.
        
        Args:
            keys: Keys to press together (e.g., 'ctrl', 'c')
        
        Returns:
            True if successful
        """
        try:
            if self.pyautogui_available:
                pyautogui.hotkey(*keys)
                return True
            elif self.xdotool_available:
                key_combo = '+'.join(keys)
                subprocess.run(
                    ["xdotool", "key", key_combo],
                    timeout=2, check=True
                )
                return True
        except Exception as e:
            print(f"[MotorControl] Hotkey failed: {e}")
            return False
        
        return False
    
    # ============ UTILITY FUNCTIONS ============
    
    def screenshot(self, save_path: Optional[str] = None) -> Optional[str]:
        """
        Take screenshot.
        
        Args:
            save_path: Path to save screenshot (auto-generated if None)
        
        Returns:
            Path to screenshot file if successful
        """
        if save_path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            save_path = f"/tmp/iri_screenshot_{timestamp}.png"
        
        try:
            if self.pyautogui_available:
                screenshot = pyautogui.screenshot()
                screenshot.save(save_path)
                return save_path
            else:
                # Use scrot
                subprocess.run(
                    ["scrot", save_path],
                    timeout=5, check=True
                )
                if os.path.exists(save_path):
                    return save_path
        except Exception as e:
            print(f"[MotorControl] Screenshot failed: {e}")
        
        return None


def test_motor_control():
    """Test motor control capabilities (dry-run)."""
    print("=" * 60)
    print("Motor Control Engine - Dry-Run Test")
    print("=" * 60)
    
    # Initialize
    motor = MotorControl(enable_safety=True)
    
    print("\n1. Mouse Position Test:")
    x, y = motor.get_mouse_position()
    print(f"   Current position: ({x}, {y})")
    
    print("\n2. Screen Information:")
    print(f"   Screen size: {motor.screen_width}x{motor.screen_height}")
    print(f"   Safe zone: ({motor.min_x},{motor.min_y}) to ({motor.max_x},{motor.max_y})")
    
    print("\n3. Safety Bounds Test:")
    test_positions = [
        (100, 100),
        (motor.screen_width - 50, motor.screen_height - 50),
        (motor.screen_width // 2, motor.screen_height // 2)
    ]
    for tx, ty in test_positions:
        vx, vy = motor._validate_position(tx, ty)
        status = "✓ SAFE" if (vx, vy) == (tx, ty) else f"✗ CLAMPED to ({vx},{vy})"
        print(f"   Position ({tx},{ty}): {status}")
    
    print("\n4. Available Tools:")
    print(f"   xdotool: {'✓ Available' if motor.xdotool_available else '✗ Not found'}")
    print(f"   pyautogui: {'✓ Available' if motor.pyautogui_available else '✗ Not found'}")
    
    print("\n5. Keyboard Test (Simulated):")
    print("   Would type: 'Hello from Iri (ไอริ)'")
    print("   Would press: Enter")
    
    print("\n" + "=" * 60)
    print("Dry-run complete - No actual mouse/keyboard actions performed")
    print("=" * 60)


if __name__ == "__main__":
    test_motor_control()
