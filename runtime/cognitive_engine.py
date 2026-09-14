from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from runtime.memory import Memory
from runtime.semantic_cognitive_bridge import SemanticCognitiveBridge
from runtime.semantic_response_generator import SemanticResponseGenerator
from runtime.knowledge_response_builder import KnowledgeResponseBuilder


@dataclass
class CognitiveState:
    recall_active: bool = False
    reasoning_active: bool = False
    decision_active: bool = False
    last_input: str = ""
    last_recalled: str = ""
    last_reasoning: str = ""
    last_decision: str = ""
    last_semantic_context: Optional[str] = None
    last_response: Optional[str] = None  # NEW: Generated response


class CognitiveEngine:
    def __init__(self, memory: Memory, enable_semantic: bool = True, enable_response: bool = True) -> None:
        self.state = CognitiveState()
        self.memory = memory
        self.semantic_bridge = SemanticCognitiveBridge() if enable_semantic else None
        self.response_generator = SemanticResponseGenerator() if enable_response else None
        self.knowledge_builder = KnowledgeResponseBuilder(memory) if enable_response else None

    def snapshot(self) -> CognitiveState:
        return CognitiveState(
            recall_active=self.state.recall_active,
            reasoning_active=self.state.reasoning_active,
            decision_active=self.state.decision_active,
            last_input=self.state.last_input,
            last_recalled=self.state.last_recalled,
            last_reasoning=self.state.last_reasoning,
            last_decision=self.state.last_decision,
            last_semantic_context=self.state.last_semantic_context,
            last_response=self.state.last_response,
        )

    def process(self, user_input: str, record_experience: bool = True) -> str:
        self.state.last_input = user_input

        # Process through semantic bridge if enabled
        processed_input = user_input
        semantic_context = None
        if self.semantic_bridge:
            processed_input, semantic_context = self.semantic_bridge.process_input(user_input)
            self.state.last_semantic_context = semantic_context

        self.state.recall_active = True
        recalled = self._recall(processed_input, semantic_context)
        self.state.last_recalled = recalled

        self.state.reasoning_active = True
        reasoning = self._reason(recalled, semantic_context)
        self.state.last_reasoning = reasoning

        self.state.decision_active = True
        decision = self._decide(reasoning)
        self.state.last_decision = decision

        # NEW: Generate response if decision is RESPOND
        if decision == "RESPOND" and self.response_generator:
            # First try knowledge-based response from semantic memory
            knowledge_response = None
            if self.knowledge_builder:
                knowledge_response = self.knowledge_builder.build_response(user_input, recalled)
            
            if knowledge_response:
                # Use knowledge-constructed response
                self.state.last_response = knowledge_response
            else:# Fall back to semantic response generator
                response = self.response_generator.generate_response(
                    semantic_context=semantic_context,
                    user_input=user_input,
                    cognitive_reasoning=reasoning
                )
                self.state.last_response = response
        else:
            self.state.last_response = None

        if decision == "RESPOND" and record_experience:
            self.memory.add_experience(user_input)

        self.state.recall_active = False
        self.state.reasoning_active = False
        self.state.decision_active = False

        # Return generated response if available, otherwise return decision
        if self.state.last_response:
            return self.state.last_response
        return decision

    def _recall(self, user_input: str, semantic_context: Optional[str] = None) -> str:
        user_input = user_input.strip()

        if not user_input:
            return ""

        # Combine semantic understanding with memory recall
        recalled = self.memory.recall(user_input)

        if semantic_context:
            # Add semantic understanding to recalled context
            if recalled:
                recalled = f"{recalled}\n[Semantic: {semantic_context}]"
            else:
                recalled = f"[Semantic: {semantic_context}]"

        return recalled

    def _reason(self, recalled: str, semantic_context: Optional[str] = None) -> str:
        # Enhanced reasoning with semantic context
        if semantic_context and "understood" in semantic_context.lower():
            # Has semantic understanding
            return recalled if recalled else semantic_context
        return recalled

    @staticmethod
    def _decide(reasoning: str) -> str:
        if not reasoning:
            return "NO_ACTION"

        return "RESPOND"
