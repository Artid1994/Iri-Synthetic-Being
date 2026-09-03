# PROJECT_MAP.md — AE01M

Purpose: compact navigation index for agents. This is NOT a source of truth.
Use `PROJECT_PLAN.md` for goals/architecture and source code/tests for implementation/behavior.

## Core Runtime / Cognition

`runtime/runtime.py`
- `TranscendingRuntime` — top-level runtime composition, autonomous actions, sensors, persistence, speech.

`runtime/cognitive_loop.py`
- `CognitiveLoop` / `CognitiveCycle` — cognitive cycle and context construction.

`runtime/cognitive_engine.py`
- `CognitiveEngine` / `CognitiveState` — baseline cognitive boundary.

`runtime/gemma_cognitive_engine.py`
- `GemmaCognitiveEngine` — Gemma-facing cognitive implementation.

`runtime/llama_cpp_inference.py`
- `LlamaCppInference` — llama.cpp inference adapter.

`runtime/ae01m_cognitive_factory.py`
- `create_cognitive_engine()` — cognitive engine construction.

`runtime/cognitive_context.py`
- `CognitiveContext` — compact cognitive context rendering.

## Identity / Brain State

`runtime/identity.py`
- `Identity` / `IdentityState` — identity state and experience progression.

`runtime/identity_continuity.py`
- `IdentityContinuity` — continuity state/history.

`runtime/self_model.py`
- `SelfModel` / `SelfModelState` — self-model state.

`runtime/personality.py`
- `Personality` / `PersonalityState` — personality adaptation/state.

`runtime/development.py`
- `Development` / `DevelopmentAssessment` — development stage evaluation.

`runtime/internal_state.py`
- `InternalStateManager` — internal state.

## Memory

`runtime/memory.py`
- `Memory` / `MemoryState` — main memory container and memory APIs.
- `co_activate()` — graph co-activation entry point.

`runtime/memory_graph.py`
- `MemoryGraph`, `MemoryNode`, `MemoryEdge` — graph memory mechanism.

`runtime/recall_index.py`
- `RecallIndex` — recall position index.

`runtime/association_index.py`
- `AssociationIndex` — association index.

`runtime/associative_recall.py`
- `AssociativeRecall` — associative recall behavior.

`runtime/semantic_index.py`
- `SemanticIndex` — semantic knowledge index.

`runtime/memory_processing.py`
- `MemoryProcessor` / `StructuredMemory` — memory structuring.

`runtime/memory_consolidation.py`
- `MemoryConsolidation` — consolidation behavior.

## Learning

`runtime/learning.py`
- `Learning` / `LearningCandidate` / `LearningEvaluation` — existing learning mechanism.

`runtime/learning_task.py`
- `LearningTask` — learning task state.

`runtime/self_directed_learning.py`
- `SelfDirectedLearning` — self-directed task creation/selection.

`runtime/autonomous_learning.py`
- `AutonomousLearning` — autonomous learning behavior.

`runtime/goal_learning.py`
- `GoalLearning` — goal-related learning.

`runtime/research_learning.py`
- `ResearchLearning` — research-to-learning bridge.

### Learning Exercise subsystem

`runtime/learning_exercise.py`
- `LearningExercise` — exercise representation/verification type.

`runtime/learning_exercise_generator.py`
- `LearningExerciseGenerator` — generates exercises from knowledge.

`runtime/learning_exercise_spec.py`
- `LearningExerciseSpec` — exercise specification.

`runtime/learning_exercise_spec_generator.py`
- `LearningExerciseSpecGenerator` — generates exercise specifications.

`runtime/learning_exercise_verifier.py`
- `LearningExerciseVerifier` — validates exercise answers.

`runtime/learning_exercise_runner.py`
- `LearningExerciseRunner` — runs/verifies an exercise.

`runtime/learning_exercise_generation_loop.py`
- `LearningExerciseGenerationLoop` — generation/retry flow.

`runtime/learning_exercise_retry_policy.py`
- `LearningExerciseRetryPolicy` — retry policy.

`runtime/learning_exercise_generation_result.py`
- `LearningExerciseGenerationResult` — generation result state.

`runtime/learning_practice.py`
- `LearningPractice` — practice checking.

`runtime/learning_verification.py`
- `LearningVerification` — learning verification result/checking.

`runtime/learning_expression_evaluator.py`
- `LearningExpressionEvaluator` — restricted expression evaluation.

## Perception / World

`runtime/perception.py`
- `Perception` / `PerceptionModule` — perception processing.

`runtime/perception_adapter.py`
- `PerceptionAdapter` — perception-to-cognitive input boundary.

`runtime/perception_payload.py`
- `PerceptionPayload` — structured perception payload.

`runtime/world_model.py`
- `WorldModel` / `WorldState` — world state.

`runtime/world_observation.py`
- `WorldObservation` — world observation representation.

`runtime/environment.py`
- `Environment` / `EnvironmentState` — environment state.

## Sensors / Voice

`runtime/sensor.py`
- `Sensor` / `SensorReading` — sensor abstraction.

`runtime/sensor_source.py`
- `SensorSource`, `MockSensor`, `CameraSensorSource`, `MicrophoneSensorSource` — sensor backends.

`runtime/audio_input.py`
- `AudioInput` / `AudioChunk` — audio input.

`runtime/speech_recognition.py`
- `SpeechRecognition` — audio transcription boundary.

`runtime/speech_output.py`
- `SpeechOutput` — speech/TTS boundary.

`runtime/voice_capture.py`
- `VoiceCapture` — voice capture.

`runtime/voice_activity.py`
- `VoiceActivityDetector` — voice activity detection.

`runtime/voice_conversation.py`
- `VoiceConversation` — voice response flow.

## Research

`runtime/numerical_engine.py`
- `NumericalEngine` — numerical model evaluation/search.

`runtime/numerical_research.py`
- `NumericalResearch` — numerical research execution.

`runtime/research_loop.py`
- `ResearchLoop` — research loop orchestration.

`runtime/research_prompt.py`
- `ResearchPrompt` — research prompt construction.

`runtime/research_proposal.py`
- `ResearchProposal` — proposal parsing/validation.

`runtime/research_safety.py`
- `ResearchSafetyGate` — research safety checks.

`runtime/experiment.py`
- `Experiment` / `ExperimentResult` — experiment representation/results.

`runtime/experiment_history.py`
- `ExperimentHistory` — experiment persistence/history.

`runtime/web_research.py`
- `WebResearch` — web research interface.

## Action / Embodiment / Autonomous Runtime

`runtime/action.py`
- `ActionModule` — action execution abstraction.

`runtime/action_mapper.py`
- `ActionMapper` — decision-to-action mapping.

`runtime/body_action.py`
- `BodyActionModule` — body action abstraction.

`runtime/body_command.py`
- `BodyCommand` — body command representation.

`runtime/body_command_adapter.py`
- `BodyCommandAdapter` — command-to-body-action conversion.

`runtime/embodiment.py`
- `EmbodimentLoop` — observe/decide/apply/feedback cycle.

`runtime/virtual_body.py`
- `VirtualBody` — virtual body state.

`runtime/robot_adapter.py`
- `RobotAdapter` — future hardware boundary.

`runtime/robot_feedback.py`
- `RobotFeedback` — robot feedback representation.

`runtime/autonomous_controller.py`
- `AutonomousController` — autonomous decision/action control.

`runtime/autonomous_loop.py`
- `AutonomousLoopController` — autonomous step loop.

`runtime/autonomous_runner.py`
- `AutonomousRunner` — autonomous execution lifecycle.

`runtime/autonomous_step.py`
- `AutonomousStep` — goal execution step.

`runtime/autonomous_gate.py`
- `AutonomousGate` — autonomous enable/allow gate.

`runtime/autonomous_policy_gate.py`
- `AutonomousPolicyGate` — autonomous policy evaluation.

`runtime/safe_runtime_control.py`
- `SafeRuntimeControl` — safe runtime start/stop.

## Safety / Resource / Persistence

`runtime/cognitive_safety_gate.py`
- `CognitiveSafetyGate` — cognitive safety evaluation.

`runtime/safety_policy.py`
- `SafetyPolicy` — command/learning safety policy and persistence.

`runtime/safety_event.py`
- `SafetyEvent` — safety event representation.

`runtime/resource_guard.py`
- `ResourceGuard` — resource constraints.

`runtime/process_guard.py`
- `ProcessGuard` — shutdown/state-save guard.

`runtime/error_recovery.py`
- `ErrorRecovery` — runtime error recovery.

`runtime/heartbeat.py`
- `Heartbeat` — runtime health/cycle state.

`runtime/heartbeat_storage.py`
- `HeartbeatStorage` — heartbeat persistence.

## Supporting Modules

`runtime/current_state.py`
- `CurrentStateModule` — current input/state capture.

`runtime/experience.py`
- `Experience` — experience representation.

`runtime/intention.py`
- `Intention` — intention state.

`runtime/goal.py`
- `Goal` — goal state/lifecycle.

`runtime/teaching.py`
- `Teaching` — teaching input/state.

`runtime/reflection.py`
- `Reflection` — reflection result/processing.

`runtime/prediction.py`
- `Prediction` — prediction state/evaluation.

`tools/code_reviewer.py`
- `CodeReviewer` — code review helper.

## Important Navigation Rules

- For a task, start here to locate likely files.
- Then search the actual symbol/import/call path.
- Read only the smallest useful source range.
- Do not trust stale line numbers; symbols are the stable navigation key.
- Do not treat the presence of a module as proof that it is integrated.
- Before integrating Learning, inspect existing `learning.py`, `learning_task.py`, `self_directed_learning.py`, and `research_learning.py` for overlap.
- Ignore `runtime.v0.2.*.py` historical/checkpoint files unless the task explicitly concerns them.

