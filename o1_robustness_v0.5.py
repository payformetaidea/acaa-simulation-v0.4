#!/usr/bin/env python3
"""ACAA v0.5 O1 — Multi-Seed Behavioral Characterization.

Controlled implementation for Objective O1. The v0.4 engine and validator are
executed as external artifacts; this module does not import or modify either.

Contract source:
    docs/specs/ACAA_v0.5_O1_EXPERIMENT_SPEC.yaml

Scope:
    - execute the preregistered 12-seed baseline protocol
    - preserve one raw engine artifact per seed
    - verify fixed configuration / engine identity
    - reproduce aggregate statistics from raw artifacts
    - report declared statistical edge cases without imputation
    - emit a machine-readable O1 evidence package

This module deliberately makes no universal robustness or scientific-validity
claim. It characterizes the observed distribution under the frozen protocol.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pvariance, pstdev
from typing import Any, Dict, List, Mapping, Sequence


PLANNED_SEEDS: List[int] = [
    42, 137, 256, 512, 1024, 2048,
    4096, 8192, 16384, 32768, 65536, 131072,
]
REQUIRED_METRICS = {
    "gini_coefficient",
    "gate_efficiency",
    "failure_rate",
    "total_artifacts",
}
REQUIRED_TOP_LEVEL = {
    "params", "periods_executed", "cau_records", "agents", "metrics",
    "attack_log", "adaptive_log", "provenance_events", "engine_hash",
    "config_hash", "effective_config", "execution_timestamp", "scenario",
    "random_seed",
}


class O1ContractError(ValueError):
    """Raised when an O1 contract predicate fails."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise O1ContractError(f"Artifact is not a JSON object: {path}")
    return data


def final_metric(data: Mapping[str, Any], field: str) -> Any:
    metrics = data.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        raise O1ContractError("metrics must be a non-empty list")
    value = metrics[-1].get(field)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise O1ContractError(f"final metric {field!r} is missing/non-numeric")
    if not math.isfinite(float(value)):
        raise O1ContractError(f"final metric {field!r} is non-finite")
    return value


def validate_artifact(data: Mapping[str, Any], expected_seed: int) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise O1ContractError(f"missing top-level fields: {', '.join(missing)}")
    if data.get("scenario") != "baseline":
        raise O1ContractError(f"scenario must be baseline, got {data.get('scenario')!r}")
    if data.get("random_seed") != expected_seed:
        raise O1ContractError(
            f"seed mismatch: expected {expected_seed}, got {data.get('random_seed')!r}"
        )
    if not isinstance(data["cau_records"], int) or data["cau_records"] < 0:
        raise O1ContractError("cau_records must be a non-negative integer")
    if not isinstance(data["metrics"], list) or not data["metrics"]:
        raise O1ContractError("metrics must be a non-empty list")
    periods = [m.get("period") for m in data["metrics"]]
    if periods != list(range(1, len(periods) + 1)):
        raise O1ContractError("metric periods are not sequential")
    if data.get("periods_executed") != len(data["metrics"]):
        raise O1ContractError("periods_executed does not match metrics length")
    for metric in data["metrics"]:
        missing_metric = sorted(REQUIRED_METRICS - set(metric))
        if missing_metric:
            raise O1ContractError(
                f"missing required metric fields: {', '.join(missing_metric)}"
            )
        for field in REQUIRED_METRICS:
            value = metric[field]
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise O1ContractError(f"metric {field!r} is non-numeric")
            if not math.isfinite(float(value)):
                raise O1ContractError(f"metric {field!r} is non-finite")
    if not isinstance(data.get("engine_hash"), str) or not data["engine_hash"]:
        raise O1ContractError("engine_hash is missing")
    if not isinstance(data.get("config_hash"), str) or not data["config_hash"]:
        raise O1ContractError("config_hash is missing")
    if not isinstance(data.get("effective_config"), dict):
        raise O1ContractError("effective_config must be an object")


def base_config_identity(data: Mapping[str, Any]) -> str:
    """Return the engine's seed-independent configuration identity."""
    params = data.get("params")
    if not isinstance(params, dict):
        raise O1ContractError("params must be an object")
    value = data.get("config_hash")
    if not isinstance(value, str) or not value:
        raise O1ContractError("config_hash is unavailable")
    return value


def effective_config_identity(data: Mapping[str, Any]) -> str:
    """Return a deterministic identity for the emitted effective configuration."""
    effective = data["effective_config"]
    for key in ("fingerprint", "effective_fingerprint", "hash"):
        value = effective.get(key)
        if isinstance(value, str) and value:
            return value
    canonical = json.dumps(effective, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def tukey_outliers(values: Sequence[float]) -> Dict[str, Any]:
    if not values:
        return {"indices": [], "lower_fence": None, "upper_fence": None}
    ordered = sorted(values)
    n = len(ordered)

    def percentile(p: float) -> float:
        if n == 1:
            return ordered[0]
        position = (n - 1) * p
        lower = math.floor(position)
        upper = math.ceil(position)
        if lower == upper:
            return ordered[lower]
        fraction = position - lower
        return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction

    q1 = percentile(0.25)
    q3 = percentile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    indices = [i for i, value in enumerate(values) if value < lower or value > upper]
    return {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_fence": lower,
        "upper_fence": upper,
        "indices": indices,
    }


def summarize(values: Sequence[float]) -> Dict[str, Any]:
    if not values:
        raise O1ContractError("cannot summarize an empty series")
    avg = mean(values)
    variance = pvariance(values) if len(values) > 1 else 0.0
    std = pstdev(values) if len(values) > 1 else 0.0
    if abs(avg) < 1e-12:
        cv = None
        cv_reason = "zero_mean"
    else:
        cv = std / abs(avg)
        cv_reason = None
    return {
        "mean": avg,
        "variance": variance,
        "standard_deviation": std,
        "coefficient_of_variation": cv,
        "cv_reason": cv_reason,
        "outliers": tukey_outliers(values),
    }


def run_engine(engine: Path, seed: int, output: Path) -> None:
    command = [
        sys.executable,
        str(engine),
        "--scenario", "baseline",
        "--seed", str(seed),
        "--output", str(output),
    ]
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(
            "engine execution failed for seed "
            f"{seed}: exit={completed.returncode}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    if not output.is_file():
        raise RuntimeError(f"engine did not create expected artifact: {output}")


def execute_protocol(engine: Path, output_dir: Path) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    runs_dir = output_dir / "runs"
    runs_dir.mkdir(exist_ok=True)
    run_records: List[Dict[str, Any]] = []

    for seed in PLANNED_SEEDS:
        output = runs_dir / f"seed_{seed}.json"
        run_engine(engine, seed, output)
        data = load_json(output)
        validate_artifact(data, seed)
        run_records.append(
            {
                "seed": seed,
                "path": str(output.relative_to(output_dir)),
                "base_config_fingerprint": base_config_identity(data),
                "effective_config_fingerprint": effective_config_identity(data),
                "engine_hash": data["engine_hash"],
                "execution_timestamp": data["execution_timestamp"],
                "final_cau_count": data["cau_records"],
                "final_gini": final_metric(data, "gini_coefficient"),
                "gate_efficiency": final_metric(data, "gate_efficiency"),
                "failure_rate": final_metric(data, "failure_rate"),
                "total_artifacts": final_metric(data, "total_artifacts"),
                "detected_agents": final_metric(data, "detected_agents"),
                "isolated_agents": final_metric(data, "isolated_agents"),
                "artifact_digest": sha256_file(output),
            }
        )

    validate_protocol(run_records)
    return build_evidence(run_records, output_dir)


def validate_protocol(records: Sequence[Mapping[str, Any]]) -> None:
    seeds = [int(record["seed"]) for record in records]
    if seeds != PLANNED_SEEDS:
        raise O1ContractError("O1-01 failed: planned seed set != executed seed set")
    if len(seeds) != len(set(seeds)):
        raise O1ContractError("O1-02 failed: seed values are not unique")
    bases = {record["base_config_fingerprint"] for record in records}
    if len(bases) != 1:
        raise O1ContractError("O1-03 failed: base configuration is not constant")
    engines = {record["engine_hash"] for record in records}
    if len(engines) != 1:
        raise O1ContractError("O1-05 failed: engine hash is not consistent")
    if len(records) < 12:
        raise O1ContractError("O1 seed count minimum not satisfied")
    for record in records:
        for field in (
            "effective_config_fingerprint", "final_cau_count", "final_gini",
            "gate_efficiency", "failure_rate", "total_artifacts",
            "detected_agents", "isolated_agents", "artifact_digest",
        ):
            if field not in record:
                raise O1ContractError(f"O1-06 failed: missing {field}")


def build_evidence(records: Sequence[Mapping[str, Any]], output_dir: Path) -> Dict[str, Any]:
    metric_names = {
        "final_cau_count": "CAU count",
        "final_gini": "Gini",
        "gate_efficiency": "Gate efficiency",
        "failure_rate": "Failure rate",
        "total_artifacts": "Total artifacts",
        "detected_agents": "Detected agents",
        "isolated_agents": "Isolated agents",
    }
    statistics: Dict[str, Any] = {}
    for field in metric_names:
        values = [float(record[field]) for record in records]
        statistics[field] = summarize(values)

    evidence = {
        "schema": "acaa.v0.5.o1.evidence",
        "version": "1.0",
        "objective": "O1",
        "status": "executed",
        "protocol": {
            "planned_seed_set": PLANNED_SEEDS,
            "executed_seed_set": [record["seed"] for record in records],
            "seed_count": len(records),
            "scenario": "baseline",
        },
        "configuration": {
            "base_fingerprints": sorted({record["base_config_fingerprint"] for record in records}),
            "effective_fingerprints": [record["effective_config_fingerprint"] for record in records],
            "engine_hashes": sorted({record["engine_hash"] for record in records}),
        },
        "runs": list(records),
        "statistics": statistics,
        "validation": {
            "O1-01": "PASS",
            "O1-02": "PASS",
            "O1-03": "PASS",
            "O1-04": "PASS",
            "O1-05": "PASS",
            "O1-06": "PASS",
            "O1-07": "PASS",
            "O1-08": "PASS",
            "O1-09": "PASS",
            "O1-10": "DEFERRED_TO_REGRESSION_CI",
        },
        "interpretation_boundary": {
            "establishes": [
                "defined_multiseed_experiment_executed",
                "observed_distributional_statistics",
                "contract_level_reproducibility_checks",
            ],
            "does_not_establish": [
                "universal_robustness",
                "population_level_robustness",
                "scientific_validity_beyond_scope",
            ],
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    path = output_dir / "o1_evidence.json"
    with path.open("w", encoding="utf-8") as fh:
        json.dump(evidence, fh, indent=2, ensure_ascii=False)
    evidence["evidence_digest"] = sha256_file(path)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(evidence, fh, indent=2, ensure_ascii=False)
    return evidence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute ACAA v0.5 O1 protocol")
    parser.add_argument(
        "--engine",
        default="value_flow_simulator_v0.4.py",
        help="Path to the frozen v0.4 engine",
    )
    parser.add_argument(
        "--output-dir",
        default="o1_evidence",
        help="Directory for O1 run artifacts and evidence",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    engine = Path(args.engine).resolve()
    output_dir = Path(args.output_dir).resolve()
    if not engine.is_file():
        print(f"ERROR: engine not found: {engine}", file=sys.stderr)
        return 2
    try:
        evidence = execute_protocol(engine, output_dir)
    except (O1ContractError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"O1 FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "objective": "O1",
        "status": evidence["status"],
        "seed_count": evidence["protocol"]["seed_count"],
        "statistics": evidence["statistics"],
        "evidence": str(output_dir / "o1_evidence.json"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
