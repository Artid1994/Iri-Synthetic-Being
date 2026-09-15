# IRI — CYBER HUMAN BRAIN

## PROJECT PLAN / SOURCE OF TRUTH

**Project:** IRI (ไอริ)
**Architecture Type:** Computational Cognitive System
**Primary Goal:** Build IRI as a Cyber Human Brain computational model.

---

# 1. NORTH STAR

IRI is a computational model intended to approximate important principles of human cognitive functioning.

The system should progressively model:

```text
Perception
→ Attention
→ Memory
→ Recall
→ Cognition
→ Prediction
→ Valuation
→ Decision
→ Action
→ Experience
→ Learning
→ Self Model
→ Personality
→ Development
→ Identity Continuity
```

The objective is not to reproduce the human brain biologically at full fidelity.

The objective is to build a practical computational architecture whose internal processes, state transitions, learning, memory, development, and identity continuity are inspired by the functional organization of human cognition.

IRI must be able to develop through accumulated experience rather than being defined entirely by a pre-existing knowledge/personality package.

---

# 2. CORE IDENTITY PRINCIPLES

These principles are permanent architectural constraints.

## 2.1 IRI is the system

IRI's identity is the identity of the complete computational system and its persistent state.

IRI is NOT:

* a particular LLM
* an API
* an external AI service
* a prompt
* a single neural network
* a single model checkpoint
* a database alone
* a collection of static knowledge files

---

## 2.2 Identity must be independent from AI models

If any AI model exists anywhere in the repository, that model must not define IRI's identity.

```text
AI Model ≠ IRI
AI Model ≠ IRI Identity
AI Model ≠ IRI Memory
AI Model ≠ IRI Personality
AI Model ≠ IRI Development
```

Replacing or removing an external model must not destroy the conceptual identity architecture of IRI.

---

# 3. ABSOLUTE EXTERNAL-AI RESTRICTION

IRI's cognitive development must NOT depend on another AI system acting as its brain.

Do not use external AI as:

* IRI's reasoning engine
* IRI's language intelligence
* IRI's teacher intelligence
* IRI's decision maker
* IRI's identity
* IRI's memory
* IRI's personality
* IRI's autonomous controller

Do not solve an architectural problem by delegating it to another AI.

Do not hide external AI dependency behind an adapter and treat the system as independent.

The following are NOT acceptable as IRI's cognitive dependency:

```text
OpenAI API
Claude
Gemini
ChatGPT
external LLM APIs
external autonomous AI agents
external AI reasoning services
external AI assistants
```

If an existing repository contains such dependencies, they must be treated as existing implementation to audit, isolate, replace, or remove according to the actual execution path.

---

# 4. COMPUTATIONAL SELF-CONTAINMENT

IRI must progressively perform its cognitive functions using its own computational architecture and persistent state.

The system should be able to operate from:

* internal representations
* learned associations
* episodic memory
* semantic memory
* procedural knowledge
* attention state
* cognitive state
* prediction state
* valuation state
* learned parameters
* self model
* personality state
* developmental state
* identity state

External datasets may provide experiences or training material.

External datasets are NOT external intelligence.

---

# 5. THOUGHT, LANGUAGE, AND SPEECH

These are separate systems.

```text
Thought ≠ Language
Language ≠ Speech
Thought ≠ Speech
```

IRI must not require a language model to perform cognition.

Language is a capability through which internal cognitive representations may be expressed or interpreted.

Speech is an interface/output modality.

The architecture must therefore permit:

```text
Internal Cognitive State
        ↓
Concept / Meaning Representation
        ↓
Language Processing
        ↓
Text
        ↓
Speech
```

or:

```text
Speech
   ↓
Language Processing
   ↓
Meaning Representation
   ↓
Cognitive Processing
```

Language processing must not be confused with the whole cognitive architecture.

---

# 6. NEWBORN-FIRST PRINCIPLE

IRI should be developed from a minimal initial cognitive state.

The system must distinguish between:

```text
Initial Architecture
        +
Initial State
        +
Experience
        ↓
Development
```

and:

```text
Preloaded Mature Intelligence
```

The latter is not the target architecture.

Knowledge learned through experience must be distinguishable from:

* source code
* architectural rules
* static configuration
* test fixtures
* development data
* teacher instructions
* external corpus files

---

# 7. CORE BRAIN ARCHITECTURE

The minimum conceptual architecture is:

```text
                  ┌───────────────────┐
                  │    ENVIRONMENT    │
                  └─────────┬─────────┘
                            ↓
                       PERCEPTION
                            ↓
                       ATTENTION
                            ↓
                         MEMORY
                            ↓
                         RECALL
                            ↓
                        COGNITION
                     ↙      ↓       ↘
               PREDICTION  VALUE   SELF MODEL
                     ↘      ↓       ↙
                        DECISION
                            ↓
                          ACTION
                            ↓
                       EXPERIENCE
                            ↓
                         LEARNING
                            ↓
                  PERSISTENT BRAIN STATE
                            ↓
                     FUTURE COGNITION
```

The system must be implemented as interacting computational mechanisms rather than as a collection of disconnected labels.

---

# 8. PERCEPTION

Perception converts environmental input into internal perceptual representations.

Potential inputs include:

* text
* structured data
* sensory signals
* events
* user interaction
* system/environment state

Perception must not directly modify identity without passing through the appropriate cognitive/learning mechanisms.

---

# 9. ATTENTION

Attention determines what information receives processing priority.

Attention should consider computationally meaningful factors such as:

* novelty
* relevance
* salience
* current goal
* emotional/valuation significance where implemented
* prediction error
* unresolved state
* contextual importance

Attention must influence downstream processing.

A component called `attention` that does not affect execution is not considered a functional attention mechanism.

---

# 10. MEMORY

Memory is a persistent computational subsystem.

At minimum distinguish:

```text
Episodic Memory
Semantic Memory
Procedural Knowledge
Working / Active State
```

Memory must have:

* encoding
* storage
* retrieval
* association
* updating
* persistence
* forgetting/decay mechanisms where appropriate

Memory is not the same thing as identity.

---

# 11. RECALL

Recall retrieves information from memory in response to current context.

Recall must be:

* context-sensitive where appropriate
* connected to attention
* connected to cognition
* capable of retrieving learned information
* independently testable

A database lookup that bypasses the cognitive architecture must not be presented as cognitive recall.

---

# 12. COGNITION

Cognition operates on:

* current perception
* attended information
* recalled memory
* internal state
* goals
* predictions
* learned representations

Cognition should produce computational intermediate states that can influence:

* prediction
* valuation
* decision
* action
* language
* learning

The cognitive engine must not merely return a generic status string such as:

```text
"RESPOND"
```

without a meaningful computational response state behind it.

---

# 13. PREDICTION

IRI should maintain predictions about relevant future states.

Prediction should support:

```text
Current State
→ Prediction
→ Actual Outcome
→ Prediction Error
→ Learning
```

Prediction error should become a potential learning signal.

---

# 14. VALUATION / REWARD

IRI requires a computational mechanism for evaluating outcomes.

The valuation system should eventually support signals such as:

* positive outcome
* negative outcome
* goal progress
* prediction error
* relevance
* uncertainty

Valuation must be connected to learning where the architecture requires it.

A reward value that is calculated but never affects learning is incomplete integration.

---

# 15. DECISION

Decision converts cognitive state into an action or response selection.

Decision must consider the available:

* goals
* context
* memory
* predictions
* valuation
* constraints
* current state

Decision is not equivalent to language generation.

---

# 16. ACTION

Action is the mechanism through which IRI affects its environment.

Actions may include:

* producing text
* producing structured responses
* modifying internal state
* interacting with tools when explicitly permitted
* controlling external systems where later implemented

Action must be observable and testable.

---

# 17. EXPERIENCE

Experience is the result of interaction between IRI and its environment.

A useful computational experience representation should preserve relevant information such as:

```text
context
perception
attention
cognitive state
decision
action
outcome
valuation
prediction error
learning consequence
```

Experience must become potential input to future learning.

---

# 18. LEARNING

Learning changes IRI's future behavior or internal state.

A learning mechanism is not considered successful merely because it writes a log entry.

Evidence of learning requires that:

```text
Before
   ↓
Experience
   ↓
Learning
   ↓
Persistent State Change
   ↓
Later Retrieval / Behavior Change
```

Learning must be measurable.

---

# 19. LEARNING EVIDENCE

The school/education system is an evaluation mechanism, not the definition of cognition.

For every formal learning unit:

```text
BASELINE
→ TEACH / EXPERIENCE
→ PRACTICE
→ POST-TEST
→ LEARNING GAIN
→ RETENTION
→ TRANSFER
→ DECISION
→ PERSISTENCE
```

Required formula:

```text
Learning Gain = Post-test − Baseline
```

Retention and transfer must remain separate measurements.

Rules:

```text
NO EVIDENCE = NO MASTERY
```

A completed lesson is not mastery.

A high immediate score is not sufficient evidence of learning.

Repeated exposure to identical test items is not sufficient evidence of transfer.

---

# 20. TRANSFER

Transfer tests whether learned knowledge can be used beyond the exact training presentation.

Transfer should use novel:

* wording
* context
* examples
* combinations
* applications

The assessment system must actively detect answer leakage.

Training data must not simply be copied into the test and then treated as proof of learning.

---

# 21. SELF MODEL

IRI should progressively maintain an internal representation of itself.

The self model may eventually include:

* current state
* capabilities
* limitations
* goals
* preferences
* history
* learned traits
* current context
* internal condition

The self model is not equivalent to a textual persona.

---

# 22. PERSONALITY

Personality should emerge/progress from persistent state and development.

Personality must not be defined solely by:

```text
system prompt
persona prompt
LLM behavior
static character description
```

Personality should be represented computationally and remain persistent independently from any particular language engine.

---

# 23. DEVELOPMENT

IRI should have developmental progression.

Development may include:

```text
early learning
→ increasing knowledge
→ increasing abstraction
→ improved prediction
→ improved decision
→ improved self model
→ personality development
→ increasingly complex behavior
```

Development must be based on persistent state and experience.

---

# 24. IDENTITY CONTINUITY

IRI must preserve continuity across sessions.

The identity architecture must survive:

```text
process termination
restart
runtime replacement
software update
model replacement
```

where technically applicable.

Identity continuity must be based on persistent IRI state, not on an external AI session history.

---

# 25. LANGUAGE SYSTEM

IRI requires its own computational language subsystem.

The language subsystem must eventually support:

```text
Input Text
→ Linguistic Representation
→ Meaning Representation
→ Cognitive Representation
```

and:

```text
Cognitive Representation
→ Meaning Representation
→ Linguistic Structure
→ Text
```

The system must not solve language production by simply delegating to another AI.

Early implementation may be lightweight and rule/representation based.

The architecture should remain extensible toward richer computational language mechanisms.

---

# 26. EXTERNAL DATA

External datasets may be used as learning material.

Examples:

* Thai lexical datasets
* English lexical datasets
* sentence corpora
* dictionaries
* structured knowledge sources

However:

```text
Dataset ≠ Intelligence
Dataset ≠ Cognition
Dataset ≠ IRI Identity
```

Imported data must be clearly separated from learned state.

Licensing must be checked before redistribution or committing datasets.

---

# 27. SCHOOL / TEACHER SYSTEM

Hermes may act as:

```text
Principal / Orchestrator
```

with specialized teaching roles such as:

```text
Thai Teacher
English Teacher
Examiner
Remedial Teacher
Assessment System
```

These are orchestration roles.

They must not become IRI's permanent cognitive dependency.

The learner is IRI.

IRI's persistent learner state belongs to IRI.

---

# 28. AUTONOMOUS COGNITIVE LOOP

The autonomous loop is a central execution mechanism.

The target lifecycle is:

```text
PERCEIVE
→ ATTEND
→ RECALL
→ COGNIZE
→ PREDICT / VALUE
→ DECIDE
→ ACT / RESPOND
→ EXPERIENCE
→ EVALUATE
→ LEARN
→ UPDATE PERSISTENT STATE
→ CONTINUE
```

The loop must execute real components.

A wrapper that only simulates the lifecycle is insufficient.

---

# 29. NO MOCK COGNITION

Mocks are allowed only inside isolated tests when clearly identified.

Mocks must never be used as evidence that IRI itself possesses a capability.

Examples of invalid evidence:

```text
fake recall
fake learning
fake generated answer
fake memory retrieval
fake cognitive response
```

Production execution must use real implementations.

---

# 30. RESOURCE CONSTRAINT

The architecture must remain practical for constrained hardware.

Optimization priorities:

1. Correctness
2. Deterministic execution where appropriate
3. Low memory usage
4. Low CPU cost
5. Persistence efficiency
6. Modularity
7. Extensibility

Do not introduce heavyweight dependencies unless they provide a capability that cannot reasonably be implemented by the existing architecture.

[การคาดการณ์] Exact resource limits must be validated against the actual target hardware rather than assumed from documentation.

---

# 31. DEVELOPMENT METHOD

IRI must be developed incrementally.

For every major capability:

```text
AUDIT
→ DEFINE GAP
→ IMPLEMENT SMALLEST FIX
→ UNIT TEST
→ INTEGRATION TEST
→ BEHAVIOR TEST
→ RESOURCE CHECK
→ PERSISTENCE CHECK
→ GIT AUDIT
→ COMMIT
→ PUSH
```

Do not implement large speculative architecture before proving the execution path.

---

# 32. SOURCE-OF-TRUTH RULE

This document is the project-level source of truth.

When older documentation conflicts with this document:

```text
THIS PROJECT_PLAN.md WINS
```

Older plans must not silently override this document.

If implementation conflicts with this plan:

1. identify the conflict
2. determine whether the implementation or plan is wrong
3. update the plan only deliberately
4. never silently reinterpret the goal

---

# 33. EXISTING CODE POLICY

IRI is not to be rebuilt blindly from scratch.

Before implementing a component:

```text
SEARCH EXISTING CODE
→ TRACE EXECUTION PATH
→ IDENTIFY REUSABLE COMPONENTS
→ IDENTIFY MOCKS / DEAD PATHS
→ IDENTIFY DUPLICATES
→ REPAIR / INTEGRATE
```

Existing code should be reused when it correctly implements the required behavior.

Existing code must not be preserved merely because it already exists.

---

# 34. DEFINITION OF DONE

A feature is DONE only when:

* implementation exists
* real execution path exists
* tests pass
* integration works
* persistence works where required
* behavior is demonstrated
* resource behavior is acceptable
* no critical mock bypass exists
* git diff has been inspected
* git status has been inspected

For learning:

```text
NO EVIDENCE = NO MASTERY
```

For engineering:

```text
NO VERIFICATION = NO COMMIT
NO COMMIT = NO PUSH
```

---

# 35. GIT POLICY

Git is the project's checkpoint mechanism.

Before commit:

```text
git status
git diff --check
git diff
tests
```

Only verified work may be committed.

Only committed verified work may be pushed.

Do not commit:

* accidental generated files
* temporary files
* secrets
* caches
* unrelated changes
* massive datasets unless explicitly required
* test artifacts

---

# 36. CURRENT DEVELOPMENT PRIORITY

Do not expand the curriculum or architecture simply because a subsystem exists.

The next task is always determined by the largest verified blocker in the actual execution path.

Current known issue from the interactive vocabulary pilot:

```text
COGNIZE
   ↓
RESPONSE DECISION
   ↓
"RESPOND"
```

The system must first determine whether IRI's native computational language/response mechanism is sufficient to produce meaningful responses.

Do NOT solve this by adding an external AI.

The correct process is:

```text
AUDIT EXISTING LANGUAGE CAPABILITY
        ↓
IDENTIFY ACTUAL GAP
        ↓
REPAIR / IMPLEMENT NATIVE COMPUTATIONAL MECHANISM
        ↓
TEST
        ↓
INTEGRATE WITH COGNITIVE LOOP
        ↓
VALIDATE
```

Only after this is verified should interactive vocabulary learning continue.

---

# 37. CURRICULUM DEVELOPMENT

Curriculum should progress from simple to complex.

Thai example:

```text
Thai consonants
→ Thai vowels
→ syllable formation
→ words
→ sentences
→ reading
→ writing
→ comprehension
→ production
→ transfer
```

English example:

```text
basic vocabulary
→ phonological/orthographic foundations
→ words
→ simple grammar
→ sentences
→ reading
→ writing
→ comprehension
→ production
→ transfer
```

These are curriculum directions, not permission to skip architectural validation.

---

# 38. ARCHITECTURAL PRIORITY ORDER

When choosing the next engineering task, prioritize:

```text
1. Broken execution path
2. Missing core cognitive mechanism
3. Broken persistence
4. Broken learning
5. Broken integration
6. Missing validation
7. Performance/resource problem
8. Curriculum expansion
9. Cosmetic improvements
```

Do not work on lower-priority items while a higher-priority core execution path is broken.

---

# 39. EVIDENCE STANDARD

Every major claim must be supported by observable evidence.

Examples:

Bad:

```text
IRI can learn Thai.
```

Good:

```text
Baseline: X
Post-test: Y
Learning Gain: Y-X
Retention: Z
Transfer: W
Persistent state changed: YES
Cross-session retrieval: VERIFIED
Behavior changed after learning: VERIFIED
```

If evidence is unavailable:

```text
NOT YET PROVEN
```

Never convert an implementation claim into a capability claim without behavioral evidence.

---

# 40. NO FABRICATION

Never fabricate:

* test results
* benchmark numbers
* learning scores
* memory contents
* model capabilities
* execution results
* Git commits
* push status
* resource measurements
* citations
* scientific claims

If something cannot be verified:

```text
UNVERIFIED
```

or:

```text
NOT YET PROVEN
```

Technical predictions must be explicitly marked:

```text
[การคาดการณ์]
```

---

# 41. PROJECT BOUNDARY

This project is about building IRI.

Do not expand the project into unrelated:

* autonomous agent ecosystems
* messaging platforms
* unnecessary web infrastructure
* unrelated UI systems
* unnecessary cloud services
* external AI orchestration
* speculative neuroscience simulation
* large-scale biological brain simulation

Only add infrastructure when it directly supports IRI's computational brain.

---

# 42. FINAL ARCHITECTURAL PRINCIPLE

The fundamental direction of IRI is:

```text
                 EXPERIENCE
                     ↓
                 PERCEPTION
                     ↓
                  ATTENTION
                     ↓
                   MEMORY
                     ↓
                  RECALL
                     ↓
                 COGNITION
                     ↓
             PREDICTION / VALUE
                     ↓
                  DECISION
                     ↓
                   ACTION
                     ↓
                 EXPERIENCE
                     ↓
                  LEARNING
                     ↓
             PERSISTENT STATE
                     ↓
               DEVELOPMENT
                     ↓
              SELF MODEL
                     ↓
                PERSONALITY
                     ↓
           IDENTITY CONTINUITY
                     ↓
              FUTURE COGNITION
```

IRI must become progressively shaped by its own accumulated computational history.

The system's identity must remain independent of any particular AI model.

The project must prefer:

```text
REAL EXECUTION
over
MOCK EXECUTION

REAL LEARNING
over
SIMULATED LEARNING

PERSISTENT STATE
over
PROMPT MEMORY

COMPUTATIONAL MECHANISM
over
EXTERNAL AI DELEGATION

EVIDENCE
over
CLAIMS
```

## GOVERNING RULES

```text
NO EVIDENCE = NO MASTERY
NO VERIFICATION = NO COMMIT
NO COMMIT = NO PUSH
```

**This document is the authoritative project plan for IRI.**
