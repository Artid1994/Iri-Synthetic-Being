#!/usr/bin/env python3
import re
import random
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field, asdict

# Import neural core for intent classification
try:
    from neural_core import classify_intent, NeuralIntentClassifier
    NEURAL_AVAILABLE = True
except ImportError:
    NEURAL_AVAILABLE = False

@dataclass
class Intent:
    """Classified intent from user input."""
    type: str  # greeting, question, statement, command, unknown
    confidence: float
    entities: List[str]
    context_weight: Dict[str, float] = field(default_factory=dict)

@dataclass
class Concept:
    """Extracted concept with weighted relevance."""
    name: str
    category: str
    relevance: float
    related_facts: List[str] = field(default_factory=list)

class KnowledgeGraph:
    """Internal knowledge representation for autonomous reasoning."""
    
    def __init__(self):
        # Core knowledge base about Iri's architecture
        self.facts = {
            "identity": {
                "name": "ไอริ",
                "name_variants": ["Iri", "ไอริ", "AE01M"],
                "system_name": "AE01M",
                "designation": "The Transcending Form",
                "creator": "อาทิตย์ อ้วนพร (Artid Aunporn)",
                "honorific": "เจ้านาย",
                "role": "ผู้ช่วยอัจฉริยะที่มีสมองแบบชีวภาพ"
            },
            "architecture": {
                "brain_layers": ["Neocortex", "Limbic", "Hippocampus", "Cerebellum"],
                "neocortex": {
                    "function": "การคิดเชิงสัญลักษณ์และตัดสินใจ",
                    "description": "ระบบให้เหตุผลแบบอัตโนมัติ ไม่ใช้ AI ภายนอก",
                    "components": ["intent classification", "concept extraction", "reasoning rules"]
                },
                "limbic": {
                    "function": "การปรับน้ำเสียงและอารมณ์",
                    "description": "ประเมินและปรับโทนเสียงให้เหมาะสม",
                    "states": ["formal", "warm", "attentive", "supportive"]
                },
                "hippocampus": {
                    "function": "การจัดเก็บและค้นหาความจำ",
                    "description": "ค้นหาข้อมูลจากไฟล์ markdown ในระบบ",
                    "capabilities": ["context retrieval", "history tracking", "vault search"]
                },
                "cerebellum": {
                    "function": "การสังเคราะน์เสียงพูด",
                    "description": "แปลงข้อความเป็นเสียงภาษาไทย",
                    "technologies": ["gTTS", "pygame audio"]
                }
            },
            "capabilities": [
                "การให้เหตุผลอัตโนมัติ",
                "การค้นหาความจำ",
                "การสังเคราะน์เสียง",
                "การตอบสนองตามบริบท",
                "การประมวลผลภาษาไทย"
            ]
        }
        
        # Semantic relationships with weighted connections
        self.relations = {
            "สมอง": {
                "related": ["Neocortex", "brain", "reasoning", "thinking", "คิด", "ตัดสินใจ"],
                "weight": 1.0
            },
            "ความจำ": {
                "related": ["Hippocampus", "memory", "recall", "จำ", "เก็บข้อมูล"],
                "weight": 0.9
            },
            "เสียง": {
                "related": ["Cerebellum", "voice", "speech", "audio", "พูด", "เล่นเสียง"],
                "weight": 0.85
            },
            "อารมณ์": {
                "related": ["Limbic", "emotion", "affect", "feeling", "รู้สึก", "น้ำเสียง"],
                "weight": 0.9
            },
            "ระบบ": {
                "related": ["system", "architecture", "structure", "โครงสร้าง"],
                "weight": 0.7
            },
            "ทำงาน": {
                "related": ["function", "operate", "work", "process", "ประมวลผล"],
                "weight": 0.8
            }
        }
    
    def query(self, concept: str, context: Optional[str] = None) -> Tuple[List[str], float]:
        """Query knowledge graph for concept and return related facts with relevance score."""
        concept_lower = concept.lower()
        found_facts = []
        relevance_score = 0.0
        
        # Direct fact lookup with context awareness
        for category, data in self.facts.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    if self._matches_concept(concept_lower, key, value):
                        if isinstance(value, dict):
                            # Extract nested information
                            for sub_key, sub_value in value.items():
                                found_facts.append(f"{key}.{sub_key}: {sub_value}")
                                relevance_score += 0.8
                        else:
                            found_facts.append(f"{key}: {value}")
                            relevance_score += 1.0
            elif isinstance(data, list):
                for item in data:
                    if concept_lower in str(item).lower():
                        found_facts.append(item)
                        relevance_score += 0.7
        
        # Semantic relation lookup with weighted scoring
        for thai_term, relation_data in self.relations.items():
            if concept_lower in thai_term.lower():
                related_items = relation_data["related"]
                weight = relation_data["weight"]
                found_facts.extend([f"เกี่ยวข้องกับ: {item}" for item in related_items[:3]])
                relevance_score += weight
            elif any(concept_lower in r.lower() for r in relation_data["related"]):
                found_facts.append(f"สัมพันธ์กับแนวคิด: {thai_term}")
                relevance_score += relation_data["weight"] * 0.8
        
        # Context-based relevance boost
        if context and found_facts:
            relevance_score *= 1.2
        
        return found_facts, min(relevance_score, 1.0)
    
    def _matches_concept(self, concept: str, key: str, value: Any) -> bool:
        """Check if concept matches key or value."""
        return (concept in key.lower() or 
                concept in str(value).lower() or
                any(concept in str(v).lower() if isinstance(value, (list, dict)) else False 
                    for v in (value.values() if isinstance(value, dict) else value if isinstance(value, list) else [])))

class PatternGraphSynthesizer:
    """Dynamic pattern-based response synthesis without static templates."""
    
    def __init__(self):
        # Response building blocks with natural variations (MALE PERSONA)
        self.greeting_patterns = [
            "สวัสดีครับ",
            "ยินดีต้อนรับครับ",
            "ดีใจที่ได้พูดคุยครับ"
        ]
        
        self.identity_patterns = [
            "ผมคือ {name}",
            "ผมชื่อ {name}",
            "{name} เองครับ"
        ]
        
        self.explanation_starters = [
            "{topic} ของผม",
            "เกี่ยวกับ {topic} ครับ",
            "สำหรับ {topic}",
            "ในส่วนของ {topic}"
        ]
        
        self.function_descriptions = [
            "ทำหน้าที่ {function}",
            "รับผิดชอบ {function}",
            "มีหน้าที่ {function}",
            "ใช้ในการ {function}"
        ]
        
        self.acknowledgment_patterns = [
            "เข้าใจครับ",
            "รับทราบครับ",
            "ผมเข้าใจแล้วครับ",
            "ได้รับข้อมูลแล้วครับ"
        ]
        
        self.connectors = [
            "ซึ่ง", "โดย", "ทั้งนี้", "นอกจากนี้", "และ"
        ]
    
    def synthesize_greeting(self, include_identity: bool = True) -> str:
        """Generate natural greeting with male persona."""
        greeting = random.choice(self.greeting_patterns)
        if include_identity:
            identity = random.choice(self.identity_patterns).format(name="ไอริ")
            return f"{greeting} {identity} พร้อมรับใช้เจ้านายครับ"
        return greeting
    
    def synthesize_explanation(self, topic: str, facts: List[str], context_weight: float = 0.5) -> str:
        """Generate natural explanation from facts with data structure sanitization."""
        if not facts:
            return f"ผมยังไม่มีข้อมูลเกี่ยวกับ {topic} ในขณะนี้ครับ"
        
        # Sanitize and extract meaningful content from facts
        cleaned_facts = []
        for fact in facts[:3]:  # Limit to 3 most relevant facts
            # Remove list/dict artifacts and extract clean text
            clean = self._sanitize_data_structures(fact)
            if clean and len(clean) > 3:  # Skip very short fragments
                cleaned_facts.append(clean)
        
        if not cleaned_facts:
            return f"ผมมีข้อมูลเกี่ยวกับ {topic} แต่ยังประมวลผลไม่เสร็จครับ"
        
        # Start with topic introduction
        starter = random.choice(self.explanation_starters).format(topic=topic)
        
        # Build natural explanation
        parts = [starter]
        
        for i, clean_fact in enumerate(cleaned_facts):
            # Add natural connectors between facts
            if i > 0 and random.random() > 0.4:
                parts.append(random.choice(self.connectors))
            
            parts.append(clean_fact)
        
        # Join with natural spacing and add polite ending (male)
        explanation = " ".join(parts)
        
        # Add context-aware confidence marker (male)
        if context_weight > 0.8:
            explanation += " ครับ"
        else:
            explanation += " นะครับ"
        
        return explanation
    
    def _sanitize_data_structures(self, text: str) -> str:
        """Remove raw data structures from response text."""
        import re
        
        # Remove list brackets and clean up
        clean = re.sub(r'\[([^\]]+)\]', r'\1', text)
        
        # Remove dict-like patterns
        clean = re.sub(r'\{[^}]+\}', '', clean)
        
        # Remove quoted list items like ['item1', 'item2']
        clean = re.sub(r"'([^']+)'[,\s]*", r'\1 ', clean)
        
        # Clean up multiple spaces
        clean = re.sub(r'\s+', ' ', clean)
        
        # Extract meaningful parts after colons (key: value patterns)
        if ':' in clean:
            parts = clean.split(':')
            if len(parts) > 1:
                clean = parts[1].strip()
        
        # Remove common artifacts
        clean = clean.replace('เกี่ยวข้องกับ:', '')
        clean = clean.replace('สัมพันธ์กับแนวคิด:', '')
        
        return clean.strip()
    
    def synthesize_acknowledgment(self, concepts: List[str]) -> str:
        """Generate natural acknowledgment."""
        ack = random.choice(self.acknowledgment_patterns)
        if concepts:
            concept_list = ", ".join(concepts[:2])
            return f"{ack} เรื่อง{concept_list}"
        return ack

class SymbolicReasoner:
    """Enhanced rule-based symbolic reasoning engine with dynamic synthesis."""
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.kg = knowledge_graph
        self.synthesizer = PatternGraphSynthesizer()
        
        # Intent classification patterns
        self.intent_patterns = {
            "greeting": [
                r"(?:สวัสดี|หวัดดี|ดีจ้า|hello|hi|เฮลโล|ทักทาย)",
                r"(?:เป็นไง|สบายดี|ยินดี)"
            ],
            "question": [
                r".*(?:อะไร|ไง|ยังไง|อย่างไร|คือ|มี|เป็น).*\?*$",
                r"(?:ทำไม|เพราะอะไร|อธิบาย|บอก|แนะนำ|ช่วย.*อธิบาย)",
                r"^(?:what|how|why|when|where|who)",
                r"(?:ทำงาน|ใช้งาน|คืออะไร)"
            ],
            "command": [
                r"^(?:ทำ|จง|ช่วย|กรุณา|please|do)",
                r"(?:ให้|ด้วย)$"
            ],
            "statement": [
                r".*(?:นะ|นะคะ|ครับ|ค่ะ|เลย)$",
                r"^(?:ผม|ฉัน|เรา|i|we)"
            ]
        }
    
    def classify_intent(self, text: str) -> Intent:
        """Classify user intent with context weighting."""
        text_lower = text.lower()
        best_intent = "unknown"
        best_confidence = 0.0
        
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    confidence = 0.9 if intent_type == "question" else 0.8
                    if confidence > best_confidence:
                        best_intent = intent_type
                        best_confidence = confidence
        
        # Extract entities with importance weighting
        entities = self._extract_entities(text)
        context_weight = self._calculate_context_weight(entities, text)
        
        return Intent(
            type=best_intent,
            confidence=best_confidence,
            entities=entities,
            context_weight=context_weight
        )
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract meaningful entities from text."""
        stop_words = {
            "ค่ะ", "ครับ", "นะ", "จ้า", "เลย", "แล้ว", "มาก", "จัง",
            "the", "a", "an", "is", "are", "was", "were"
        }
        words = re.findall(r'[\w]+', text)
        return [w for w in words if w.lower() not in stop_words and len(w) > 1]
    
    def _calculate_context_weight(self, entities: List[str], text: str) -> Dict[str, float]:
        """Calculate context importance weights for entities."""
        weights = {}
        text_lower = text.lower()
        
        # Known important terms get higher weights
        important_terms = {
            "สมอง": 1.0, "brain": 1.0, "ระบบ": 0.9,
            "ความจำ": 0.95, "memory": 0.95,
            "เสียง": 0.85, "voice": 0.85,
            "อารมณ์": 0.9, "emotion": 0.9
        }
        
        for entity in entities:
            entity_lower = entity.lower()
            # Check if entity is important
            weight = important_terms.get(entity_lower, 0.5)
            
            # Boost weight if entity appears multiple times
            count = text_lower.count(entity_lower)
            weight *= min(1.0 + (count - 1) * 0.1, 1.2)
            
            weights[entity] = weight
        
        return weights
    
    def extract_concepts(self, text: str, entities: List[str], context: Optional[str]) -> List[Concept]:
        """Extract semantic concepts with knowledge graph integration."""
        concepts = []
        
        for entity in entities:
            # Query knowledge graph for concept
            facts, relevance = self.kg.query(entity, context)
            
            if facts:
                concepts.append(Concept(
                    name=entity,
                    category="known",
                    relevance=relevance,
                    related_facts=facts
                ))
            else:
                concepts.append(Concept(
                    name=entity,
                    category="unknown",
                    relevance=0.3,
                    related_facts=[]
                ))
        
        # Sort by relevance
        concepts.sort(key=lambda c: c.relevance, reverse=True)
        return concepts
    
    def reason_and_synthesize(self, intent: Intent, concepts: List[Concept], context: Optional[str]) -> str:
        """Apply reasoning and synthesize natural response dynamically."""
        
        # Check for emotional/feeling queries first
        if self._is_emotional_query(intent):
            return "EMOTIONAL_STATUS_QUERY"  # Signal to Limbic layer
        
        # Greeting intent
        if intent.type == "greeting":
            return self.synthesizer.synthesize_greeting(include_identity=True)
        
        # Question intent with concepts
        if intent.type == "question" and concepts:
            primary_concept = concepts[0]
            
            # Architecture/brain-related question
            if any(term in primary_concept.name.lower() for term in ["สมอง", "brain", "ระบบ", "architecture"]):
                facts = primary_concept.related_facts if primary_concept.related_facts else []
                
                # Add layer information if asking about brain
                if "สมอง" in primary_concept.name.lower() or "brain" in primary_concept.name.lower():
                    facts.extend([
                        "ประกอบด้วย 4 ชั้น: Neocortex (การคิดและตัดสินใจ)",
                        "Limbic (การปรับอารมณ์และน้ำเสียง)",
                        "Hippocampus (การจัดเก็บและค้นหาความจำ)",
                        "Cerebellum (การสังเคราะน์เสียงพูด)"
                    ])
                
                return self.synthesizer.synthesize_explanation(
                    "ระบบสมอง",
                    facts,
                    primary_concept.relevance
                )
            
            # General concept explanation
            elif primary_concept.related_facts:
                return self.synthesizer.synthesize_explanation(
                    primary_concept.name,
                    primary_concept.related_facts,
                    primary_concept.relevance
                )
        
        # Acknowledgment for statements or unclear intents
        concept_names = [c.name for c in concepts[:2]]
        return self.synthesizer.synthesize_acknowledgment(concept_names)
    
    def _is_emotional_query(self, intent: Intent) -> bool:
        """Check if intent contains emotional status query patterns."""
        for entity in intent.entities:
            entity_lower = entity.lower()
            if any(pattern in entity_lower for pattern in ["รู้สึก", "อารมณ์", "สบายด", "เป็นไง", "ยังไง"]):
                return True
        return False

class ExecutiveCore:
    """
    Enhanced Neocortex Executive Core with Dynamic Pattern Graph Synthesis.
    Produces natural, context-aware responses without external LLM dependencies.
    Includes self-autonomous learning with weight persistence.
    """
    
    def __init__(self, system_prompt: Optional[str] = None, state_path: Optional[str] = None):
        self.system_prompt = system_prompt or (
            "ระบบให้เหตุผลแบบสัญลักษณ์พร้อมสังเคราะน์รูปแบบแบบไดนามิก"
        )
        self.active_context: Dict[str, Any] = {}
        self.state_path = Path(state_path or "/home/artid1994/Projects/THE_TRANSCENDING_FORM/neocortex_state.json")
        
        # Initialize enhanced reasoning components
        self.knowledge_graph = KnowledgeGraph()
        self.reasoner = SymbolicReasoner(self.knowledge_graph)
        
        # Learning statistics
        self.interaction_count = 0
        self.concept_success_rates: Dict[str, Dict[str, float]] = {}  # concept -> {success: count, total: count}
        
        # Attempt to load persisted state if exists
        try:
            self.load_neocortex_state()
        except:
            pass  # Fresh start if no state file exists
    
    def process_thought(self, user_input: str, memory_context: Optional[str] = None) -> str:
        """
        Process input with dynamic pattern synthesis and context-aware reasoning.
        Generates natural, fluid responses without static templates.
        """
        if not user_input or not user_input.strip():
            return "ไม่พบข้อมูลอินพุตครับ"
        
        # Step 1: Classify intent with context awareness
        intent = self.reasoner.classify_intent(user_input)
        
        # Step 2: Extract concepts with knowledge graph integration
        concepts = self.reasoner.extract_concepts(user_input, intent.entities, memory_context)
        
        # Step 3: Reason and synthesize natural response
        response = self.reasoner.reason_and_synthesize(intent, concepts, memory_context)
        
        # Store in active context for continuity
        self.active_context["last_intent"] = intent
        self.active_context["last_concepts"] = concepts
        self.active_context["last_input"] = user_input
        
        # Autonomous learning: update concept weights based on usage
        self.interaction_count += 1
        self._update_concept_weights(concepts, intent)
        
        return response
    
    def _update_concept_weights(self, concepts: List[Concept], intent: Intent):
        """Autonomously adapt concept weights based on interaction patterns."""
        for concept in concepts:
            if concept.name not in self.concept_success_rates:
                self.concept_success_rates[concept.name] = {"success": 0, "total": 0}
            
            stats = self.concept_success_rates[concept.name]
            stats["total"] += 1
            
            # Success heuristic: high-confidence intents with known concepts
            if intent.confidence > 0.7 and concept.category == "known":
                stats["success"] += 1
                
                # Increase weight in knowledge graph relations
                for thai_term, relation_data in self.knowledge_graph.relations.items():
                    if concept.name.lower() in [r.lower() for r in relation_data["related"]]:
                        # Hebbian-style reinforcement: successful concepts get weight boost
                        relation_data["weight"] = min(1.0, relation_data["weight"] * 1.02)
    
    def save_neocortex_state(self) -> bool:
        """Persist learned reasoning weights and statistics to disk."""
        try:
            state = {
                "version": "1.0.0",
                "interaction_count": self.interaction_count,
                "concept_success_rates": self.concept_success_rates,
                "knowledge_graph_relations": {
                    term: {"related": data["related"], "weight": data["weight"]}
                    for term, data in self.knowledge_graph.relations.items()
                },
                "active_context": {
                    k: str(v) for k, v in self.active_context.items()
                    if k in ["last_input"]
                }
            }
            
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    def load_neocortex_state(self) -> bool:
        """Load persisted reasoning weights and learned patterns from disk."""
        try:
            if not self.state_path.exists():
                return False
            
            with open(self.state_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            if state.get("version") != "1.0.0":
                return False
            
            self.interaction_count = state.get("interaction_count", 0)
            self.concept_success_rates = state.get("concept_success_rates", {})
            
            # Restore learned relation weights
            saved_relations = state.get("knowledge_graph_relations", {})
            for term, data in saved_relations.items():
                if term in self.knowledge_graph.relations:
                    self.knowledge_graph.relations[term]["weight"] = data["weight"]
            
            return True
        except Exception:
            return False

if __name__ == "__main__":
    cortex = ExecutiveCore()
    
    test_queries = [
        "สวัสดีไอริ",
        "ระบบสมองทำงานอย่างไร",
        "Hippocampus คืออะไร",
        "บอกเกี่ยวกับเสียงพูด",
        "สมองมี 4 ชั้นใช่ไหม"
    ]
    
    print("🧪 Testing Enhanced Autonomous Neocortex\n")
    for query in test_queries:
        print(f"👤 User: {query}")
        result = cortex.process_thought(query)
        print(f"🧠 Iri: {result}\n")
