#!/usr/bin/env python3
"""ACAA Gate-2 execution runner — fail-closed control plane.

This runner deliberately refuses execution until all frozen measurement and
provenance contracts are satisfied and explicit authorization is present.
It does not rewrite baseline artifacts or silently adapt incompatible IDs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G2 = ROOT / "docs/research-control-layer/v0.6-gate2"
TAG = "v0.6-gate2-protocol"
COMMIT = "e5fde0b298e5bff9fd00196bd718a62934f09060"
REGISTRY_HASH = "4a856e4777a64d4e59ddc8fab4e66967e7232fd4e9132aff7b916d31a912a18e"
CAU_RE = re.compile(r"^CAU-[0-9A-F]{16}$")


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit_for_tag() -> str:
    return subprocess.check_output(
        ["git", "rev-list", "-n", "1", TAG], text=True
    ).strip()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(msg: str) -> None:
    raise SystemExit(f"HARD STOP: {msg}")


def preflight() -> None:
    manifest = load_json(G2 / "EXECUTION_MANIFEST.json")
    registry = load_json(G2 / "SEED_REGISTRY.json")
    auth = (G2 / "EXECUTION_AUTHORIZATION.md").read_text(encoding="utf-8")

    if git_commit_for_tag() != COMMIT:
        fail("protocol tag does not resolve to the frozen commit")
    if file_sha256(G2 / "SEED_REGISTRY.json") != REGISTRY_HASH:
        fail("seed registry hash mismatch")
    if manifest["protocol_tag"] != TAG or manifest["frozen_commit"] != COMMIT:
        fail("execution manifest binding mismatch")
    if manifest["planned_executions"] != 33:
        fail("planned execution count is not 33")
    if manifest["authorization_required"] is not True:
        fail("authorization gate is not enabled")
    if "Status: PENDING" not in auth and "Status:** PENDING" not in auth:
        fail("authorization record is not pending")

    seeds = registry["seeds"]
    if [x["index"] for x in seeds] != list(range(11)):
        fail("seed indices are not exactly 0..10")
    values = [x["value"] for x in seeds]
    if len(values) != len(set(values)) or any(v in (0, 1) for v in values):
        fail("seed rejection/uniqueness invariant failed")

    # Frozen M-P1 schema compatibility gate. The baseline engine currently
    # emits CAU-###### identifiers; do not rewrite them here.
    engine = ROOT / "value_flow_simulator_v0.4.py"
    source = engine.read_text(encoding="utf-8")
    if "f\"CAU-{self.cau_seq:06d}\"" in source:
        fail("baseline CAU_ID format is incompatible with frozen M-P1 schema; amendment required")
    if not CAU_RE.search("CAU-0000000000000000"):
        fail("internal M-P1 schema validator failure")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    if args.execute:
        # Execution remains deliberately unreachable while the frozen metric
        # contract is incompatible with the baseline engine.
        preflight()
        fail("execution path is unavailable until all compatibility gates pass")

    preflight()
    print("PREFLIGHT: PASS")
    print("NO EXECUTION PERFORMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
