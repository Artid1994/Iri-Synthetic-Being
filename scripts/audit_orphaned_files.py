#!/usr/bin/env python3
"""
Safe Read-Only Audit: Identify Potentially Orphaned Files
No files will be moved or deleted - report only.
"""
import os
import ast
from pathlib import Path
from typing import Set, List, Dict
import json
import time

PROJECT_ROOT = Path.home() / "Projects" / "THE_TRANSCENDING_FORM"

# Core architectural folders that must be preserved
CORE_FOLDERS = {
    "00_BrainStem",
    "01_Neocortex",
    "02_VisualCortex", 
    "03_Hippocampus",
    "04_Cerebellum",
    "05_Limbic",
    ".venv",
    "logs",
    "docs",
    "scripts",
    ".git"
}

# Essential root files that should never be archived
ESSENTIAL_ROOT_FILES = {
    ".gitignore",
    "README.md",
    "AGENTS.md",
    "PROJECT_PLAN.md",
    "MASTER_DEVELOPMENT_PLAN.md",
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
    ".python-version"
}

# File extensions that are likely temporary/cache
TEMP_EXTENSIONS = {
    ".tmp", ".temp", ".bak", ".swp", "~", 
    ".pyc", ".pyo", "__pycache__"
}

def find_all_python_imports(root: Path) -> Set[str]:
    """Find all module names imported in Python files."""
    imported_modules = set()
    
    for py_file in root.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        # Extract just the module name
                        module = alias.name.split('.')[0]
                        imported_modules.add(module)
                        
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module = node.module.split('.')[0]
                        imported_modules.add(module)
                        
        except Exception as e:
            print(f"[Audit] Could not parse {py_file}: {e}")
            continue
    
    return imported_modules

def find_referenced_files(root: Path) -> Set[str]:
    """Find files referenced in code via string patterns."""
    referenced = set()
    
    for py_file in root.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for common file reference patterns
            import re
            
            # Path() constructor
            path_refs = re.findall(r'Path\(["\']([^"\']+)["\']\)', content)
            referenced.update(path_refs)
            
            # open() calls
            open_refs = re.findall(r'open\(["\']([^"\']+)["\']\)', content)
            referenced.update(open_refs)
            
            # JSON/config file references
            json_refs = re.findall(r'["\']([^"\']*\.json)["\']', content)
            referenced.update(json_refs)
            
            md_refs = re.findall(r'["\']([^"\']*\.md)["\']', content)
            referenced.update(md_refs)
            
        except Exception as e:
            continue
    
    return referenced

def check_systemd_services() -> Dict[str, List[str]]:
    """Check systemd service files for referenced paths."""
    service_refs = {}
    
    systemd_dir = Path.home() / ".config" / "systemd" / "user"
    
    for service_file in systemd_dir.glob("iri-*.service"):
        try:
            with open(service_file, 'r') as f:
                content = f.read()
            
            refs = []
            for line in content.splitlines():
                if "THE_TRANSCENDING_FORM" in line:
                    refs.append(line.strip())
            
            if refs:
                service_refs[service_file.name] = refs
                
        except Exception as e:
            print(f"[Audit] Could not read {service_file}: {e}")
    
    return service_refs

def audit_project():
    """Perform complete read-only audit."""
    print("=" * 70)
    print("READ-ONLY AUDIT: Potentially Orphaned Files")
    print("NO FILES WILL BE MOVED OR DELETED")
    print("=" * 70)
    
    report = []
    report.append("=" * 70)
    report.append("ORPHANED FILES AUDIT REPORT")
    report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Project: {PROJECT_ROOT}")
    report.append("=" * 70)
    report.append("")
    
    # Step 1: Find all Python imports
    print("\n[1/6] Analyzing Python imports...")
    imported_modules = find_all_python_imports(PROJECT_ROOT)
    report.append(f"1. PYTHON IMPORTS ANALYSIS")
    report.append(f"   Found {len(imported_modules)} imported module names")
    report.append("")
    
    # Step 2: Find referenced files
    print("[2/6] Finding file references in code...")
    referenced_files = find_referenced_files(PROJECT_ROOT)
    report.append(f"2. FILE REFERENCES IN CODE")
    report.append(f"   Found {len(referenced_files)} file references")
    report.append("")
    
    # Step 3: Check systemd services
    print("[3/6] Checking systemd service references...")
    service_refs = check_systemd_services()
    report.append(f"3. SYSTEMD SERVICE REFERENCES")
    for service, refs in service_refs.items():
        report.append(f"   {service}:")
        for ref in refs:
            report.append(f"     {ref}")
    report.append("")
    
    # Step 4: Scan all project files
    print("[4/6] Scanning all project files...")
    all_files = []
    for item in PROJECT_ROOT.rglob("*"):
        if item.is_file():
            # Skip .git internals
            if ".git/" in str(item):
                continue
            all_files.append(item)
    
    report.append(f"4. PROJECT FILE INVENTORY")
    report.append(f"   Total files scanned: {len(all_files)}")
    report.append("")
    
    # Step 5: Categorize files
    print("[5/6] Categorizing files...")
    
    core_folder_files = []
    essential_root = []
    temp_files = []
    orphaned_candidates = []
    
    for file_path in all_files:
        rel_path = file_path.relative_to(PROJECT_ROOT)
        
        # Check if in core folder
        in_core_folder = any(
            str(rel_path).startswith(folder + "/") or str(rel_path) == folder
            for folder in CORE_FOLDERS
        )
        
        if in_core_folder:
            core_folder_files.append(rel_path)
            continue
        
        # Check if essential root file
        if rel_path.parent == Path(".") and rel_path.name in ESSENTIAL_ROOT_FILES:
            essential_root.append(rel_path)
            continue
        
        # Check if temp file
        if any(str(rel_path).endswith(ext) for ext in TEMP_EXTENSIONS):
            temp_files.append(rel_path)
            continue
        
        # Check if Python module that's imported
        if file_path.suffix == ".py":
            module_name = file_path.stem
            if module_name in imported_modules:
                core_folder_files.append(rel_path)
                continue
        
        # Check if referenced in code
        is_referenced = any(
            str(rel_path) in ref or file_path.name in ref
            for ref in referenced_files
        )
        
        if is_referenced:
            core_folder_files.append(rel_path)
            continue
        
        # Otherwise, candidate for archiving
        orphaned_candidates.append(rel_path)
    
    # Generate report
    report.append(f"5. FILE CATEGORIZATION")
    report.append(f"   Core folder files (preserved): {len(core_folder_files)}")
    report.append(f"   Essential root files (preserved): {len(essential_root)}")
    report.append(f"   Temporary files (candidates): {len(temp_files)}")
    report.append(f"   Orphaned candidates: {len(orphaned_candidates)}")
    report.append("")
    
    # Step 6: Detail orphaned candidates
    print("[6/6] Listing orphaned candidates...")
    
    report.append("6. ORPHANED FILE CANDIDATES")
    report.append("   (Files not in core folders, not imported, not referenced)")
    report.append("")
    
    if orphaned_candidates:
        # Group by directory
        by_dir = {}
        for path in orphaned_candidates:
            parent = str(path.parent)
            if parent not in by_dir:
                by_dir[parent] = []
            by_dir[parent].append(path.name)
        
        for dir_name in sorted(by_dir.keys()):
            report.append(f"   {dir_name}/")
            for filename in sorted(by_dir[dir_name]):
                file_path = PROJECT_ROOT / dir_name / filename
                size = file_path.stat().st_size if file_path.exists() else 0
                report.append(f"     - {filename} ({size:,} bytes)")
            report.append("")
    else:
        report.append("   No orphaned files detected!")
        report.append("")
    
    # Temp files section
    report.append("7. TEMPORARY FILES")
    report.append("   (Cache, backup, compiled files)")
    report.append("")
    
    if temp_files:
        for temp_file in sorted(temp_files):
            file_path = PROJECT_ROOT / temp_file
            size = file_path.stat().st_size if file_path.exists() else 0
            report.append(f"   - {temp_file} ({size:,} bytes)")
        report.append("")
    else:
        report.append("   No temporary files detected!")
        report.append("")
    
    # Summary
    report.append("=" * 70)
    report.append("SUMMARY")
    report.append("=" * 70)
    report.append(f"Total files scanned: {len(all_files)}")
    report.append(f"Core/Essential files: {len(core_folder_files) + len(essential_root)}")
    report.append(f"Orphaned candidates: {len(orphaned_candidates)}")
    report.append(f"Temporary files: {len(temp_files)}")
    report.append("")
    report.append("RECOMMENDED ACTION:")
    report.append("1. Review orphaned candidates manually")
    report.append("2. Verify they are truly not needed")
    report.append("3. Create archive directory: ~/THE_TRANSCENDING_FORM_ARCHIVE")
    report.append("4. Move verified orphaned files to archive")
    report.append("5. Test all services after archiving")
    report.append("")
    report.append("SAFETY NOTES:")
    report.append("- All core architectural folders preserved")
    report.append("- All imported Python modules preserved")
    report.append("- All referenced files preserved")
    report.append("- Systemd service paths checked")
    report.append("- No files have been moved or deleted")
    report.append("")
    report.append("=" * 70)
    report.append("END OF AUDIT REPORT")
    report.append("=" * 70)
    
    # Print summary
    print("\n" + "=" * 70)
    print("AUDIT COMPLETE")
    print("=" * 70)
    print(f"Orphaned candidates: {len(orphaned_candidates)}")
    print(f"Temporary files: {len(temp_files)}")
    print(f"Core files preserved: {len(core_folder_files) + len(essential_root)}")
    print("=" * 70)
    
    return "\n".join(report)

if __name__ == "__main__":
    report = audit_project()
    
    # Save report
    log_file = PROJECT_ROOT / "logs" / "orphan_files_audit.log"
    log_file.parent.mkdir(exist_ok=True)
    
    with open(log_file, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved: {log_file}")
