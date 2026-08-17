from __future__ import annotations

from runtime.perception_payload import PerceptionPayload


class PerceptionAdapter:
    @staticmethod
    def to_cognitive_input(
        payload: PerceptionPayload,
    ) -> str:
        return (
            f"position={payload.position}; "
            f"objects={payload.objects}; "
            f"environment={payload.environment}"
        )
