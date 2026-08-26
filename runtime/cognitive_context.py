from __future__ import annotations

from dataclasses import dataclass

from runtime.world_observation import WorldObservation


@dataclass(frozen=True)
class CognitiveContext:
    identity_stage: str
    identity_experience: int
    self_awareness: float
    self_knowledge: float
    episodic_memory: tuple[str, ...]
    semantic_memory: tuple[str, ...]
    working_memory: tuple[str, ...]
    self_history: tuple[str, ...]
    recalled_memory: tuple[str, ...] = ()
    world: WorldObservation | None = None

    def render_for_llm(self, limit: int = 2) -> str:
        sections = []

        recalled = self.recalled_memory[-limit:]
        if recalled:
            sections.append(
                "RECALLED_MEMORY:\\n"
                + "\\n".join(f"- {item}" for item in recalled)
            )

        return "\\n\\n".join(sections)

    def render(self, limit: int = 8) -> str:
        episodic = self.episodic_memory[-limit:]
        semantic = self.semantic_memory[-limit:]
        working = self.working_memory[-limit:]
        history = self.self_history[-limit:]
        recalled = self.recalled_memory[-limit:]

        sections = [
            f"IDENTITY_STAGE: {self.identity_stage}",
            f"IDENTITY_EXPERIENCE: {self.identity_experience}",
            f"SELF_AWARENESS: {self.self_awareness:.2f}",
            f"SELF_KNOWLEDGE: {self.self_knowledge:.2f}",
        ]

        if self.world is not None:
            sections.append(
                "WORLD:\n" + self.world.render()
            )

        if recalled:
            sections.append(
                "RECALLED_MEMORY:\n"
                + "\n".join(f"- {item}" for item in recalled)
            )

        if working:
            sections.append(
                "WORKING_MEMORY:\n"
                + "\n".join(f"- {item}" for item in working)
            )

        if semantic:
            sections.append(
                "KNOWN_KNOWLEDGE:\n"
                + "\n".join(f"- {item}" for item in semantic)
            )

        if episodic:
            sections.append(
                "RECENT_EXPERIENCES:\n"
                + "\n".join(f"- {item}" for item in episodic)
            )

        if history:
            sections.append(
                "SELF_HISTORY:\n"
                + "\n".join(f"- {item}" for item in history)
            )

        return "\n\n".join(sections)
