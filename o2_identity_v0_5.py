#!/usr/bin/env python3
"""O2 CAU identity evidence producer.

Loads the frozen v0.4 engine by file path and projects its existing ledger
into a machine-checkable identity evidence artifact. No v0.4 engine semantics
are modified here.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ENGINE_PATH = Path(__file__).with_name("value_flow_simulator_v0.4.py")
spec = importlib.util.spec_from_file_location("acaa_engine_v04", ENGINE_PATH)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
BaseConfig = engine.BaseConfig
ValueFlowSim = engine.ValueFlowSim

CONTRACT = "acaa.v0.5.o2.identity-contract@1.0"


def canonical_json(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def record_dict(cau):
    return {
        "cau_id": cau.cau_id,
        "actor_id": cau.actor_id,
        "action": cau.action.value,
        "verdict": cau.verdict.value,
        "timestamp": cau.ts,
        "level": cau.level.value,
        "provenance_linkage": [
            {"ts": e.ts, "actor": e.actor, "action": e.action, "detail": e.detail}
            for e in cau.chain
        ],
        "deterministic_record_representation": canonical_json({
            "cau_id": cau.cau_id,
            "actor_id": cau.actor_id,
            "action": cau.action.value,
            "verdict": cau.verdict.value,
            "timestamp": cau.ts,
            "level": cau.level.value,
        }),
    }


def build_evidence(seed=42, periods=None):
    sim = ValueFlowSim(BaseConfig(), seed, "baseline")
    sim.run(periods)
    records = [record_dict(c) for c in sim.ledger]
    records.sort(key=lambda r: r["cau_id"])
    record_hashes = [sha256_text(r["deterministic_record_representation"]) for r in records]
    evidence = {
        "schema": CONTRACT,
        "objective": "O2",
        "execution": {
            "seed": seed,
            "periods_executed": sim.period,
            "scenario": "baseline",
            "engine_hash": sim.export()["engine_hash"],
        },
        "aggregate": {"cau_records": len(records)},
        "records": records,
        "record_hashes": record_hashes,
    }
    evidence["evidence_digest"] = sha256_text(canonical_json(evidence))
    manifest = {
        "schema": CONTRACT,
        "artifact": "o2_identity_evidence.json",
        "record_count": len(records),
        "record_hashes_digest": sha256_text(canonical_json(record_hashes)),
        "evidence_digest": evidence["evidence_digest"],
    }
    evidence["manifest"] = manifest
    evidence["manifest_digest"] = sha256_text(canonical_json(manifest))
    return evidence


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--periods", type=int, default=100)
    p.add_argument("--output", default="o2_identity_evidence.json")
    args = p.parse_args()
    data = build_evidence(args.seed, args.periods)
    Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"O2 evidence generated: {args.output} ({data['aggregate']['cau_records']} records)")


if __name__ == "__main__":
    main()
