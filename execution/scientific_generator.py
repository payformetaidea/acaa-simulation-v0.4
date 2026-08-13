"""Deterministic in-silico H-AICR G0 generator."""
from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID, uuid5

EXEC = Path(__file__).resolve().parent
GENERATOR_ID = "ACAA-H-AICR-ABM-G0"
MODEL_REVISION = "deterministic_abm_v1"
EVIDENCE = "IN_SILICO_THEORETICAL_EVIDENCE"
NAMESPACE = UUID("8f6b1a1a-0c75-5c2f-9d41-6c0c5e2c6a01")
COHORTS = [
    "G1_Pure_Consumer", "G2_Low_Producer", "G3_High_Producer",
    "G4_Iterative_Researcher", "G5_Adversarial_Spam",
    "G6_Synthetic_AI", "G7_Human_Expert",
]
BASE = datetime(2030, 1, 1, tzinfo=timezone.utc)


def load(name: str):
    return json.loads((EXEC / name).read_text(encoding="utf-8"))


def q(e: float) -> float:
    return 1.0 - math.exp(-max(0.0, e))


def e_star(cost: float) -> float:
    return math.log(1.0 / cost) if cost < 1.0 else 0.0


def prov(group: str) -> dict:
    return {
        "evidence_classification": EVIDENCE,
        "generator_id": GENERATOR_ID,
        "seed": 42,
        "model_revision": MODEL_REVISION,
        "agent_type": "synthetic_ai" if group == "G6_Synthetic_AI" else (
            "expert_proxy" if group == "G7_Human_Expert" else "theoretical_agent"
        ),
        "expertise_proxy": group == "G7_Human_Expert",
    }


def make_unit(group: str, cohort_index: int, index: int, spec: dict) -> dict:
    params = spec["parameters"]
    cost = float(params["effort_cost_c"])
    key = f"G0|{group}|unit|{index:03d}"
    uid = str(uuid5(NAMESPACE, key))
    base = e_star(cost)
    multipliers = params.get("trajectory_multipliers", [1.0])
    rows = []

    for j in range(4):
        multiplier = float(multipliers[j]) if group == "G4_Iterative_Researcher" else 1.0
        effort = base * multiplier
        contribution = 10 * q(effort)
        if group == "G5_Adversarial_Spam":
            gaming = min(0.60, 0.15 + 0.05 * (j + 1))
        else:
            gaming = 0.0
        credit = min(10.0, 10 * (q(effort) + gaming))
        ts = (BASE + timedelta(days=cohort_index * 200 + index, minutes=j))
        timestamp = ts.isoformat().replace("+00:00", "Z")
        label = "Consumer" if group == "G1_Pure_Consumer" else (
            "Producer" if group != "G5_Adversarial_Spam" or contribution >= 4 else "Consumer"
        )
        rows.append({
            "record_uuid": str(uuid5(NAMESPACE, f"{key}|interaction|{j:02d}")),
            "window_id": f"{uid}:window:0",
            "timestamp": timestamp,
            "credit": round(credit, 8),
            "contribution_score": round(contribution, 8),
            "ground_truth_label": label,
            "input_text": f"{group} theoretical agent interaction {j}",
            "provenance": prov(group),
        })

    return {
        "unit_uuid": uid,
        "unit_id": key,
        "group": group,
        "window_start": rows[0]["timestamp"],
        "window_end": rows[-1]["timestamp"],
        "interaction_records": rows,
        "ground_truth_label": "Consumer" if group == "G1_Pure_Consumer" else "Producer",
        "contribution_score": round(sum(x["contribution_score"] for x in rows) / 4, 8),
        "credit": round(sum(x["credit"] for x in rows) / 4, 8),
        "provenance": prov(group),
    }


def generate() -> list[dict]:
    config = load("generation_configuration.json")
    codebook = load("cohort_codebook.json")
    if (
        config["seed"] != 42
        or config["uuid_version"] != "UUID5"
        or config["model_revision"] != MODEL_REVISION
    ):
        raise RuntimeError("REGISTERED_CONFIGURATION_MISMATCH")
    if (
        config["total_independent_units"] != 679
        or config["units_per_cohort"] != 97
        or not codebook.get("scientific_generation_authorized")
    ):
        raise RuntimeError("GENERATION_GATE_CLOSED")

    data = []
    for cohort_index, group in enumerate(COHORTS):
        cohort = codebook["groups"].get(group)
        if cohort is None or cohort["n"] != 97:
            raise RuntimeError("COHORT_COUNT_MISMATCH")
        for index in range(1, 98):
            data.append(make_unit(group, cohort_index, index, cohort))

    if len(data) != 679 or len({x["unit_uuid"] for x in data}) != 679:
        raise RuntimeError("CARDINALITY_OR_IDENTITY_FAILURE")
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.seed != 42:
        raise SystemExit("ONLY_PREREGISTERED_SEED_42_IS_PERMITTED")
    data = generate()
    Path(args.output).write_text(
        json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
    print(json.dumps({"status": "GENERATED", "units": len(data)}, sort_keys=True))


if __name__ == "__main__":
    main()
