#!/usr/bin/env python3
"""Fail-closed verifier for the canonical retained O2 evidence artifact.

The verifier is intentionally independent from the M-P1 implementation. It
checks the exact JSON bytes, artifact identity supplied by the gate, and the
canonical O2 structural/cardinality contract before any metric replay occurs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

CAU_ID_RE = re.compile(r"^CAU-[0-9]{6}$")


def fail(reason: str) -> int:
    print(f"DATA_INTEGRITY_FAIL: {reason}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--expected-record-count", required=True, type=int)
    args = parser.parse_args()

    if not args.path.is_file():
        return fail("artifact file does not exist")

    raw = args.path.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != args.expected_sha256.lower():
        return fail("exact JSON SHA-256 mismatch")

    try:
        data: Any = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return fail(f"malformed JSON: {exc}")

    if not isinstance(data, dict):
        return fail("artifact root is not an object")

    records = data.get("records")
    aggregate = data.get("aggregate")
    if not isinstance(records, list):
        return fail("records is missing or not an array")
    if not isinstance(aggregate, dict):
        return fail("aggregate is missing or not an object")

    cau_records = aggregate.get("cau_records")
    if isinstance(cau_records, bool) or not isinstance(cau_records, int):
        return fail("aggregate.cau_records is not an integer")
    if cau_records < 0:
        return fail("aggregate.cau_records is negative")
    if cau_records != len(records):
        return fail(
            f"aggregate.cau_records={cau_records} does not equal len(records)={len(records)}"
        )
    if len(records) != args.expected_record_count:
        return fail(
            f"record count {len(records)} does not equal expected {args.expected_record_count}"
        )

    valid_ids: set[str] = set()
    invalid_count = 0
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            return fail(f"record[{index}] is not an object")
        raw_id = record.get("cau_id")
        if not isinstance(raw_id, str) or not raw_id.strip():
            invalid_count += 1
            continue
        canonical = raw_id.strip().upper()
        if not CAU_ID_RE.fullmatch(canonical):
            invalid_count += 1
            continue
        valid_ids.add(canonical)

    # The canonical retained artifact must contain usable CAU identity data.
    # A structurally valid zero-record artifact is valid, but a non-empty
    # artifact with no valid CAU identifiers is not a measured zero.
    if records and not valid_ids:
        return fail("all CAU records are invalid or unusable")

    print(
        json.dumps(
            {
                "status": "VALID",
                "artifact_id": str(args.artifact_id),
                "sha256": actual_sha,
                "record_count": len(records),
                "valid_cau_ids": len(valid_ids),
                "invalid_record_count": invalid_count,
                "aggregate_cau_records": cau_records,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
