#!/usr/bin/env python3
"""Evidence probe for F2.4 format-contract reconciliation."""
import hashlib
import importlib.metadata
import json
import platform
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "infrastructure/schemas/invariant-registry.schema.json"
FIXTURE = ROOT / "infrastructure/schema-conformance/invalid/invariant-registry.invalid-date-time.json"
VALIDATOR = ROOT / "infrastructure/schema-conformance/validate_s1.py"
FORMAT_ASSERTION_VOCAB = "https://json-schema.org/draft/2020-12/vocab/format-assertion"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_formats(node, path="$", out=None):
    if out is None:
        out = []
    if isinstance(node, dict):
        if "format" in node:
            out.append({"path": path + ".format", "value": node["format"]})
        for key, value in node.items():
            find_formats(value, f"{path}.{key}", out)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            find_formats(value, f"{path}[{i}]", out)
    return out


def validate_with(schema, data, checker):
    validator = Draft202012Validator(schema, format_checker=checker)
    errors = list(validator.iter_errors(data))
    return {"errors": len(errors), "messages": [e.message for e in errors], "result": "FAIL" if errors else "PASS"}


def primitive_check(checker, value):
    try:
        checker.check("date-time", value)
        return {"result": "PASS", "exception": None}
    except Exception as exc:
        return {"result": "FAIL", "exception": type(exc).__name__ + ": " + str(exc)}


def main():
    schema = json.loads(SCHEMA.read_text())
    fixture = json.loads(FIXTURE.read_text())
    checker = FormatChecker()
    draft_checker = Draft202012Validator.FORMAT_CHECKER

    explicit_assertion_schema = dict(schema)
    vocab = dict(explicit_assertion_schema.get("$vocabulary", {}))
    vocab[FORMAT_ASSERTION_VOCAB] = True
    explicit_assertion_schema["$vocabulary"] = vocab

    report = {
        "protocol": "F2.4",
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "jsonschema_version": importlib.metadata.version("jsonschema"),
        "jsonschema_module": __import__("jsonschema").__file__,
        "format_module": __import__("jsonschema._format", fromlist=["_"]).__file__,
        "files": {
            "schema_sha256": sha256(SCHEMA),
            "fixture_sha256": sha256(FIXTURE),
            "validator_sha256": sha256(VALIDATOR),
        },
        "schema": {
            "$schema": schema.get("$schema"),
            "$vocabulary": schema.get("$vocabulary"),
            "format_assertion_declared": schema.get("$vocabulary", {}).get(FORMAT_ASSERTION_VOCAB),
            "formats": find_formats(schema),
        },
        "validator_contract": {
            "construction": "Draft202012Validator(schema, format_checker=FormatChecker())",
            "source_sha256": sha256(VALIDATOR),
        },
        "runtime_checker": {
            "generic_has_date_time": "date-time" in checker.checkers,
            "draft_has_date_time": "date-time" in draft_checker.checkers,
            "generic_keys": sorted(checker.checkers.keys()),
            "draft_keys": sorted(draft_checker.checkers.keys()),
        },
        "tests": {
            "primitive_generic": primitive_check(checker, fixture["metadata"]["created_at"]),
            "primitive_draft": primitive_check(draft_checker, fixture["metadata"]["created_at"]),
            "actual_schema_generic_checker": validate_with(schema, fixture, checker),
            "actual_schema_draft_checker": validate_with(schema, fixture, draft_checker),
            "explicit_format_assertion_schema_generic_checker": validate_with(explicit_assertion_schema, fixture, checker),
            "explicit_format_assertion_schema_draft_checker": validate_with(explicit_assertion_schema, fixture, draft_checker),
        },
    }

    if schema.get("$vocabulary", {}).get(FORMAT_ASSERTION_VOCAB) is True:
        classification = "FORMAT_ASSERTION_EXPLICIT_IN_SCHEMA"
    else:
        classification = "FORMAT_IS_NOT_NORMATIVE_ASSERTION_IN_FROZEN_SCHEMA"
        if report["tests"]["actual_schema_generic_checker"]["result"] == "PASS":
            classification += "+RUNTIME_ACCEPTANCE_CONSISTENT_WITH_ANNOTATION_SEMANTICS"
        else:
            classification += "+IMPLEMENTATION_LEVEL_FORMAT_ENFORCEMENT_PRESENT"

    report["classification"] = classification
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
