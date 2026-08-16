#!/usr/bin/env python3
"""Cross-runtime contract tests for M-P1-v1.1.

Both independent implementations consume the same canonical O2 artifact
boundary: records[] plus aggregate.cau_records. The expected semantics are
trim+uppercase canonicalization, unique-cardinality measurement, valid zero,
and fail-closed structural validation.
"""
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY_IMPL = ROOT / "scripts/gate2_mp1_v1_1_independent_verifier_py.py"
JS_IMPL = ROOT / "scripts/gate2_mp1_v1_1_independent_verifier_js.js"


def artifact(records, aggregate=None):
    return {
        "records": records,
        "aggregate": {"cau_records": len(records)} if aggregate is None else aggregate,
    }


CASES = [
    ("valid_unique", artifact([{"cau_id": "CAU-000001"}, {"cau_id": "CAU-000002"}]), {"status": "VALID", "m_p1": 2}),
    ("duplicate_counts_once", artifact([{"cau_id": "CAU-000001"}, {"cau_id": "CAU-000001"}]), {"status": "VALID", "m_p1": 1}),
    ("canonicalization", artifact([{"cau_id": " cau-000001 "}, {"cau_id": "CAU-000002"}]), {"status": "VALID", "m_p1": 2}),
    ("mixed_valid_invalid", artifact([{"cau_id": "CAU-000001"}, {"cau_id": "BAD"}]), {"status": "VALID", "m_p1": 1}),
    ("zero_count", artifact([]), {"status": "VALID", "m_p1": 0}),
    ("all_invalid", artifact([{"cau_id": "BAD"}]), {"status": "DATA_INTEGRITY_FAIL", "m_p1": None}),
    ("missing_records", {"aggregate": {"cau_records": 0}}, {"status": "DATA_INTEGRITY_FAIL", "m_p1": None}),
    ("missing_aggregate", {"records": []}, {"status": "DATA_INTEGRITY_FAIL", "m_p1": None}),
    ("null_records", {"records": None, "aggregate": {"cau_records": 0}}, {"status": "DATA_INTEGRITY_FAIL", "m_p1": None}),
    ("aggregate_mismatch", artifact([{"cau_id": "CAU-000001"}], {"cau_records": 2}), {"status": "DATA_INTEGRITY_FAIL", "m_p1": None}),
]


def run_impl(command, payload):
    encoded = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
    result = subprocess.run(command, input=encoded, capture_output=True, check=False)
    return json.loads(result.stdout)


class MP1V11CrossRuntimeTests(unittest.TestCase):
    def test_python_and_javascript_agree(self):
        for name, payload, expected in CASES:
            with self.subTest(case=name):
                py = run_impl(["python3", str(PY_IMPL)], payload)
                js = run_impl(["node", str(JS_IMPL)], payload)
                self.assertEqual(py, expected)
                self.assertEqual(js, expected)
                self.assertEqual(py, js)

    def test_actual_o2_artifact_shape(self):
        payload = {
            "records": [
                {"cau_id": "CAU-000001"},
                {"cau_id": "CAU-000002"},
                {"cau_id": "CAU-000001"},
            ],
            "aggregate": {"cau_records": 3},
        }
        expected = {"status": "VALID", "m_p1": 2}
        self.assertEqual(run_impl(["python3", str(PY_IMPL)], payload), expected)
        self.assertEqual(run_impl(["node", str(JS_IMPL)], payload), expected)

    def test_malformed_json_fails_closed_in_both_runtimes(self):
        raw = b"{not-json"
        expected = {"status": "DATA_INTEGRITY_FAIL", "m_p1": None}
        self.assertEqual(run_impl(["python3", str(PY_IMPL)], raw), expected)
        self.assertEqual(run_impl(["node", str(JS_IMPL)], raw), expected)


if __name__ == "__main__":
    unittest.main()
