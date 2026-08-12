#!/usr/bin/env python3
"""Deterministic O2 pre-validation contract gate.

Full integrity assertions remain the responsibility of the independent
validator executed immediately after this gate.
"""
from o2_identity_v0_5 import build_evidence


def main():
    evidence = build_evidence(seed=42, periods=20)
    records = evidence["records"]
    assert evidence["aggregate"]["cau_records"] == len(records)
    assert len({r["cau_id"] for r in records}) == len(records)
    assert all(r["cau_id"].startswith("CAU-") and len(r["cau_id"]) == 10 for r in records)
    required = {"cau_id", "actor_id", "action", "verdict", "timestamp", "level", "provenance_linkage", "deterministic_record_representation"}
    assert all(required.issubset(r) for r in records)
    assert all(r["provenance_linkage"] for r in records)
    print(f"O2 pre-validation contract: PASS ({len(records)} identities)")

if __name__ == "__main__":
    main()
