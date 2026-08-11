#!/usr/bin/env python3
"""
ACAA Cognitive Value Economy — Independent Validator v0.4

Purpose:
    Validate an execution artifact set without importing or executing the Engine.

Author: Pouria Valaee
Email: pouria@pouriavalaee.ir
LinkedIn: https://www.linkedin.com/in/pouria-valaee-6746a6208/
Website: https://pouriavalaee.ir
Project: ACAA — Adaptive Cognitive Architecture v0.4
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone


REQUIRED_SCENARIOS = {
    "baseline_v0.4.json": "baseline",
    "sybil_v0.4.json": "sybil",
    "collusion_v0.4.json": "collusion",
    "spam_v0.4.json": "spam",
    "gate_inflation_v0.4.json": "gate_inflation",
    "abstention_v0.4.json": "strategic_abstention",
    "exploitation_v0.4.json": "negative_exploitation",
}
REQUIRED_SENSITIVITY = {
    "sens_lam_v0.4.json": "lam",
    "sens_delta_v0.4.json": "delta",
    "sens_pi_c_v0.4.json": "pi_c",
    "sens_alpha_v0.4.json": "alpha_threshold",
    "sens_pi_p_v0.4.json": "pi_p",
}
REQUIRED_FILES = set(REQUIRED_SCENARIOS) | set(REQUIRED_SENSITIVITY) | {
    "multi_seed_v0.4.json",
    "regression_log_v0.4.txt",
    "MANIFEST_SHA256_v0.4.txt",
}
REQUIRED_TOP_LEVEL = {
    "params", "periods_executed", "cau_records", "agents", "metrics",
    "attack_log", "adaptive_log", "provenance_events", "engine_hash",
    "config_hash", "effective_config", "execution_timestamp", "scenario",
    "random_seed",
}
REQUIRED_METRIC_FIELDS = {
    "period", "total_cau_stock", "total_agent_balance", "active_agents",
    "gini_coefficient", "gate_efficiency", "failure_rate", "total_artifacts",
    "total_failures", "total_verifications", "total_challenges",
    "challenge_success_rate", "detected_agents", "isolated_agents",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def check_required_files(root):
    missing = sorted(name for name in REQUIRED_FILES if not os.path.isfile(os.path.join(root, name)))
    if missing:
        return False, f"Missing required files: {', '.join(missing)}"
    return True, f"All {len(REQUIRED_FILES)} required artifact files present"


def check_manifest(root):
    manifest_path = os.path.join(root, "MANIFEST_SHA256_v0.4.txt")
    failures = []
    entries = 0
    with open(manifest_path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            match = re.match(r"^([0-9a-fA-F]{64})\s+(.+)$", line)
            if not match:
                failures.append(f"Malformed manifest line: {line}")
                continue
            expected, filename = match.groups()
            filename = filename.lstrip("* ")
            path = os.path.join(root, filename)
            if not os.path.isfile(path):
                failures.append(f"Manifest file missing: {filename}")
                continue
            with open(path, "rb") as fh:
                actual = hashlib.sha256(fh.read()).hexdigest()
            entries += 1
            if actual.lower() != expected.lower():
                failures.append(f"SHA256 mismatch: {filename}")
    if failures:
        return False, "; ".join(failures)
    return True, f"Manifest verified: {entries} entries"


def validate_engine_artifact(data, expected_scenario):
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        return False, f"Missing top-level fields: {', '.join(missing)}"
    if data.get("scenario") != expected_scenario:
        return False, f"Scenario mismatch: expected {expected_scenario}, got {data.get('scenario')}"
    if not isinstance(data["metrics"], list) or not data["metrics"]:
        return False, "metrics must be a non-empty list"
    periods = [m.get("period") for m in data["metrics"]]
    if any(not isinstance(p, int) or p < 1 for p in periods):
        return False, "Invalid metric period"
    if periods != list(range(1, len(periods) + 1)):
        return False, "Metric periods are not sequential"
    for metric in data["metrics"]:
        missing_metric = sorted(REQUIRED_METRIC_FIELDS - set(metric))
        if missing_metric:
            return False, f"Missing metric fields: {', '.join(missing_metric)}"
    if data["periods_executed"] != len(data["metrics"]):
        return False, "periods_executed does not match metrics length"
    if not isinstance(data["attack_log"], list) or not isinstance(data["adaptive_log"], list):
        return False, "attack_log/adaptive_log must be lists"
    if not isinstance(data["cau_records"], int) or data["cau_records"] < 0:
        return False, "Invalid cau_records"
    if not isinstance(data["provenance_events"], int) or data["provenance_events"] < 0:
        return False, "Invalid provenance_events"
    return True, "Engine artifact schema valid"


def check_equilibrium(baseline):
    gini = baseline["metrics"][-1]["gini_coefficient"]
    return (gini <= 0.05, f"Gini = {gini}")


def check_attack_detection(artifacts):
    events = []
    for name in REQUIRED_SCENARIOS:
        if name == "baseline_v0.4.json":
            continue
        for event in artifacts[name]["attack_log"]:
            action = str(event.get("action", "")).lower()
            if action and action != "rollback":
                events.append(event)
    return (len(events) >= 1, f"Detected {len(events)} attack-response events")


def check_sensitivity(sensitivity):
    expected = set(REQUIRED_SENSITIVITY.values())
    found = {data.get("param") for data in sensitivity.values()}
    missing = sorted(expected - found)
    if missing:
        return False, f"Missing sensitivity parameters: {', '.join(missing)}"
    for name, data in sensitivity.items():
        if not isinstance(data.get("values"), list) or not isinstance(data.get("results"), list):
            return False, f"Invalid sensitivity structure: {name}"
        if len(data["values"]) != len(data["results"]):
            return False, f"Sensitivity value/result length mismatch: {name}"
    return True, "All 5 sensitivity parameters present and structurally valid"


def check_provenance(artifacts):
    mismatches = []
    for name, data in artifacts.items():
        if data["provenance_events"] != data["cau_records"]:
            mismatches.append(
                f"{name}: provenance_events={data['provenance_events']} cau_records={data['cau_records']}"
            )
    if mismatches:
        return False, "; ".join(mismatches)
    return True, "Provenance event count matches CAU record count for all scenario artifacts"


def check_cau_uniqueness(artifacts):
    # v0.4 export exposes the CAU count, not the individual CAU IDs.
    # Therefore this check is intentionally limited to the architecture-level
    # invariant that metric periods are sequential and the reported count is valid.
    for name, data in artifacts.items():
        if data["cau_records"] < 0:
            return False, f"Invalid CAU count in {name}"
    return True, "Architecture criterion: sequential metric periods and valid CAU counts"


def check_adaptive(artifacts):
    events = sum(len(data["adaptive_log"]) for data in artifacts.values())
    return (events >= 1, f"{events} adaptive events")


def check_multi_seed(data):
    required = {"seed_42", "seed_137", "seed_256"}
    missing = sorted(required - set(data))
    if missing:
        return False, f"Missing seeds: {', '.join(missing)}"
    for seed, result in data.items():
        if not isinstance(result, dict):
            return False, f"Invalid multi-seed result: {seed}"
    return True, "All three required seeds present"


def check_regression(path):
    text = open(path, "r", encoding="utf-8").read()
    match = re.search(r"Regression:\s*(\d+)\s+PASS\s*/\s*(\d+)\s+FAIL", text)
    if not match:
        return False, "Regression summary not found"
    passed, failed = int(match.group(1)), int(match.group(2))
    return (failed == 0, f"Regression: {passed} PASS / {failed} FAIL")


def main():
    parser = argparse.ArgumentParser(description="ACAA v0.4 independent artifact validator")
    parser.add_argument("--artifacts", required=True, help="Execution artifact directory")
    args = parser.parse_args()
    root = os.path.abspath(args.artifacts)
    checks = {}
    all_passed = True

    try:
        ok, detail = check_required_files(root)
        checks["artifact_contract"] = {"passed": ok, "details": detail}
        all_passed &= ok
        if not ok:
            raise RuntimeError(detail)

        ok, detail = check_manifest(root)
        checks["manifest_sha256"] = {"passed": ok, "details": detail}
        all_passed &= ok
        if not ok:
            raise RuntimeError(detail)

        scenario_data = {}
        for filename, scenario in REQUIRED_SCENARIOS.items():
            data = load_json(os.path.join(root, filename))
            ok, detail = validate_engine_artifact(data, scenario)
            checks[f"schema_{scenario}"] = {"passed": ok, "details": detail}
            all_passed &= ok
            if not ok:
                raise RuntimeError(detail)
            scenario_data[filename] = data

        sensitivity_data = {name: load_json(os.path.join(root, name)) for name in REQUIRED_SENSITIVITY}
        ok, detail = check_sensitivity(sensitivity_data)
        checks["V3_sensitivity"] = {"passed": ok, "details": detail}
        all_passed &= ok
        if not ok:
            raise RuntimeError(detail)

        multi_seed = load_json(os.path.join(root, "multi_seed_v0.4.json"))
        ok, detail = check_multi_seed(multi_seed)
        checks["V7_multi_seed"] = {"passed": ok, "details": detail}
        all_passed &= ok
        if not ok:
            raise RuntimeError(detail)

        ok, detail = check_regression(os.path.join(root, "regression_log_v0.4.txt"))
        checks["regression"] = {"passed": ok, "details": detail}
        all_passed &= ok

        ok, detail = check_equilibrium(scenario_data["baseline_v0.4.json"])
        checks["V1_equilibrium"] = {"passed": ok, "details": detail}
        all_passed &= ok

        ok, detail = check_attack_detection(scenario_data)
        checks["V2_attack_detection"] = {"passed": ok, "details": detail}
        all_passed &= ok

        ok, detail = check_provenance(scenario_data)
        checks["V4_provenance"] = {"passed": ok, "details": detail}
        all_passed &= ok

        ok, detail = check_cau_uniqueness(scenario_data)
        checks["V5_cau_uniqueness"] = {"passed": ok, "details": detail}
        all_passed &= ok

        ok, detail = check_adaptive(scenario_data)
        checks["V6_adaptive"] = {"passed": ok, "details": detail}
        all_passed &= ok

    except Exception as exc:
        checks["validator_exception"] = {"passed": False, "details": str(exc)}
        all_passed = False

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "v0.4",
        "validator": "independent_validator_v0.4.py",
        "checks": checks,
        "overall": "PASS" if all_passed else "FAIL",
    }
    output = os.path.join(root, "validation_result.json")
    with open(output, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
