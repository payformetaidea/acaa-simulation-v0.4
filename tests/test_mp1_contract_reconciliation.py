#!/usr/bin/env python3
"""Contract-level regression tests for the M-P1/O2 reconciliation.

These tests define the contract only. They are intentionally independent from
historical M-P1 implementations and never use deduplication to repair invalid
input.
"""
import copy
import re
import unittest

O2_ID_RE = re.compile(r"^CAU-[0-9]{6}$")
LEGACY_MP1_V1_RE = re.compile(r"^CAU-[0-9A-F]{16}$")


DATA_INTEGRITY_FAIL = ("DATA_INTEGRITY_FAIL", None)


def artifact(records):
    return {"aggregate": {"cau_records": len(records)}, "records": records}


def classify_mp1_v11(data):
    """Reference classifier for the v1.1 draft; not a historical implementation.

    Validation is fail-closed. Record identity is validated before uniqueness
    is evaluated, and duplicate IDs are an integrity failure. No deduplication
    is permitted as a recovery mechanism.
    """
    if not isinstance(data, dict):
        return DATA_INTEGRITY_FAIL

    records = data.get("records")
    if not isinstance(records, list):
        return DATA_INTEGRITY_FAIL

    aggregate = data.get("aggregate", {}).get("cau_records")
    if not isinstance(aggregate, int) or isinstance(aggregate, bool):
        return DATA_INTEGRITY_FAIL
    if aggregate != len(records):
        return DATA_INTEGRITY_FAIL

    seen = set()
    for record in records:
        if not isinstance(record, dict):
            return DATA_INTEGRITY_FAIL
        cau_id = record.get("cau_id")
        if not isinstance(cau_id, str) or not O2_ID_RE.fullmatch(cau_id):
            return DATA_INTEGRITY_FAIL
        if cau_id in seen:
            return DATA_INTEGRITY_FAIL
        seen.add(cau_id)

    value = len(records)
    return ("VALID / ZERO_COUNT", 0) if value == 0 else ("VALID", value)


class MP1ContractReconciliationTests(unittest.TestCase):
    def test_canonical_o2_contract_uses_records_and_count(self):
        data = artifact([{"cau_id": "CAU-000001"}, {"cau_id": "CAU-000002"}])
        self.assertIsInstance(data["records"], list)
        self.assertIsInstance(data["aggregate"]["cau_records"], int)
        self.assertEqual(data["aggregate"]["cau_records"], len(data["records"]))
        self.assertFalse(isinstance(data.get("cau_records"), list))

    def test_o2_identifier_schema_is_six_digit(self):
        self.assertTrue(O2_ID_RE.fullmatch("CAU-000001"))
        self.assertTrue(O2_ID_RE.fullmatch("CAU-001936"))
        self.assertFalse(O2_ID_RE.fullmatch("CAU-ABCDEF1234567890"))

    def test_reported_artifact_shape_is_incompatible_with_legacy_mp1_v1_0_id_schema(self):
        ids = ["CAU-000001", "CAU-001936"]
        self.assertTrue(all(O2_ID_RE.fullmatch(x) for x in ids))
        self.assertFalse(any(LEGACY_MP1_V1_RE.fullmatch(x) for x in ids))

    def test_missing_records_fails_closed(self):
        data = artifact([{"cau_id": "CAU-000001"}])
        data.pop("records")
        self.assertEqual(classify_mp1_v11(data), DATA_INTEGRITY_FAIL)

    def test_empty_valid_records_is_zero_count(self):
        self.assertEqual(classify_mp1_v11(artifact([])), ("VALID / ZERO_COUNT", 0))

    def test_aggregate_count_mismatch_fails(self):
        data = artifact([{"cau_id": "CAU-000001"}])
        data["aggregate"]["cau_records"] = 0
        self.assertEqual(classify_mp1_v11(data), DATA_INTEGRITY_FAIL)

    def test_duplicate_identity_is_data_integrity_failure(self):
        data = artifact([{"cau_id": "CAU-000001"}, {"cau_id": "CAU-000001"}])
        self.assertEqual(classify_mp1_v11(data), DATA_INTEGRITY_FAIL)

    def test_duplicate_is_not_repaired_by_deduplication(self):
        data = artifact([{"cau_id": "CAU-000001"}, {"cau_id": "CAU-000001"}])
        status, value = classify_mp1_v11(data)
        self.assertEqual(status, "DATA_INTEGRITY_FAIL")
        self.assertIsNone(value)

    def test_invalid_identity_is_rejected_before_uniqueness(self):
        data = artifact([
            {"cau_id": "CAU-INVALID"},
            {"cau_id": "CAU-INVALID"},
        ])
        self.assertEqual(classify_mp1_v11(data), DATA_INTEGRITY_FAIL)

    def test_missing_field_is_not_silently_converted_to_empty_list(self):
        data = artifact([{"cau_id": "CAU-000001"}])
        broken = copy.deepcopy(data)
        broken.pop("records")
        self.assertNotEqual(classify_mp1_v11(broken)[0], "VALID / ZERO_COUNT")


if __name__ == "__main__":
    unittest.main()
