"""
Media & System Control Tool
Advanced OS integration for XFCE/Linux environments.
"""

import subprocess
import os
from typing import Optional, Dict, List


class MediaSystemControl:
    """System control and media management tool."""
    
    def __init__(self):
        self.timeout = 10
    
    def get_audio_volume(self) -> Optional[int]:
        """Get current system audio volume (0-100)."""
        try:
            # Try pactl (PulseAudio)
            result = subprocess.run(
                ['pactl', 'get-sink-volume', '@DEFAULT_SINK@'],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if result.returncode == 0:
                # Parse volume percentage
                import re
                match = re.search(r'(\d+)%', result.stdout)
                if match:
                    return int(match.group(1))
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return None
    
    def set_audio_volume(self, volume: int) -> bool:
        """Set system audio volume (0-100)."""
        try:
            volume = max(0, min(100, volume))  # Clamp to 0-100
            result = subprocess.run(
                ['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{volume}%'],
                capture_output=True,
                timeout=self.timeout
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def take_screenshot(self, filepath: str) -> bool:
        """Take screenshot using available tool."""
        try:
            # Try scrot first
            result = subprocess.run(
                ['scrot', filepath],
                capture_output=True,
                timeout=self.timeout
            )
            if result.returncode == 0:
                return os.path.exists(filepath)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Try import (ImageMagick)
        try:
            result = subprocess.run(
                ['import', '-window', 'root', filepath],
                capture_output=True,
                timeout=self.timeout
            )
            return result.returncode == 0 and os.path.exists(filepath)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return False
    
    def get_process_list(self) -> List[Dict[str, str]]:
        """Get list of running processes (top 10 by CPU)."""
        try:
            result = subprocess.run(
                ['ps', 'aux', '--sort=-%cpu'],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if result.returncode != 0:
                return []
            
            lines = result.stdout.strip().split('\n')[1:11]  # Skip header, take top 10
            processes = []
            
            for line in lines:
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    processes.append({
                        'user': parts[0],
                        'pid': parts[1],
                        'cpu': parts[2],
                        'mem': parts[3],
                        'command': parts[10][:50]  # Truncate command
                    })
            
            return processes
        
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return []
    
    def get_memory_usage(self) -> Optional[Dict[str, float]]:
        """Get system memory usage."""
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            import re
            total = int(re.search(r'MemTotal:\s+(\d+)', meminfo).group(1))
            available = int(re.search(r'MemAvailable:\s+(\d+)', meminfo).group(1))
            
            used = total - available
            used_percent = (used / total) * 100
            
            return {
                'total_mb': total / 1024,
                'used_mb': used / 1024,
                'available_mb': available / 1024,
                'used_percent': used_percent
            }
        
        except Exception:
            return None
