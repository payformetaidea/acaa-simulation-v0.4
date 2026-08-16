#!/usr/bin/env python3
"""S1-V evidence-bearing validation for the invariant registry contract."""
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

# These fixtures are intentionally structurally valid. Their expected failure
# belongs to Layer 2, not JSON Schema Layer 1.
SEMANTIC_NEGATIVE_FIXTURES = {
    "invariant-registry.duplicate-id.json": "REG-C-001",
    "invariant-registry.cross-field-mismatch.json": "REG-C-002",
}


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
        "format_checker": "ENABLED",
        "semantic_negative_fixtures": SEMANTIC_NEGATIVE_FIXTURES,
        "files": {},
        "schema_tests": [],
        "semantic_tests": [],
    }

    paths = [SCHEMA, VALID] + sorted(INVALID.glob("invariant-registry.*.json"))
    for p in paths:
        report["files"][str(p.relative_to(BASE.parent))] = sha256(p)

    # Layer 1: valid fixture must pass structural validation.
    valid = schema_check(validator, VALID)
    report["schema_tests"].append({
        "fixture": "valid",
        "expected": "PASS",
        "result": "PASS",
    })

    # Layer 1: structurally invalid fixtures must fail schema validation.
    # Semantic-negative fixtures are excluded from this expectation because
    # they are deliberately valid under JSON Schema and are tested in Layer 2.
    for p in sorted(INVALID.glob("invariant-registry.*.json")):
        name = p.name
        with p.open() as f:
            data = json.load(f)

        if name in SEMANTIC_NEGATIVE_FIXTURES:
            try:
                validator.validate(data)
                report["schema_tests"].append({
                    "fixture": name,
                    "class": "semantic-negative",
                    "expected": "PASS",
                    "result": "PASS",
                    "message": "Structurally valid; semantic rejection belongs to Layer 2",
                })
            except ValidationError as e:
                report["schema_tests"].append({
                    "fixture": name,
                    "class": "semantic-negative",
                    "expected": "PASS",
                    "result": "FAIL",
                    "message": e.message,
                })
            continue

        try:
            validator.validate(data)
            report["schema_tests"].append({
                "fixture": name,
                "class": "structural-negative",
                "expected": "FAIL",
                "result": "PASS",
                "message": "Unexpectedly accepted by JSON Schema",
            })
        except ValidationError as e:
            report["schema_tests"].append({
                "fixture": name,
                "class": "structural-negative",
                "expected": "FAIL",
                "result": "FAIL",
                "message": e.message,
            })

    # Layer 2: valid fixture must satisfy all registry invariants.
    errors = semantic_errors(valid)
    report["semantic_tests"].append({
        "fixture": "valid",
        "expected": "PASS",
        "result": "PASS" if not errors else "FAIL",
        "errors": errors,
    })

    # Layer 2: semantic-negative fixtures must trigger their declared invariant.
    for filename, invariant in SEMANTIC_NEGATIVE_FIXTURES.items():
        p = INVALID / filename
        data = json.loads(p.read_text())
        errors = semantic_errors(data)
        hit = any(code == invariant for code, _ in errors)
        report["semantic_tests"].append({
            "fixture": filename,
            "invariant": invariant,
            "expected": "FAIL",
            "result": "FAIL" if hit else "PASS",
            "errors": errors,
        })

    # Lifecycle negatives are independently checked semantically as well,
    # even though their schema constraints already reject them structurally.
    for filename, invariant in [
        ("invariant-registry.active-deprecation.json", "REG-C-003"),
        ("invariant-registry.deprecated-no-deprecation.json", "REG-C-003"),
    ]:
        p = INVALID / filename
        data = json.loads(p.read_text())
        errors = semantic_errors(data)
        hit = any(code == invariant for code, _ in errors)
        report["semantic_tests"].append({
            "fixture": filename,
            "invariant": invariant,
            "expected": "FAIL",
            "result": "FAIL" if hit else "PASS",
            "errors": errors,
        })

    failed = []
    for t in report["schema_tests"] + report["semantic_tests"]:
        expected = t["expected"]
        result = t["result"]
        if (expected == "PASS" and result != "PASS") or (expected == "FAIL" and result != "FAIL"):
            failed.append(t)

    report["verdict"] = "PASS" if not failed else "FAIL"
    report["failed_tests"] = failed
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
