#!/usr/bin/env python3
"""Dependency-free O2 contract gate with explicit diagnostics."""
from o2_identity_v0_5 import build_evidence
from independent_o2_validator_v0_5 import validate, negative_cases


def main():
    evidence = build_evidence(seed=42, periods=20)
    failures = validate(evidence)
    negatives = negative_cases(evidence)
    print("O2 positive failures:", failures)
    print("O2 negative results:", negatives)
    if failures:
        raise SystemExit("O2 positive contract failed")
    if not negatives or not all(negatives.values()):
        raise SystemExit("O2 negative contract failed")
    evidence2 = build_evidence(seed=137, periods=10)
    records = evidence2["records"]
    assert evidence2["aggregate"]["cau_records"] == len(records)
    assert len({r["cau_id"] for r in records}) == len(records)
    assert all(r["cau_id"].startswith("CAU-") for r in records)
    print("O2 contract: PASS")

if __name__ == "__main__":
    main()
