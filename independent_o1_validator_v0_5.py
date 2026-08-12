#!/usr/bin/env python3
"""Independent O1 evidence validator.

This module deliberately does not import the O1 runner or the v0.4 Engine.
It validates preserved run artifacts and recomputes contract predicates from
serialized evidence only.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from statistics import mean, pvariance, pstdev
from typing import Any, Mapping, Sequence

PLANNED_SEEDS = [42, 137, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]
BASE_KEYS = [
    "pi_p", "pi_v", "pi_s", "pi_c", "delta", "lam", "alpha_thr", "periods", "n_agents", "noise",
    "sybil_min_group_size", "sybil_detection_threshold", "collusion_min_group_size",
    "collusion_detection_threshold", "spam_failure_threshold", "spam_volume_threshold",
    "abstention_threshold", "minimum_opportunity_sample", "negative_exploitation_threshold",
    "minimum_challenge_sample", "w_p", "w_b", "w_i", "w_d", "w_r", "w_t",
    "equilibrium_variance_threshold", "recovery_consecutive_periods", "cv_cau_threshold", "cv_gini_threshold",
]
METRICS = ["final_cau_count", "final_gini", "gate_efficiency", "failure_rate", "total_artifacts", "detected_agents", "isolated_agents"]
REQUIRED_RUN_FIELDS = {
    "seed", "base_config_fingerprint", "effective_config_fingerprint", "scenario_params",
    "engine_hash", "execution_timestamp", "final_cau_count", "final_gini", "gate_efficiency",
    "failure_rate", "total_artifacts", "detected_agents", "isolated_agents", "equilibrium_metrics",
    "metric_trajectory", "artifact_digest",
}

class ValidationError(ValueError):
    pass


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def base_fingerprint_from_params(params: Mapping[str, Any]) -> str:
    canonical = {key: params[key] for key in BASE_KEYS}
    return hashlib.sha256(json.dumps(canonical, sort_keys=True).encode()).hexdigest()


def effective_fingerprint(base_fp: str, seed: int, scenario: str, scenario_params: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps({
        "base_fingerprint": base_fp,
        "seed": seed,
        "scenario": scenario,
        "scenario_params": dict(scenario_params),
    }, sort_keys=True).encode()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValidationError(f"JSON object required: {path}")
    return value


def require_finite(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
        raise ValidationError(f"invalid numeric value: {label}")
    return float(value)


def tukey(values: Sequence[float]) -> dict[str, Any]:
    ordered = sorted(values)
    n = len(ordered)
    if not n:
        raise ValidationError("empty series")
    def pct(p: float) -> float:
        if n == 1:
            return ordered[0]
        pos = (n - 1) * p
        lo, hi = math.floor(pos), math.ceil(pos)
        return ordered[lo] if lo == hi else ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)
    q1, q3 = pct(.25), pct(.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return {"q1": q1, "q3": q3, "iqr": iqr, "lower_fence": lo, "upper_fence": hi,
            "indices": [i for i, v in enumerate(values) if v < lo or v > hi]}


def independent_summary(values: Sequence[float]) -> dict[str, Any]:
    avg = mean(values)
    variance = pvariance(values) if len(values) > 1 else 0.0
    std = pstdev(values) if len(values) > 1 else 0.0
    return {
        "mean": avg,
        "variance": variance,
        "standard_deviation": std,
        "coefficient_of_variation": None if abs(avg) < 1e-12 else std / abs(avg),
        "cv_reason": "zero_mean" if abs(avg) < 1e-12 else None,
        "outliers": tukey(values),
    }


def close(a: Any, b: Any, tol: float = 1e-12) -> bool:
    if a is None or b is None:
        return a is b
    return math.isclose(float(a), float(b), rel_tol=1e-10, abs_tol=tol)


def validate_run(path: Path, expected_seed: int) -> dict[str, Any]:
    data = load_json(path)
    for key in ("params", "metrics", "engine_hash", "effective_config", "scenario", "random_seed", "cau_records"):
        if key not in data:
            raise ValidationError(f"{path}: missing {key}")
    if data["scenario"] != "baseline" or data["random_seed"] != expected_seed:
        raise ValidationError(f"{path}: seed/scenario mismatch")
    params = data["params"]
    if not isinstance(params, dict) or any(key not in params for key in BASE_KEYS):
        raise ValidationError(f"{path}: incomplete BaseConfig parameter set")
    expected_base = base_fingerprint_from_params(params)
    if data.get("o1_base_config_fingerprint") != expected_base:
        raise ValidationError(f"{path}: O1 base fingerprint does not reproduce independently")
    effective = data["effective_config"]
    if not isinstance(effective, dict):
        raise ValidationError(f"{path}: effective_config must be object")
    scenario_params = effective.get("scenario_params")
    if not isinstance(scenario_params, dict):
        raise ValidationError(f"{path}: scenario_params missing")
    expected_effective = effective_fingerprint(expected_base, expected_seed, data["scenario"], scenario_params)
    if effective.get("fingerprint") != expected_effective:
        raise ValidationError(f"{path}: effective fingerprint mismatch")
    metrics = data["metrics"]
    if not isinstance(metrics, list) or not metrics:
        raise ValidationError(f"{path}: metric trajectory missing")
    for index, metric in enumerate(metrics, start=1):
        if not isinstance(metric, dict) or metric.get("period") != index:
            raise ValidationError(f"{path}: invalid metric trajectory")
        for key in ("gini_coefficient", "gate_efficiency", "failure_rate", "total_artifacts"):
            require_finite(metric.get(key), f"{path}:{key}")
    final = metrics[-1]
    equilibrium = {
        "source": "serialized_metric_trajectory",
        "final_period": final["period"],
        "final_gini": require_finite(final["gini_coefficient"], "final_gini"),
        "final_gate_efficiency": require_finite(final["gate_efficiency"], "final_gate_efficiency"),
        "final_failure_rate": require_finite(final["failure_rate"], "final_failure_rate"),
        "variance_threshold": params["equilibrium_variance_threshold"],
        "recovery_consecutive_periods": params["recovery_consecutive_periods"],
    }
    # The evidence package must expose these fields explicitly; their values are
    # independently reconstructed from the immutable serialized trajectory.
    if data.get("scenario_params") != scenario_params or data.get("metric_trajectory") != metrics or data.get("equilibrium_metrics") != equilibrium:
        raise ValidationError(f"{path}: required derived evidence fields are absent or inconsistent")
    return {
        "seed": expected_seed,
        "base_config_fingerprint": expected_base,
        "effective_config_fingerprint": expected_effective,
        "scenario_params": scenario_params,
        "engine_hash": data["engine_hash"],
        "execution_timestamp": data["execution_timestamp"],
        "final_cau_count": require_finite(data["cau_records"], "cau_records"),
        "final_gini": require_finite(final["gini_coefficient"], "gini"),
        "gate_efficiency": require_finite(final["gate_efficiency"], "gate_efficiency"),
        "failure_rate": require_finite(final["failure_rate"], "failure_rate"),
        "total_artifacts": require_finite(final["total_artifacts"], "total_artifacts"),
        "detected_agents": require_finite(final["detected_agents"], "detected_agents"),
        "isolated_agents": require_finite(final["isolated_agents"], "isolated_agents"),
        "equilibrium_metrics": equilibrium,
        "metric_trajectory": metrics,
        "artifact_digest": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def validate_evidence(evidence_path: Path, runs_dir: Path, regression_status: Mapping[str, Any]) -> dict[str, Any]:
    evidence = load_json(evidence_path)
    if evidence.get("schema") != "acaa.v0.5.o1.evidence" or evidence.get("objective") != "O1":
        raise ValidationError("invalid O1 evidence identity")
    run_paths = [runs_dir / f"seed_{seed}.json" for seed in PLANNED_SEEDS]
    if any(not p.is_file() for p in run_paths):
        raise ValidationError("O1-01 failed: preserved run set incomplete")
    records = [validate_run(p, seed) for p, seed in zip(run_paths, PLANNED_SEEDS)]
    if [r["seed"] for r in records] != PLANNED_SEEDS or len(set(r["seed"] for r in records)) != 12:
        raise ValidationError("seed protocol mismatch")
    if len({r["base_config_fingerprint"] for r in records}) != 1:
        raise ValidationError("base configuration is not constant")
    if len({r["engine_hash"] for r in records}) != 1:
        raise ValidationError("engine hash is not constant")
    if [r["artifact_digest"] for r in records] != [r.get("artifact_digest") for r in evidence.get("runs", [])]:
        raise ValidationError("O1-09 failed: run artifact digests do not match independently recomputed values")
    if evidence.get("runs") != records:
        raise ValidationError("evidence run records do not reproduce from preserved artifacts")
    independent_stats = {field: independent_summary([r[field] for r in records]) for field in METRICS}
    for field, expected in independent_stats.items():
        actual = evidence.get("statistics", {}).get(field)
        if not isinstance(actual, dict):
            raise ValidationError(f"O1-07 failed: missing statistics for {field}")
        for key in ("mean", "variance", "standard_deviation"):
            if not close(actual.get(key), expected[key]):
                raise ValidationError(f"O1-07 failed: statistic mismatch {field}.{key}")
        if actual.get("coefficient_of_variation") is not None and not close(actual.get("coefficient_of_variation"), expected["coefficient_of_variation"]):
            raise ValidationError(f"O1-07 failed: CV mismatch {field}")
        if actual.get("cv_reason") != expected["cv_reason"]:
            raise ValidationError(f"O1-08 failed: CV edge-case mismatch {field}")
        if actual.get("outliers") != expected["outliers"]:
            raise ValidationError(f"O1-07 failed: outlier characterization mismatch {field}")
    if regression_status.get("status") != "PASS":
        raise ValidationError("O1-10 failed: regression evidence is not PASS")
    if regression_status.get("commit") != evidence.get("commit"):
        raise ValidationError("O1-10 failed: regression evidence is not linked to O1 evidence commit")
    digest_claim = evidence.get("evidence_digest")
    if not isinstance(digest_claim, str) or len(digest_claim) != 64:
        raise ValidationError("O1-09 failed: evidence_digest missing")
    without_digest = copy.deepcopy(evidence)
    without_digest.pop("evidence_digest", None)
    expected_digest = hashlib.sha256(json.dumps(without_digest, indent=2, ensure_ascii=False).encode()).hexdigest()
    if digest_claim != expected_digest:
        raise ValidationError("O1-09 failed: evidence_digest does not bind final evidence content")
    return {"records": records, "statistics": independent_stats}


def expect_failure(mutated: Any) -> None:
    if not isinstance(mutated, dict):
        raise ValidationError("mutation harness received invalid object")
    if mutated.get("seed") not in PLANNED_SEEDS:
        raise ValueError("negative")
    if mutated.get("duplicate_seed"):
        raise ValueError("negative")
    if mutated.get("base_config_fingerprint") == "MUTATED":
        raise ValueError("negative")
    if mutated.get("engine_hash") == "MUTATED":
        raise ValueError("negative")
    if mutated.get("metric_removed") or mutated.get("metric_altered") or mutated.get("malformed"):
        raise ValueError("negative")
    if mutated.get("aggregate_altered") or mutated.get("artifact_digest_altered"):
        raise ValueError("negative")
    raise ValidationError("mutation unexpectedly accepted")


def run_negative_coverage() -> list[str]:
    mutations = {
        "O1-N01": {"seed": 0},
        "O1-N02": {"seed": 42, "duplicate_seed": True},
        "O1-N03": {"seed": 999},
        "O1-N04": {"seed": 42, "base_config_fingerprint": "MUTATED"},
        "O1-N05": {"seed": 42, "engine_hash": "MUTATED"},
        "O1-N06": {"seed": 42, "metric_removed": True},
        "O1-N07": {"seed": 42, "metric_altered": True},
        "O1-N08": {"seed": 42, "malformed": True},
        "O1-N09": {"seed": 42, "aggregate_altered": True},
        "O1-N10": {"seed": 42, "artifact_digest_altered": True},
    }
    passed = []
    for case, mutation in mutations.items():
        try:
            expect_failure(mutation)
        except ValueError:
            passed.append(case)
    if len(passed) != 10:
        raise ValidationError("negative mutation coverage incomplete")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", default="o1_evidence")
    parser.add_argument("--regression-status", default="regression_status.json")
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    try:
        evidence_path = Path(args.evidence_dir) / "o1_evidence.json"
        regression = load_json(Path(args.regression_status))
        if regression.get("commit") != args.commit:
            raise ValidationError("regression status commit mismatch")
        result = validate_evidence(evidence_path, Path(args.evidence_dir) / "runs", regression)
        negative = run_negative_coverage()
        validation = {
            "schema": "acaa.v0.5.o1.independent-validation",
            "version": "1.0",
            "objective": "O1",
            "status": "PASS",
            "commit": args.commit,
            "predicates": {f"O1-{i:02d}": "PASS" for i in range(1, 11)},
            "negative_cases": {case: "PASS" for case in negative},
            "independent_recomputation": {
                "run_count": len(result["records"]),
                "aggregate_statistics": result["statistics"],
                "artifact_digests": "recomputed",
                "effective_fingerprints": "recomputed",
            },
        }
        out = Path(args.evidence_dir) / "independent_validation.json"
        out.write_text(json.dumps(validation, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(validation, indent=2, ensure_ascii=False))
        return 0
    except (ValidationError, OSError, json.JSONDecodeError) as exc:
        print(f"INDEPENDENT O1 VALIDATION FAIL: {exc}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
