#!/usr/bin/env python3
"""
Iri Audio Hotkey Listener
Logs hotkey events and provides audio feedback.
Integrates with systemd service logging.
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import subprocess

# Project paths
PROJECT_ROOT = Path("/home/artid1994/Projects/THE_TRANSCENDING_FORM")
LOG_FILE = PROJECT_ROOT / "logs" / "iri-evolution.log"

def log_event(message: str):
    """Log event to evolution log file."""
    LOG_FILE.parent.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] HOTKEY: {message}\n")
    
    # Also log to systemd journal if available
    try:
        subprocess.run(
            ["logger", "-t", "iri-hotkey", message],
            check=False,
            timeout=1
        )
    except:
        pass

def play_audio_feedback():
    """Play audio feedback using ffplay."""
    try:
        # Try ffplay with system sound
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", "/usr/share/sounds/freedesktop/stereo/message.oga"],
            check=False,
            timeout=2,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        # Fallback to terminal bell
        print("\a", flush=True)

def speak_greeting():
    """Speak Thai greeting using 04_Cerebellum voice synthesizer."""
    greeting = "ครับเจ้านาย ผมไอริพร้อมรับคำสั่งครับ"
    
    try:
        # Use 04_Cerebellum voice synthesizer
        sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))
        from voice_synthesis import VoiceSynthesizer
        
        vs = VoiceSynthesizer()
        output_path = "/tmp/iri_greeting.mp3"
        
        # Synthesize
        result = vs.synthesize(greeting, output_path=output_path)
        
        if result:
            # Play with ffplay
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", result],
                check=False,
                timeout=10,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            Path(output_path).unlink(missing_ok=True)
    except:
        # Fallback to terminal bell
        print("\a", flush=True)

def show_notification(title: str, message: str):
    """Show desktop notification."""
    try:
        subprocess.run(
            ["notify-send", title, message, "--icon=dialog-information", "--expire-time=3000"],
            check=False,
            timeout=2,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        pass

def launch_iri_chat():
    """Launch Iri chat in terminal."""
    venv_python = PROJECT_ROOT / ".venv" / "bin" / "python"
    chat_script = PROJECT_ROOT / "scripts" / "iri_chat.py"
    
    # Try gnome-terminal first
    try:
        subprocess.Popen(
            ["gnome-terminal", "--title=Iri Chat (ไอริ)", "--", 
             "bash", "-c", f"cd {PROJECT_ROOT} && {venv_python} {chat_script}; exec bash"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except:
        pass
    
    # Fallback to xterm
    try:
        subprocess.Popen(
            ["xterm", "-T", "Iri Chat", "-e", 
             f"cd {PROJECT_ROOT} && {venv_python} {chat_script}; bash"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except:
        pass
    
    return False

def main():
    """Main hotkey handler."""
    log_event("Hotkey triggered by user")
    
    # Audio feedback
    play_audio_feedback()
    
    # Visual notification
    show_notification("Iri (ไอริ)", "กำลังเริ่มต้น Iri Chat ครับเจ้านาย")
    
    # Speak greeting (non-blocking)
    speak_greeting()
    
    # Launch chat
    if launch_iri_chat():
        log_event("Iri chat launched successfully")
    else:
        log_event("Warning: Could not launch terminal, check logs")
        show_notification("Iri (ไอริ)", "⚠️ ไม่สามารถเปิด terminal ได้")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
