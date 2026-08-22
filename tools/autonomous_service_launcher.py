from __future__ import annotations

import signal
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from runtime.runtime import TranscendingRuntime


class ServiceCognitive:
    def process(
        self,
        user_input,
        record_experience=True,
    ):
        return "service_response"


runtime = None


def shutdown_handler(
    signum,
    frame,
):
    if runtime is not None:
        runtime.shutdown(
            f"SIGNAL_{signum}"
        )

    sys.exit(0)


def main():
    global runtime

    signal.signal(
        signal.SIGTERM,
        shutdown_handler,
    )

    signal.signal(
        signal.SIGINT,
        shutdown_handler,
    )

    runtime = TranscendingRuntime(
        cognitive=ServiceCognitive()
    )

    runtime.enable_autonomous_mode()

    while not runtime.process_guard.is_shutdown_requested():

        runtime.start_safe_autonomous_runtime(
            "service cycle",
            max_cycles=1,
            memory_usage=0.5,
        )

        time.sleep(1)


if __name__ == "__main__":
    main()
