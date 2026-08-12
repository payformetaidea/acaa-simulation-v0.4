import json
import tempfile
from pathlib import Path

from o2_identity_v0_5 import build_evidence
from independent_o2_validator_v0_5 import validate, negative_cases


def test_o2_positive_contract():
    evidence = build_evidence(seed=42, periods=20)
    assert not validate(evidence)


def test_o2_negative_contracts():
    evidence = build_evidence(seed=42, periods=20)
    results = negative_cases(evidence)
    assert results
    assert all(results.values())


def test_identity_shape_and_count():
    evidence = build_evidence(seed=137, periods=10)
    records = evidence["records"]
    assert evidence["aggregate"]["cau_records"] == len(records)
    assert len({r["cau_id"] for r in records}) == len(records)
    assert all(r["cau_id"].startswith("CAU-") for r in records)
