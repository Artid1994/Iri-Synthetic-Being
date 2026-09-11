#!/usr/bin/env python3
"""
Force Execution Shortcut Handler for AE01M (Iri)
Mode 2: Forced Shortcut Execution

Listens for keyboard shortcuts:
  - Super+Ctrl+M (Motor Control Force Run)
  - Super+Ctrl+R (Immediate Task Execution)

When triggered:
  1. Announce: "Shortcut activated. Iri will begin execution in 5 seconds..."
  2. Wait 5 seconds countdown
  3. FORCE EXECUTION: Bypass all idle checks, override active screen restrictions,
     ignore goal queues, and immediately capture screen OCR and execute top priority goal.
"""
import os
import sys
import time
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "01_Neocortex"))
sys.path.insert(0, str(PROJECT_ROOT / "02_VisualCortex"))

from goal_engine import GoalEngine, GoalStatus
from autonomous_loop import AutonomousLoop, CircadianState
from screen_eye import ScreenEye

# Import pyautogui for mouse control
try:
    import pyautogui
    MOUSE_CONTROL_AVAILABLE = True
except ImportError:
    MOUSE_CONTROL_AVAILABLE = False

# Setup logging
log_dir = PROJECT_ROOT / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "shortcut_mode_update.log"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ForceExecutionTrigger:
    """Handles forced execution via keyboard shortcuts."""
    
    def __init__(self):
        """Initialize force execution trigger."""
        self.project_root = PROJECT_ROOT
        self.loop = AutonomousLoop(self.project_root)
        self.screen_eye = ScreenEye()
        logger.info("[ForceExecutionTrigger] Initialized")
    
    def announce_execution(self, shortcut_name: str):
        """
        Announce execution with Thai voice feedback via 04_Cerebellum.
        
        Args:
            shortcut_name: Name of the triggered shortcut
        """
        logger.info(f"[SHORTCUT] {shortcut_name} activated")
        
        # Determine Thai announcement based on shortcut
        if "Motor Control" in shortcut_name or "Super+Ctrl+M" in shortcut_name:
            announcement = "สลับโหมดการเคลื่อนไหวแล้วครับ"  # Motor mode switched
        elif "Immediate" in shortcut_name or "Super+Ctrl+R" in shortcut_name:
            announcement = "สลับโหมดการวิจัยแล้วครับ"  # Research mode switched
        elif "Status" in shortcut_name or "Super+Ctrl+I" in shortcut_name:
            announcement = "สถานะไอริ ปกติดีครับเจ้านาย"  # Iri status normal, Master
        elif "Emergency" in shortcut_name or "Super+Ctrl+Esc" in shortcut_name:
            announcement = "ยกเลิกการทำงานฉุกเฉินครับ"  # Emergency stop
        else:
            announcement = "รับทราบคำสั่งครับเจ้านาย"  # Command acknowledged, Master
        
        logger.info(f"[ANNOUNCE] {announcement}")
        
        try:
            # Use 04_Cerebellum voice synthesizer
            sys.path.insert(0, str(self.project_root / "04_Cerebellum"))
            from voice_synthesis import VoiceSynthesizer
            
            vs = VoiceSynthesizer()
            output_path = "/tmp/iri_hotkey_announce.mp3"
            
            # Synthesize
            result = vs.synthesize(announcement, output_path=output_path)
            
            if result:
                # Play with ffplay (non-blocking)
                subprocess.Popen(
                    ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", result],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        except Exception as e:
            logger.warning(f"[ANNOUNCE] Voice synthesis failed: {e}")
        except:
            # Fallback: just log
            logger.info("[ANNOUNCE] TTS not available, using log only")
        
        # 5-second countdown
        for i in range(5, 0, -1):
            logger.info(f"[COUNTDOWN] {i}...")
            time.sleep(1)
        
        logger.info("[COUNTDOWN] Starting execution NOW")
    
    def capture_screen_ocr(self) -> str:
        """
        Capture screen and perform OCR to understand current context.
        
        Returns:
            Extracted text from screen
        """
        logger.info("[OCR] Capturing screen...")
        
        # Use VisualCortex for screen capture
        try:
            screenshot_path = self.screen_eye.capture_screen()
            if screenshot_path:
                logger.info(f"[OCR] Screenshot saved via VisualCortex: {screenshot_path}")
            else:
                raise Exception("VisualCortex capture returned None")
        except Exception as e:
            logger.warning(f"[OCR] VisualCortex capture failed: {e}, falling back to scrot")
            
            # Fallback to scrot
            screenshot_path = "/tmp/iri_force_execution_screen.png"
            
            try:
                # Capture screenshot using scrot or gnome-screenshot
                result = subprocess.run(
                    ["scrot", "-o", screenshot_path],
                    timeout=5,
                    capture_output=True
                )
                
                if result.returncode != 0:
                    # Try gnome-screenshot as fallback
                    subprocess.run(
                        ["gnome-screenshot", "-f", screenshot_path],
                        timeout=5,
                        capture_output=True
                    )
                
                logger.info(f"[OCR] Screenshot saved: {screenshot_path}")
            except Exception as fallback_error:
                logger.error(f"[OCR] All capture methods failed: {fallback_error}")
                return ""
        
        # Perform OCR using tesseract
        try:
            ocr_result = subprocess.run(
                ["tesseract", str(screenshot_path), "stdout"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if ocr_result.returncode == 0:
                ocr_text = ocr_result.stdout.strip()
                logger.info(f"[OCR] Extracted {len(ocr_text)} characters")
                return ocr_text
            else:
                logger.warning(f"[OCR] Tesseract failed: {ocr_result.stderr}")
                return ""
        except Exception as e:
            logger.error(f"[OCR] OCR processing failed: {e}")
            return ""
    
    def execute_mouse_control_test(self):
        """
        Execute direct mouse control test with visible square movement pattern.
        Demonstrates active motor control on screen.
        """
        logger.info("[MOTOR] Starting direct mouse control test")
        
        # Check for pyautogui
        if not MOUSE_CONTROL_AVAILABLE:
            logger.error("[MOTOR] pyautogui not available! Install with: pip install pyautogui")
            print("ERROR: pyautogui not installed. Cannot control mouse.")
            return
        
        # Capture screen first using VisualCortex
        logger.info("[MOTOR] Capturing screen via VisualCortex...")
        try:
            screenshot_path = self.screen_eye.capture_screen()
            if screenshot_path:
                logger.info(f"[MOTOR] Screen captured: {screenshot_path}")
            else:
                logger.warning("[MOTOR] Screen capture returned None")
        except Exception as e:
            logger.warning(f"[MOTOR] Screen capture failed: {e}")
        
        # Get screen size
        screen_width, screen_height = pyautogui.size()
        logger.info(f"[MOTOR] Detected screen size: {screen_width}x{screen_height}")
        
        # Center screen coordinates
        center_x, center_y = screen_width // 2, screen_height // 2
        
        # Move to center
        logger.info(f"[MOTOR] Moving mouse to center: ({center_x}, {center_y})")
        pyautogui.moveTo(center_x, center_y, duration=0.3)
        time.sleep(0.3)
        
        # Draw a smooth square pattern
        # Square size: 200x200 pixels
        square_size = 200
        
        logger.info("[MOTOR] Executing square movement pattern")
        
        # Starting position (top-left of square)
        start_x = center_x - square_size // 2
        start_y = center_y - square_size // 2
        
        # Move to starting position
        pyautogui.moveTo(start_x, start_y, duration=0.2)
        time.sleep(0.2)
        
        # Draw square: Right -> Down -> Left -> Up
        # Using relative movements for smooth animation
        logger.info("[MOTOR] Drawing right edge...")
        pyautogui.moveRel(square_size, 0, duration=0.5)
        
        logger.info("[MOTOR] Drawing bottom edge...")
        pyautogui.moveRel(0, square_size, duration=0.5)
        
        logger.info("[MOTOR] Drawing left edge...")
        pyautogui.moveRel(-square_size, 0, duration=0.5)
        
        logger.info("[MOTOR] Drawing top edge...")
        pyautogui.moveRel(0, -square_size, duration=0.5)
        
        # Return to center
        time.sleep(0.2)
        logger.info("[MOTOR] Returning to center...")
        pyautogui.moveTo(center_x, center_y, duration=0.3)
        
        logger.info("[MOTOR] Mouse control test completed successfully")
        print("Mouse interaction test executed successfully")
    
    def force_execute(self, shortcut_name: str):
        """
        FORCE EXECUTION: Bypass all checks and execute top priority goal immediately.
        
        Args:
            shortcut_name: Name of the triggered shortcut
        """
        logger.info(f"[FORCE_EXEC] Triggered by {shortcut_name}")
        logger.info("[FORCE_EXEC] Bypassing ALL safety checks:")
        logger.info("[FORCE_EXEC]   - Idle time check: BYPASSED")
        logger.info("[FORCE_EXEC]   - User activity detection: BYPASSED")
        logger.info("[FORCE_EXEC]   - Active screen restriction: BYPASSED")
        logger.info("[FORCE_EXEC]   - Goal queue: BYPASSED")
        
        # Step 1: Announce execution
        self.announce_execution(shortcut_name)
        
        # Step 2: For Motor Control shortcut, execute mouse control test
        if "Motor Control" in shortcut_name or "Super+Ctrl+M" in shortcut_name:
            logger.info("[FORCE_EXEC] Motor Control shortcut detected - executing mouse test")
            self.execute_mouse_control_test()
            return  # Motor control test is the primary action for this shortcut
        
        # Step 3: Capture screen context (for other shortcuts)
        ocr_text = self.capture_screen_ocr()
        if ocr_text:
            logger.info(f"[FORCE_EXEC] Screen context captured: {ocr_text[:200]}...")
        
        # Step 3: Get top priority goal
        goal_engine = GoalEngine()
        goal = goal_engine.get_active_goal()
        
        if not goal:
            logger.warning("[FORCE_EXEC] No active goals found!")
            logger.info("[FORCE_EXEC] Creating default exploration goal...")
            
            # Create a default goal for exploration
            from goal_engine import Goal, GoalPriority, Subtask, SubtaskType
            
            default_goal = Goal(
                id=f"FORCED_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title="Forced Exploration Task",
                description="Execute immediate task based on screen context",
                priority=GoalPriority.HIGH,
                status=GoalStatus.IN_PROGRESS
            )
            
            # Add a simple verification subtask
            default_goal.subtasks.append(Subtask(
                id=f"{default_goal.id}_01",
                title="System Status Check",
                description="Check system status and active applications",
                type=SubtaskType.TERMINAL,
                command="ps aux | head -20",
                estimated_duration=5
            ))
            
            goal_engine.goals.append(default_goal)
            goal_engine.save_goals()
            goal = default_goal
        
        logger.info(f"[FORCE_EXEC] Executing goal: {goal.title} (priority: {goal.priority.value})")
        
        # Step 4: Execute goal immediately (bypass all checks in autonomous_loop)
        # Mark as in progress
        if goal.status == GoalStatus.PENDING:
            goal.status = GoalStatus.IN_PROGRESS
            goal_engine.save_goals()
        
        # Get next subtask
        subtask = goal_engine.get_next_subtask(goal)
        
        if not subtask:
            logger.info("[FORCE_EXEC] All subtasks completed!")
            goal.status = GoalStatus.COMPLETED
            goal_engine.save_goals()
            return
        
        logger.info(f"[FORCE_EXEC] Executing subtask: {subtask.title}")
        logger.info(f"[FORCE_EXEC] Type: {subtask.type.value}")
        logger.info(f"[FORCE_EXEC] Command: {subtask.command}")
        
        # Execute immediately using autonomous loop's execution methods
        try:
            result = self.loop._execute_terminal_subtask(subtask)
            
            # Update status
            goal_engine.update_subtask_status(
                goal.id, subtask.id,
                GoalStatus.COMPLETED, result
            )
            
            logger.info(f"[FORCE_EXEC] Subtask completed successfully")
            logger.info(f"[FORCE_EXEC] Result: {result[:200]}...")
            
        except Exception as e:
            logger.error(f"[FORCE_EXEC] Subtask failed: {e}")
            goal_engine.update_subtask_status(
                goal.id, subtask.id,
                GoalStatus.FAILED, str(e)
            )
        
        logger.info("[FORCE_EXEC] Force execution complete")
    
    def handle_shortcut(self, shortcut_name: str):
        """
        Handle shortcut trigger.
        
        Args:
            shortcut_name: Name of the triggered shortcut
        """
        logger.info(f"[SHORTCUT] Handling: {shortcut_name}")
        
        # Log to update file
        with open(log_file, 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{datetime.now().isoformat()}] SHORTCUT TRIGGERED: {shortcut_name}\n")
            f.write(f"{'='*60}\n")
        
        # Execute forced execution
        self.force_execute(shortcut_name)


def main():
    """Main entry point for shortcut handler."""
    
    if len(sys.argv) < 2:
        print("Usage: force_execution_shortcut.py <shortcut_name>")
        print("  shortcut_name: 'motor' (Super+Ctrl+M) or 'immediate' (Super+Ctrl+R)")
        sys.exit(1)
    
    shortcut_arg = sys.argv[1].lower()
    
    if shortcut_arg == "motor":
        shortcut_name = "Super+Ctrl+M (Motor Control Force Run)"
    elif shortcut_arg == "immediate":
        shortcut_name = "Super+Ctrl+R (Immediate Task Execution)"
    else:
        logger.error(f"Unknown shortcut: {shortcut_arg}")
        sys.exit(1)
    
    logger.info(f"[Main] Starting Force Execution Trigger for: {shortcut_name}")
    
    # Create trigger and handle shortcut
    trigger = ForceExecutionTrigger()
    trigger.handle_shortcut(shortcut_name)
    
    logger.info("[Main] Force execution complete")


if __name__ == "__main__":
    main()
