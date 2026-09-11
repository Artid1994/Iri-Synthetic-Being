#!/bin/bash
# Iri Voice Trigger Script
# Hotkey: Super+Ctrl+M or Super+Alt+I
# Provides audible feedback and launches Iri chat

set -e

PROJECT_ROOT="/home/artid1994/Projects/THE_TRANSCENDING_FORM"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"
LOG_FILE="$PROJECT_ROOT/logs/voice_trigger.log"

# Ensure log directory exists
mkdir -p "$PROJECT_ROOT/logs"

# Log trigger
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Voice trigger activated" >> "$LOG_FILE"

# Function to play audible chime/beep
play_chime() {
    # Try multiple methods for audio feedback
    
    # Method 1: System beep
    if command -v paplay >/dev/null 2>&1; then
        paplay /usr/share/sounds/freedesktop/stereo/message.oga 2>/dev/null &
        return 0
    fi
    
    # Method 2: PC speaker beep
    if command -v beep >/dev/null 2>&1; then
        beep -f 1000 -l 100 2>/dev/null &
        return 0
    fi
    
    # Method 3: Terminal bell
    printf '\a'
}

# Function to speak greeting
speak_greeting() {
    local text="$1"
    
    # Try Edge-TTS (best quality for Thai)
    if command -v edge-tts >/dev/null 2>&1; then
        TMP_AUDIO=$(mktemp --suffix=.mp3)
        edge-tts --voice th-TH-NiwatNeural --text "$text" --write-media "$TMP_AUDIO" >/dev/null 2>&1 && \
        paplay "$TMP_AUDIO" 2>/dev/null && \
        rm -f "$TMP_AUDIO" &
        return 0
    fi
    
    # Fallback: espeak-ng
    if command -v espeak-ng >/dev/null 2>&1; then
        espeak-ng -v th "$text" 2>/dev/null &
        return 0
    fi
    
    # Fallback: spd-say
    if command -v spd-say >/dev/null 2>&1; then
        spd-say -l th "$text" 2>/dev/null &
        return 0
    fi
}

# Function to show notification
show_notification() {
    if command -v notify-send >/dev/null 2>&1; then
        notify-send "Iri (ไอริ)" "$1" --icon=dialog-information --expire-time=3000 2>/dev/null &
    fi
}

# Main execution
main() {
    # Play audible chime
    play_chime
    
    # Show notification
    show_notification "กำลังเริ่มต้น Iri Chat ครับเจ้านาย"
    
    # Speak greeting (non-blocking)
    speak_greeting "ครับเจ้านาย ผมไอริพร้อมรับคำสั่งครับ"
    
    # Wait a moment for audio to start
    sleep 0.5
    
    # Launch Iri chat in terminal
    if command -v gnome-terminal >/dev/null 2>&1; then
        gnome-terminal --title="Iri Chat (ไอริ)" -- bash -c "cd '$PROJECT_ROOT' && '$VENV_PYTHON' scripts/iri_chat.py; exec bash"
    elif command -v xterm >/dev/null 2>&1; then
        xterm -T "Iri Chat" -e "cd '$PROJECT_ROOT' && '$VENV_PYTHON' scripts/iri_chat.py; bash" &
    elif command -v konsole >/dev/null 2>&1; then
        konsole --title "Iri Chat" -e bash -c "cd '$PROJECT_ROOT' && '$VENV_PYTHON' scripts/iri_chat.py; exec bash" &
    else
        # Fallback: Run in background and notify
        show_notification "เปิด Iri Chat แล้วครับ (รันใน background)"
        cd "$PROJECT_ROOT" && "$VENV_PYTHON" scripts/iri_chat.py >> "$LOG_FILE" 2>&1 &
    fi
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iri chat launched successfully" >> "$LOG_FILE"
}

# Execute
main

exit 0
