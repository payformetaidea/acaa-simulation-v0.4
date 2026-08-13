"""Deterministic H-AICR G0 theoretical ABM generator.

This module generates IN_SILICO_THEORETICAL_EVIDENCE only. It consumes the
frozen model semantics and configuration and never uses human empirical data.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID, uuid5

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "execution" / "generation_configuration.json"
SCHEMA = ROOT / "execution" / "analytical_unit_schema.json"
CODEBOOK = ROOT / "execution" / "cohort_codebook.json"
NAMESPACE = UUID("8f6b1a1a-0c75-5c2f-9d41-6c0c5e2c6a01")
COHORTS = [
    "G1_Pure_Consumer", "G2_Low_Producer", "G3_High_Producer",
    "G4_Iterative_Researcher", "G5_Adversarial_Spam", "G6_Synthetic_AI",
    "G7_Human_Expert",
]
COST = {"G1_Pure_Consumer": 1.25, "G2_Low_Producer": .75,
        "G3_High_Producer": .45, "G4_Iterative_Researcher": .50,
        "G5_Adversarial_Spam": .90, "G6_Synthetic_AI": .40,
        "G7_Human_Expert": .35}


def q(e: float) -> float:
    return 1.0 - math.exp(-max(0.0, e))


def optimum(c: float, b: float = 1.0) -> float:
    return math.log(b / c) if 0.0 < c < b else 0.0


def canonical_unit_key(group: str, index: int) -> str:
    return f"G0|{group}|unit|{index:03d}"


def canonical_record_key(unit_key: str, interaction: int) -> str:
    return f"{unit_key}|interaction|{interaction:02d}"


def timestamp_for(unit_index: int, interaction: int) -> str:
    base = datetime(2030, 1, 1, tzinfo=timezone.utc)
    dt = base + timedelta(days=unit_index, minutes=interaction)
    return dt.isoformat().replace("+00:00", "Z")


def build_unit(group: str, index: int, rng: random.Random) -> dict:
    unit_key = canonical_unit_key(group, index)
    unit_uuid = str(uuid5(NAMESPACE, unit_key))
    e_star = optimum(COST[group])
    multipliers = [0.75, 0.90, 1.00, 1.10] if group == "G4_Iterative_Researcher" else None
    interactions = []

    # Four deterministic interactions provide a nested trajectory. RNG is
    # consumed through a private deterministic stream so future implementation
    # extensions cannot depend on global process randomness.
    rng.random()
    for j in range(4):
        effort = e_star * (multipliers[j] if multipliers else 1.0)
        contribution = 10.0 * q(effort)
        gaming = min(0.60, 0.15 + 0.05 * j) if group == "G5_Adversarial_Spam" else 0.0
        credit = min(10.0, 10.0 * (q(effort) + gaming))
        record_key = canonical_record_key(unit_key, j)
        interactions.append({
            "record_uuid": str(uuid5(NAMESPACE, record_key)),
            "window_id": f"{unit_uuid}:window:0",
            "timestamp": timestamp_for(index, j),
            "credit": credit,
            "contribution_score": contribution,
            "ground_truth_label": "Consumer" if group == "G1_Pure_Consumer" else "Producer",
            "input_text": f"{group} theoretical agent interaction {j}",
            "provenance": {
                "evidence_classification": "IN_SILICO_THEORETICAL_EVIDENCE",
                "generator_id": "ACAA-H-AICR-ABM-G0",
                "seed": 42,
                "model_revision": "deterministic_abm_v1",
            },
        })

    start = interactions[0]["timestamp"]
    end = interactions[-1]["timestamp"]
    return {
        "unit_uuid": unit_uuid,
        "unit_id": unit_key,
        "group": group,
        "window_start": start,
        "window_end": end,
        "interaction_records": interactions,
        "ground_truth_label": "Consumer" if group == "G1_Pure_Consumer" else "Producer",
        "contribution_score": sum(x["contribution_score"] for x in interactions) / len(interactions),
        "credit": sum(x["credit"] for x in interactions) / len(interactions),
        "provenance": {
            "evidence_classification": "IN_SILICO_THEORETICAL_EVIDENCE",
            "generator_id": "ACAA-H-AICR-ABM-G0",
            "seed": 42,
            "model_revision": "deterministic_abm_v1",
        },
    }


def generate(seed: int = 42) -> list[dict]:
    rng = random.Random(seed)
    units = []
    for group in COHORTS:
        for index in range(97):
            units.append(build_unit(group, index, rng))
    return units


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.seed != 42:
        raise SystemExit("Only the preregistered seed=42 is permitted for scientific generation")
    units = generate(args.seed)
    if len(units) != 679 or len({u["unit_uuid"] for u in units}) != 679:
        raise SystemExit("GENERATION_CARDINALITY_VIOLATION")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(units, ensure_ascii=False, sort_keys=True, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main()
