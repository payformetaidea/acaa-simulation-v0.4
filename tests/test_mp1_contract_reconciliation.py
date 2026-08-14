#!/usr/bin/env python3
"""Contract-level regression tests for the M-P1/O2 reconciliation."""
import copy
import re
import unittest

O2_ID_RE = re.compile(r"^CAU-[0-9]{6}$")
LEGACY_MP1_V1_RE = re.compile(r"^CAU-[0-9A-F]{16}$")


def artifact(records):
    return {"aggregate": {"cau_records": len(records)}, "records": records}


def classify_mp1_v11(data):
    """Reference classifier for the v1.1 draft; not a historical implementation."""
    if not isinstance(data, dict):
        return "DATA_INTEGRITY_FAIL", None
    records = data.get("records")
    if not isinstance(records, list):
        return "DATA_INTEGRITY_FAIL", None
    aggregate = data.get("aggregate", {}).get("cau_records")
    if not isinstance(aggregate, int) or isinstance(aggregate, bool):
        return "DATA_INTEGRITY_FAIL", None
    if aggregate != len(records):
        return "DATA_INTEGRITY_FAIL", None
    ids = []
    for record in records:
        if not isinstance(record, dict):
            return "DATA_INTEGRITY_FAIL", None
        cau_id = record.get("cau_id")
        if not isinstance(cau_id, str) or not O2_ID_RE.fullmatch(cau_id):
            return "DATA_INTEGRITY_FAIL", None
        ids.append(cau_id)
    value = len(set(ids))
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
        self.assertEqual(classify_mp1_v11(data), ("DATA_INTEGRITY_FAIL", None))

    def test_empty_valid_records_is_zero_count(self):
        self.assertEqual(classify_mp1_v11(artifact([])), ("VALID / ZERO_COUNT", 0))

    def test_aggregate_count_mismatch_fails(self):
        data = artifact([{"cau_id": "CAU-000001"}])
        data["aggregate"]["cau_records"] = 0
        self.assertEqual(classify_mp1_v11(data), ("DATA_INTEGRITY_FAIL", None))

    def test_duplicate_identity_is_counted_once(self):
        data = artifact([{"cau_id": "CAU-000001"}, {"cau_id": "CAU-000001"}])
        self.assertEqual(classify_mp1_v11(data), ("VALID", 1))

    def test_missing_field_is_not_silently_converted_to_empty_list(self):
        data = artifact([{"cau_id": "CAU-000001"}])
        broken = copy.deepcopy(data)
        broken.pop("records")
        self.assertNotEqual(classify_mp1_v11(broken)[0], "VALID / ZERO_COUNT")


if __name__ == "__main__":
    unittest.main()
