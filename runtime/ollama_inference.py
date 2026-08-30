from __future__ import annotations

import json
import urllib.request


class OllamaInference:
    def __init__(
        self,
        model: str = "ae01m-qwen-fast",
        host: str = "http://10.74.65.85:11434",
        timeout: int = 120,
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    def __call__(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "stream": False,
            "think": False,
            "options": {
                "num_ctx": 1024,
                "num_predict": 16,
                "temperature": 0.2,
                "top_p": 0.7,
            },
        }

        request = urllib.request.Request(
            f"{self.host}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(
            request,
            timeout=self.timeout,
        ) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        return str(
            data.get("message", {}).get("content", "")
        ).strip()
