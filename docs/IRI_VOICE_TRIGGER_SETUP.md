# Iri Voice Trigger Setup Guide

## Audio System Status

**✓ All Audio Components Working:**
- PulseAudio/PipeWire: ✓ Active
- System Sounds: ✓ Working
- espeak-ng: ✓ Installed (English + Thai)
- Edge-TTS: ✓ Installed (th-TH-NiwatNeural)
- Master Volume: 150% (unmuted)

## Voice Trigger Script

**Location:** `~/Projects/THE_TRANSCENDING_FORM/scripts/iri_voice_trigger.sh`

**Features:**
- Audible chime on activation
- Thai voice greeting: "ครับเจ้านาย ผมไอริพร้อมรับคำสั่งครับ"
- Visual notification
- Launches Iri chat in terminal
- Logging to `logs/voice_trigger.log`

**Audio Fallback Chain:**
1. Edge-TTS (th-TH-NiwatNeural) - Best quality
2. espeak-ng (Thai voice) - Fast offline
3. spd-say - System speech dispatcher
4. System beep - Minimal fallback

## Hotkey Setup (GNOME)

### Method 1: Using GNOME Settings GUI

1. Open Settings
   ```bash
   gnome-control-center
   ```

2. Navigate: **Keyboard** → **View and Customize Shortcuts** → **Custom Shortcuts**

3. Click **Add Shortcut** (+ button)

4. Fill in details:
   - **Name:** `Iri Voice Trigger`
   - **Command:** `/home/artid1994/Projects/THE_TRANSCENDING_FORM/scripts/iri_voice_trigger.sh`
   - **Shortcut:** Press `Super+Ctrl+M` (or `Super+Alt+I`)

5. Click **Add**

### Method 2: Using gsettings CLI

```bash
# Set custom keybinding for Iri
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/iri-trigger/']"

# Configure the binding
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/iri-trigger/ name 'Iri Voice Trigger'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/iri-trigger/ command '/home/artid1994/Projects/THE_TRANSCENDING_FORM/scripts/iri_voice_trigger.sh'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/iri-trigger/ binding '<Super><Ctrl>m'
```

### Method 3: Alternative Shortcut (Super+Alt+I)

```bash
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/iri-trigger/ binding '<Super><Alt>i'
```

## Verification

### Test Audio System
```bash
~/Projects/THE_TRANSCENDING_FORM/scripts/test_audio.sh
```

Expected output:
```
✓ System sound working
✓ espeak-ng working
✓ Thai speech working
✓ Edge-TTS Thai voice working
```

### Test Voice Trigger Manually
```bash
~/Projects/THE_TRANSCENDING_FORM/scripts/iri_voice_trigger.sh
```

Expected behavior:
1. Hear system chime
2. See notification: "กำลังเริ่มต้น Iri Chat ครับเจ้านาย"
3. Hear greeting: "ครับเจ้านาย ผมไอริพร้อมรับคำสั่งครับ"
4. Terminal opens with Iri chat

### Check Logs
```bash
tail -f ~/Projects/THE_TRANSCENDING_FORM/logs/voice_trigger.log
```

## Troubleshooting

### No Audio Output
1. Check volume:
   ```bash
   amixer get Master
   pactl list sinks
   ```

2. Test system sound:
   ```bash
   paplay /usr/share/sounds/freedesktop/stereo/message.oga
   ```

3. Unmute if needed:
   ```bash
   amixer set Master unmute
   amixer set Master 100%
   ```

### Edge-TTS Not Working
Edge-TTS requires internet connection for first-time voice download.

Fallback: Script will use espeak-ng automatically.

### Hotkey Not Working
1. Check existing bindings:
   ```bash
   gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings
   ```

2. Verify script is executable:
   ```bash
   ls -la ~/Projects/THE_TRANSCENDING_FORM/scripts/iri_voice_trigger.sh
   ```

3. Try alternative key combination if conflict exists

### Terminal Not Opening
Script supports multiple terminals:
- gnome-terminal (GNOME default)
- xterm (fallback)
- konsole (KDE)

If none available, runs in background with notification.

## Recommended Hotkeys

**Primary:** `Super+Ctrl+M` (M for "Machine" or "ไมโครโฟน")
**Alternative:** `Super+Alt+I` (I for "Iri")
**Casual:** `Super+Space` (if not used by launcher)

## Usage

1. Press hotkey: `Super+Ctrl+M`
2. Wait for audio greeting
3. Type Thai/English commands
4. Iri responds with system inspection or conversation

**Example Commands:**
- `ตรวจสภาพเครื่อง` → System health report
- `สวัสดี` → Greeting
- `วิเคราะห์ระบบ` → Full system analysis
- `exit` → Exit chat

## Integration Status

✓ Voice trigger script: Created
✓ Audio test script: Created
✓ Audio system: Verified working
✓ Edge-TTS: Available (th-TH-NiwatNeural)
✓ espeak-ng fallback: Available
✓ System sounds: Working
⏳ Hotkey binding: User action required

**Status:** Ready for hotkey configuration
