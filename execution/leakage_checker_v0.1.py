"""Deterministic leakage checks for H-AICR execution manifests.

This checker validates manifest-level separation. It does not infer scientific
validity and does not inspect model outputs.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REQUIRED_SPLITS = {"train", "validation", "test"}


def load_rows(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def check_user_disjoint(rows):
    by_split = {s: set() for s in REQUIRED_SPLITS}
    for row in rows:
        split = row.get("split")
        user_id = row.get("user_id")
        if split not in REQUIRED_SPLITS or not user_id:
            raise ValueError("Each row requires split in train/validation/test and user_id")
        by_split[split].add(user_id)
    collisions = {}
    for a, b in (("train", "validation"), ("train", "test"), ("validation", "test")):
        overlap = sorted(by_split[a] & by_split[b])
        if overlap:
            collisions[f"{a}:{b}"] = overlap
    return collisions


def check_temporal(rows):
    timestamps = {}
    for row in rows:
        split = row.get("split")
        ts = row.get("timestamp")
        if split not in REQUIRED_SPLITS or not ts:
            raise ValueError("Temporal check requires split and timestamp")
        timestamps.setdefault(split, []).append(ts)
    if not timestamps.get("train") or not timestamps.get("test"):
        return {"status": "INSUFFICIENT_DATA"}
    train_max = max(timestamps["train"])
    test_min = min(timestamps["test"])
    return {
        "status": "PASS" if train_max <= test_min else "FAIL",
        "train_max": train_max,
        "test_min": test_min,
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python execution/leakage_checker_v0.1.py <split_manifest.csv>")
    path = Path(sys.argv[1])
    rows = load_rows(path)
    collisions = check_user_disjoint(rows)
    temporal = check_temporal(rows)
    result = {
        "user_disjoint": "PASS" if not collisions else "FAIL",
        "collisions": collisions,
        "temporal": temporal,
        "row_count": len(rows),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if collisions or temporal.get("status") == "FAIL":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
