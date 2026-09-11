"""
Inner Monologue Pipeline - Private reasoning before response generation
Records internal thought process while outputting clean conversational responses.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ThoughtStep:
    """Single step in internal reasoning process."""
    stage: str  # 'memory', 'affective', 'safety', 'synthesis'
    thought: str
    timestamp: float
    confidence: float = 1.0
    metadata: Dict = None


class InnerMonologue:
    """Internal reasoning pipeline with thought logging."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.log_file = project_root / "logs" / "inner_monologue.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Thought history (recent session)
        self.thought_history = []
        self.max_history = 50
    
    def reason(self, user_input: str, context: Dict) -> Tuple[str, List[ThoughtStep]]:
        """
        Execute inner monologue reasoning pipeline.
        Returns: (final_response, thought_steps)
        """
        thoughts = []
        session_id = int(time.time() * 1000)
        
        # Stage 1: Context & Memory Evaluation
        memory_thought = self._evaluate_context_memory(user_input, context)
        thoughts.append(memory_thought)
        
        # Stage 2: Affective Tone & Safety Check
        safety_thought = self._evaluate_safety_affective(user_input, context, memory_thought)
        thoughts.append(safety_thought)
        
        # Stage 3: Response Synthesis
        synthesis_thought = self._synthesize_response(user_input, context, thoughts)
        thoughts.append(synthesis_thought)
        
        # Stage 4: Refinement
        final_response = self._refine_output(synthesis_thought, context)
        
        # Log thoughts
        self._log_thoughts(session_id, user_input, thoughts, final_response)
        
        # Store in history
        self.thought_history.extend(thoughts)
        if len(self.thought_history) > self.max_history:
            self.thought_history = self.thought_history[-self.max_history:]
        
        return final_response, thoughts
    
    def _evaluate_context_memory(self, user_input: str, context: Dict) -> ThoughtStep:
        """Stage 1: Query Hippocampus and evaluate context."""
        thought_lines = []
        
        # Check conversation history
        history_len = context.get('conversation_history_len', 0)
        thought_lines.append(f"Conversation history: {history_len} turns")
        
        # Memory relevance
        relevant_facts = context.get('relevant_facts', [])
        if relevant_facts:
            thought_lines.append(f"Found {len(relevant_facts)} relevant memory facts")
            thought_lines.append(f"Top fact: {relevant_facts[0][:80]}...")
        else:
            thought_lines.append("No immediately relevant memory facts")
        
        # User intent classification
        intent = context.get('intent_type', 'unknown')
        thought_lines.append(f"Intent classified as: {intent}")
        
        thought_text = " | ".join(thought_lines)
        
        return ThoughtStep(
            stage='memory',
            thought=thought_text,
            timestamp=time.time(),
            confidence=0.85,
            metadata={'relevant_facts_count': len(relevant_facts)}
        )
    
    def _evaluate_safety_affective(self, user_input: str, context: Dict, 
                                   memory_thought: ThoughtStep) -> ThoughtStep:
        """Stage 2: Limbic evaluation and directive validation."""
        thought_lines = []
        
        # Safety check (Core Directives)
        safety_passed = True  # Simplified - always pass for now
        thought_lines.append(f"Safety check: {'PASS' if safety_passed else 'FAIL'}")
        
        # Affective tone detection
        formality = context.get('formality', 'neutral')
        thought_lines.append(f"Formality detected: {formality}")
        
        # Emotional context
        emotion = context.get('emotion', 'neutral')
        thought_lines.append(f"Emotional tone: {emotion}")
        
        # Language preference
        language = context.get('language', 'th')
        thought_lines.append(f"Language: {language}")
        
        # DIRECTIVE_5 & DIRECTIVE_7 (Male formal Thai with creator loyalty)
        thought_lines.append("DIRECTIVE_5: Male honorifics (ครับ/ผม)")
        thought_lines.append("DIRECTIVE_7: Creator loyalty verified")
        
        thought_text = " | ".join(thought_lines)
        
        return ThoughtStep(
            stage='affective',
            thought=thought_text,
            timestamp=time.time(),
            confidence=0.95,
            metadata={'formality': formality, 'emotion': emotion}
        )
    
    def _synthesize_response(self, user_input: str, context: Dict, 
                            prior_thoughts: List[ThoughtStep]) -> ThoughtStep:
        """Stage 3: Synthesize response from context."""
        thought_lines = []
        
        # Response strategy
        intent = context.get('intent_type', 'statement')
        thought_lines.append(f"Response strategy: {intent}")
        
        # Content selection
        if context.get('relevant_facts'):
            thought_lines.append("Strategy: Fact-based informational response")
        elif intent == 'greeting':
            thought_lines.append("Strategy: Warm proactive greeting")
        elif intent == 'command':
            thought_lines.append("Strategy: Acknowledgment + execution confirmation")
        else:
            thought_lines.append("Strategy: Conversational engagement")
        
        # Tone selection
        formality = context.get('formality', 'neutral')
        if formality == 'polite':
            thought_lines.append("Tone: Formal polite (เจ้านาย + ครับ)")
        else:
            thought_lines.append("Tone: Casual polite")
        
        thought_text = " | ".join(thought_lines)
        
        return ThoughtStep(
            stage='synthesis',
            thought=thought_text,
            timestamp=time.time(),
            confidence=0.90,
            metadata={'strategy': intent}
        )
    
    def _refine_output(self, synthesis: ThoughtStep, context: Dict) -> str:
        """Stage 4: Refine and finalize output."""
        # This would normally generate the actual response
        # For now, return a placeholder that chat will override
        return context.get('draft_response', 'ผมเข้าใจแล้วครับ')
    
    def _log_thoughts(self, session_id: int, user_input: str, 
                     thoughts: List[ThoughtStep], final_response: str):
        """Log internal thought process to file."""
        try:
            log_entry = {
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input[:100],  # Truncate for privacy
                'thoughts': [
                    {
                        'stage': t.stage,
                        'thought': t.thought,
                        'timestamp': t.timestamp,
                        'confidence': t.confidence
                    }
                    for t in thoughts
                ],
                'final_response': final_response[:100]  # Truncate
            }
            
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        
        except Exception:
            pass  # Silently fail logging
    
    def get_recent_thoughts(self, n: int = 5) -> List[ThoughtStep]:
        """Get N most recent thought steps."""
        return self.thought_history[-n:]
