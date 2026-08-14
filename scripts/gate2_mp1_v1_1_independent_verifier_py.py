#!/usr/bin/env python3
"""Independent reference implementation for M-P1-v1.1 verification.

This verifier performs metric extraction only. It never rewrites CAU identifiers.
"""
import json
import re
import sys

PATTERN = re.compile(r"^CAU-[0-9]{6}$")


def extract(manifest):
    records = manifest.get("cau_records", [])
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
    manifest = json.load(sys.stdin)
    status, value = extract(manifest)
    print(json.dumps({"status": status, "m_p1": value}, sort_keys=True))


if __name__ == "__main__":
    main()
