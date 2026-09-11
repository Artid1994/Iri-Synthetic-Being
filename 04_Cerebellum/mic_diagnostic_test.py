#!/usr/bin/env python3
"""
Microphone Diagnostic Test - 3 second audio level verification
Tests speech recognition input pipeline for Iri voice system
"""
import speech_recognition as sr
import time

def test_microphone():
    print("\n" + "="*60)
    print(" 🎙️ MICROPHONE DIAGNOSTIC TEST")
    print("="*60)
    
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    
    try:
        # Use device 0 explicitly (HDA Intel PCH: ALC255 Analog)
        microphone = sr.Microphone(device_index=0)
        print("\n✓ Microphone device initialized")
        print(f"  Device index: 0 (HDA Intel PCH: ALC255 Analog)")
        print(f"  Device: {sr.Microphone.list_microphone_names()[0]}")
    except Exception as e:
        print(f"\n✗ FAILED: Cannot initialize microphone")
        print(f"  Error: {e}")
        return
    
    print("\n[Phase 1] Measuring ambient noise level...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        ambient_energy = recognizer.energy_threshold
        print(f"✓ Ambient noise calibrated")
        print(f"  Energy threshold: {ambient_energy}")
    
    print("\n[Phase 2] Recording 3-second audio sample...")
    print("  >>> SPEAK NOW (Thai or English) <<<")
    
    with microphone as source:
        recognizer.pause_threshold = 1.0
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            print("✓ Audio captured successfully")
            
            # Try to recognize
            print("\n[Phase 3] Attempting speech recognition (Thai)...")
            try:
                text = recognizer.recognize_google(audio, language="th-TH")
                print(f"✓ RECOGNIZED: '{text}'")
            except sr.UnknownValueError:
                print("⚠ Audio captured but speech not recognized")
                print("  Possible causes: too quiet, no speech, or background noise")
            except sr.RequestError as e:
                print(f"✗ Recognition service error: {e}")
                
        except sr.WaitTimeoutError:
            print("⚠ No audio detected within 3 seconds")
            print("  Possible causes:")
            print("    - Microphone muted or unplugged")
            print("    - Input level too low")
            print("    - Wrong audio device selected")
    
    print("\n" + "="*60)
    print(" DIAGNOSTIC COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_microphone()
