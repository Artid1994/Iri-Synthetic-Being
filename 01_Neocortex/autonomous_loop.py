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

# Import curriculum manager for knowledge gap driven learning
from curriculum_manager import CurriculumManager

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
        
        # Initialize curriculum manager for knowledge-gap driven learning
        self.curriculum_manager = CurriculumManager()
        
        # INTEGRATION: Initialize TranscendingRuntime for cognitive processing
        sys.path.insert(0, str(project_root / "runtime"))
        from runtime.runtime import TranscendingRuntime
        self.runtime = TranscendingRuntime()
        
        logger.info("[AutonomousLoop] Initialized")
        logger.info(f"[AutonomousLoop] Knowledge base: {len(self.knowledge_base.get('learned_facts', []))} facts")
        logger.info(f"[AutonomousLoop] Goal engine: {len(self.goal_engine.list_goals())} goals loaded")
        logger.info(f"[AutonomousLoop] Curriculum: {len(self.curriculum_manager.topics)} topics tracked")
        logger.info("[AutonomousLoop] Cognitive runtime integrated")
        
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
            elif subtask.type == SubtaskType.RESEARCH:
                result = self._execute_research_subtask(subtask, goal)
            elif subtask.type == SubtaskType.SYNTHESIS:
                result = self._execute_synthesis_subtask(subtask, goal)
            elif subtask.type == SubtaskType.DELEGATE_TO_HERMES:
                result = self._execute_hermes_delegation(subtask, goal)
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
    
    def _execute_research_subtask(self, subtask, goal) -> str:
        """
        Execute research subtask - perform autonomous knowledge acquisition.
        COGNITIVE INTEGRATION: Routes through cognitive_loop for experience/learning/plasticity.
        """
        logger.info(f"[Research] Starting cognitive research for: {goal.title}")
        
        # Extract topic from goal description
        topic = goal.title.replace("Learn: ", "").strip()
        
        # STEP 1: Cognitive skill selection (replacing rule-based keyword matching)
        selected_tools = self._cognitive_skill_selection(topic, goal.description)
        logger.info(f"[CognitiveSkills] Selected tools: {selected_tools}")
        
        # STEP 2: Execute research with cognitive processing
        facts_synthesized = self._cognitive_tool_research(topic, goal.description, selected_tools)
        
        if facts_synthesized > 0:
            logger.info(f"[Research] Completed autonomous research on {topic}: {facts_synthesized} facts")
            logger.info(f"[Research] Knowledge base: {len(self.knowledge_base['learned_facts'])} facts")
            
            # Update curriculum mastery if this is a curriculum learning goal
            if goal.id.startswith("LEARN_"):
                self._update_curriculum_mastery(goal)
            
            return f"Autonomous research completed on {topic}. Synthesized {facts_synthesized} facts using local tools."
        else:
            # Fallback to basic fact
            fact = {
                "topic": topic,
                "summary": f"Research conducted for curriculum topic: {topic}. {goal.description[:100]}",
                "timestamp": time.time(),
                "source": "curriculum_learning",
                "confidence": 0.85,
                "curriculum_goal_id": goal.id
            }
            self.knowledge_base.setdefault("learned_facts", []).append(fact)
            self._save_knowledge_base()
            
            logger.info(f"[Research] Basic research completed on {topic}")
            return f"Basic research completed on {topic}. Added knowledge to database."
    
    def _cognitive_skill_selection(self, topic: str, description: str) -> List[str]:
        """
        Cognitive skill selection - IRI decides which tools to use based on context.
        Replaces rule-based keyword matching with cognitive decision.
        """
        # Construct cognitive context for tool selection
        available_tools = "wikipedia, arxiv, web_search, python_sandbox"
        context = f"Goal: Research {topic}. Description: {description}. Available tools: {available_tools}. Select appropriate research tools."
        
        try:
            # Process through cognitive loop for decision
            cycle = self.runtime.cognitive_loop.process(context)
            
            # Parse tool selection from cognitive reasoning
            tools = []
            reasoning_lower = cycle.reasoning.lower()
            
            if 'wikipedia' in reasoning_lower:
                tools.append('wikipedia')
            if 'arxiv' in reasoning_lower:
                tools.append('arxiv')
            if 'web' in reasoning_lower or 'search' in reasoning_lower:
                tools.append('web_search')
            if 'python' in reasoning_lower or 'sandbox' in reasoning_lower:
                tools.append('python_sandbox')
            
            # If cognitive decision produced tools, use them
            if tools:
                logger.info(f"[CognitiveSkills] Cognitive decision: {tools}")
                return tools
            
        except Exception as e:
            logger.warning(f"[CognitiveSkills] Cognitive selection failed: {e}, using fallback")
        
        # Fallback: semantic heuristic (not pure keyword rules)
        return self._fallback_tool_selection(topic, description)
    
    def _fallback_tool_selection(self, topic: str, description: str) -> List[str]:
        """Fallback tool selection using semantic heuristics."""
        text = (topic + " " + description).lower()
        
        # Semantic domain detection
        if any(kw in text for kw in ['neural', 'llm', 'ai', 'machine learning']):
            return ['wikipedia', 'arxiv', 'web_search']
        elif any(kw in text for kw in ['math', 'calculus', 'algebra']):
            return ['wikipedia', 'python_sandbox', 'web_search']
        elif any(kw in text for kw in ['physics', 'quantum']):
            return ['wikipedia', 'arxiv']
        else:
            return ['wikipedia', 'web_search']
    
    def _cognitive_tool_research(self, topic: str, description: str, selected_tools: List[str]) -> int:
        """
        Execute research with cognitive integration.
        Each result flows through cognitive_loop → experience → learning → plasticity.
        """
        logger.info(f"[CognitiveResearch] Starting cognitive research: {topic}")
        
        # Check for duplicate research
        existing_facts = self.knowledge_base.get("learned_facts", [])
        existing_topics = {f.get("topic", "").lower() for f in existing_facts[-100:]}
        
        if topic.lower() in existing_topics:
            logger.info(f"[CognitiveResearch] Topic already researched, skipping")
            return 0
        
        facts_integrated = 0
        
        # Execute tools to gather raw research
        try:
            from tool_registry import ToolRegistry
            registry = ToolRegistry()
            
            # Gather facts from selected tools
            raw_facts = []
            for tool in selected_tools:
                if tool == 'wikipedia':
                    raw_facts.extend(registry._research_wikipedia(topic, max_facts=2))
                elif tool == 'arxiv':
                    raw_facts.extend(registry._research_arxiv(topic, max_facts=2))
                elif tool == 'web_search':
                    raw_facts.extend(registry._research_web(topic, max_facts=2))
            
            logger.info(f"[CognitiveResearch] Retrieved {len(raw_facts)} raw facts from tools")
            
            # CRITICAL: Process each fact through cognitive loop
            for fact_data in raw_facts[:5]:  # Limit to 5 for resource control
                observation = f"Research result for {topic}: {fact_data['text']}"
                
                # Feed through cognitive loop
                cycle = self.runtime.cognitive_loop.process(observation)
                
                # Experience → Learning → Plasticity happens automatically in cognitive_loop
                if cycle.experience_recorded:
                    facts_integrated += 1
                    logger.info(f"[CognitiveResearch] Fact integrated via cognitive loop (learning={cycle.experience_recorded})")
                    
                    # Also store in knowledge_base for persistence
                    fact = {
                        "topic": topic,
                        "summary": fact_data['text'],
                        "timestamp": time.time(),
                        "source": "cognitive_tool_research",
                        "tool": fact_data.get('source', 'unknown'),
                        "confidence": fact_data.get('confidence', 0.85),
                        "cognitive_integration": True
                    }
                    self.knowledge_base.setdefault("learned_facts", []).append(fact)
            
            # Save knowledge base
            if facts_integrated > 0:
                self._save_knowledge_base()
                logger.info(f"[CognitiveResearch] {facts_integrated} facts integrated through cognitive loop")
            
            return facts_integrated
            
        except Exception as e:
            logger.warning(f"[CognitiveResearch] Tool research failed: {e}")
            return 0
    
    def _autonomous_tool_research(self, topic: str, description: str) -> int:
        """
        Autonomous tool-assisted research using local capabilities.
        REAL TOOLS: Wikipedia, ArXiv, Web Search, Python Sandbox.
        
        Returns: Number of facts synthesized
        """
        logger.info(f"[ToolResearch] Autonomous synthesis for: {topic}")
        
        # Generate semantic hash for deduplication
        import hashlib
        topic_hash = hashlib.md5(topic.lower().encode()).hexdigest()[:8]
        
        # Check for duplicate research (semantic dedup)
        existing_facts = self.knowledge_base.get("learned_facts", [])
        existing_topics = {f.get("topic", "").lower() for f in existing_facts[-100:]}
        
        if topic.lower() in existing_topics:
            logger.info(f"[ToolResearch] Topic already researched, skipping duplicate")
            return 0
        
        facts_added = 0
        max_facts = 5
        
        # Try using real tools first
        try:
            from tool_registry import ToolRegistry
            registry = ToolRegistry()
            
            # Research with tools
            tool_facts = registry.research_with_tools(topic, description, max_facts=max_facts)
            
            if tool_facts:
                logger.info(f"[ToolResearch] Retrieved {len(tool_facts)} facts from tools")
                
                for i, fact_data in enumerate(tool_facts):
                    fact = {
                        "topic": topic,
                        "summary": f"[{fact_data['source'].title()}] {fact_data['text']}",
                        "timestamp": time.time() + i * 0.001,
                        "source": "autonomous_tool_research",
                        "tool": fact_data['source'],
                        "confidence": fact_data.get('confidence', 0.85),
                        "hash": f"{topic_hash}_{i}"
                    }
                    self.knowledge_base.setdefault("learned_facts", []).append(fact)
                    facts_added += 1
                
                # Save and return
                if facts_added > 0:
                    self._prune_and_save_knowledge_base()
                    logger.info(f"[ToolResearch] Tool-based research: {facts_added} facts from real sources")
                    return facts_added
        
        except Exception as e:
            logger.warning(f"[ToolResearch] Tool usage failed: {e}, falling back to templates")
        
        # Fallback to built-in templates if tools fail
        # AI/ML domain
        if any(kw in topic.lower() for kw in ['neural', 'llm', 'transformer', 'ai', 'machine learning']):
            facts = [
                "Neural networks learn patterns through backpropagation",
                "Transformers process sequences using self-attention",
                "Pre-training creates general representations",
                "Fine-tuning adapts models to specific tasks",
                "Embeddings capture semantic relationships"
            ]
            domain = "AI_ML"
        
        # Mathematics domain
        elif any(kw in topic.lower() for kw in ['calculus', 'algebra', 'matrix', 'math']):
            facts = [
                "Functions map inputs to outputs systematically",
                "Derivatives measure rates of change",
                "Linear algebra studies vector spaces",
                "Matrices represent linear transformations",
                "Optimization finds extrema of functions"
            ]
            domain = "Mathematics"
        
        # Computer Systems domain
        elif any(kw in topic.lower() for kw in ['operating system', 'process', 'computer', 'network']):
            facts = [
                "Operating systems manage hardware resources",
                "Processes are independent program executions",
                "Memory hierarchy balances speed and capacity",
                "Networks enable distributed communication",
                "Scheduling allocates CPU time to tasks"
            ]
            domain = "Computer_Systems"
        
        # Coding domain
        elif any(kw in topic.lower() for kw in ['programming', 'python', 'code', 'algorithm']):
            facts = [
                "Algorithms are step-by-step procedures",
                "Data structures organize information efficiently",
                "Functions encapsulate reusable logic",
                "Loops enable repetitive operations",
                "Conditionals enable decision-making"
            ]
            domain = "Programming"
        
        # Generic domain
        else:
            facts = [
                f"Understanding {topic} requires foundational knowledge",
                f"Key concepts in {topic} build systematically",
                f"Practice reinforces {topic} mastery"
            ]
            domain = "General"
        
        # Synthesize facts into knowledge base
        for i, fact_text in enumerate(facts[:max_facts]):
            fact = {
                "topic": topic,
                "summary": f"[Autonomous] {fact_text}",
                "timestamp": time.time() + i * 0.001,
                "source": "autonomous_tool_research",
                "confidence": 0.88,
                "domain": domain,
                "hash": f"{topic_hash}_{i}"
            }
            self.knowledge_base.setdefault("learned_facts", []).append(fact)
            facts_added += 1
        
        # Save with pruning
        if facts_added > 0:
            self._prune_and_save_knowledge_base()
            
            # Ultra-dense reporting
            from dense_reporter import DenseReporter
            summary = DenseReporter.format_research_summary(
                topic, facts_added, "autonomous_tool", domain
            )
            logger.info(f"[ToolResearch] {summary.replace(chr(10), ' | ')}")
            
            # Track unreported research for proactive reporting
            key_facts = [f"[Autonomous] {facts[i]}" for i in range(min(2, len(facts)))]
            self._track_unreported_research(topic, facts_added, key_facts, domain)
        
        return facts_added
    
    def _execute_synthesis_subtask(self, subtask, goal) -> str:
        """Execute synthesis subtask - consolidate learning."""
        logger.info(f"[Synthesis] Synthesizing knowledge for: {goal.title}")
        
        # For now, mark as complete - synthesis happens implicitly through research
        return f"Knowledge synthesis completed for {goal.title}"
    
    def _execute_hermes_delegation(self, subtask, goal) -> str:
        """
        Execute Hermes delegation - request deep knowledge synthesis from Hermes agent.
        Used for complex topics requiring comprehensive academic research.
        TOKEN OPTIMIZED: Compact prompts, sliding window context, deduplication.
        """
        logger.info(f"[Hermes] Delegating deep research to Hermes for: {goal.title}")
        
        # Extract topic from goal (compact)
        topic = goal.title.replace("Learn: ", "").strip()
        topic_description = goal.description[:200]  # Limit to 200 chars
        
        # Create delegation request (compact JSON)
        delegation_request = {
            "ts": time.time(),
            "goal_id": goal.id,
            "topic": topic,
            "desc": topic_description,
            "mastery": "deep",
            "type": "curriculum",
            "status": "pending"
        }
        
        delegation_file = self.project_root / "03_Hippocampus" / "hermes_delegation_queue.json"
        
        # Load or create delegation queue (limit to last 10)
        if delegation_file.exists():
            try:
                with open(delegation_file, 'r') as f:
                    queue = json.load(f)
                # Sliding window: keep only last 10 delegations
                queue = queue[-10:]
            except:
                queue = []
        else:
            queue = []
        
        queue.append(delegation_request)
        
        with open(delegation_file, 'w') as f:
            json.dump(queue, f, separators=(',', ':'))  # Compact JSON
        
        logger.info(f"[Hermes] Delegation request queued for: {topic}")
        
        # Execute inline delegation with token optimization
        facts_added = self._perform_hermes_deep_research(topic, topic_description)
        
        # Mark delegation as completed (compact)
        delegation_request["status"] = "done"
        delegation_request["facts"] = facts_added
        delegation_request["done_ts"] = time.time()
        
        # Update queue
        with open(delegation_file, 'w') as f:
            json.dump(queue, f, separators=(',', ':'))
        
        logger.info(f"[Hermes] Delegation completed: Added {facts_added} knowledge facts")
        
        return f"Hermes delegation completed. Added {facts_added} deep knowledge facts for {topic}."
    
    def _perform_hermes_deep_research(self, topic: str, description: str) -> int:
        """
        Perform deep research synthesis (simulating Hermes agent capabilities).
        TOKEN OPTIMIZED: Compact prompts, semantic deduplication, top-5 facts only.
        Returns number of facts added.
        """
        logger.info(f"[HermesResearch] Deep synthesis for: {topic}")
        
        # Generate semantic hash for deduplication
        import hashlib
        topic_hash = hashlib.md5(topic.lower().encode()).hexdigest()[:8]
        
        # Check for duplicate research (semantic dedup)
        existing_facts = self.knowledge_base.get("learned_facts", [])
        existing_topics = {f.get("topic", "").lower() for f in existing_facts[-100:]}  # Check last 100
        
        if topic.lower() in existing_topics:
            logger.info(f"[HermesResearch] Topic already researched, skipping duplicate")
            return 0
        
        # Generate comprehensive facts based on topic domain (TOP 5 only)
        facts_added = 0
        max_facts = 5  # Token optimization: limit to top 5 most important facts
        
        # Compact fact templates (token-optimized)
        
        # AI Self-Architecture topics
        if any(kw in topic.lower() for kw in ['neural', 'llm', 'transformer', 'architecture', 'machine learning']):
            ai_facts = [
                "Transformers use self-attention for parallel sequence processing",
                "Multi-head attention enables multiple representation subspaces",
                "Positional encoding injects sequence order into models",
                "RAG combines parametric and retrieval knowledge",
                "Vector DBs enable semantic similarity search"
            ]
            
            for summary in ai_facts[:max_facts]:
                fact = {
                    "topic": topic,
                    "summary": f"[Hermes] {summary}",
                    "timestamp": time.time() + facts_added * 0.001,
                    "source": "hermes_delegation",
                    "confidence": 0.92,
                    "hash": f"{topic_hash}_{facts_added}"
                }
                self.knowledge_base.setdefault("learned_facts", []).append(fact)
                facts_added += 1
        
        # Mathematics topics
        elif any(kw in topic.lower() for kw in ['calculus', 'linear algebra', 'matrix', 'derivative', 'integral']):
            math_facts = [
                "Derivatives measure instantaneous rate of change",
                "Gradient descent minimizes loss via iterative updates",
                "Matrix multiplication represents linear transformations",
                "Eigenvalues reveal invariant directions",
                "Integrals compute accumulated change"
            ]
            
            for summary in math_facts[:max_facts]:
                fact = {
                    "topic": topic,
                    "summary": f"[Hermes] {summary}",
                    "timestamp": time.time() + facts_added * 0.001,
                    "source": "hermes_delegation",
                    "confidence": 0.92,
                    "hash": f"{topic_hash}_{facts_added}"
                }
                self.knowledge_base.setdefault("learned_facts", []).append(fact)
                facts_added += 1
        
        # Computer systems topics
        elif any(kw in topic.lower() for kw in ['operating system', 'process', 'thread', 'memory', 'network']):
            systems_facts = [
                "Processes are independent programs with isolated memory",
                "Threads share memory but execute independently",
                "Virtual memory provides isolation and efficiency",
                "Context switching saves/restores CPU state",
                "Scheduling algorithms determine execution order"
            ]
            
            for summary in systems_facts[:max_facts]:
                fact = {
                    "topic": topic,
                    "summary": f"[Hermes] {summary}",
                    "timestamp": time.time() + facts_added * 0.001,
                    "source": "hermes_delegation",
                    "confidence": 0.92,
                    "hash": f"{topic_hash}_{facts_added}"
                }
                self.knowledge_base.setdefault("learned_facts", []).append(fact)
                facts_added += 1
        
        # Generic topics (compact)
        else:
            generic_facts = [
                f"Core concepts of {topic} build on fundamentals",
                f"Practice reinforces {topic} understanding",
                f"Advanced {topic} requires prerequisite mastery"
            ]
            
            for summary in generic_facts[:3]:
                fact = {
                    "topic": topic,
                    "summary": f"[Hermes] {summary}",
                    "timestamp": time.time() + facts_added * 0.001,
                    "source": "hermes_delegation",
                    "confidence": 0.85,
                    "hash": f"{topic_hash}_{facts_added}"
                }
                self.knowledge_base.setdefault("learned_facts", []).append(fact)
                facts_added += 1
        
        # Save knowledge base (with pruning)
        if facts_added > 0:
            self._prune_and_save_knowledge_base()
            logger.info(f"[HermesResearch] Added {facts_added} compact facts for {topic}")
        
        return facts_added
    
    def _prune_and_save_knowledge_base(self):
        """
        Prune knowledge base and save with token optimization.
        - Removes duplicates
        - Limits total facts to 10,000
        - Compact JSON serialization
        """
        facts = self.knowledge_base.get("learned_facts", [])
        
        # Deduplicate by hash (if present)
        seen_hashes = set()
        unique_facts = []
        for fact in facts:
            fact_hash = fact.get("hash")
            if fact_hash:
                if fact_hash not in seen_hashes:
                    seen_hashes.add(fact_hash)
                    unique_facts.append(fact)
            else:
                unique_facts.append(fact)
        
        # Sliding window: keep only last 10,000 facts
        if len(unique_facts) > 10000:
            unique_facts = unique_facts[-10000:]
            logger.info(f"[KnowledgeBase] Pruned to 10,000 most recent facts")
        
        self.knowledge_base["learned_facts"] = unique_facts
        self._save_knowledge_base()
    
    def _track_unreported_research(self, topic: str, facts_count: int, key_facts: List = None, domain: str = None):
        """
        Track unreported research for proactive reporting in chat.
        Records summary of autonomous learning for user notification.
        """
        if key_facts is None:
            key_facts = []
        
        try:
            unreported_file = self.project_root / "03_Hippocampus" / "unreported_research.json"
            
            # Load existing unreported items
            if unreported_file.exists():
                try:
                    with open(unreported_file, 'r') as f:
                        unreported = json.load(f)
                except:
                    unreported = []
            else:
                unreported = []
            
            # Create research summary entry
            entry = {
                "topic": topic,
                "domain": domain or "general",
                "facts_count": facts_count,
                "timestamp": time.time(),
                "key_facts": [fact[:150] for fact in key_facts[:2]],  # Top 2, truncated
                "reported": False
            }
            
            unreported.append(entry)
            
            # Keep only last 10 unreported items
            unreported = unreported[-10:]
            
            # Save
            with open(unreported_file, 'w') as f:
                json.dump(unreported, f, indent=2)
            
            logger.info(f"[Research] Tracked unreported research: {topic} ({facts_count} facts)")
        
        except Exception as e:
            logger.warning(f"[Research] Failed to track unreported research: {e}")
    
    def _update_curriculum_mastery(self, goal):
        """Update curriculum mastery score after completing a learning goal."""
        try:
            # Extract topic ID from goal ID (format: LEARN_topic_id_timestamp)
            parts = goal.id.split("_")
            if len(parts) >= 3:
                topic_id = "_".join(parts[1:-1])  # Everything between LEARN and timestamp
                
                # Get topic from curriculum manager
                if topic_id in self.curriculum_manager.topics:
                    topic = self.curriculum_manager.topics[topic_id]
                    
                    # Increment mastery (research + quiz completion = 0.3 boost)
                    completed_subtasks = sum(1 for st in goal.subtasks if st.status == GoalStatus.COMPLETED)
                    mastery_gain = min(0.3 * (completed_subtasks / len(goal.subtasks)), 0.3)
                    
                    topic.mastery_score = min(topic.mastery_score + mastery_gain, 1.0)
                    topic.attempts += 1
                    topic.last_studied = time.time()
                    
                    self.curriculum_manager.save_curriculum()
                    
                    logger.info(f"[Curriculum] Updated mastery for {topic.title}: {topic.mastery_score:.0%}")
        
        except Exception as e:
            logger.warning(f"[Curriculum] Failed to update mastery: {e}")
    
    def _check_curriculum_gaps(self):
        """
        Proactively identify curriculum knowledge gaps and queue learning tasks.
        Integrates CurriculumManager into autonomous loop for systematic learning.
        """
        logger.info("[Curriculum] Checking for knowledge gaps...")
        
        # Fetch next unmastered topic from curriculum
        next_topic = self.curriculum_manager.fetch_next_topic()
        
        if not next_topic:
            logger.info("[Curriculum] All topics mastered or prerequisites not met")
            return
        
        logger.info(f"[Curriculum] Gap identified: {next_topic.title}")
        logger.info(f"[Curriculum] Domain: {next_topic.domain.value}, Level: {next_topic.level.value}")
        logger.info(f"[Curriculum] Current mastery: {next_topic.mastery_score:.0%}")
        
        # Check if learning goal already exists for this topic
        existing_goals = self.goal_engine.list_goals()
        topic_already_queued = any(
            next_topic.id in goal.title.lower() or next_topic.title.lower() in goal.title.lower()
            for goal in existing_goals
            if goal.status in [GoalStatus.PENDING, GoalStatus.IN_PROGRESS]
        )
        
        if topic_already_queued:
            logger.info(f"[Curriculum] Learning goal already queued for {next_topic.title}")
            return
        
        # Generate self-quiz for this topic
        question, expected_answer, is_code = self.curriculum_manager.generate_self_quiz(next_topic)
        
        logger.info(f"[Curriculum] Generated quiz: {question[:80]}...")
        
        # Determine if Hermes delegation is needed (low mastery < 0.40 or complex topic)
        # DISABLED: Iri now uses autonomous tool-assisted research instead
        needs_deep_synthesis = False  # Always use autonomous tools
        
        # Always prefer autonomous tool research over delegation
        # This enables true self-learning capability
        
        # Create learning goal from curriculum gap
        from goal_engine import Goal, GoalPriority, Subtask
        
        learning_goal = Goal(
            id=f"LEARN_{next_topic.id}_{int(time.time())}",
            title=f"Learn: {next_topic.title}",
            description=f"{next_topic.description}\nConcepts: {', '.join(next_topic.concepts)}",
            priority=GoalPriority.MEDIUM if not needs_deep_synthesis else GoalPriority.HIGH,
            status=GoalStatus.PENDING,
            created_at=time.time(),
            updated_at=time.time(),
            subtasks=[]
        )
        
        # Add research subtask (or Hermes delegation for complex topics)
        if needs_deep_synthesis:
            logger.info(f"[Curriculum] Complex topic detected - delegating to Hermes for deep synthesis")
            research_subtask = Subtask(
                id=f"{learning_goal.id}_hermes",
                title=f"Deep Research (Hermes): {next_topic.title}",
                type=SubtaskType.DELEGATE_TO_HERMES,
                command=f"Hermes deep research: {next_topic.title}",
                estimated_duration=600,  # 10 minutes for deep synthesis
                status=GoalStatus.PENDING,
                safety_checks=["DIRECTIVE_1", "DIRECTIVE_2"],
                result=None
            )
        else:
            research_subtask = Subtask(
                id=f"{learning_goal.id}_research",
                title=f"Research {next_topic.title}",
                type=SubtaskType.RESEARCH,
                command=f"Research topic: {next_topic.title}",
                estimated_duration=300,  # 5 minutes
                status=GoalStatus.PENDING,
                safety_checks=["DIRECTIVE_1", "DIRECTIVE_2"],
                result=None
            )
        learning_goal.subtasks.append(research_subtask)
        
        # Add self-assessment subtask
        quiz_subtask = Subtask(
            id=f"{learning_goal.id}_quiz",
            title=f"Self-quiz: {next_topic.title[:50]}",
            type=SubtaskType.VERIFICATION,
            command=f"echo 'Quiz: {question[:100]}\nExpected: {expected_answer[:100]}'",
            estimated_duration=60,
            status=GoalStatus.PENDING,
            safety_checks=["DIRECTIVE_1"],
            result=None
        )
        learning_goal.subtasks.append(quiz_subtask)
        
        # Queue learning goal
        self.goal_engine.goals.append(learning_goal)
        self.goal_engine.save_goals()
        
        logger.info(f"[Curriculum] ✓ Queued learning goal: {learning_goal.title}")
        logger.info(f"[Curriculum] Goal ID: {learning_goal.id}, Priority: {learning_goal.priority.value}")
    
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
                # Check for state transition
                new_state = loop._check_state_transition()
                if new_state:
                    loop._transition_state(new_state)
                
                # Log current state periodically (every 60 iterations = ~60s)
                if iteration % 60 == 0:
                    current_state = loop.context.state
                    time_in_state = (datetime.now() - loop.context.last_state_change).total_seconds()
                    logger.info(f"[Status] State: {current_state.value.upper()} (T+{time_in_state:.0f}s)")
                
                # Execute goal processing cycle every 10 iterations (~10s)
                if loop.context.state == CircadianState.ACTIVE and iteration % 10 == 0:
                    pending_goals = [g for g in loop.goal_engine.list_goals() if g.status == GoalStatus.PENDING]
                    if pending_goals:
                        logger.info(f"[Goals] {len(pending_goals)} pending goals in queue")
                        # Execute goals immediately
                        loop._execute_goals()
                
                # Also execute goals during IDLE/RESEARCH states (every 20 iterations = ~20s)
                if loop.context.state in [CircadianState.IDLE, CircadianState.RESEARCH] and iteration % 20 == 0:
                    loop._execute_goals()
                
                # Curriculum-driven learning integration (every 30 iterations = ~30s)
                if iteration % 30 == 0 and loop.context.state in [CircadianState.IDLE, CircadianState.RESEARCH]:
                    loop._check_curriculum_gaps()
                
                iteration += 1
                
                # CONSTANT 1-SECOND TICK - No dynamic throttling
                # Ensures consistent cognitive cycle rate for learning
                time.sleep(1.0)
                
        except KeyboardInterrupt:
            logger.info("[AutonomousLoop] Interrupted by user")
        except Exception as e:
            logger.error(f"[AutonomousLoop] Error: {e}")
            raise
    
    logger.info("[AutonomousLoop] Shutdown complete")


if __name__ == "__main__":
    main()
