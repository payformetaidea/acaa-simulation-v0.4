#!/usr/bin/env python3
"""S1-V evidence-bearing validation for the invariant registry contract."""
import glob
import hashlib
import importlib.metadata
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

BASE = Path(__file__).resolve().parent.parent
SCHEMA = BASE / "schemas" / "invariant-registry.schema.json"
VALID = BASE / "schema-conformance" / "valid" / "invariant-registry.valid.json"
INVALID = BASE / "schema-conformance" / "invalid"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def semantic_errors(data):
    errors = []
    ids = [inv.get("id") for inv in data.get("invariants", [])]
    duplicates = sorted({x for x in ids if ids.count(x) > 1})
    if duplicates:
        errors.append(("REG-C-001", f"duplicate IDs: {duplicates}"))

    cid = data.get("contract_id")
    cv = data.get("contract_version")
    for inv in data.get("invariants", []):
        intro = inv.get("introduced_in", {})
        if intro.get("contract_id") != cid:
            errors.append(("REG-C-002", f"{inv.get('id')}: contract_id mismatch"))
        if intro.get("contract_version") != cv:
            errors.append(("REG-C-002", f"{inv.get('id')}: contract_version mismatch"))

    for inv in data.get("invariants", []):
        status = inv.get("status")
        has_dep = "deprecation" in inv
        if status == "active" and has_dep:
            errors.append(("REG-C-003", f"{inv.get('id')}: active has deprecation"))
        if status == "deprecated" and not has_dep:
            errors.append(("REG-C-003", f"{inv.get('id')}: deprecated lacks deprecation"))
    return errors


def schema_check(validator, path):
    with path.open() as f:
        data = json.load(f)
    validator.validate(data)
    return data


def main():
    schema = json.loads(SCHEMA.read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    report = {
        "schema": str(SCHEMA),
        "python_version": sys.version.split()[0],
        "jsonschema_version": importlib.metadata.version("jsonschema"),
        "files": {},
        "schema_tests": [],
        "semantic_tests": [],
    }

    paths = [SCHEMA, VALID] + sorted(INVALID.glob("invariant-registry.*.json"))
    for p in paths:
        report["files"][str(p.relative_to(BASE.parent))] = sha256(p)

    valid = schema_check(validator, VALID)
    report["schema_tests"].append({"fixture": "valid", "expected": "PASS", "result": "PASS"})
    for p in sorted(INVALID.glob("invariant-registry.*.json")):
        with p.open() as f:
            data = json.load(f)
        name = p.name
        try:
            validator.validate(data)
            report["schema_tests"].append({"fixture": name, "expected": "FAIL", "result": "PASS"})
        except ValidationError as e:
            report["schema_tests"].append({"fixture": name, "expected": "FAIL", "result": "FAIL", "message": e.message})

    # Semantic tests are explicitly separated because duplicate IDs and cross-field
    # consistency are registry invariants, not JSON Schema constraints.
    for inv_name, data in [("valid", valid)]:
        errors = semantic_errors(data)
        report["semantic_tests"].append({"fixture": inv_name, "expected": "PASS", "result": "PASS" if not errors else "FAIL", "errors": errors})

    for filename, invariant in [
        ("invariant-registry.duplicate-id.json", "REG-C-001"),
        ("invariant-registry.cross-field-mismatch.json", "REG-C-002"),
        ("invariant-registry.active-deprecation.json", "REG-C-003"),
        ("invariant-registry.deprecated-no-deprecation.json", "REG-C-003"),
    ]:
        p = INVALID / filename
        data = json.loads(p.read_text())
        errors = semantic_errors(data)
        hit = any(code == invariant for code, _ in errors)
        report["semantic_tests"].append({"fixture": filename, "invariant": invariant, "expected": "FAIL", "result": "FAIL" if hit else "PASS", "errors": errors})

    failed = []
    for t in report["schema_tests"]:
        if (t["expected"] == "PASS" and t["result"] != "PASS") or (t["expected"] == "FAIL" and t["result"] != "FAIL"):
            failed.append(t)
    for t in report["semantic_tests"]:
        if (t["expected"] == "PASS" and t["result"] != "PASS") or (t["expected"] == "FAIL" and t["result"] != "FAIL"):
            failed.append(t)
    report["verdict"] = "PASS" if not failed else "FAIL"
    report["failed_tests"] = failed
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
