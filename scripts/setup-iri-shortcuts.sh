#!/bin/bash
# setup-iri-shortcuts.sh
# Quick installation of Iri keyboard shortcuts for GNOME

set -e

CUSTOM_KEYS="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"
IRI_CTL="/home/artid1994/.local/bin/iri-ctl"

echo "Installing Iri keyboard shortcuts for GNOME..."

# Custom 0: Status (Super+Ctrl+I)
dconf write "$CUSTOM_KEYS/custom0/name" "'Iri Status'"
dconf write "$CUSTOM_KEYS/custom0/command" "'$IRI_CTL status'"
dconf write "$CUSTOM_KEYS/custom0/binding" "'<Super><Ctrl>i'"
echo "✓ Super+Ctrl+I → iri-ctl status"

# Custom 1: Toggle Motor (Super+Ctrl+M)
dconf write "$CUSTOM_KEYS/custom1/name" "'Iri Toggle Motor'"
dconf write "$CUSTOM_KEYS/custom1/command" "'$IRI_CTL toggle-motor'"
dconf write "$CUSTOM_KEYS/custom1/binding" "'<Super><Ctrl>m'"
echo "✓ Super+Ctrl+M → iri-ctl toggle-motor"

# Custom 2: Toggle Idle (Super+Ctrl+R)
dconf write "$CUSTOM_KEYS/custom2/name" "'Iri Toggle Idle'"
dconf write "$CUSTOM_KEYS/custom2/command" "'$IRI_CTL toggle-idle'"
dconf write "$CUSTOM_KEYS/custom2/binding" "'<Super><Ctrl>r'"
echo "✓ Super+Ctrl+R → iri-ctl toggle-idle"

# Custom 3: Emergency Abort (Super+Ctrl+Esc)
dconf write "$CUSTOM_KEYS/custom3/name" "'Iri Emergency Abort'"
dconf write "$CUSTOM_KEYS/custom3/command" "'$IRI_CTL abort'"
dconf write "$CUSTOM_KEYS/custom3/binding" "'<Super><Ctrl>Escape'"
echo "✓ Super+Ctrl+Esc → iri-ctl abort"

# Register all shortcuts
dconf write "$CUSTOM_KEYS" "['$CUSTOM_KEYS/custom0/', '$CUSTOM_KEYS/custom1/', '$CUSTOM_KEYS/custom2/', '$CUSTOM_KEYS/custom3/']"

echo ""
echo "=========================================="
echo "Iri keyboard shortcuts installed!"
echo "=========================================="
echo ""
echo "Available shortcuts:"
echo "  Super+Ctrl+I   → Show Iri status"
echo "  Super+Ctrl+M   → Toggle motor control"
echo "  Super+Ctrl+R   → Toggle research mode"
echo "  Super+Ctrl+Esc → Emergency abort"
echo ""
echo "Test with: iri-ctl status"
