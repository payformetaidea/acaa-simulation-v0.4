"""ACAA v0.6 E1 controlled runner.

This harness records an execution envelope around an explicit adapter. It never
modifies the frozen v0.5.0 target. A real experiment must be supplied through
--adapter-json; the default mode is a non-evidence smoke envelope.
"""
from __future__ import annotations
import argparse, hashlib, json, platform
from pathlib import Path

PROTOCOL = "ACAA-v0.6-E1"
CONTROL_TAG = "v0.5.0"
CONTROL_COMMIT = "de7d11ed9457ede84c1954aa70a59331bf07b72e"

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def make_record(seed: int, adapter: dict | None = None) -> dict:
    executed = adapter is not None
    outputs = adapter if executed else {"mode": "smoke", "executed": False}
    raw = json.dumps(outputs, sort_keys=True, separators=(",", ":")).encode()
    return {
        "protocol": PROTOCOL,
        "control_target": {"tag": CONTROL_TAG, "commit": CONTROL_COMMIT},
        "seed": seed,
        "status": "PASS" if executed else "SMOKE_ONLY",
        "outputs": outputs,
        "provenance": {
            "runner": "e1_runner.py",
            "python": platform.python_version(),
            "platform": platform.platform(),
            "input_sha256": sha256(str(seed).encode()),
            "artifact_sha256": sha256(raw),
        },
    }

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--adapter-json", type=Path)
    a = p.parse_args()
    adapter = json.loads(a.adapter_json.read_text(encoding="utf-8")) if a.adapter_json else None
    record = make_record(a.seed, adapter)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
