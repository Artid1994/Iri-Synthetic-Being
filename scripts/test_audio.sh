#!/bin/bash
# Quick Audio Test for Iri Voice System
# Tests available audio output methods

echo "=== Iri Voice System - Audio Test ==="
echo ""

# Test 1: Check audio devices
echo "1. Audio Devices:"
pactl list sinks short 2>/dev/null | head -3 || echo "  ⚠️  PulseAudio not available"
echo ""

# Test 2: Check volume
echo "2. Master Volume:"
amixer get Master 2>/dev/null | grep -E "Playback|%" | head -2 || echo "  ⚠️  ALSA mixer not available"
echo ""

# Test 3: Test system sound
echo "3. Testing system beep..."
if paplay /usr/share/sounds/freedesktop/stereo/message.oga 2>/dev/null; then
    echo "  ✓ System sound working"
else
    echo "  ⚠️  System sound failed"
fi
sleep 1

# Test 4: Test espeak-ng
echo ""
echo "4. Testing espeak-ng (English)..."
if command -v espeak-ng >/dev/null 2>&1; then
    espeak-ng "Audio test successful" 2>/dev/null && echo "  ✓ espeak-ng working" || echo "  ✗ espeak-ng failed"
else
    echo "  ⚠️  espeak-ng not installed"
fi
sleep 1

# Test 5: Test Thai speech
echo ""
echo "5. Testing Thai speech..."
if command -v espeak-ng >/dev/null 2>&1; then
    espeak-ng -v th "ทดสอบเสียงภาษาไทย" 2>/dev/null && echo "  ✓ Thai speech working" || echo "  ⚠️  Thai voice not available"
else
    echo "  ⚠️  espeak-ng not installed"
fi

# Test 6: Check Edge-TTS
echo ""
echo "6. Checking Edge-TTS availability..."
if command -v edge-tts >/dev/null 2>&1; then
    echo "  ✓ Edge-TTS installed"
    echo "  Testing Edge-TTS (th-TH-NiwatNeural)..."
    TMP_AUDIO=$(mktemp --suffix=.mp3)
    if edge-tts --voice th-TH-NiwatNeural --text "สวัสดีครับเจ้านาย ผมไอริครับ" --write-media "$TMP_AUDIO" >/dev/null 2>&1; then
        paplay "$TMP_AUDIO" 2>/dev/null && echo "  ✓ Edge-TTS Thai voice working"
        rm -f "$TMP_AUDIO"
    else
        echo "  ⚠️  Edge-TTS failed (network required)"
    fi
else
    echo "  ⚠️  Edge-TTS not installed (pip install edge-tts)"
fi

echo ""
echo "=== Audio Test Complete ==="
