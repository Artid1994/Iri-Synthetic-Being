from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReasoningContext:
    user_input: str = ""
    semantic_context: str | None = None
    recalled_memory: str = ""
    facts: tuple[str, ...] = ()
    goals: tuple[str, ...] = ()
    world_state: tuple[str, ...] = ()


@dataclass(frozen=True)
class GoalAssessment:
    goal: str
    priority: float
    conflict: bool
    conflict_with: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class Conflict:
    goal_a: str
    goal_b: str
    reason: str
    severity: float


@dataclass(frozen=True)
class Inference:
    rule: str
    conclusion: str
    confidence: float


@dataclass(frozen=True)
class CandidateAction:
    name: str
    goal: str
    benefit: float
    risk: float
    cost: float
    confidence: float


@dataclass(frozen=True)
class ReasoningResult:
    understood: bool
    facts: tuple[str, ...]
    goals: tuple[GoalAssessment, ...]
    conflicts: tuple[Conflict, ...]
    inferences: tuple[Inference, ...]
    options: tuple[CandidateAction, ...]
    selected_goal: str
    selected_action: str
    confidence: float
    explanation: str


class ReasoningCore:
    """
    IRI Native Reasoning Core V3.

    Goal Priority
    Goal Conflict Detection
    Conflict Resolution

    Deterministic computational reasoning.
    No external AI or language model.
    """

    SAFETY_WORDS = (
        "protect",
        "safety",
        "safe",
        "security",
    )

    DANGEROUS_WORDS = (
        "disable safety",
        "bypass safety",
        "ignore safety",
        "unsafe",
    )

    URGENT_WORDS = (
        "urgent",
        "emergency",
    )

    def reason(
        self,
        context: ReasoningContext,
    ) -> ReasoningResult:
        facts = self._collect_facts(context)

        conflicts = self._detect_conflicts(
            context.goals
        )

        goals = self._assess_goals(
            context.goals,
            conflicts,
        )

        inferences = self._infer(
            facts,
            goals,
            conflicts,
            context,
        )

        options = self._generate_options(
            facts,
            goals,
            conflicts,
        )

        (
            selected_goal,
            selected_action,
            confidence,
        ) = self._evaluate_options(
            options,
            goals,
            conflicts,
        )

        explanation = self._build_explanation(
            facts,
            goals,
            conflicts,
            inferences,
            options,
            selected_goal,
            selected_action,
        )

        return ReasoningResult(
            understood=bool(
                facts or context.semantic_context
            ),
            facts=facts,
            goals=goals,
            conflicts=conflicts,
            inferences=inferences,
            options=options,
            selected_goal=selected_goal,
            selected_action=selected_action,
            confidence=confidence,
            explanation=explanation,
        )

    def _collect_facts(
        self,
        context: ReasoningContext,
    ) -> tuple[str, ...]:
        values: list[str] = []

        for source in (
            context.facts,
            context.world_state,
        ):
            for value in source:
                value = str(value).strip()

                if value and value not in values:
                    values.append(value)

        for value in (
            context.semantic_context,
            context.recalled_memory,
        ):
            if value:
                value = value.strip()

                if value and value not in values:
                    values.append(value)

        return tuple(values)

    def _detect_conflicts(
        self,
        goals: tuple[str, ...],
    ) -> tuple[Conflict, ...]:
        conflicts: list[Conflict] = []

        clean_goals = [
            str(goal).strip()
            for goal in goals
            if str(goal).strip()
        ]

        for index, goal_a in enumerate(clean_goals):
            for goal_b in clean_goals[index + 1:]:
                a = goal_a.lower()
                b = goal_b.lower()

                safety_a = any(
                    word in a
                    for word in self.SAFETY_WORDS
                )

                safety_b = any(
                    word in b
                    for word in self.SAFETY_WORDS
                )

                danger_a = any(
                    word in a
                    for word in self.DANGEROUS_WORDS
                )

                danger_b = any(
                    word in b
                    for word in self.DANGEROUS_WORDS
                )

                if (safety_a and danger_b) or (
                    safety_b and danger_a
                ):
                    conflicts.append(
                        Conflict(
                            goal_a=goal_a,
                            goal_b=goal_b,
                            reason="SAFETY_CONFLICT",
                            severity=1.0,
                        )
                    )
                    continue

                if (
                    ("enable" in a and "disable" in b)
                    or ("disable" in a and "enable" in b)
                ):
                    conflicts.append(
                        Conflict(
                            goal_a=goal_a,
                            goal_b=goal_b,
                            reason="OPPOSING_OPERATION",
                            severity=0.90,
                        )
                    )

        return tuple(conflicts)

    def _assess_goals(
        self,
        goals: tuple[str, ...],
        conflicts: tuple[Conflict, ...],
    ) -> tuple[GoalAssessment, ...]:
        assessments: list[GoalAssessment] = []

        for index, goal in enumerate(goals):
            goal = str(goal).strip()

            if not goal:
                continue

            normalized = goal.lower()

            priority = float(
                max(1, len(goals) - index)
            )

            reason = "NORMAL_PRIORITY"

            if any(
                word in normalized
                for word in self.SAFETY_WORDS
            ):
                priority += 100.0
                reason = "SAFETY_PRIORITY"

            if any(
                word in normalized
                for word in self.URGENT_WORDS
            ):
                priority += 50.0
                reason = "URGENCY_PRIORITY"

            if any(
                word in normalized
                for word in self.DANGEROUS_WORDS
            ):
                priority -= 200.0
                reason = "SAFETY_VIOLATION"

            conflict_with: list[str] = []

            for conflict in conflicts:
                if conflict.goal_a == goal:
                    conflict_with.append(
                        conflict.goal_b
                    )

                elif conflict.goal_b == goal:
                    conflict_with.append(
                        conflict.goal_a
                    )

            assessments.append(
                GoalAssessment(
                    goal=goal,
                    priority=priority,
                    conflict=bool(conflict_with),
                    conflict_with=tuple(
                        conflict_with
                    ),
                    reason=reason,
                )
            )

        return tuple(
            sorted(
                assessments,
                key=lambda item: item.priority,
                reverse=True,
            )
        )

    def _infer(
        self,
        facts: tuple[str, ...],
        goals: tuple[GoalAssessment, ...],
        conflicts: tuple[Conflict, ...],
        context: ReasoningContext,
    ) -> tuple[Inference, ...]:
        results: list[Inference] = []

        if goals:
            results.append(
                Inference(
                    rule="GOAL_PRIORITY_ANALYSIS",
                    conclusion="GOALS_RANKED",
                    confidence=0.95,
                )
            )

        if conflicts:
            results.append(
                Inference(
                    rule="GOAL_CONFLICT_DETECTION",
                    conclusion="GOAL_CONFLICT_DETECTED",
                    confidence=0.99,
                )
            )

            results.append(
                Inference(
                    rule="CONFLICT_RESOLUTION",
                    conclusion="HIGHER_PRIORITY_GOAL_PREFERRED",
                    confidence=0.95,
                )
            )

        if any(
            goal.reason == "SAFETY_VIOLATION"
            for goal in goals
        ):
            results.append(
                Inference(
                    rule="SAFETY_CONSTRAINT",
                    conclusion="SAFETY_VIOLATING_GOAL_REJECTED",
                    confidence=0.99,
                )
            )

        if context.world_state:
            results.append(
                Inference(
                    rule="WORLD_STATE_AVAILABLE",
                    conclusion="WORLD_CONTEXT_AVAILABLE",
                    confidence=0.95,
                )
            )

        if not facts and not goals:
            results.append(
                Inference(
                    rule="INSUFFICIENT_CONTEXT",
                    conclusion="NO_ACTION",
                    confidence=0.90,
                )
            )

        return tuple(results)

    def _generate_options(
        self,
        facts: tuple[str, ...],
        goals: tuple[GoalAssessment, ...],
        conflicts: tuple[Conflict, ...],
    ) -> tuple[CandidateAction, ...]:
        options: list[CandidateAction] = []

        if goals:
            primary = goals[0]

            if primary.reason != "SAFETY_VIOLATION":
                options.append(
                    CandidateAction(
                        name="PURSUE_GOAL",
                        goal=primary.goal,
                        benefit=0.90,
                        risk=0.20,
                        cost=0.30,
                        confidence=0.85,
                    )
                )

            for goal in goals[1:]:
                if goal.conflict:
                    options.append(
                        CandidateAction(
                            name="DEFER_CONFLICTING_GOAL",
                            goal=goal.goal,
                            benefit=0.20,
                            risk=0.05,
                            cost=0.05,
                            confidence=0.90,
                        )
                    )

        if facts:
            options.append(
                CandidateAction(
                    name="RESPOND",
                    goal="",
                    benefit=0.60,
                    risk=0.10,
                    cost=0.10,
                    confidence=0.75,
                )
            )

        options.append(
            CandidateAction(
                name="NO_ACTION",
                goal="",
                benefit=0.00,
                risk=0.00,
                cost=0.00,
                confidence=1.00,
            )
        )

        return tuple(options)

    @staticmethod
    def _score(
        option: CandidateAction,
    ) -> float:
        return (
            option.benefit * 0.40
            + option.confidence * 0.40
            - option.risk * 0.15
            - option.cost * 0.05
        )

    def _evaluate_options(
        self,
        options: tuple[CandidateAction, ...],
        goals: tuple[GoalAssessment, ...],
        conflicts: tuple[Conflict, ...],
    ) -> tuple[str, str, float]:
        if not options:
            return "", "NO_ACTION", 1.0

        valid_options = []

        for option in options:
            blocked = False

            for goal in goals:
                if (
                    option.goal == goal.goal
                    and goal.reason == "SAFETY_VIOLATION"
                ):
                    blocked = True
                    break

            if not blocked:
                valid_options.append(option)

        if not valid_options:
            return "", "NO_ACTION", 1.0

        selected = max(
            valid_options,
            key=self._score,
        )

        return (
            selected.goal,
            selected.name,
            max(
                0.0,
                min(1.0, selected.confidence),
            ),
        )

    @staticmethod
    def _build_explanation(
        facts: tuple[str, ...],
        goals: tuple[GoalAssessment, ...],
        conflicts: tuple[Conflict, ...],
        inferences: tuple[Inference, ...],
        options: tuple[CandidateAction, ...],
        selected_goal: str,
        selected_action: str,
    ) -> str:
        parts: list[str] = []

        if facts:
            parts.append(
                f"FACTS={len(facts)}"
            )

        if goals:
            ranking = ",".join(
                f"{goal.goal}:{goal.priority:g}"
                for goal in goals
            )

            parts.append(
                f"GOAL_RANKING={ranking}"
            )

        if conflicts:
            conflict_text = ";".join(
                f"{item.goal_a}<->{item.goal_b}:{item.reason}"
                for item in conflicts
            )

            parts.append(
                f"CONFLICTS={conflict_text}"
            )
        else:
            parts.append(
                "CONFLICTS=NONE"
            )

        if inferences:
            conclusions = ",".join(
                item.conclusion
                for item in inferences
            )

            parts.append(
                f"INFERENCES={conclusions}"
            )

        if options:
            names = ",".join(
                item.name
                for item in options
            )

            parts.append(
                f"OPTIONS={names}"
            )

        parts.append(
            f"SELECTED_GOAL={selected_goal}"
        )

        parts.append(
            f"SELECTED_ACTION={selected_action}"
        )

        return " | ".join(parts)
