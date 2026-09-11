#!/bin/bash
#
# Setup Force Execution Keyboard Shortcuts for AE01M (Iri)
# Mode 2: Forced Shortcut Execution
#
# Shortcuts:
#   Super+Ctrl+M - Motor Control Force Run
#   Super+Ctrl+R - Immediate Task Execution
#

PROJECT_ROOT="$HOME/Projects/THE_TRANSCENDING_FORM"
SHORTCUT_SCRIPT="$PROJECT_ROOT/scripts/force_execution_shortcut.py"
LOG_FILE="$PROJECT_ROOT/logs/shortcut_mode_update.log"

echo "[Setup] Configuring Force Execution Keyboard Shortcuts..."
echo "[Setup] Project Root: $PROJECT_ROOT"
echo "[Setup] Log File: $LOG_FILE"

# Ensure script is executable
chmod +x "$SHORTCUT_SCRIPT"

# Create logs directory
mkdir -p "$PROJECT_ROOT/logs"

# Log configuration start
echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Keyboard Shortcut Setup Started" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Check if running on GNOME
if [ "$XDG_CURRENT_DESKTOP" = "GNOME" ] || [ "$XDG_CURRENT_DESKTOP" = "ubuntu:GNOME" ]; then
    echo "[Setup] Detected GNOME desktop environment"
    echo "[Setup] Configuring shortcuts via gsettings..."
    
    # Super+Ctrl+M - Motor Control Force Run
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ name 'AE01M Motor Control Force Run'
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ command "$PROJECT_ROOT/.venv/bin/python3 $SHORTCUT_SCRIPT motor"
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ binding '<Super><Ctrl>m'
    
    # Super+Ctrl+R - Immediate Task Execution
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/ name 'AE01M Immediate Task Execution'
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/ command "$PROJECT_ROOT/.venv/bin/python3 $SHORTCUT_SCRIPT immediate"
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/ binding '<Super><Ctrl>r'
    
    # Register custom keybindings
    gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/', '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/']"
    
    echo "[Setup] ✓ GNOME shortcuts configured"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] GNOME shortcuts configured successfully" >> "$LOG_FILE"
    
else
    echo "[Setup] Non-GNOME desktop detected, creating xbindkeys configuration..."
    
    # Create xbindkeys configuration
    XBINDKEYS_CONFIG="$HOME/.xbindkeysrc"
    
    # Backup existing config
    if [ -f "$XBINDKEYS_CONFIG" ]; then
        cp "$XBINDKEYS_CONFIG" "${XBINDKEYS_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
        echo "[Setup] Backed up existing xbindkeys config"
    fi
    
    # Add AE01M shortcuts
    cat >> "$XBINDKEYS_CONFIG" << EOF

# AE01M Force Execution Shortcuts
# Super+Ctrl+M - Motor Control Force Run
"$PROJECT_ROOT/.venv/bin/python3 $SHORTCUT_SCRIPT motor"
    Mod4+Control + m

# Super+Ctrl+R - Immediate Task Execution
"$PROJECT_ROOT/.venv/bin/python3 $SHORTCUT_SCRIPT immediate"
    Mod4+Control + r

EOF
    
    # Restart xbindkeys
    pkill xbindkeys 2>/dev/null
    xbindkeys &
    
    echo "[Setup] ✓ xbindkeys configuration updated"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] xbindkeys configuration updated" >> "$LOG_FILE"
fi

# Log shortcut details
cat >> "$LOG_FILE" << EOF

Keyboard Shortcuts Configured:
  1. Super+Ctrl+M - Motor Control Force Run
  2. Super+Ctrl+R - Immediate Task Execution

Behavior:
  - 5-second countdown before execution
  - Bypasses all idle checks
  - Overrides active screen restrictions
  - Ignores goal queues
  - Immediately executes top priority goal/subtask

Script Location: $SHORTCUT_SCRIPT
Log File: $LOG_FILE

Configuration Complete: $(date '+%Y-%m-%d %H:%M:%S')
EOF

echo ""
echo "[Setup] =============================================="
echo "[Setup] Keyboard Shortcuts Configured Successfully!"
echo "[Setup] =============================================="
echo "[Setup]"
echo "[Setup] Available Shortcuts:"
echo "[Setup]   • Super+Ctrl+M - Motor Control Force Run"
echo "[Setup]   • Super+Ctrl+R - Immediate Task Execution"
echo "[Setup]"
echo "[Setup] Configuration logged to:"
echo "[Setup]   $LOG_FILE"
echo "[Setup]"
echo "[Setup] =============================================="
