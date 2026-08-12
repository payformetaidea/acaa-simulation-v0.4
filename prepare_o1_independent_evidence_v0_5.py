#!/usr/bin/env python3
"""Prepare O1 evidence for independent validation without importing the runner/engine."""
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path

SEEDS = [42, 137, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--evidence-dir", default="o1_evidence")
    p.add_argument("--commit", required=True)
    args = p.parse_args()
    root = Path(args.evidence_dir)
    evidence_path = root / "o1_evidence.json"
    evidence = load(evidence_path)
    records = []
    for seed in SEEDS:
        path = root / "runs" / f"seed_{seed}.json"
        data = load(path)
        metrics = data["metrics"]
        final = metrics[-1]
        scenario_params = copy.deepcopy(data["effective_config"].get("scenario_params", {}))
        equilibrium = {
            "source": "serialized_metric_trajectory",
            "final_period": final["period"],
            "final_gini": final["gini_coefficient"],
            "final_gate_efficiency": final["gate_efficiency"],
            "final_failure_rate": final["failure_rate"],
            "variance_threshold": data["params"]["equilibrium_variance_threshold"],
            "recovery_consecutive_periods": data["params"]["recovery_consecutive_periods"],
        }
        data["scenario_params"] = scenario_params
        data["metric_trajectory"] = metrics
        data["equilibrium_metrics"] = equilibrium
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        records.append({
            "seed": seed,
            "path": f"runs/seed_{seed}.json",
            "base_config_fingerprint": data["o1_base_config_fingerprint"],
            "effective_config_fingerprint": data["effective_config"].get("fingerprint"),
            "scenario_params": scenario_params,
            "engine_hash": data["engine_hash"],
            "execution_timestamp": data["execution_timestamp"],
            "final_cau_count": data["cau_records"],
            "final_gini": final["gini_coefficient"],
            "gate_efficiency": final["gate_efficiency"],
            "failure_rate": final["failure_rate"],
            "total_artifacts": final["total_artifacts"],
            "detected_agents": final["detected_agents"],
            "isolated_agents": final["isolated_agents"],
            "equilibrium_metrics": equilibrium,
            "metric_trajectory": metrics,
            "artifact_digest": digest(path),
        })
    evidence["commit"] = args.commit
    evidence["runs"] = records
    evidence["validation"] = {f"O1-{i:02d}": "PENDING_INDEPENDENT_VALIDATION" for i in range(1, 11)}
    evidence.pop("evidence_digest", None)
    evidence_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
    evidence["evidence_digest"] = digest(evidence_path)
    evidence_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
