#!/usr/bin/env python3
"""
Brain Architecture Verification Script for AE01M (Iri).
Validates all 4 brain layer modules for syntax, imports, and structural integrity.
"""
import sys
import py_compile
from pathlib import Path
import importlib.util

PROJECT_ROOT = Path(__file__).parent

# Define all brain layer modules to verify
BRAIN_MODULES = [
    "01_Neocortex/executive_core.py",
    "02_Limbic/affective_filter.py",
    "03_Hippocampus/memory_store.py",
    "04_Cerebellum/voice_synthesis.py",
    "04_Cerebellum/voice_interactive_loop.py",
]

def verify_syntax(file_path: Path) -> bool:
    """Verify Python syntax by compiling the file."""
    try:
        py_compile.compile(str(file_path), doraise=True)
        print(f"✓ Syntax valid: {file_path.name}")
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ Syntax error in {file_path.name}: {e}")
        return False

def verify_import(file_path: Path) -> bool:
    """Verify module can be imported."""
    try:
        spec = importlib.util.spec_from_file_location(
            f"test_import_{file_path.stem}",
            file_path
        )
        if spec is None or spec.loader is None:
            print(f"✗ Import failed: {file_path.name} (cannot create spec)")
            return False
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✓ Import successful: {file_path.name}")
        return True
    except Exception as e:
        print(f"✗ Import error in {file_path.name}: {e}")
        return False

def verify_class_exists(file_path: Path, expected_classes: list) -> bool:
    """Verify expected classes exist in module."""
    try:
        spec = importlib.util.spec_from_file_location(
            f"test_class_{file_path.stem}",
            file_path
        )
        if spec is None or spec.loader is None:
            return False
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        for class_name in expected_classes:
            if not hasattr(module, class_name):
                print(f"✗ Missing class {class_name} in {file_path.name}")
                return False
        
        print(f"✓ Classes verified: {', '.join(expected_classes)} in {file_path.name}")
        return True
    except Exception as e:
        print(f"✗ Class verification error in {file_path.name}: {e}")
        return False

def main():
    """Execute complete brain architecture verification."""
    print("=" * 60)
    print("AE01M (Iri) Brain Architecture Verification")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Verify each brain module
    for module_path in BRAIN_MODULES:
        full_path = PROJECT_ROOT / module_path
        
        if not full_path.exists():
            print(f"✗ File not found: {module_path}")
            all_passed = False
            continue
        
        print(f"\n--- Verifying: {module_path} ---")
        
        # Syntax check
        if not verify_syntax(full_path):
            all_passed = False
            continue
        
        # Import check
        if not verify_import(full_path):
            all_passed = False
            continue
    
    # Verify critical classes
    print("\n--- Class Structure Verification ---")
    critical_checks = [
        ("01_Neocortex/executive_core.py", ["ExecutiveCore"]),
        ("02_Limbic/affective_filter.py", ["LimbicAffect"]),
        ("03_Hippocampus/memory_store.py", ["HippocampusMemory"]),
        ("04_Cerebellum/voice_interactive_loop.py", ["IriVoiceLoop"]),
    ]
    
    for module_path, classes in critical_checks:
        full_path = PROJECT_ROOT / module_path
        if not verify_class_exists(full_path, classes):
            all_passed = False
    
    # Final report
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL VERIFICATIONS PASSED")
        print("Brain architecture integration complete and verified.")
        return 0
    else:
        print("✗ VERIFICATION FAILED")
        print("Some modules failed verification. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
