#!/usr/bin/env python3
"""Gate-2 preflight verifier.

This script is intentionally non-executing: it validates repository-side
bindings and the canonical seed registry without running any experiment.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/research-control-layer/v0.6-gate2"
EXPECTED_COMMIT = "e5fde0b298e5bff9fd00196bd718a62934f09060"
EXPECTED_TAG = "v0.6-gate2-protocol"
EXPECTED_REGISTRY_HASH = "4a856e4777a64d4e59ddc8fab4e66967e7232fd4e9132aff7b916d31a912a18e"
EXPECTED_SEEDS = 11
EXPECTED_REPEATS = 3


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    registry_path = BASE / "SEED_REGISTRY.json"
    manifest_path = BASE / "EXECUTION_MANIFEST.json"
    auth_path = BASE / "EXECUTION_AUTHORIZATION.md"

    for path in (registry_path, manifest_path, auth_path):
        if not path.exists():
            raise SystemExit(f"MISSING: {path}")

    registry_bytes = registry_path.read_bytes()
    registry = json.loads(registry_bytes)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    checks = []
    checks.append(("protocol tag", manifest["protocol_tag"] == EXPECTED_TAG))
    checks.append(("frozen commit", manifest["frozen_commit"] == EXPECTED_COMMIT))
    checks.append(("registry hash", sha256_bytes(registry_bytes) == EXPECTED_REGISTRY_HASH))
    checks.append(("seed count", len(registry["seeds"]) == EXPECTED_SEEDS))
    checks.append(("repeat count", manifest["repeats_per_seed"] == EXPECTED_REPEATS))
    checks.append(("planned executions", manifest["planned_executions"] == 33))
    checks.append(("authorization required", manifest["authorization_required"] is True))
    checks.append(("evidence disabled", manifest["evidence_generation_allowed"] is False))
    checks.append(("claims disabled", manifest["result_claims_allowed"] is False))
    checks.append(("promotion disabled", manifest["hypothesis_promotion_allowed"] is False))

    values = [entry["value"] for entry in registry["seeds"]]
    checks.append(("indices 0..10", [e["index"] for e in registry["seeds"]] == list(range(11))))
    checks.append(("no rejected values", all(v not in (0, 1) for v in values)))
    checks.append(("unique values", len(values) == len(set(values))))

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}: {name}")

    if failed:
        print("PREFLIGHT: BLOCKED")
        return 1
    print("PREFLIGHT: PASS — NO EXECUTION PERFORMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
