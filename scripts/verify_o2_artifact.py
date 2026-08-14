#!/usr/bin/env python3
"""Independent verification of the canonical retained O2 evidence artifact.

This verifier deliberately operates on raw artifact bytes before any metric
calculation. It performs no deduplication and treats duplicate CAU identities
as an integrity failure.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

O2_ID_RE = re.compile(r"^CAU-[0-9]{6}$")
EXPECTED_ARTIFACT_ID = "9147901382"
EXPECTED_RECORD_COUNT = 1936


def fail(message):
    print(f"DATA_INTEGRITY_FAIL: {message}")
    return 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--expected-record-count", type=int, default=EXPECTED_RECORD_COUNT)
    args = parser.parse_args()

    if args.artifact_id != EXPECTED_ARTIFACT_ID:
        return fail(f"unexpected artifact id: {args.artifact_id}")
    if not args.artifact.is_file():
        return fail(f"artifact not found: {args.artifact}")

    raw = args.artifact.read_bytes()
    actual_sha256 = hashlib.sha256(raw).hexdigest()
    if actual_sha256.lower() != args.expected_sha256.lower():
        return fail(
            f"SHA-256 mismatch: expected {args.expected_sha256}, got {actual_sha256}"
        )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")

    if not isinstance(data, dict):
        return fail("artifact root must be an object")

    records = data.get("records")
    if not isinstance(records, list):
        return fail("records must be an array")

    aggregate = data.get("aggregate")
    if not isinstance(aggregate, dict):
        return fail("aggregate must be an object")

    cau_records = aggregate.get("cau_records")
    if not isinstance(cau_records, int) or isinstance(cau_records, bool):
        return fail("aggregate.cau_records must be an integer")

    if cau_records != len(records):
        return fail(
            f"aggregate.cau_records={cau_records} != len(records)={len(records)}"
        )

    if len(records) != args.expected_record_count:
        return fail(
            f"record count mismatch: expected {args.expected_record_count}, got {len(records)}"
        )

    seen = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            return fail(f"record[{index}] must be an object")
        cau_id = record.get("cau_id")
        if not isinstance(cau_id, str) or not O2_ID_RE.fullmatch(cau_id):
            return fail(f"record[{index}] has invalid cau_id: {cau_id!r}")
        if cau_id in seen:
            return fail(f"duplicate cau_id at record[{index}]: {cau_id}")
        seen.add(cau_id)

    if len(seen) != EXPECTED_RECORD_COUNT:
        return fail(
            f"unique ID count mismatch: expected {EXPECTED_RECORD_COUNT}, got {len(seen)}"
        )

    print("REAL_ARTIFACT_VERIFICATION=PASS")
    print(f"ARTIFACT_ID={args.artifact_id}")
    print(f"SHA256={actual_sha256}")
    print(f"RECORDS={len(records)}")
    print(f"UNIQUE_IDS={len(seen)}")
    print("O2_SCHEMA=PASS")
    print(f"AGGREGATE_CAU_RECORDS={cau_records}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
