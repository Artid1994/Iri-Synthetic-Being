from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from runtime.runtime import TranscendingRuntime


class TrialCognitive:
    def process(
        self,
        user_input,
        record_experience=True,
    ):
        return "trial_response"


def run_trial(
    cycles: int,
    output: str,
):
    runtime = TranscendingRuntime(
        cognitive=TrialCognitive()
    )

    runtime.enable_autonomous_mode()

    start = time.time()

    results = runtime.start_safe_autonomous_runtime(
        "physical trial",
        max_cycles=cycles,
        memory_usage=0.5,
    )

    runtime.shutdown(
        "TRIAL_COMPLETE"
    )

    report = {
        "cycles_requested": cycles,
        "cycles_completed": len(results),
        "heartbeat": runtime.heartbeat_storage.load(),
        "duration_seconds": round(
            time.time() - start,
            3,
        ),
        "shutdown": (
            runtime.process_guard.shutdown_reason
        ),
    }

    Path(output).write_text(
        json.dumps(
            report,
            indent=2,
        )
    )

    return report


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cycles",
        type=int,
        default=100,
    )

    parser.add_argument(
        "--output",
        default="logs/autonomous_trial_report.json",
    )

    args = parser.parse_args()

    report = run_trial(
        args.cycles,
        args.output,
    )

    print(
        json.dumps(
            report,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
