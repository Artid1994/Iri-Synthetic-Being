from __future__ import annotations

from pathlib import Path

from datetime import datetime, timezone
from uuid import uuid4


class ExperimentHistory:
    def __init__(self) -> None:
        self._entries: list[dict[str, object]] = []

    def record(
        self,
        hypothesis: str,
        model: str,
        parameters: dict[str, object],
        metrics: dict[str, float],
        status: str,
    ) -> None:
        self._entries.append(
            {
                "experiment_id": str(uuid4()),
                "hypothesis": hypothesis,
                "model": model,
                "parameters": dict(parameters),
                "metrics": dict(metrics),
                "status": status,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    def record_result(
        self,
        hypothesis: str,
        model: str,
        parameters: dict[str, object],
        result: dict[str, object],
    ) -> None:
        self.record(
            hypothesis=hypothesis,
            model=model,
            parameters=parameters,
            metrics={
                "error": float(result["error"]),
            },
            status=str(result["status"]),
        )

    def save(self, path) -> None:
        import json

        path = Path(path)
        path.write_text(
            json.dumps(self._entries, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path) -> "ExperimentHistory":
        import json

        path = Path(path)
        history = cls()
        history._entries = json.loads(
            path.read_text(encoding="utf-8")
        )
        return history

    def entries(self) -> list[dict[str, object]]:
        return list(self._entries)
