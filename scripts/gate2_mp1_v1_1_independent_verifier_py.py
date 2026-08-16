#!/usr/bin/env python3
"""Independent reference implementation for M-P1-v1.1 verification.

The verifier consumes the canonical O2 artifact boundary directly. It preserves
M-P1's unique-cardinality semantics while failing closed on an unusable O2
record container or aggregate invariant. Canonicalization is limited to
trimming surrounding whitespace and uppercasing; no alternate identity source
or identifier rewriting is permitted.
"""
import json
import re
import sys

PATTERN = re.compile(r"^CAU-[0-9]{6}$")


def extract(artifact):
    if not isinstance(artifact, dict):
        return "DATA_INTEGRITY_FAIL", None

    if "records" not in artifact:
        return "DATA_INTEGRITY_FAIL", None
    records = artifact["records"]
    if not isinstance(records, list):
        return "DATA_INTEGRITY_FAIL", None

    if "aggregate" not in artifact or not isinstance(artifact["aggregate"], dict):
        return "DATA_INTEGRITY_FAIL", None
    aggregate = artifact["aggregate"]
    cau_records = aggregate.get("cau_records")
    if not isinstance(cau_records, int) or isinstance(cau_records, bool):
        return "DATA_INTEGRITY_FAIL", None
    if cau_records != len(records):
        return "DATA_INTEGRITY_FAIL", None

    valid = []
    invalid = 0
    for record in records:
        if not isinstance(record, dict):
            invalid += 1
            continue
        raw = record.get("cau_id")
        if not isinstance(raw, str) or not raw.strip():
            invalid += 1
            continue
        candidate = raw.strip().upper()
        if PATTERN.fullmatch(candidate):
            valid.append(candidate)
        else:
            invalid += 1

    if records and invalid == len(records):
        return "DATA_INTEGRITY_FAIL", None
    return "VALID", len(set(valid))


def main():
    try:
        artifact = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({"status": "DATA_INTEGRITY_FAIL", "m_p1": None}, sort_keys=True))
        return 1

    status, value = extract(artifact)
    print(json.dumps({"status": status, "m_p1": value}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
