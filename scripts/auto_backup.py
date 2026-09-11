#!/usr/bin/env python3
"""
Iri Automated Memory & State Backup System
Creates timestamped archives of Iri's memory, state, and cognitive data.
"""
import sys
import os
import tarfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional

# Configuration
PROJECT_ROOT = Path("/home/artid1994/Projects/THE_TRANSCENDING_FORM")
BACKUP_ROOT = Path.home() / "Projects" / "legacy_backup_archive" / "iri_memory_snapshots"
RETENTION_DAYS = 7

# Backup targets
BACKUP_TARGETS = [
    "memory.db",
    "neocortex_state.json",
    "heartbeat.json",
    "ttf_memory.txt",
    "03_Hippocampus/memory_store.db",
    "03_Hippocampus/knowledge_base.json",
    "03_Hippocampus/iri_state.json",
    "04_Cerebellum/iri_state.json",
    "01_Neocortex/state/",
    "logs/iri-evolution.log",
]

class IriBackup:
    """Automated backup manager for Iri memory and state."""
    
    def __init__(self, project_root: Path, backup_root: Path):
        self.project_root = project_root
        self.backup_root = backup_root
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.archive_name = f"iri_memory_{self.timestamp}.tar.gz"
        self.archive_path = self.backup_root / self.archive_name
        
    def create_backup_directory(self):
        """Ensure backup directory exists."""
        self.backup_root.mkdir(parents=True, exist_ok=True)
        print(f"✓ Backup directory: {self.backup_root}")
    
    def collect_files(self) -> List[Path]:
        """Collect all files to backup."""
        files_to_backup = []
        
        for target in BACKUP_TARGETS:
            target_path = self.project_root / target
            
            if target_path.exists():
                if target_path.is_file():
                    files_to_backup.append(target_path)
                    print(f"  + {target} ({target_path.stat().st_size:,} bytes)")
                elif target_path.is_dir():
                    # Add all files in directory
                    for file_path in target_path.rglob("*"):
                        if file_path.is_file():
                            files_to_backup.append(file_path)
                    print(f"  + {target}/ ({len(list(target_path.rglob('*')))} files)")
            else:
                print(f"  - {target} (not found, skipped)")
        
        return files_to_backup
    
    def create_archive(self, files: List[Path]) -> bool:
        """Create compressed tar archive of collected files."""
        try:
            print(f"\n📦 Creating archive: {self.archive_name}")
            
            with tarfile.open(self.archive_path, "w:gz") as tar:
                for file_path in files:
                    # Calculate relative path from project root
                    arcname = file_path.relative_to(self.project_root)
                    tar.add(file_path, arcname=arcname)
            
            archive_size = self.archive_path.stat().st_size
            archive_size_mb = archive_size / (1024 * 1024)
            
            print(f"✓ Archive created: {archive_size_mb:.2f} MB")
            print(f"✓ Location: {self.archive_path}")
            
            return True
            
        except Exception as e:
            print(f"✗ Archive creation failed: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period."""
        if not self.backup_root.exists():
            return
        
        cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)
        deleted_count = 0
        
        print(f"\n🗑️  Cleaning up backups older than {RETENTION_DAYS} days...")
        
        for backup_file in self.backup_root.glob("iri_memory_*.tar.gz"):
            try:
                # Extract timestamp from filename (remove .tar.gz extension)
                filename = backup_file.name
                timestamp_str = filename.replace("iri_memory_", "").replace(".tar.gz", "")
                file_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                
                if file_date < cutoff_date:
                    file_size_mb = backup_file.stat().st_size / (1024 * 1024)
                    backup_file.unlink()
                    deleted_count += 1
                    print(f"  - Deleted: {backup_file.name} ({file_size_mb:.2f} MB)")
                    
            except (ValueError, OSError) as e:
                print(f"  ⚠️  Could not process {backup_file.name}: {e}")
        
        if deleted_count == 0:
            print("  ✓ No old backups to clean up")
        else:
            print(f"✓ Cleaned up {deleted_count} old backup(s)")
    
    def list_backups(self):
        """List all existing backups."""
        if not self.backup_root.exists():
            print("No backups found")
            return
        
        backups = sorted(self.backup_root.glob("iri_memory_*.tar.gz"), reverse=True)
        
        if not backups:
            print("No backups found")
            return
        
        print(f"\n📋 Existing backups ({len(backups)} total):")
        
        for i, backup_file in enumerate(backups[:10], 1):  # Show last 10
            size_mb = backup_file.stat().st_size / (1024 * 1024)
            mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)
            age_days = (datetime.now() - mtime).days
            
            print(f"  {i}. {backup_file.name}")
            print(f"     Size: {size_mb:.2f} MB, Age: {age_days} days")
    
    def run(self) -> bool:
        """Execute complete backup workflow."""
        print("=" * 70)
        print("Iri Memory & State Backup")
        print("=" * 70)
        print(f"Timestamp: {self.timestamp}")
        print(f"Project: {self.project_root}")
        print()
        
        # Step 1: Create backup directory
        self.create_backup_directory()
        
        # Step 2: Collect files
        print(f"\n📂 Collecting files to backup...")
        files = self.collect_files()
        
        if not files:
            print("✗ No files found to backup")
            return False
        
        print(f"\n✓ Found {len(files)} files to backup")
        
        # Step 3: Create archive
        success = self.create_archive(files)
        
        if not success:
            return False
        
        # Step 4: Cleanup old backups
        self.cleanup_old_backups()
        
        # Step 5: List backups
        self.list_backups()
        
        print("\n" + "=" * 70)
        print("✓ Backup completed successfully")
        print("=" * 70)
        
        return True


def main():
    """Main entry point."""
    backup = IriBackup(PROJECT_ROOT, BACKUP_ROOT)
    success = backup.run()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
