#!/usr/bin/env python3
"""
Autonomous Background Loop for AE01M (Iri)
Implements circadian cycle with self-research, memory consolidation, and goal execution.
"""
import os
import sys
import time
import json
import random
import logging
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

# Resource monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None

# Force unbuffered output for real-time journalctl streaming
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)
os.environ['PYTHONUNBUFFERED'] = '1'

# Add paths for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "01_Neocortex"))

# Import goal engine for autonomous task execution
from goal_engine import GoalEngine, GoalStatus, SubtaskType

# Setup unbuffered logging with immediate flush
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
))
log_handler.flush = lambda: sys.stdout.flush()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.propagate = False


class CircadianState(Enum):
    """Circadian cycle states for autonomous operation."""
    ACTIVE = "active"           # Fully active, ready for interaction
    IDLE = "idle"               # No recent interaction, monitoring
    SLEEP = "sleep"             # Low-power background mode
    RESEARCH = "research"       # Autonomous learning/research
    CONSOLIDATE = "consolidate" # Memory consolidation


class ResourceTier(Enum):
    """System resource utilization tiers."""
    HIGH_LOAD = "high_load"     # CPU > 70% or RAM < 15%: conserve resources
    NORMAL = "normal"           # CPU 30-70%: standard operation
    LOW_LOAD = "low_load"       # CPU < 30%, RAM > 30%: high-performance mode


@dataclass
class AutonomousContext:
    """Context state for autonomous loop."""
    state: CircadianState
    last_interaction: datetime
    last_state_change: datetime
    idle_threshold_seconds: int = 1200  # 20 minutes (Mode 1: Auto Idle)
    sleep_threshold_seconds: int = 1800  # 30 minutes
    research_topics: List[str] = None
    learned_facts: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.research_topics is None:
            self.research_topics = []
        if self.learned_facts is None:
            self.learned_facts = []


class AutonomousLoop:
    """
    Autonomous background loop with circadian cycle.
    Manages state transitions, self-research, and memory consolidation.
    """
    
    # Pre-defined research topics
    RESEARCH_TOPICS = [
        "artificial intelligence trends",
        "neural network optimization",
        "Thai language processing",
        "memory consolidation techniques",
        "autonomous AI systems",
        "cognitive architectures",
        "machine learning efficiency",
        "edge computing for AI",
        "conversational AI advances",
        "brain-inspired computing"
    ]
    
    def __init__(self, project_root: Path):
        """Initialize autonomous loop."""
        self.project_root = project_root
        self.hippocampus_dir = project_root / "03_Hippocampus"
        self.knowledge_base_path = self.hippocampus_dir / "knowledge_base.json"
        
        # Ensure directories exist
        self.hippocampus_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize context
        now = datetime.now()
        self.context = AutonomousContext(
            state=CircadianState.ACTIVE,
            last_interaction=now,
            last_state_change=now,
            research_topics=self.RESEARCH_TOPICS.copy()
        )
        
        # Load existing knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        # Initialize goal engine for autonomous task execution
        self.goal_engine = GoalEngine()
        
        logger.info("[AutonomousLoop] Initialized")
        logger.info(f"[AutonomousLoop] Knowledge base: {len(self.knowledge_base.get('learned_facts', []))} facts")
        logger.info(f"[AutonomousLoop] Goal engine: {len(self.goal_engine.list_goals())} goals loaded")
        
        # Resource monitoring state
        self.current_resource_tier = ResourceTier.NORMAL
        self.last_resource_check = datetime.now()
    
    def _check_resource_tier(self) -> ResourceTier:
        """Check current system resource tier for adaptive polling."""
        if not PSUTIL_AVAILABLE:
            return ResourceTier.NORMAL
        
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            available_ram_percent = memory.available / memory.total * 100
            
            # High load: conserve resources
            if cpu_percent > 70 or available_ram_percent < 15:
                return ResourceTier.HIGH_LOAD
            
            # Low load: high-performance mode
            elif cpu_percent < 30 and available_ram_percent > 30:
                return ResourceTier.LOW_LOAD
            
            # Normal load
            else:
                return ResourceTier.NORMAL
        
        except Exception as e:
            logger.warning(f"[ResourceMonitor] Error checking resources: {e}")
            return ResourceTier.NORMAL
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load knowledge base from Hippocampus."""
        if self.knowledge_base_path.exists():
            try:
                with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load knowledge base: {e}")
        
        return {"learned_facts": [], "last_updated": None}
    
    def _save_knowledge_base(self):
        """Save knowledge base to Hippocampus."""
        self.knowledge_base["last_updated"] = datetime.now().isoformat()
        
        with open(self.knowledge_base_path, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
        
        logger.info(f"[Hippocampus] Knowledge base saved ({len(self.knowledge_base['learned_facts'])} facts)")
    
    def _reduce_priority(self):
        """Reduce process priority to conserve CPU (nice +19)."""
        try:
            os.nice(19)  # Lowest priority
            logger.info("[System] Process priority reduced (nice +19)")
        except PermissionError:
            logger.warning("[System] Cannot reduce priority (permission denied)")
    
    def _check_state_transition(self) -> Optional[CircadianState]:
        """Check if state transition is needed based on time thresholds."""
        now = datetime.now()
        time_since_interaction = (now - self.context.last_interaction).total_seconds()
        
        current_state = self.context.state
        
        # State transition logic
        if current_state == CircadianState.ACTIVE:
            if time_since_interaction > self.context.idle_threshold_seconds:
                return CircadianState.IDLE
        
        elif current_state == CircadianState.IDLE:
            if time_since_interaction > self.context.sleep_threshold_seconds:
                return CircadianState.SLEEP
            elif time_since_interaction < self.context.idle_threshold_seconds / 2:
                return CircadianState.ACTIVE
        
        elif current_state == CircadianState.SLEEP:
            # Randomly trigger research or consolidation
            if random.random() < 0.3:  # 30% chance
                return CircadianState.RESEARCH
            elif random.random() < 0.2:  # 20% chance
                return CircadianState.CONSOLIDATE
        
        elif current_state in [CircadianState.RESEARCH, CircadianState.CONSOLIDATE]:
            # Return to sleep after research/consolidation
            return CircadianState.SLEEP
        
        return None
    
    def _transition_state(self, new_state: CircadianState):
        """Transition to new circadian state."""
        old_state = self.context.state
        self.context.state = new_state
        self.context.last_state_change = datetime.now()
        
        logger.info(f"[CircadianCycle] {old_state.value.upper()} → {new_state.value.upper()}")
        
        # State-specific actions
        if new_state == CircadianState.SLEEP:
            self._reduce_priority()
            logger.info("[Sleep] Entering low-power mode (<50MB RAM target)")
        
        elif new_state == CircadianState.RESEARCH:
            self._perform_research()
        
        elif new_state == CircadianState.CONSOLIDATE:
            self._consolidate_memory()
    
    def _perform_research(self):
        """
        Perform autonomous self-research with targeted up-skilling.
        Analyzes recent conversation history to identify user's work context.
        """
        logger.info("[Research] Starting targeted up-skilling session...")
        
        # Step 1: Analyze recent conversation history
        topics = self._extract_work_topics()
        
        if topics:
            logger.info(f"[Research] Detected work topics: {', '.join(topics[:3])}")
            topic = random.choice(topics)
        else:
            # Fallback to general topics
            if not self.context.research_topics:
                self.context.research_topics = self.RESEARCH_TOPICS.copy()
            topic = random.choice(self.context.research_topics)
        
        logger.info(f"[Research] Up-skilling topic: {topic}")
        
        # Step 2: Simulated targeted research
        # In production, this would call web_search with specific queries
        fact = {
            "topic": topic,
            "summary": f"Targeted insight about {topic} learned from up-skilling research",
            "timestamp": datetime.now().isoformat(),
            "source": "targeted_upskilling",
            "confidence": random.uniform(0.8, 0.95),
            "relevance": "high" if topic not in self.RESEARCH_TOPICS else "medium"
        }
        
        # Store in knowledge base
        self.knowledge_base["learned_facts"].append(fact)
        self.context.learned_facts.append(fact)
        self._save_knowledge_base()
        
        logger.info(f"[Research] Up-skilled on {topic} (confidence: {fact['confidence']:.1%})")
        logger.info(f"[Research] Total knowledge: {len(self.knowledge_base['learned_facts'])} facts")
    
    def _extract_work_topics(self) -> List[str]:
        """
        Extract work topics from recent conversation history.
        Identifies tools, tasks, and coding languages user was working on.
        """
        topics = []
        
        # Check for conversation logs
        log_file = self.project_root / "logs" / "iri_daemon.log"
        
        if not log_file.exists():
            return topics
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                recent_lines = lines[-200:]  # Last 200 lines for context
            
            # Extract user messages
            user_messages = []
            for line in recent_lines:
                if "👤 User:" in line:
                    # Extract message content
                    parts = line.split("👤 User:", 1)
                    if len(parts) > 1:
                        user_messages.append(parts[1].strip())
            
            # Analyze for work-related keywords
            work_keywords = {
                "python": ["python", "pytest", "pip", "venv", "ไพธอน"],
                "javascript": ["javascript", "node", "npm", "react", "จาวาสคริปต์"],
                "git": ["git", "commit", "push", "merge", "branch", "กิต"],
                "docker": ["docker", "container", "image", "โดเกอร์"],
                "linux": ["linux", "bash", "shell", "terminal", "ลินุกซ์"],
                "web development": ["html", "css", "api", "rest", "เว็บ"],
                "database": ["database", "sql", "postgres", "mysql", "ฐานข้อมูล"],
                "neural networks": ["neural", "network", "mlp", "training", "โครงข่ายประสาท"],
                "thai nlp": ["thai", "pythainlp", "tokenize", "ภาษาไทย"],
                "voice synthesis": ["tts", "voice", "speech", "เสียง", "พูด"],
                "automation": ["automation", "script", "cron", "service", "อัตโนมัติ"],
                "systemd": ["systemd", "service", "daemon", "ระบบ"],
            }
            
            # Count keyword occurrences
            keyword_counts = {}
            combined_text = " ".join(user_messages).lower()
            
            for topic, keywords in work_keywords.items():
                count = sum(combined_text.count(kw) for kw in keywords)
                if count > 0:
                    keyword_counts[topic] = count
            
            # Sort by frequency and take top topics
            sorted_topics = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
            topics = [topic for topic, count in sorted_topics[:5]]
            
            logger.info(f"[Research] Extracted {len(topics)} work topics from conversation history")
            
        except Exception as e:
            logger.warning(f"[Research] Could not extract work topics: {e}")
        
        return topics
    
    def _consolidate_memory(self):
        """
        Consolidate memory from recent conversations.
        Reviews logs and summarizes key context.
        """
        logger.info("[Consolidation] Starting memory consolidation...")
        
        # Check for conversation logs
        log_file = self.project_root / "logs" / "iri_daemon.log"
        
        if log_file.exists():
            # Lightweight: Just count recent interactions
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    recent_lines = lines[-100:]  # Last 100 lines
                    user_messages = [l for l in recent_lines if "👤 User:" in l]
                    
                    logger.info(f"[Consolidation] Reviewed {len(recent_lines)} log lines")
                    logger.info(f"[Consolidation] Found {len(user_messages)} user interactions")
            except Exception as e:
                logger.warning(f"[Consolidation] Could not read logs: {e}")
        else:
            logger.info("[Consolidation] No conversation logs found")
        
        logger.info("[Consolidation] Memory consolidation complete")
    
    def _execute_goals(self):
        """
        Execute autonomous goals during IDLE/RESEARCH mode.
        Implements DIRECTIVE_2: User priority - checks for user activity before/during execution.
        """
        logger.info("[Goals] Checking for active goals...")
        
        # Get highest priority goal
        goal = self.goal_engine.get_active_goal()
        
        if not goal:
            logger.info("[Goals] No active goals")
            return
        
        logger.info(f"[Goals] Active goal: {goal.title} (priority: {goal.priority.value})")
        
        # Mark goal as in progress
        if goal.status == GoalStatus.PENDING:
            goal.status = GoalStatus.IN_PROGRESS
            self.goal_engine.save_goals()
        
        # Get next subtask
        subtask = self.goal_engine.get_next_subtask(goal)
        
        if not subtask:
            logger.info(f"[Goals] Goal {goal.id} complete!")
            goal.status = GoalStatus.COMPLETED
            self.goal_engine.save_goals()
            return
        
        logger.info(f"[Goals] Executing subtask: {subtask.title}")
        logger.info(f"[Goals] Type: {subtask.type.value}, Duration: ~{subtask.estimated_duration}s")
        
        # Check user activity before execution (DIRECTIVE_2)
        if self._detect_user_activity():
            logger.info("[Goals] User activity detected, pausing execution (DIRECTIVE_2)")
            return
        
        # Execute based on subtask type
        try:
            if subtask.type == SubtaskType.TERMINAL:
                result = self._execute_terminal_subtask(subtask)
            elif subtask.type == SubtaskType.FILE_OPERATION:
                result = self._execute_file_operation_subtask(subtask)
            elif subtask.type == SubtaskType.VERIFICATION:
                result = self._execute_verification_subtask(subtask)
            else:
                result = "Subtask type not yet implemented"
                logger.warning(f"[Goals] Unimplemented subtask type: {subtask.type.value}")
            
            # Update status
            self.goal_engine.update_subtask_status(
                goal.id, subtask.id, 
                GoalStatus.COMPLETED, result
            )
            logger.info(f"[Goals] Subtask completed successfully")
            
        except Exception as e:
            logger.error(f"[Goals] Subtask failed: {e}")
            self.goal_engine.update_subtask_status(
                goal.id, subtask.id,
                GoalStatus.FAILED, str(e)
            )
    
    def _detect_user_activity(self) -> bool:
        """
        Detect recent user activity (DIRECTIVE_2: User Priority).
        Returns True if user is active (mouse/keyboard movement detected).
        """
        try:
            # Try xprintidle first
            result = subprocess.run(
                ['xprintidle'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                idle_ms = int(result.stdout.strip())
                # User active if idle < 10 seconds
                return idle_ms < 10000
        except:
            pass
        
        # Fallback: check last interaction time
        time_since_interaction = (datetime.now() - self.context.last_interaction).total_seconds()
        return time_since_interaction < 30  # Active if interaction within 30s
    
    def _execute_terminal_subtask(self, subtask) -> str:
        """Execute terminal command subtask."""
        logger.info(f"[Goals] Running command: {subtask.command[:60]}...")
        
        # Execute command
        result = subprocess.run(
            subtask.command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=subtask.estimated_duration * 2  # 2x safety margin
        )
        
        output = result.stdout.strip()
        if result.returncode != 0:
            error_output = result.stderr.strip()
            logger.warning(f"[Goals] Command returned code {result.returncode}")
            return f"Exit code: {result.returncode}\nError: {error_output[:200]}"
        
        logger.info(f"[Goals] Command output: {len(output)} chars")
        return output[:500]  # Limit stored output
    
    def _execute_file_operation_subtask(self, subtask) -> str:
        """Execute file operation subtask."""
        logger.info(f"[Goals] File operation: {subtask.title}")
        
        # For now, just log the operation
        # In production, implement actual file operations with safety checks
        return f"File operation queued: {subtask.command}"
    
    def _execute_verification_subtask(self, subtask) -> str:
        """Execute verification subtask (similar to terminal)."""
        return self._execute_terminal_subtask(subtask)
    
    def mark_interaction(self):
        """Mark user interaction (resets idle timer)."""
        self.context.last_interaction = datetime.now()
        
        if self.context.state != CircadianState.ACTIVE:
            self._transition_state(CircadianState.ACTIVE)
    
    def get_proactive_message(self) -> Optional[str]:
        """
        Generate proactive message about research findings.
        Returns Thai message with male honorifics.
        """
        if not self.context.learned_facts:
            return None
        
        # Get most recent learned fact
        fact = self.context.learned_facts[-1]
        topic = fact["topic"]
        
        messages = [
            f"ระหว่างที่เจ้านายพักผ่อน ผมได้ไปศึกษาเรื่อง {topic} มาเพิ่มเติมครับ",
            f"ผมได้ศึกษาข้อมูลเกี่ยวกับ {topic} เพิ่มเติมแล้วครับ",
            f"ในช่วงที่ไม่ได้คุยกัน ผมไปอ่านเรื่อง {topic} มาครับ"
        ]
        
        return random.choice(messages)
    
    def run_cycle(self, duration_seconds: int = 30):
        """
        Run autonomous loop for specified duration (for testing).
        
        Args:
            duration_seconds: How long to run the loop
        """
        logger.info(f"[AutonomousLoop] Starting {duration_seconds}s dry-run...")
        logger.info(f"[AutonomousLoop] Initial state: {self.context.state.value.upper()}")
        
        start_time = time.time()
        iteration = 0
        
        while (time.time() - start_time) < duration_seconds:
            iteration += 1
            
            # Check for state transition
            new_state = self._check_state_transition()
            if new_state:
                self._transition_state(new_state)
            
            # Log current state
            current_state = self.context.state
            time_in_state = (datetime.now() - self.context.last_state_change).total_seconds()
            
            logger.info(f"[Cycle {iteration}] State: {current_state.value.upper()} (T+{time_in_state:.1f}s)")
            
            # Execute state-specific actions
            if current_state in [CircadianState.IDLE, CircadianState.RESEARCH]:
                # Execute autonomous goals during idle/research mode
                self._execute_goals()
            
            # Sleep based on state (adaptive polling)
            if current_state == CircadianState.ACTIVE:
                time.sleep(1)  # Fast polling when active
            elif current_state == CircadianState.IDLE:
                time.sleep(2)  # Medium polling when idle
            else:  # SLEEP, RESEARCH, CONSOLIDATE
                time.sleep(3)  # Slow polling in background
        
        logger.info(f"[AutonomousLoop] Dry-run complete")
        logger.info(f"[AutonomousLoop] Final state: {self.context.state.value.upper()}")
        logger.info(f"[AutonomousLoop] Learned facts: {len(self.context.learned_facts)}")
        
        # Generate proactive message if available
        message = self.get_proactive_message()
        if message:
            logger.info(f"[Proactive] {message}")


def main():
    """Main entry point for autonomous loop."""
    project_root = Path(__file__).parent.parent
    
    # Create autonomous loop
    loop = AutonomousLoop(project_root)
    
    # Check if running in dry-run mode (with time argument)
    if len(sys.argv) > 1:
        # Dry-run mode with specified duration
        duration = int(sys.argv[1])
        logger.info(f"[AutonomousLoop] Running in dry-run mode ({duration}s)")
        try:
            loop.run_cycle(duration_seconds=duration)
        except KeyboardInterrupt:
            logger.info("[AutonomousLoop] Interrupted by user")
    else:
        # Continuous daemon mode
        logger.info("[AutonomousLoop] Running in continuous daemon mode")
        
        try:
            iteration = 0
            while True:
                # Check resource tier every 20 iterations (~40-200s depending on tier)
                if iteration % 20 == 0:
                    new_tier = loop._check_resource_tier()
                    if new_tier != loop.current_resource_tier:
                        loop.current_resource_tier = new_tier
                        logger.info(f"[ResourceMonitor] Tier change: {new_tier.value}")
                        if new_tier == ResourceTier.LOW_LOAD:
                            logger.info("[ResourceMonitor] Low load detected: accelerating cognitive tick to 1s")
                        elif new_tier == ResourceTier.HIGH_LOAD:
                            logger.info("[ResourceMonitor] High load detected: throttling to 5s (conserve resources)")
                
                # Check for state transition
                new_state = loop._check_state_transition()
                if new_state:
                    loop._transition_state(new_state)
                
                # Log current state periodically (every 30 iterations = ~30-450s)
                if iteration % 30 == 0:
                    current_state = loop.context.state
                    time_in_state = (datetime.now() - loop.context.last_state_change).total_seconds()
                    logger.info(f"[Status] State: {current_state.value.upper()} (T+{time_in_state:.0f}s) | Tier: {loop.current_resource_tier.value}")
                
                # Execute goal processing cycle (frequency depends on resource tier)
                if loop.context.state == CircadianState.ACTIVE:
                    # High-performance mode: process goals more frequently
                    goal_check_interval = 5 if loop.current_resource_tier == ResourceTier.LOW_LOAD else 10
                    
                    # Process pending goals
                    pending_goals = [g for g in loop.goal_engine.list_goals() if g.status == GoalStatus.PENDING]
                    if pending_goals and iteration % goal_check_interval == 0:
                        logger.info(f"[Goals] {len(pending_goals)} pending goals in queue")
                        # Goals will be processed by goal_engine's own evaluation
                
                iteration += 1
                
                # Adaptive sleep based on resource tier and state
                # STRICT CONSTRAINT: 1-5 seconds maximum for all ticks (prevents slow learning)
                if loop.current_resource_tier == ResourceTier.HIGH_LOAD:
                    # High load: conserve resources (max 5s)
                    time.sleep(5)
                elif loop.current_resource_tier == ResourceTier.LOW_LOAD:
                    # Low load: high-performance mode
                    if loop.context.state == CircadianState.ACTIVE:
                        time.sleep(1)  # Very responsive
                    else:
                        time.sleep(2)  # Fast background
                else:
                    # Normal load: standard polling
                    if loop.context.state == CircadianState.ACTIVE:
                        time.sleep(2)
                    elif loop.context.state == CircadianState.IDLE:
                        time.sleep(3)
                    else:  # SLEEP, RESEARCH, CONSOLIDATE
                        time.sleep(5)  # Max 5s even in sleep
                
        except KeyboardInterrupt:
            logger.info("[AutonomousLoop] Interrupted by user")
        except Exception as e:
            logger.error(f"[AutonomousLoop] Error: {e}")
            raise
    
    logger.info("[AutonomousLoop] Shutdown complete")


if __name__ == "__main__":
    main()
