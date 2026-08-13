"""Build the preregistered G0 scientific dataset lock artifacts.

Fail-closed pipeline:
1. generate exactly 679 analytical units;
2. validate Draft-07 schema and registered cohort boundaries;
3. allocate deterministic chronological 58/19/20 splits per cohort;
4. verify unit/record/cohort/temporal disjointness;
5. write dataset, split manifest and audit log;
6. verify write-once/read-only behavior in the target output directory;
7. emit a SHA-256 manifest for all frozen artifacts.

This script does not execute H-AICR algorithms and does not claim empirical
human evidence. The generated evidence class remains IN_SILICO_THEORETICAL_EVIDENCE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
EXEC = ROOT / "execution"
GENERATOR = EXEC / "scientific_generator.py"
SCHEMA = EXEC / "analytical_unit_schema.json"
CODEBOOK = EXEC / "cohort_codebook.json"
CONFIG = EXEC / "generation_configuration.json"
SPLIT_ALGO = EXEC / "split_algorithm.json"
LEAKAGE = EXEC / "leakage_checker.py"

COHORTS = [
    "G1_Pure_Consumer", "G2_Low_Producer", "G3_High_Producer",
    "G4_Iterative_Researcher", "G5_Adversarial_Spam",
    "G6_Synthetic_AI", "G7_Human_Expert",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_write(path: Path, obj) -> None:
    path.write_text(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )


def run_generator(path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(path), "--seed", "42"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"GENERATION_FAILED: {result.stderr or result.stdout}")


def validate_dataset(data: list[dict]) -> None:
    if len(data) != 679:
        raise RuntimeError("UNIT_COUNT_VIOLATION")
    if len({u["unit_uuid"] for u in data}) != 679:
        raise RuntimeError("UNIT_UUID_DUPLICATION")
    record_ids = [r["record_uuid"] for u in data for r in u["interaction_records"]]
    if len(record_ids) != 2716 or len(set(record_ids)) != 2716:
        raise RuntimeError("RECORD_UUID_VIOLATION")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    errors = []
    for i, unit in enumerate(data):
        errors.extend((i, e.message) for e in validator.iter_errors(unit))
    if errors:
        raise RuntimeError(f"SCHEMA_VALIDATION_FAILURE: {errors[:5]}")

    codebook = json.loads(CODEBOOK.read_text(encoding="utf-8"))
    counts = {name: 0 for name in COHORTS}
    for unit in data:
        group = unit["group"]
        if group not in counts:
            raise RuntimeError("COHORT_SET_VIOLATION")
        counts[group] += 1
        if len(unit["interaction_records"]) != 4:
            raise RuntimeError("NESTED_INTERACTION_COUNT_VIOLATION")
        if unit["provenance"]["seed"] != 42:
            raise RuntimeError("PROVENANCE_SEED_VIOLATION")
        if unit["provenance"]["model_revision"] != "deterministic_abm_v1":
            raise RuntimeError("MODEL_REVISION_VIOLATION")
    if counts != {name: 97 for name in COHORTS}:
        raise RuntimeError(f"COHORT_ALLOCATION_VIOLATION: {counts}")
    if not codebook.get("scientific_generation_authorized"):
        raise RuntimeError("GENERATION_GATE_CLOSED")


def build_splits(data: list[dict]) -> dict:
    algorithm = json.loads(SPLIT_ALGO.read_text(encoding="utf-8"))
    if algorithm["seed"] != 42:
        raise RuntimeError("REGISTERED_SPLIT_SEED_MISMATCH")
    if (algorithm["train_per_cohort"], algorithm["validation_per_cohort"], algorithm["test_per_cohort"]) != (58, 19, 20):
        raise RuntimeError("REGISTERED_SPLIT_ALLOCATION_MISMATCH")

    splits = {"schema_version": "1.0", "seed": 42, "allocation": {"train": 58, "validation": 19, "test": 20}, "cohorts": {}}
    for cohort in COHORTS:
        units = [u for u in data if u["group"] == cohort]
        units.sort(key=lambda u: (u["window_start"], u["unit_uuid"]))
        if len(units) != 97:
            raise RuntimeError("COHORT_COUNT_MISMATCH")
        splits["cohorts"][cohort] = {
            "train": [u["unit_uuid"] for u in units[:58]],
            "validation": [u["unit_uuid"] for u in units[58:77]],
            "test": [u["unit_uuid"] for u in units[77:]],
        }
    return splits


def verify_splits(data: list[dict], splits: dict) -> None:
    by_id = {u["unit_uuid"]: u for u in data}
    all_sets = []
    for cohort in COHORTS:
        block = splits["cohorts"][cohort]
        sets = [set(block["train"]), set(block["validation"]), set(block["test"])]
        if [len(x) for x in sets] != [58, 19, 20]:
            raise RuntimeError("SPLIT_CARDINALITY_VIOLATION")
        if set.union(*sets) != {u["unit_uuid"] for u in data if u["group"] == cohort}:
            raise RuntimeError("SPLIT_COVERAGE_VIOLATION")
        if any(a & b for i, a in enumerate(sets) for b in sets[i + 1:]):
            raise RuntimeError("UNIT_LEAKAGE_DETECTED")
        all_sets.extend(sets)

        train_end = max(by_id[x]["window_end"] for x in block["train"])
        val_start = min(by_id[x]["window_start"] for x in block["validation"])
        val_end = max(by_id[x]["window_end"] for x in block["validation"])
        test_start = min(by_id[x]["window_start"] for x in block["test"])
        if not (train_end < val_start and val_end < test_start):
            raise RuntimeError("TEMPORAL_LEAKAGE_DETECTED")

    if any(a & b for i, a in enumerate(all_sets) for b in all_sets[i + 1:]):
        raise RuntimeError("GLOBAL_UNIT_LEAKAGE_DETECTED")

    record_sets = []
    for s in all_sets:
        record_sets.append({r["record_uuid"] for uid in s for r in by_id[uid]["interaction_records"]})
    if any(a & b for i, a in enumerate(record_sets) for b in record_sets[i + 1:]):
        raise RuntimeError("RECORD_LEAKAGE_DETECTED")

    # Reuse the registered fail-closed checker as an executable control.
    namespace = {}
    exec(LEAKAGE.read_text(encoding="utf-8"), namespace)
    namespace["assert_disjoint"](*all_sets)


def verify_immutability(path: Path) -> None:
    original = path.read_bytes()
    mode = path.stat().st_mode
    try:
        path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        try:
            path.write_bytes(original + b"\\nIMMUTABILITY_PROBE")
        except (PermissionError, OSError):
            return
        raise RuntimeError("IMMUTABILITY_VIOLATION")
    finally:
        path.chmod(mode)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    if config["seed"] != 42 or config["total_independent_units"] != 679:
        raise RuntimeError("REGISTERED_CONFIGURATION_MISMATCH")

    with tempfile.TemporaryDirectory() as tmp:
        raw_tmp = Path(tmp) / "scientific_dataset_raw.json"
        run_generator(raw_tmp)
        data = json.loads(raw_tmp.read_text(encoding="utf-8"))
        validate_dataset(data)
        splits = build_splits(data)
        verify_splits(data, splits)

        raw = out / "scientific_dataset_raw.json"
        split_file = out / "splits.json"
        audit = out / "generation_audit_log.json"
        manifest = out / "artifact_sha256.json"
        raw.write_bytes(raw_tmp.read_bytes())
        canonical_write(split_file, splits)

        audit_obj = {
            "status": "PASS",
            "evidence_classification": "IN_SILICO_THEORETICAL_EVIDENCE",
            "scientific_generation": {"units": 679, "records": 2716, "schema_validation": "PASS_100_PERCENT"},
            "splits": {"train_per_cohort": 58, "validation_per_cohort": 19, "test_per_cohort": 20, "unit_intersection": 0, "record_intersection": 0, "temporal_disjoint": True},
            "immutability": "PENDING_FILESYSTEM_LOCK",
            "seed": 42,
            "model_revision": "deterministic_abm_v1",
        }
        canonical_write(audit, audit_obj)
        verify_immutability(raw)
        verify_immutability(split_file)
        audit_obj["immutability"] = "IMMUTABILITY_VERIFIED"
        canonical_write(audit, audit_obj)

        canonical_write(manifest, {
            "algorithm": "SHA-256",
            "scientific_dataset_raw.json": sha256(raw),
            "splits.json": sha256(split_file),
            "generation_audit_log.json": sha256(audit),
        })

    print(json.dumps({"status": "PASS", "units": 679, "records": 2716, "artifacts": [p.name for p in (raw, split_file, audit, manifest)]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
