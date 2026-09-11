#!/usr/bin/env python3
"""
Raw audio level test - measures actual microphone input levels
"""
import speech_recognition as sr
import audioop

def test_raw_audio_level():
    print("\n" + "="*60)
    print(" 🎤 RAW AUDIO LEVEL TEST (2 seconds)")
    print("="*60)
    
    recognizer = sr.Recognizer()
    
    try:
        microphone = sr.Microphone(device_index=0)
        print("\n✓ Using: HDA Intel PCH: ALC255 Analog (hw:0,0)")
    except Exception as e:
        print(f"✗ Microphone error: {e}")
        return
    
    print("\n[Recording 2 seconds of raw audio...]")
    print("  Stay SILENT to measure noise floor")
    
    with microphone as source:
        # Don't calibrate - just record raw
        audio = recognizer.record(source, duration=2)
    
    # Get raw audio data
    raw_data = audio.get_raw_data()
    
    # Calculate RMS (root mean square) volume
    rms = audioop.rms(raw_data, audio.sample_width)
    
    print(f"\n✓ Audio captured: {len(raw_data)} bytes")
    print(f"  Sample rate: {audio.sample_rate} Hz")
    print(f"  Sample width: {audio.sample_width} bytes")
    print(f"  RMS level: {rms}")
    
    if rms < 300:
        print("\n✓ EXCELLENT - Very quiet, optimal for speech recognition")
    elif rms < 1000:
        print("\n✓ GOOD - Acceptable noise level")
    elif rms < 3000:
        print("\n⚠ MODERATE - Some background noise present")
    else:
        print("\n✗ HIGH - Excessive noise detected!")
        print("  Possible causes:")
        print("    - Music/video playing")
        print("    - Fan noise too close to microphone")
        print("    - Microphone boost too high")
        print("    - Electrical interference")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_raw_audio_level()
