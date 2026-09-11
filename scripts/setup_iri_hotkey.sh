#!/bin/bash
# Configure GNOME Hotkey for Iri Audio Listener
# Sets up Super+Ctrl+M to trigger Iri voice system

SCRIPT_PATH="/home/artid1994/Projects/THE_TRANSCENDING_FORM/scripts/iri_audio_listener.py"
PYTHON_PATH="/home/artid1994/Projects/THE_TRANSCENDING_FORM/.venv/bin/python"

echo "Configuring Iri hotkey binding..."

# Get existing custom keybindings
EXISTING=$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)

# Add iri-trigger to the list if not already there
if [[ "$EXISTING" == "@as []" ]]; then
    # No existing bindings
    gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/iri-trigger/']"
else
    # Append to existing bindings if not already present
    if [[ ! "$EXISTING" =~ "iri-trigger" ]]; then
        NEW_LIST=$(echo "$EXISTING" | sed "s/]$/, '\/org\/gnome\/settings-daemon\/plugins\/media-keys\/custom-keybindings\/iri-trigger\/']/" | sed "s/\[@as /[/")
        gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "$NEW_LIST"
    fi
fi

# Configure the binding
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/iri-trigger/ name 'Iri Voice Trigger'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/iri-trigger/ command "$PYTHON_PATH $SCRIPT_PATH"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/iri-trigger/ binding '<Super><Alt>i'

echo "✓ Hotkey configured: Super+Alt+I"
echo "✓ Command: $PYTHON_PATH $SCRIPT_PATH"
echo ""
echo "Test the hotkey by pressing Super+Alt+I"
echo "Check logs with: iri-ctl logs-bg"
