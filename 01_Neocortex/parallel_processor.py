"""
Parallel Processor - Async dual-threading architecture
Decouples user interaction from background autonomous processing.
"""

import asyncio
import threading
import queue
import time
from typing import Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ProcessingStream(Enum):
    """Processing stream identifier."""
    FOREGROUND = "foreground"  # User interaction
    BACKGROUND = "background"  # Autonomous tasks


@dataclass
class Task:
    """Async task descriptor."""
    stream: ProcessingStream
    function: Callable
    args: tuple
    kwargs: dict
    priority: int = 0  # Higher = more urgent


class ParallelProcessor:
    """Dual-threading cognitive architecture."""
    
    def __init__(self):
        # Task queues
        self.foreground_queue = queue.PriorityQueue()
        self.background_queue = queue.PriorityQueue()
        
        # Worker threads
        self.foreground_thread = None
        self.background_thread = None
        
        # Control flags
        self.running = False
        self.paused = False
        
        # Performance metrics
        self.foreground_tasks_completed = 0
        self.background_tasks_completed = 0
    
    def start(self):
        """Start parallel processing threads."""
        if self.running:
            return
        
        self.running = True
        
        # Start foreground thread (user interaction)
        self.foreground_thread = threading.Thread(
            target=self._foreground_worker,
            daemon=True,
            name="Foreground-Cognition"
        )
        self.foreground_thread.start()
        
        # Start background thread (autonomous processing)
        self.background_thread = threading.Thread(
            target=self._background_worker,
            daemon=True,
            name="Background-Cognition"
        )
        self.background_thread.start()
    
    def stop(self):
        """Stop parallel processing threads."""
        self.running = False
        
        if self.foreground_thread:
            self.foreground_thread.join(timeout=2.0)
        
        if self.background_thread:
            self.background_thread.join(timeout=2.0)
    
    def submit_foreground(self, function: Callable, *args, priority: int = 0, **kwargs):
        """
        Submit task to foreground stream (user interaction).
        Higher priority = processed first.
        """
        task = Task(
            stream=ProcessingStream.FOREGROUND,
            function=function,
            args=args,
            kwargs=kwargs,
            priority=priority
        )
        self.foreground_queue.put((-priority, task))  # Negative for priority queue
    
    def submit_background(self, function: Callable, *args, priority: int = 0, **kwargs):
        """
        Submit task to background stream (autonomous processing).
        Lower priority than foreground to avoid blocking user.
        """
        task = Task(
            stream=ProcessingStream.BACKGROUND,
            function=function,
            args=args,
            kwargs=kwargs,
            priority=priority
        )
        self.background_queue.put((-priority, task))
    
    def _foreground_worker(self):
        """Foreground processing loop - user interaction."""
        while self.running:
            try:
                # Block for up to 0.1s waiting for tasks
                priority, task = self.foreground_queue.get(timeout=0.1)
                
                if not self.paused:
                    # Execute task
                    task.function(*task.args, **task.kwargs)
                    self.foreground_tasks_completed += 1
                
                self.foreground_queue.task_done()
            
            except queue.Empty:
                continue
            except Exception:
                pass  # Continue on error
    
    def _background_worker(self):
        """Background processing loop - autonomous tasks."""
        while self.running:
            try:
                # Block for up to 0.5s (less aggressive than foreground)
                priority, task = self.background_queue.get(timeout=0.5)
                
                if not self.paused:
                    # Execute task
                    task.function(*task.args, **task.kwargs)
                    self.background_tasks_completed += 1
                
                self.background_queue.task_done()
            
            except queue.Empty:
                # No tasks - yield CPU
                time.sleep(0.1)
            except Exception:
                pass  # Continue on error
    
    def pause(self):
        """Pause processing (useful for resource-intensive operations)."""
        self.paused = True
    
    def resume(self):
        """Resume processing."""
        self.paused = False
    
    def get_stats(self) -> dict:
        """Get processing statistics."""
        return {
            'running': self.running,
            'paused': self.paused,
            'foreground_tasks': self.foreground_tasks_completed,
            'background_tasks': self.background_tasks_completed,
            'foreground_queue_size': self.foreground_queue.qsize(),
            'background_queue_size': self.background_queue.qsize()
        }


# Global singleton processor
_processor = None


def get_processor() -> ParallelProcessor:
    """Get global parallel processor instance."""
    global _processor
    if _processor is None:
        _processor = ParallelProcessor()
        _processor.start()
    return _processor


def shutdown_processor():
    """Shutdown global processor."""
    global _processor
    if _processor:
        _processor.stop()
        _processor = None
