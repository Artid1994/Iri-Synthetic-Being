from __future__ import annotations

import signal


class ProcessGuard:
    def __init__(
        self,
        heartbeat_storage=None,
        heartbeat=None,
    ) -> None:
        self.heartbeat_storage = heartbeat_storage
        self.heartbeat = heartbeat
        self.shutdown_requested = False
        self.shutdown_reason = None

    def request_shutdown(
        self,
        reason: str = "MANUAL",
    ) -> None:
        self.shutdown_requested = True
        self.shutdown_reason = reason

        self._save_state()

    def _signal_handler(
        self,
        signum,
        frame,
    ) -> None:
        self.request_shutdown(
            f"SIGNAL_{signum}"
        )

    def install(self) -> None:
        signal.signal(
            signal.SIGINT,
            self._signal_handler,
        )

        signal.signal(
            signal.SIGTERM,
            self._signal_handler,
        )

    def _save_state(self) -> None:
        if self.heartbeat_storage is None:
            return

        data = {}

        if self.heartbeat is not None:
            data = self.heartbeat.snapshot()

        data["status"] = "SHUTDOWN"
        data["reason"] = self.shutdown_reason

        self.heartbeat_storage.save(data)

    def is_shutdown_requested(self) -> bool:
        return self.shutdown_requested
