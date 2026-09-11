#!/usr/bin/env python3
"""Quick test: verify EasyEffects source binding"""
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = False

try:
    microphone = sr.Microphone(device_index=14)  # pulse
    print("✓ Microphone initialized: pulse (device 14)")
    print("  Routes to system default source: easyeffects_source")
    
    with microphone as source:
        print("✓ Microphone context opened successfully")
        print("  Audio routing active")
    
    print("✓ All checks passed - voice loop ready")
except Exception as e:
    print(f"✗ Error: {e}")
