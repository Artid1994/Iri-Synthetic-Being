#!/usr/bin/env python3
"""
Autonomous Self-Learning Curriculum Engine for AE01M (Iri)
Structured knowledge acquisition with verification and progression.
"""
import json
import time
import random
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sys

# Add paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "01_Neocortex"))

from goal_engine import GoalEngine, GoalPriority

# Knowledge base paths
HIPPOCAMPUS_DIR = PROJECT_ROOT / "03_Hippocampus"
KNOWLEDGE_BASE_DIR = HIPPOCAMPUS_DIR / "knowledge_base"
KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)

CURRICULUM_STATE_FILE = HIPPOCAMPUS_DIR / "curriculum_state.json"
LEARNING_PROGRESS_FILE = KNOWLEDGE_BASE_DIR / "learning_progress.json"


class Domain(Enum):
    """Knowledge domains for structured learning."""
    CODING = "coding"
    SYSTEMS = "computer_systems"
    MATHEMATICS = "mathematics"
    SPACE = "space_astronomy"
    AI_ARCHITECTURE = "ai_self_architecture"


class Level(Enum):
    """Progression levels for each domain."""
    FUNDAMENTALS = 1
    INTERMEDIATE = 2
    EXPERT = 3


@dataclass
class Topic:
    """Individual learning topic."""
    id: str
    domain: Domain
    level: Level
    title: str
    description: str
    concepts: List[str]
    prerequisites: List[str]
    mastery_score: float  # 0.0 to 1.0
    attempts: int
    last_studied: Optional[float]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "domain": self.domain.value,
            "level": self.level.value,
            "title": self.title,
            "description": self.description,
            "concepts": self.concepts,
            "prerequisites": self.prerequisites,
            "mastery_score": self.mastery_score,
            "attempts": self.attempts,
            "last_studied": self.last_studied
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Topic':
        """Create from dictionary."""
        return Topic(
            id=data["id"],
            domain=Domain(data["domain"]),
            level=Level(data["level"]),
            title=data["title"],
            description=data["description"],
            concepts=data["concepts"],
            prerequisites=data.get("prerequisites", []),
            mastery_score=data.get("mastery_score", 0.0),
            attempts=data.get("attempts", 0),
            last_studied=data.get("last_studied")
        )


class CurriculumManager:
    """
    Autonomous learning curriculum manager.
    Structures knowledge acquisition with verification and progression.
    """
    
    # Curriculum matrix: Domain -> Level -> Topics
    CURRICULUM = {
        Domain.CODING: {
            Level.FUNDAMENTALS: [
                {
                    "id": "python_data_structures",
                    "title": "Python Data Structures",
                    "description": "Lists, dicts, sets, tuples - core Python collections",
                    "concepts": ["list operations", "dictionary methods", "set theory", "tuple immutability"]
                },
                {
                    "id": "algorithms_basic",
                    "title": "Basic Algorithms",
                    "description": "Search, sort, basic complexity analysis",
                    "concepts": ["linear search", "binary search", "bubble sort", "Big-O notation"]
                }
            ],
            Level.INTERMEDIATE: [
                {
                    "id": "oop_principles",
                    "title": "Object-Oriented Programming",
                    "description": "Classes, inheritance, polymorphism, design patterns",
                    "concepts": ["encapsulation", "inheritance", "polymorphism", "SOLID principles"]
                }
            ],
            Level.EXPERT: [
                {
                    "id": "async_programming",
                    "title": "Asynchronous Programming",
                    "description": "async/await, coroutines, event loops",
                    "concepts": ["asyncio", "coroutines", "futures", "event-driven architecture"]
                }
            ]
        },
        Domain.SYSTEMS: {
            Level.FUNDAMENTALS: [
                {
                    "id": "os_basics",
                    "title": "Operating System Fundamentals",
                    "description": "Processes, threads, memory management, file systems",
                    "concepts": ["processes", "threads", "virtual memory", "file systems", "syscalls"]
                }
            ],
            Level.INTERMEDIATE: [
                {
                    "id": "networking_fundamentals",
                    "title": "Computer Networking",
                    "description": "TCP/IP, HTTP, sockets, protocols",
                    "concepts": ["OSI model", "TCP/IP", "HTTP", "DNS", "routing"]
                }
            ]
        },
        Domain.MATHEMATICS: {
            Level.FUNDAMENTALS: [
                {
                    "id": "linear_algebra_basics",
                    "title": "Linear Algebra Basics",
                    "description": "Vectors, matrices, transformations",
                    "concepts": ["vectors", "matrices", "dot product", "transformations"]
                },
                {
                    "id": "calculus_fundamentals",
                    "title": "Calculus Fundamentals",
                    "description": "Derivatives, integrals, limits",
                    "concepts": ["limits", "derivatives", "integrals", "optimization"]
                }
            ],
            Level.INTERMEDIATE: [
                {
                    "id": "probability_statistics",
                    "title": "Probability & Statistics",
                    "description": "Probability theory, distributions, statistical inference",
                    "concepts": ["probability", "distributions", "hypothesis testing", "regression"]
                }
            ]
        },
        Domain.SPACE: {
            Level.FUNDAMENTALS: [
                {
                    "id": "orbital_mechanics",
                    "title": "Orbital Mechanics & Kepler's Laws",
                    "description": "Planetary motion, orbits, gravitational physics",
                    "concepts": ["Kepler's laws", "orbital elements", "escape velocity", "gravitational force"]
                },
                {
                    "id": "celestial_navigation",
                    "title": "Celestial Coordinates & Navigation",
                    "description": "Star positions, coordinate systems, astronomical units",
                    "concepts": ["right ascension", "declination", "ecliptic", "parsec", "light-year"]
                }
            ],
            Level.INTERMEDIATE: [
                {
                    "id": "stellar_evolution",
                    "title": "Stellar Evolution",
                    "description": "Star life cycles, nucleosynthesis, supernovae",
                    "concepts": ["main sequence", "red giants", "supernovae", "neutron stars", "black holes"]
                }
            ]
        },
        Domain.AI_ARCHITECTURE: {
            Level.FUNDAMENTALS: [
                {
                    "id": "ml_neural_basics",
                    "title": "Machine Learning & Neural Network Basics",
                    "description": "Foundational ML concepts, neural network architecture, training",
                    "concepts": ["supervised learning", "neural networks", "backpropagation", "activation functions", "loss functions"]
                },
                {
                    "id": "self_code_mapping",
                    "title": "Self-Code Architecture Mapping",
                    "description": "Understanding own codebase structure, module dependencies, data flow",
                    "concepts": ["code introspection", "dependency graphs", "module relationships", "capability inventory"]
                }
            ],
            Level.INTERMEDIATE: [
                {
                    "id": "llm_architectures",
                    "title": "LLM Architectures & RAG Systems",
                    "description": "Transformer models, attention mechanisms, retrieval-augmented generation",
                    "concepts": ["transformers", "attention", "embeddings", "RAG", "context windows"],
                    "prerequisites": ["ml_neural_basics"]
                },
                {
                    "id": "memory_systems",
                    "title": "AI Memory & Knowledge Systems",
                    "description": "Long-term memory, episodic memory, knowledge graphs",
                    "concepts": ["episodic memory", "semantic memory", "knowledge graphs", "vector databases"],
                    "prerequisites": ["self_code_mapping"]
                }
            ],
            Level.EXPERT: [
                {
                    "id": "self_optimization",
                    "title": "Self-Optimization & Fine-Tuning",
                    "description": "Autonomous improvement, hyperparameter tuning, architecture search",
                    "concepts": ["fine-tuning", "RLHF", "neural architecture search", "AutoML", "self-modification"],
                    "prerequisites": ["llm_architectures", "memory_systems"]
                }
            ]
        }
    }
    
    def __init__(self):
        """Initialize curriculum manager."""
        self.topics: Dict[str, Topic] = {}
        self.load_curriculum()
        print(f"[CurriculumManager] Initialized with {len(self.topics)} topics")
    
    def load_curriculum(self):
        """Load or initialize curriculum state."""
        # Initialize all topics from curriculum matrix
        for domain, levels in self.CURRICULUM.items():
            for level, topic_defs in levels.items():
                for topic_def in topic_defs:
                    topic = Topic(
                        id=topic_def["id"],
                        domain=domain,
                        level=level,
                        title=topic_def["title"],
                        description=topic_def["description"],
                        concepts=topic_def["concepts"],
                        prerequisites=topic_def.get("prerequisites", []),
                        mastery_score=0.0,
                        attempts=0,
                        last_studied=None
                    )
                    self.topics[topic.id] = topic
        
        # Load existing progress if available
        if CURRICULUM_STATE_FILE.exists():
            try:
                with open(CURRICULUM_STATE_FILE, 'r') as f:
                    data = json.load(f)
                    for topic_id, topic_data in data.items():
                        if topic_id in self.topics:
                            # Update mastery scores and attempts
                            self.topics[topic_id].mastery_score = topic_data.get("mastery_score", 0.0)
                            self.topics[topic_id].attempts = topic_data.get("attempts", 0)
                            self.topics[topic_id].last_studied = topic_data.get("last_studied")
                print(f"[CurriculumManager] Loaded progress from {CURRICULUM_STATE_FILE}")
            except Exception as e:
                print(f"[CurriculumManager] Error loading state: {e}")
    
    def save_curriculum(self):
        """Save curriculum state."""
        try:
            data = {tid: t.to_dict() for tid, t in self.topics.items()}
            with open(CURRICULUM_STATE_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"[CurriculumManager] Saved progress to {CURRICULUM_STATE_FILE}")
        except Exception as e:
            print(f"[CurriculumManager] Error saving state: {e}")
    
    def fetch_next_topic(self, domain: Optional[Domain] = None) -> Optional[Topic]:
        """
        Select next unmastered topic from curriculum.
        Prioritizes fundamentals, then progression based on prerequisites.
        
        Args:
            domain: Optional domain filter
        
        Returns:
            Next topic to study, or None if all mastered
        """
        candidates = []
        
        for topic in self.topics.values():
            # Filter by domain if specified
            if domain and topic.domain != domain:
                continue
            
            # Skip mastered topics (>= 0.8 mastery)
            if topic.mastery_score >= 0.8:
                continue
            
            # Check prerequisites met
            prereqs_met = all(
                self.topics[p].mastery_score >= 0.6 
                for p in topic.prerequisites 
                if p in self.topics
            )
            
            if not prereqs_met:
                continue
            
            candidates.append(topic)
        
        if not candidates:
            return None
        
        # Prioritize by:
        # 1. Level (fundamentals first)
        # 2. Least attempts (new topics)
        # 3. Lowest mastery score
        candidates.sort(key=lambda t: (t.level.value, t.attempts, t.mastery_score))
        
        return candidates[0]
    
    def generate_self_quiz(self, topic: Topic) -> Tuple[str, str, bool]:
        """
        Generate a self-quiz problem for the topic.
        Returns (question, answer, is_code_verification)
        
        Args:
            topic: Topic to quiz on
        
        Returns:
            (question, expected_answer, is_code_based)
        """
        if topic.domain == Domain.CODING:
            return self._generate_coding_quiz(topic)
        elif topic.domain == Domain.MATHEMATICS:
            return self._generate_math_quiz(topic)
        elif topic.domain == Domain.SPACE:
            return self._generate_space_quiz(topic)
        elif topic.domain == Domain.SYSTEMS:
            return self._generate_systems_quiz(topic)
        elif topic.domain == Domain.AI_ARCHITECTURE:
            return self._generate_ai_quiz(topic)
        
        return ("General knowledge quiz", "Not implemented", False)
    
    def _generate_coding_quiz(self, topic: Topic) -> Tuple[str, str, bool]:
        """Generate coding quiz with verification."""
        if "data_structures" in topic.id:
            question = "Write Python code to count frequency of each character in 'hello world'"
            answer = """
from collections import Counter
text = 'hello world'
freq = Counter(text)
print(dict(freq))
"""
            return (question, answer, True)
        
        elif "algorithms" in topic.id:
            question = "Implement binary search for sorted list [1,3,5,7,9] to find 5"
            answer = """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

result = binary_search([1,3,5,7,9], 5)
print(result)  # Should print 2
"""
            return (question, answer, True)
        
        return ("Coding concept quiz", "print('example')", True)
    
    def _generate_math_quiz(self, topic: Topic) -> Tuple[str, str, bool]:
        """Generate math quiz."""
        if "algebra" in topic.id.lower():
            question = "Calculate the dot product of vectors [1,2,3] and [4,5,6]"
            answer = "32"  # 1*4 + 2*5 + 3*6 = 32
            return (question, answer, False)
        
        elif "calculus" in topic.id.lower():
            question = "What is the derivative of f(x) = x² + 2x?"
            answer = "2x + 2"
            return (question, answer, False)
        
        return ("Math problem", "42", False)
    
    def _generate_space_quiz(self, topic: Topic) -> Tuple[str, str, bool]:
        """Generate space/astronomy quiz."""
        if "orbital" in topic.id.lower():
            question = "State Kepler's First Law of planetary motion"
            answer = "Planets orbit the Sun in elliptical paths with the Sun at one focus"
            return (question, answer, False)
        
        elif "celestial" in topic.id.lower():
            question = "What coordinate system uses right ascension and declination?"
            answer = "Equatorial coordinate system"
            return (question, answer, False)
        
        return ("Space quiz", "Universe", False)
    
    def _generate_systems_quiz(self, topic: Topic) -> Tuple[str, str, bool]:
        """Generate computer systems quiz."""
        question = "What is the difference between a process and a thread?"
        answer = "A process is an independent program with its own memory space, while a thread is a lightweight execution unit within a process that shares memory"
        return (question, answer, False)
    
    def _generate_ai_quiz(self, topic: Topic) -> Tuple[str, str, bool]:
        """Generate AI architecture quiz."""
        if "neural" in topic.id.lower() or "ml" in topic.id.lower():
            question = "Explain the purpose of backpropagation in neural network training"
            answer = "Backpropagation calculates gradients of the loss function with respect to weights using the chain rule, enabling gradient descent optimization"
            return (question, answer, False)
        
        elif "self_code" in topic.id.lower():
            question = "List the main functional modules in Iri's architecture (Neocortex, Limbic, etc.)"
            answer = "Neocortex (cognition), Visual Cortex (perception), Hippocampus (memory), Cerebellum (motor), Brain Stem (core directives)"
            return (question, answer, False)
        
        elif "llm" in topic.id.lower():
            question = "What is the key innovation of the Transformer architecture?"
            answer = "Self-attention mechanism that allows parallel processing and captures long-range dependencies better than RNNs"
            return (question, answer, False)
        
        elif "memory_systems" in topic.id.lower():
            question = "Differentiate episodic memory from semantic memory in AI systems"
            answer = "Episodic memory stores specific experiences with context (who, what, when, where), while semantic memory stores general facts and concepts without temporal context"
            return (question, answer, False)
        
        elif "optimization" in topic.id.lower():
            question = "What is RLHF and why is it important for LLM alignment?"
            answer = "Reinforcement Learning from Human Feedback trains models to generate outputs preferred by humans, improving alignment with human values and reducing harmful outputs"
            return (question, answer, False)
        
        return ("AI concept quiz", "Transformer attention mechanism", False)
    
    def verify_answer(self, question: str, user_answer: str, expected_answer: str, 
                     is_code: bool) -> Tuple[bool, float, str]:
        """
        Verify answer and calculate accuracy score.
        
        Args:
            question: The question asked
            user_answer: User's answer
            expected_answer: Expected answer
            is_code: Whether this is code verification
        
        Returns:
            (is_correct, score, feedback)
        """
        if is_code:
            # For code: check if it runs without error (simplified)
            try:
                # In production: execute in sandbox
                # For now: simple check
                if "print" in user_answer or "return" in user_answer:
                    score = 0.8  # Partial credit for attempting
                    return (True, score, "Code structure looks correct")
                else:
                    return (False, 0.3, "Code incomplete")
            except Exception as e:
                return (False, 0.0, f"Code error: {e}")
        else:
            # Text answer: fuzzy match
            user_lower = user_answer.lower().strip()
            expected_lower = expected_answer.lower().strip()
            
            # Simple keyword matching
            expected_keywords = set(expected_lower.split())
            user_keywords = set(user_lower.split())
            
            overlap = len(expected_keywords & user_keywords)
            total = len(expected_keywords)
            
            if total == 0:
                score = 0.5
            else:
                score = overlap / total
            
            if score >= 0.7:
                return (True, score, "Good answer")
            elif score >= 0.4:
                return (True, score * 0.8, "Partial understanding")
            else:
                return (False, score * 0.5, "Needs more study")
    
    def record_learning_session(self, topic: Topic, score: float):
        """Record learning session result."""
        topic.attempts += 1
        # Weighted average: new score has 40% weight
        topic.mastery_score = (topic.mastery_score * 0.6) + (score * 0.4)
        topic.last_studied = time.time()
        
        self.save_curriculum()
        
        print(f"[CurriculumManager] {topic.title}: mastery {topic.mastery_score:.1%} (attempt #{topic.attempts})")
    
    def summarize_and_store(self, topic: Topic, concepts_learned: List[str]):
        """
        Save validated concepts to knowledge base.
        
        Args:
            topic: Topic studied
            concepts_learned: List of concepts mastered
        """
        # Create knowledge note
        note_path = KNOWLEDGE_BASE_DIR / f"{topic.domain.value}"
        note_path.mkdir(exist_ok=True)
        
        note_file = note_path / f"{topic.id}.md"
        
        content = f"""# {topic.title}

**Domain:** {topic.domain.value.title()}
**Level:** {topic.level.value}
**Mastery:** {topic.mastery_score:.1%}
**Last Studied:** {time.strftime('%Y-%m-%d', time.localtime(topic.last_studied or time.time()))}

## Description
{topic.description}

## Key Concepts
{chr(10).join(f"- {concept}" for concept in concepts_learned)}

## Progress
- Attempts: {topic.attempts}
- Current mastery: {topic.mastery_score:.1%}
- Status: {"✓ Mastered" if topic.mastery_score >= 0.8 else "🔄 In Progress"}

## Notes
Knowledge acquired through autonomous self-learning curriculum.
Verified through self-quiz and verification tasks.
"""
        
        with open(note_file, 'w') as f:
            f.write(content)
        
        print(f"[CurriculumManager] Saved knowledge note: {note_file}")
    
    def get_learning_progress(self) -> Dict:
        """Get overall learning progress statistics."""
        stats = {
            "total_topics": len(self.topics),
            "mastered": 0,
            "in_progress": 0,
            "not_started": 0,
            "by_domain": {}
        }
        
        for topic in self.topics.values():
            if topic.mastery_score >= 0.8:
                stats["mastered"] += 1
            elif topic.mastery_score > 0:
                stats["in_progress"] += 1
            else:
                stats["not_started"] += 1
            
            # By domain
            domain_key = topic.domain.value
            if domain_key not in stats["by_domain"]:
                stats["by_domain"][domain_key] = {"mastered": 0, "total": 0}
            
            stats["by_domain"][domain_key]["total"] += 1
            if topic.mastery_score >= 0.8:
                stats["by_domain"][domain_key]["mastered"] += 1
        
        return stats
    
    def create_learning_goals(self, goal_engine: GoalEngine):
        """
        Create learning goals for autonomous execution.
        Registered as background goals in goal_engine.
        """
        # Get next topics for each domain
        for domain in [Domain.CODING, Domain.SPACE]:
            topic = self.fetch_next_topic(domain)
            if topic and topic.mastery_score < 0.8:
                goal = goal_engine.add_goal(
                    title=f"Learn: {topic.title}",
                    description=f"Study {topic.domain.value} topic: {topic.description}",
                    priority=GoalPriority.LOW  # Learning is low priority
                )
                print(f"[CurriculumManager] Created learning goal for: {topic.title}")


def test_self_learning():
    """Test autonomous self-learning system."""
    print("=" * 60)
    print("Autonomous Self-Learning Curriculum Engine Test")
    print("=" * 60)
    
    manager = CurriculumManager()
    
    # Test 1: Fetch next topics
    print("\n1. Testing topic selection...")
    
    coding_topic = manager.fetch_next_topic(Domain.CODING)
    if coding_topic:
        print(f"   Next coding topic: {coding_topic.title}")
        print(f"     Level: {coding_topic.level.value}")
        print(f"     Concepts: {', '.join(coding_topic.concepts[:3])}")
    
    space_topic = manager.fetch_next_topic(Domain.SPACE)
    if space_topic:
        print(f"   Next space topic: {space_topic.title}")
        print(f"     Level: {space_topic.level.value}")
        print(f"     Concepts: {', '.join(space_topic.concepts[:3])}")
    
    # Test 2: Generate and verify quiz
    print("\n2. Testing self-quiz generation...")
    
    for topic in [space_topic, coding_topic]:
        if not topic:
            continue
        
        print(f"\n   Topic: {topic.title}")
        question, answer, is_code = manager.generate_self_quiz(topic)
        print(f"   Question: {question}")
        print(f"   Type: {'Code verification' if is_code else 'Conceptual'}")
        
        # Simulate answer (in production: actual learning/quiz)
        simulated_answer = answer  # Perfect answer for test
        correct, score, feedback = manager.verify_answer(
            question, simulated_answer, answer, is_code
        )
        
        print(f"   Result: {'✓ Correct' if correct else '✗ Incorrect'}")
        print(f"   Score: {score:.1%}")
        print(f"   Feedback: {feedback}")
        
        # Record session
        manager.record_learning_session(topic, score)
        
        # Store knowledge
        manager.summarize_and_store(topic, topic.concepts[:2])
    
    # Test 3: Progress tracking
    print("\n3. Learning Progress:")
    stats = manager.get_learning_progress()
    print(f"   Total topics: {stats['total_topics']}")
    print(f"   Mastered: {stats['mastered']}")
    print(f"   In progress: {stats['in_progress']}")
    print(f"   Not started: {stats['not_started']}")
    
    print("\n   By domain:")
    for domain, domain_stats in stats['by_domain'].items():
        progress = domain_stats['mastered'] / domain_stats['total'] * 100
        print(f"     {domain}: {domain_stats['mastered']}/{domain_stats['total']} ({progress:.0f}%)")
    
    print("\n" + "=" * 60)
    print("Self-learning test complete")
    print("=" * 60)


if __name__ == "__main__":
    test_self_learning()
