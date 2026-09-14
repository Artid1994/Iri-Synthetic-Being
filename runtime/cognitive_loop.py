from __future__ import annotations

from dataclasses import dataclass

from runtime.action import Action
from runtime.cognitive_context import CognitiveContext
from runtime.memory import Memory
from runtime.associative_recall import AssociativeRecall
from runtime.memory_consolidation import MemoryConsolidation
from runtime.action import ActionModule
from runtime.current_state import CurrentState
from runtime.current_state import CurrentStateModule
from runtime.prediction import Prediction
from runtime.perception import Perception
from runtime.perception import PerceptionModule
from runtime.reflection import Reflection
from runtime.attention import AttentionMechanism, CognitiveTrigger
from runtime.valuation import ValuationSystem

# Brain module archived - make optional
try:
    from brain.brain import Brain
except ImportError:
    Brain = None


@dataclass(frozen=True)
class CognitiveCycle:
    input_text: str
    recalled: str
    reasoning: str
    decision: str
    experience_recorded: bool
    perception: Perception | None = None
    current_state: CurrentState | None = None
    action: Action | None = None
    attention_required: bool = False
    salience: float = 0.0


class CognitiveLoop:
    def __init__(
        self,
        cognitive,
        learning,
        personality,
        self_model,
        development,
        prediction=None,
        reflection=None,
        brain: Brain | None = None,
        enable_voice: bool = False,
        enable_attention: bool = True,
        enable_valuation: bool = True,
    ) -> None:
        self.cognitive = cognitive
        self.learning = learning
        self.personality = personality
        self.self_model = self_model
        self.development = development
        self.prediction = prediction or Prediction()
        self.reflection = reflection or Reflection()
        self.brain = brain
        self.enable_voice = enable_voice

        # Attention and valuation systems
        if enable_attention:
            self.attention = AttentionMechanism()
            self.cognitive_trigger = CognitiveTrigger(self.attention)
        else:
            self.attention = None
            self.cognitive_trigger = None
        self.valuation = ValuationSystem() if enable_valuation else None
        self.voice_synthesizer = None
        if self.enable_voice:
            try:
                from importlib.machinery import SourceFileLoader
                import os
                voice_path = os.path.join(os.path.dirname(__file__), "..", "04_Cerebellum", "voice_synthesis.py")
                if os.path.exists(voice_path):
                    mod = SourceFileLoader("voice_synthesis", voice_path).load_module()
                    self.voice_synthesizer = getattr(mod, "default_synthesizer", None)
            except Exception:
                pass

        try:
            from importlib.machinery import SourceFileLoader
            import os
            sleep_path = os.path.join(os.path.dirname(__file__), "..", "00_BrainStem", "sleep_homeostasis.py")
            if os.path.exists(sleep_path):
                mod = SourceFileLoader("sleep_homeostasis", sleep_path).load_module()
                self.sleep_homeostasis = getattr(mod, "default_sleep_homeostasis", None)
            else:
                self.sleep_homeostasis = None
        except Exception:
            self.sleep_homeostasis = None
        self.last_reflection = None

        self.perception = PerceptionModule()
        self.current_state = CurrentStateModule()
        self.action = ActionModule()

        memory = getattr(self.development, "memory", None)
        self.memory_consolidation = (
            MemoryConsolidation(memory)
            if isinstance(memory, Memory)
            else None
        )

        self.last_cycle: CognitiveCycle | None = None

        self.associative_recall = (
            AssociativeRecall(memory)
            if isinstance(memory, Memory)
            else None
        )

    def build_context(self) -> CognitiveContext:
        identity_stage = "NEWBORN"
        identity_experience = 0
        self_awareness = 0.0
        self_knowledge = 0.0
        episodic_memory = ()
        semantic_memory = ()
        working_memory = ()
        self_history = ()

        identity = getattr(self.development, "identity", None)
        if identity is not None:
            state = identity.snapshot()
            identity_stage = state.stage
            identity_experience = state.experience

        self_model = getattr(self, "self_model", None)
        if (
            self_model is not None
            and callable(getattr(self_model, "snapshot", None))
        ):
            state = self_model.snapshot()
            self_awareness = state.self_awareness
            self_knowledge = state.self_knowledge
            self_history = tuple(state.self_history)

        memory = getattr(self.development, "memory", None)
        if memory is not None:
            state = memory.snapshot()
            episodic_memory = tuple(state.episodic)
            semantic_memory = tuple(state.semantic)
            working_memory = tuple(state.working)

        return CognitiveContext(
            identity_stage=identity_stage,
            identity_experience=identity_experience,
            self_awareness=self_awareness,
            self_knowledge=self_knowledge,
            episodic_memory=episodic_memory,
            semantic_memory=semantic_memory,
            working_memory=working_memory,
            self_history=self_history,
        )

    def _apply_learning_plasticity(self, reward_signal) -> None:
        """
        Apply plasticity when learning occurs with positive reward.
        
        Strengthens neural connections based on reward magnitude.
        This creates the experience → plasticity → behavior link.
        """
        if self.brain is None:
            return
            
        # Import here to avoid circular dependency
        from brain.synapse import Synapse
        from brain.plasticity import Plasticity
        import numpy as np
        
        # Reward-modulated learning rate: higher reward = stronger plasticity
        base_learning_rate = 0.01
        modulated_rate = base_learning_rate * reward_signal.reward
        
        # Create plasticity with reward-modulated learning rate
        plasticity = Plasticity(learning_rate=modulated_rate)
        
        # Create a simple recurrent synapse in hippocampus for memory strengthening
        # This represents the "memory trace gets stronger with successful learning"
        if hasattr(self.brain, 'hippocampus'):
            region = self.brain.hippocampus
            if hasattr(region, 'population'):
                pop = region.population
                
                # Create sparse connections from chunk 0 to chunk 1
                connection_count = min(10, pop.chunk_size)
                source_indices = list(range(connection_count))
                target_indices = list(range(connection_count))
                initial_weights = [0.5] * connection_count  # Initial synaptic strength
                
                # Create synapse from first chunk to second chunk (recurrent memory)
                synapse = Synapse(
                    source=pop,
                    source_chunk_index=0,
                    target=pop,
                    target_chunk_index=1,
                    source_indices=source_indices,
                    target_indices=target_indices,
                    weights=initial_weights,
                )
                
                # Generate activity pattern representing successful learning
                source_input = np.ones(pop.chunk_size) * 0.5  # Moderate activity
                
                # Run neural projection cycle with plasticity
                result = self.brain.run_neural_projection_cycle(
                    synapse=synapse,
                    source_input=source_input,
                    plasticity=plasticity,
                )
                
                # Store adaptation info for development tracking
                if not hasattr(self, '_plasticity_events'):
                    self._plasticity_events = []
                self._plasticity_events.append({
                    'reward': reward_signal.reward,
                    'learning_rate': modulated_rate,
                    'adapted': result['adapted'],
                    'weight_change': float(np.mean(result['weights_after'] - result['weights_before'])),
                })

    def _brain_signal(
        self,
        region,
        strength: float,
    ) -> None:
        if self.brain is None:
            return

        chunk_size = region.population.chunk_size

        import numpy as np

        current = np.zeros(
            chunk_size,
            dtype=np.float32,
        )

        current[0] = strength

        region.population.step_chunk(
            0,
            current,
        )

    def process(self, user_input: str) -> CognitiveCycle:
        perception = self.perception.process(user_input)

        current_state = self.current_state.capture(
            perception.normalized_input
        )

        if not perception.has_input:
            cycle = CognitiveCycle(
                input_text="",
                recalled="",
                reasoning="",
                decision="NO_ACTION",
                experience_recorded=False,
                perception=perception,
                current_state=current_state,
                action=self.action.execute("NO_ACTION"),
            )
            self.last_cycle = cycle
            return cycle

        # Evaluate attention and salience
        salience_signal = None
        should_invoke_cognition = True  # Default: always invoke

        if self.cognitive_trigger is not None:
            # Get context for relevance evaluation
            memory = getattr(self.development, "memory", None)
            context_items = []
            if memory is not None:
                state = memory.snapshot()
                context_items = list(state.working[-3:])  # Recent working memory

            should_invoke_cognition, salience_signal = self.cognitive_trigger.should_invoke_cognition(
                perception.normalized_input,
                context=context_items if context_items else None,
            )

        attention_required = (
            self.last_cycle is None
            or self.last_cycle.input_text != perception.normalized_input
        ) and should_invoke_cognition

        if attention_required:
            if self.brain is not None:
                self._brain_signal(
                    self.brain.hippocampus,
                    1.0,
                )

            memory = getattr(self.development, "memory", None)
            if memory is not None:
                memory.add_working(
                    perception.normalized_input
                )

        salience = (
            salience_signal.salience if salience_signal is not None
            else (min(len(perception.normalized_input) / 64.0, 1.0) if attention_required else 0.0)
        )

        recalled = perception.normalized_input
        associations = []
        reasoning = ""

        if self.associative_recall is not None:
            associations = self.associative_recall.recall(
                perception.normalized_input
            )
            if associations:
                recalled = "\n".join(associations)

        if not attention_required:
            decision = "NO_ACTION"
        else:
            context = self.build_context()

            if recalled != perception.normalized_input:
                context = CognitiveContext(
                    identity_stage=context.identity_stage,
                    identity_experience=context.identity_experience,
                    self_awareness=context.self_awareness,
                    self_knowledge=context.self_knowledge,
                    episodic_memory=context.episodic_memory,
                    semantic_memory=context.semantic_memory,
                    working_memory=context.working_memory,
                    self_history=context.self_history,
                    recalled_memory=tuple(associations),
                    world=context.world,
                )

            if callable(getattr(self.cognitive, "think", None)):
                reasoning = self.cognitive.think(
                    perception.normalized_input,
                    context=context.render(),
                )
            elif callable(getattr(self.cognitive, "process", None)):
                reasoning = self.cognitive.process(
                    perception.normalized_input,
                    record_experience=False,
                )
            else:
                reasoning = ""

            decision = "RESPOND" if reasoning else "NO_ACTION"

            if reasoning:
                self.prediction.record(reasoning)

        action = self.action.execute(decision)

        if self.brain is not None:
            self._brain_signal(
                self.brain.motor_cortex,
                1.0 if decision == "RESPOND" else 0.0,
            )

        experience_recorded = False

        if decision == "RESPOND":
            if self.enable_voice and self.voice_synthesizer is not None and reasoning:
                try:
                    self.voice_synthesizer.speak(reasoning, block=False)
                except Exception:
                    pass

            candidate = self.learning.create_candidate(
                perception.normalized_input,
                "GENERAL",
                1.0,
            )

            evaluation = self.learning.evaluate(candidate)
            experience_recorded = evaluation.accepted

            # Valuation: evaluate outcome and produce reward signal
            reward_signal = None
            if self.valuation is not None and evaluation.accepted:
                reward_signal = self.valuation.evaluate_outcome(
                    outcome="learning_accepted",
                    goal_achieved=True,
                )

            if evaluation.accepted and candidate is not None:
                if self.brain is not None:
                    self.brain.store_memory(
                        candidate.experience
                    )
                    
                    # Apply plasticity when learning succeeds with positive reward
                    if reward_signal is not None and reward_signal.reward > 0:
                        self._apply_learning_plasticity(reward_signal)

                if self.memory_consolidation is not None:
                    self.memory_consolidation.consolidate(
                        perception.normalized_input
                    )

                self.personality.adapt(
                    openness_delta=0.1,
                    conscientiousness_delta=0.05,
                )

                self.self_model.update(
                    self_awareness_delta=0.1,
                    self_knowledge_delta=0.1,
                    history_entry=candidate.experience,
                )

                self.development.sync()

        if self.sleep_homeostasis is not None:
            wm_count = len(getattr(self.development.memory, "working", [])) if hasattr(self.development, "memory") else 0
            sleep_state = self.sleep_homeostasis.update_cycle(working_memory_count=wm_count)
            if sleep_state == "NEEDS_SLEEP" and decision == "RESPOND" and reasoning:
                drowsy_note = "\n\n(ไอริเริ่มรู้สึกง่วงและสมองตึงมากแล้วค่ะเจ้านาย... ต้องการเข้าสู่ Sleep Consolidation เพื่อพักฟื้นความจำระยะยาวค่ะ)"
                if drowsy_note not in reasoning:
                    reasoning += drowsy_note

        cycle = CognitiveCycle(
            input_text=perception.normalized_input,
            recalled=recalled,
            reasoning=reasoning if attention_required else "",
            decision=decision,
            experience_recorded=experience_recorded,
            perception=perception,
            current_state=current_state,
            action=action,
            attention_required=attention_required,
            salience=salience,
        )

        self.last_cycle = cycle
        return cycle

    def snapshot(self) -> CognitiveCycle | None:
        if self.last_cycle is None:
            return None

        return CognitiveCycle(
            input_text=self.last_cycle.input_text,
            recalled=self.last_cycle.recalled,
            reasoning=self.last_cycle.reasoning,
            decision=self.last_cycle.decision,
            experience_recorded=self.last_cycle.experience_recorded,
            perception=self.perception.snapshot(
                self.last_cycle.perception
            ),
            current_state=self.current_state.snapshot(
                self.last_cycle.current_state
            ),
            action=self.action.snapshot(
                self.last_cycle.action
            ),
            attention_required=self.last_cycle.attention_required,
            salience=self.last_cycle.salience,
        )
