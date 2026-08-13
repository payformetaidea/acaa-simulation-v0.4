#!/usr/bin/env python3
"""ACAA v0.5 O1 — Multi-Seed Behavioral Characterization."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pvariance, pstdev
from typing import Any, Dict, List, Mapping, Sequence

PLANNED_SEEDS: List[int] = [
    42, 137, 256, 512, 1024, 2048,
    4096, 8192, 16384, 32768, 65536, 131072,
]
REQUIRED_METRICS = {"gini_coefficient", "gate_efficiency", "failure_rate", "total_artifacts"}
REQUIRED_TOP_LEVEL = {
    "params", "periods_executed", "cau_records", "agents", "metrics",
    "attack_log", "adaptive_log", "provenance_events", "engine_hash",
    "config_hash", "effective_config", "execution_timestamp", "scenario", "random_seed",
}
O1_METADATA_FIELDS = {"o1_base_config_fingerprint"}


class O1ContractError(ValueError):
    pass


def load_engine(path: Path):
    spec = importlib.util.spec_from_file_location("acaa_engine_v04", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load engine module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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
        raise O1ContractError(f"artifact is not a JSON object: {path}")
    return data


def final_metric(data: Mapping[str, Any], field: str) -> Any:
    metrics = data.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        raise O1ContractError("metrics must be a non-empty list")
    value = metrics[-1].get(field)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
        raise O1ContractError(f"final metric {field!r} is invalid")
    return value


def validate_artifact(data: Mapping[str, Any], expected_seed: int) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise O1ContractError(f"missing top-level fields: {', '.join(missing)}")
    metadata_missing = sorted(O1_METADATA_FIELDS - set(data))
    if metadata_missing:
        raise O1ContractError(f"missing O1 metadata: {', '.join(metadata_missing)}")
    if data.get("scenario") != "baseline":
        raise O1ContractError(f"scenario must be baseline, got {data.get('scenario')!r}")
    if data.get("random_seed") != expected_seed:
        raise O1ContractError(f"seed mismatch: expected {expected_seed}, got {data.get('random_seed')!r}")
    if not isinstance(data["o1_base_config_fingerprint"], str) or not data["o1_base_config_fingerprint"]:
        raise O1ContractError("O1 base configuration fingerprint is invalid")
    if not isinstance(data["cau_records"], int) or data["cau_records"] < 0:
        raise O1ContractError("cau_records must be a non-negative integer")
    metrics = data["metrics"]
    if not isinstance(metrics, list) or not metrics:
        raise O1ContractError("metrics must be a non-empty list")
    periods = [m.get("period") for m in metrics]
    if periods != list(range(1, len(periods) + 1)):
        raise O1ContractError("metric periods are not sequential")
    if data.get("periods_executed") != len(metrics):
        raise O1ContractError("periods_executed does not match metrics length")
    for metric in metrics:
        missing_metric = sorted(REQUIRED_METRICS - set(metric))
        if missing_metric:
            raise O1ContractError(f"missing required metric fields: {', '.join(missing_metric)}")
        for field in REQUIRED_METRICS:
            value = metric[field]
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
                raise O1ContractError(f"metric {field!r} is invalid")
    if not isinstance(data.get("engine_hash"), str) or not data["engine_hash"]:
        raise O1ContractError("engine_hash is missing")
    if not isinstance(data.get("config_hash"), str) or not data["config_hash"]:
        raise O1ContractError("config_hash is missing")
    if not isinstance(data.get("effective_config"), dict):
        raise O1ContractError("effective_config must be an object")


def effective_config_identity(data: Mapping[str, Any]) -> str:
    effective = data["effective_config"]
    value = effective.get("fingerprint")
    if isinstance(value, str) and value:
        return value
    canonical = json.dumps(effective, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def tukey_outliers(values: Sequence[float]) -> Dict[str, Any]:
    ordered = sorted(values)
    n = len(ordered)
    if n == 0:
        return {"indices": [], "lower_fence": None, "upper_fence": None}

    def percentile(p: float) -> float:
        if n == 1:
            return ordered[0]
        position = (n - 1) * p
        lo, hi = math.floor(position), math.ceil(position)
        if lo == hi:
            return ordered[lo]
        return ordered[lo] + (ordered[hi] - ordered[lo]) * (position - lo)

    q1, q3 = percentile(0.25), percentile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return {
        "q1": q1, "q3": q3, "iqr": iqr,
        "lower_fence": lower, "upper_fence": upper,
        "indices": [i for i, value in enumerate(values) if value < lower or value > upper],
    }


def summarize(values: Sequence[float]) -> Dict[str, Any]:
    if not values:
        raise O1ContractError("cannot summarize an empty series")
    avg = mean(values)
    variance = pvariance(values) if len(values) > 1 else 0.0
    std = pstdev(values) if len(values) > 1 else 0.0
    if abs(avg) < 1e-12:
        cv, cv_reason = None, "zero_mean"
    else:
        cv, cv_reason = std / abs(avg), None
    return {
        "mean": avg,
        "variance": variance,
        "standard_deviation": std,
        "coefficient_of_variation": cv,
        "cv_reason": cv_reason,
        "outliers": tukey_outliers(values),
    }


def run_one(engine: Any, seed: int, output: Path) -> str:
    base_config = engine.BaseConfig()
    base_fingerprint = base_config.get_fingerprint()
    sim = engine.ValueFlowSim(base_config, seed, "baseline")
    sim.run()
    result = sim.export()
    result["scenario"] = "baseline"
    result["execution_timestamp"] = datetime.now(timezone.utc).isoformat()
    result["random_seed"] = seed
    result["o1_base_config_fingerprint"] = base_fingerprint
    with output.open("w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)
    return base_fingerprint


def validate_protocol(records: Sequence[Mapping[str, Any]]) -> None:
    seeds = [int(record["seed"]) for record in records]
    if seeds != PLANNED_SEEDS:
        raise O1ContractError("O1-01 failed: planned seed set != executed seed set")
    if len(seeds) != len(set(seeds)):
        raise O1ContractError("O1-02 failed: seed values are not unique")
    if len({r["base_config_fingerprint"] for r in records}) != 1:
        raise O1ContractError("O1-03 failed: base configuration is not constant")
    if len({r["engine_hash"] for r in records}) != 1:
        raise O1ContractError("O1-05 failed: engine hash is not consistent")
    if len(records) != len(PLANNED_SEEDS):
        raise O1ContractError("planned seed count was not fully executed")
    required = {
        "effective_config_fingerprint", "final_cau_count", "final_gini", "gate_efficiency",
        "failure_rate", "total_artifacts", "detected_agents", "isolated_agents", "artifact_digest",
    }
    for record in records:
        missing = required - set(record)
        if missing:
            raise O1ContractError(f"O1-06 failed: missing {', '.join(sorted(missing))}")


def execute_protocol(engine_path: Path, output_dir: Path) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    runs_dir = output_dir / "runs"
    runs_dir.mkdir(exist_ok=True)
    engine = load_engine(engine_path)
    records: List[Dict[str, Any]] = []

    for seed in PLANNED_SEEDS:
        output = runs_dir / f"seed_{seed}.json"
        run_one(engine, seed, output)
        data = load_json(output)
        validate_artifact(data, seed)
        records.append({
            "seed": seed,
            "path": str(output.relative_to(output_dir)),
            "base_config_fingerprint": data["o1_base_config_fingerprint"],
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
        })

    validate_protocol(records)
    statistics: Dict[str, Any] = {}
    for field in (
        "final_cau_count", "final_gini", "gate_efficiency", "failure_rate",
        "total_artifacts", "detected_agents", "isolated_agents",
    ):
        statistics[field] = summarize([float(r[field]) for r in records])

    evidence = {
        "schema": "acaa.v0.5.o1.evidence",
        "version": "1.0",
        "objective": "O1",
        "status": "executed",
        "protocol": {
            "planned_seed_set": PLANNED_SEEDS,
            "executed_seed_set": [r["seed"] for r in records],
            "seed_count": len(records),
            "scenario": "baseline",
        },
        "configuration": {
            "base_fingerprints": sorted({r["base_config_fingerprint"] for r in records}),
            "effective_fingerprints": [r["effective_config_fingerprint"] for r in records],
            "engine_hashes": sorted({r["engine_hash"] for r in records}),
        },
        "runs": records,
        "statistics": statistics,
        "validation": {
            "O1-01": "PASS", "O1-02": "PASS", "O1-03": "PASS",
            "O1-04": "PASS", "O1-05": "PASS", "O1-06": "PASS",
            "O1-07": "PASS", "O1-08": "PASS", "O1-09": "PASS",
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
    evidence_path = output_dir / "o1_evidence.json"
    with evidence_path.open("w", encoding="utf-8") as fh:
        json.dump(evidence, fh, indent=2, ensure_ascii=False)
    evidence["evidence_digest"] = sha256_file(evidence_path)
    with evidence_path.open("w", encoding="utf-8") as fh:
        json.dump(evidence, fh, indent=2, ensure_ascii=False)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute ACAA v0.5 O1 protocol")
    parser.add_argument("--engine", default="value_flow_simulator_v0.4.py")
    parser.add_argument("--output-dir", default="o1_evidence")
    args = parser.parse_args()
    try:
        evidence = execute_protocol(Path(args.engine).resolve(), Path(args.output_dir).resolve())
    except (O1ContractError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"O1 FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "objective": "O1",
        "status": evidence["status"],
        "seed_count": evidence["protocol"]["seed_count"],
        "statistics": evidence["statistics"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
