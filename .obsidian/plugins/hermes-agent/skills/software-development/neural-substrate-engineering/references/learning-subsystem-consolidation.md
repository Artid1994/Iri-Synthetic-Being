# Phase 9 Learning Subsystem Consolidation

## Architectural Context

In AE01M cognitive architecture, the Learning subsystem operates between observation/prediction feedback and memory consolidation:

```text
Knowledge Gap / Observation / Prediction Feedback
→ SelfDirectedLearning / LearningTask
→ LearningExerciseSpecGenerator / LearningExerciseGenerator
→ LearningPractice / LearningExerciseRunner
→ LearningExerciseVerifier / LearningVerification
→ LearningPracticeResult / PredictionEvaluation
→ Memory / Brain Synchronisation
```

## Key Principles & Contracts

1. **Learning is NOT Memory Storage**:
   - Merely storing data into an index is not learning.
   - Learning requires `Experience → Practice → Evaluation → Feedback → Update`.

2. **Verification Mechanism**:
   - `LearningExerciseVerifier`: provides deterministic verification via exact match or numerical comparison within tolerances.
   - `LearningExpressionEvaluator`: safe mathematical evaluator without `eval()` or arbitrary execution.
   - `LearningExerciseRetryPolicy`: bounds generation retries to prevent runaway loops.

3. **Runtime Integration Pattern**:
   - To expose practice flow through `TranscendingRuntime`:
     ```python
     def practice_exercise(self, exercise: LearningExercise | None, answer: str) -> LearningPracticeResult:
         result = self.learning_practice.check(exercise, answer)
         if result.passed and exercise is not None:
             experience_text = f"{exercise.question} = {answer.strip()}"
             self.learning.learn_from_prediction(experience_text, result.evaluation)
             self.sync_brain_memory()
         return result
     ```
   - Incorrect answers must not update episodic memory or sync to brain hippocampus.
   - Correct answers must produce accepted prediction evaluations, update memory, and sync to brain.

4. **Preservation of In-Progress & Untracked Subsystems**:
   - Active untracked exercise/practice modules are intentional domain layers, not transient artifacts. Never discard or clean untracked files during phase consolidation.
