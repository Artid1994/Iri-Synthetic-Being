#!/usr/bin/env python3
"""
System Inspector Skill
Autonomous system and project health inspection without external LLM calls.
"""
import os
import subprocess
import psutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class SystemInspector:
    """Inspect system health, project status, and resource usage."""
    
    def __init__(self, project_root: Optional[Path] = None):
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        self.project_root = Path(project_root)
    
    def inspect_all(self) -> Dict[str, any]:
        """Run complete system and project inspection."""
        return {
            "timestamp": datetime.now().isoformat(),
            "system": self.inspect_system(),
            "project": self.inspect_project(),
            "git": self.inspect_git(),
            "processes": self.inspect_processes(),
        }
    
    def inspect_system(self) -> Dict[str, any]:
        """Inspect system resources (CPU, memory, disk)."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(str(self.project_root))
        
        return {
            "cpu": {
                "usage_percent": cpu_percent,
                "count": psutil.cpu_count(),
                "status": "normal" if cpu_percent < 80 else "high"
            },
            "memory": {
                "total_mb": memory.total // (1024 * 1024),
                "used_mb": memory.used // (1024 * 1024),
                "available_mb": memory.available // (1024 * 1024),
                "percent": memory.percent,
                "status": "normal" if memory.percent < 80 else "high"
            },
            "disk": {
                "total_gb": disk.total // (1024 * 1024 * 1024),
                "used_gb": disk.used // (1024 * 1024 * 1024),
                "free_gb": disk.free // (1024 * 1024 * 1024),
                "percent": disk.percent,
                "status": "normal" if disk.percent < 90 else "critical"
            }
        }
    
    def inspect_project(self) -> Dict[str, any]:
        """Inspect project structure and health."""
        result = {
            "root": str(self.project_root),
            "exists": self.project_root.exists(),
            "structure": {}
        }
        
        if not self.project_root.exists():
            return result
        
        # Check key directories
        key_dirs = [
            "00_BrainStem",
            "01_Neocortex",
            "02_VisualCortex",
            "03_Hippocampus",
            "04_Cerebellum",
            "runtime",
            "scripts",
            "tests",
            "logs",
            ".venv"
        ]
        
        for dir_name in key_dirs:
            dir_path = self.project_root / dir_name
            result["structure"][dir_name] = {
                "exists": dir_path.exists(),
                "is_dir": dir_path.is_dir() if dir_path.exists() else False
            }
            
            # Count Python files
            if dir_path.exists() and dir_path.is_dir():
                py_files = list(dir_path.glob("**/*.py"))
                result["structure"][dir_name]["python_files"] = len(py_files)
        
        # Check virtualenv
        venv_python = self.project_root / ".venv" / "bin" / "python"
        result["virtualenv_active"] = venv_python.exists()
        
        return result
    
    def inspect_git(self) -> Dict[str, any]:
        """Inspect Git repository status."""
        result = {
            "is_repo": False,
            "branch": None,
            "status": None,
            "uncommitted_changes": False,
            "recent_commits": []
        }
        
        git_dir = self.project_root / ".git"
        if not git_dir.exists():
            return result
        
        result["is_repo"] = True
        
        try:
            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            if branch_result.returncode == 0:
                result["branch"] = branch_result.stdout.strip()
            
            # Get status
            status_result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            if status_result.returncode == 0:
                status = status_result.stdout.strip()
                result["status"] = status
                result["uncommitted_changes"] = len(status) > 0
            
            # Get recent commits
            log_result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            if log_result.returncode == 0:
                commits = log_result.stdout.strip().split("\n")
                result["recent_commits"] = [c for c in commits if c]
        
        except (subprocess.TimeoutExpired, Exception) as e:
            result["error"] = str(e)
        
        return result
    
    def inspect_processes(self) -> Dict[str, any]:
        """Inspect running Python processes related to the project."""
        result = {
            "iri_processes": [],
            "python_processes": 0
        }
        
        project_name = self.project_root.name
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                pinfo = proc.info
                if pinfo['name'] == 'python' or pinfo['name'] == 'python3':
                    result["python_processes"] += 1
                    
                    # Check if it's our project
                    cmdline = pinfo.get('cmdline', [])
                    if any(project_name in str(arg) for arg in cmdline):
                        result["iri_processes"].append({
                            "pid": pinfo['pid'],
                            "cmdline": ' '.join(cmdline[-2:]) if len(cmdline) > 1 else '',
                            "cpu_percent": pinfo.get('cpu_percent', 0),
                            "memory_mb": pinfo['memory_info'].rss // (1024 * 1024) if pinfo.get('memory_info') else 0
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return result
    
    def format_report(self, inspection: Dict) -> str:
        """Format inspection results as Thai text report."""
        lines = []
        lines.append("=" * 60)
        lines.append("รายงานสภาพระบบ (System Health Report)")
        lines.append("=" * 60)
        lines.append(f"เวลา: {inspection['timestamp']}")
        lines.append("")
        
        # System resources
        sys = inspection['system']
        lines.append("📊 ทรัพยากรระบบ (System Resources):")
        lines.append(f"  CPU: {sys['cpu']['usage_percent']:.1f}% ({sys['cpu']['count']} cores) - {sys['cpu']['status']}")
        lines.append(f"  Memory: {sys['memory']['used_mb']:,} MB / {sys['memory']['total_mb']:,} MB ({sys['memory']['percent']:.1f}%) - {sys['memory']['status']}")
        lines.append(f"  Disk: {sys['disk']['used_gb']} GB / {sys['disk']['total_gb']} GB ({sys['disk']['percent']:.1f}%) - {sys['disk']['status']}")
        lines.append("")
        
        # Project structure
        proj = inspection['project']
        lines.append("📁 โครงสร้างโปรเจกต์ (Project Structure):")
        lines.append(f"  Root: {proj['root']}")
        lines.append(f"  Virtual Environment: {'✓ Active' if proj['virtualenv_active'] else '✗ Not found'}")
        
        brain_regions = ['00_BrainStem', '01_Neocortex', '02_VisualCortex', '03_Hippocampus', '04_Cerebellum']
        for region in brain_regions:
            if region in proj['structure']:
                info = proj['structure'][region]
                status = "✓" if info['exists'] else "✗"
                py_count = info.get('python_files', 0)
                lines.append(f"  {region}: {status} ({py_count} Python files)")
        lines.append("")
        
        # Git status
        git = inspection['git']
        lines.append("🔀 Git Status:")
        if git['is_repo']:
            lines.append(f"  Branch: {git['branch']}")
            lines.append(f"  Uncommitted changes: {'Yes' if git['uncommitted_changes'] else 'No'}")
            if git['recent_commits']:
                lines.append("  Recent commits:")
                for commit in git['recent_commits'][:3]:
                    lines.append(f"    {commit}")
        else:
            lines.append("  Not a Git repository")
        lines.append("")
        
        # Processes
        procs = inspection['processes']
        lines.append("🔄 Iri Processes:")
        if procs['iri_processes']:
            for proc in procs['iri_processes']:
                lines.append(f"  PID {proc['pid']}: {proc['cmdline']}")
                lines.append(f"    CPU: {proc['cpu_percent']:.1f}%, Memory: {proc['memory_mb']} MB")
        else:
            lines.append("  No Iri processes running")
        lines.append(f"  Total Python processes: {procs['python_processes']}")
        lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


# Standalone execution for testing
if __name__ == "__main__":
    inspector = SystemInspector()
    inspection = inspector.inspect_all()
    report = inspector.format_report(inspection)
    print(report)
