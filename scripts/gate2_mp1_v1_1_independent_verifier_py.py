#!/usr/bin/env python3
"""Independent reference implementation for M-P1-v1.1 verification.

The implementation follows the v1.1 draft boundary: canonicalization is
limited to trimming surrounding whitespace and uppercasing; valid duplicate
identifiers are counted once; missing or unusable CAU-record containers fail
closed. No identifier rewriting or alternate identity source is permitted.
"""
import json
import re
import sys

PATTERN = re.compile(r"^CAU-[0-9]{6}$")


def extract(manifest):
    if not isinstance(manifest, dict):
        return "DATA_INTEGRITY_FAIL", None

    if "cau_records" not in manifest:
        return "DATA_INTEGRITY_FAIL", None

    records = manifest["cau_records"]
    if not isinstance(records, list):
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
        manifest = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({"status": "DATA_INTEGRITY_FAIL", "m_p1": None}, sort_keys=True))
        return 1

    status, value = extract(manifest)
    print(json.dumps({"status": status, "m_p1": value}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
