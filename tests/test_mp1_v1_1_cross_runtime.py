#!/usr/bin/env python3
"""Cross-runtime contract tests for M-P1-v1.1.

The Python and JavaScript implementations are treated as independent
consumers of the same serialized manifest bytes. The expected semantics come
from the v1.1 candidate specification: trim+uppercase canonicalization,
unique-cardinality measurement, valid zero, and fail-closed missing/unusable
record containers.
"""
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY_IMPL = ROOT / "scripts/gate2_mp1_v1_1_independent_verifier_py.py"
JS_IMPL = ROOT / "scripts/gate2_mp1_v1_1_independent_verifier_js.js"


CASES = [
    (
        "valid_unique",
        {"cau_records": [{"cau_id": "CAU-000001"}, {"cau_id": "CAU-000002"}]},
        {"status": "VALID", "m_p1": 2},
    ),
    (
        "duplicate_counts_once",
        {"cau_records": [{"cau_id": "CAU-000001"}, {"cau_id": "CAU-000001"}]},
        {"status": "VALID", "m_p1": 1},
    ),
    (
        "canonicalization",
        {"cau_records": [{"cau_id": " cau-000001 "}, {"cau_id": "CAU-000002"}]},
        {"status": "VALID", "m_p1": 2},
    ),
    (
        "mixed_valid_invalid",
        {"cau_records": [{"cau_id": "CAU-000001"}, {"cau_id": "BAD"}]},
        {"status": "VALID", "m_p1": 1},
    ),
    (
        "zero_count",
        {"cau_records": []},
        {"status": "VALID", "m_p1": 0},
    ),
    (
        "all_invalid",
        {"cau_records": [{"cau_id": "BAD"}]},
        {"status": "DATA_INTEGRITY_FAIL", "m_p1": None},
    ),
    (
        "missing_container",
        {},
        {"status": "DATA_INTEGRITY_FAIL", "m_p1": None},
    ),
    (
        "null_container",
        {"cau_records": None},
        {"status": "DATA_INTEGRITY_FAIL", "m_p1": None},
    ),
    (
        "malformed_json",
        None,
        {"status": "DATA_INTEGRITY_FAIL", "m_p1": None},
    ),
]


def run_python(payload):
    encoded = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
    result = subprocess.run(
        ["python3", str(PY_IMPL)], input=encoded, capture_output=True, check=False
    )
    return json.loads(result.stdout)


def run_node(payload):
    encoded = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
    result = subprocess.run(
        ["node", str(JS_IMPL)], input=encoded, capture_output=True, check=False
    )
    return json.loads(result.stdout)


class MP1V11CrossRuntimeTests(unittest.TestCase):
    def test_python_and_javascript_agree(self):
        for name, payload, expected in CASES:
            with self.subTest(case=name):
                py = run_python(payload if payload is not None else b"{")
                js = run_node(payload if payload is not None else b"{")
                self.assertEqual(py, expected)
                self.assertEqual(js, expected)
                self.assertEqual(py, js)

    def test_malformed_json_fails_closed_in_both_runtimes(self):
        raw = b"{not-json"
        py = run_python(raw)
        js = run_node(raw)
        expected = {"status": "DATA_INTEGRITY_FAIL", "m_p1": None}
        self.assertEqual(py, expected)
        self.assertEqual(js, expected)
        self.assertEqual(py, js)


if __name__ == "__main__":
    unittest.main()
