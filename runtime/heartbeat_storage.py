from __future__ import annotations

import json
from pathlib import Path


class HeartbeatStorage:
    def __init__(
        self,
        path: str = "heartbeat.json",
    ) -> None:
        self.path = Path(path)

    def save(
        self,
        data: dict,
    ) -> None:
        self.path.write_text(
            json.dumps(
                data,
                indent=2,
            )
        )

    def load(self) -> dict:
        if not self.path.exists():
            return {}

        return json.loads(
            self.path.read_text()
        )
