#!/usr/bin/env python3
"""F2.2 Runtime Provenance Protocol for jsonschema format checking.

This probe is investigation-only. It MUST NOT modify the S1 validator baseline.
It records distribution provenance, imported module provenance, checker identity,
checker registration, direct primitive behavior, minimal-schema behavior, actual
schema behavior, and a comparison against the baseline validator's wiring.
"""
import hashlib
import importlib.metadata
import inspect
import json
import platform
import sys
from pathlib import Path

import jsonschema
from jsonschema import Draft202012Validator, FormatChecker, FormatError

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "infrastructure" / "schemas" / "invariant-registry.schema.json"
FIXTURE_PATH = ROOT / "infrastructure" / "schema-conformance" / "invalid" / "invariant-registry.invalid-date-time.json"
BASELINE_VALIDATOR = ROOT / "infrastructure" / "schema-conformance" / "validate_s1.py"


def emit(key, value):
    print(f"{key}={json.dumps(value, sort_keys=True, default=str)}")


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def checker_info(checker):
    keys = sorted(checker.checkers.keys())
    entry = checker.checkers.get("date-time")
    callable_info = None
    if entry is not None:
        fn = entry[0] if isinstance(entry, tuple) else entry
        callable_info = {
            "repr": repr(fn),
            "module": getattr(fn, "__module__", None),
            "qualname": getattr(fn, "__qualname__", None),
            "source_file": inspect.getsourcefile(fn),
        }
    return {"date_time_registered": "date-time" in keys, "keys": keys, "date_time_callable": callable_info}


def primitive(checker):
    try:
        checker.check("not-a-date", "date-time")
        return {"result": "PASS", "exception": None}
    except FormatError as exc:
        return {"result": "FAIL", "exception": type(exc).__name__, "message": str(exc)}


def validate(validator, instance):
    errors = list(validator.iter_errors(instance))
    return {
        "error_count": len(errors),
        "result": "FAIL" if errors else "PASS",
        "first_error": None if not errors else {
            "validator": errors[0].validator,
            "path": list(errors[0].absolute_path),
            "schema_path": list(errors[0].absolute_schema_path),
            "message": errors[0].message,
            "type": type(errors[0]).__name__,
        },
    }


def main():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    generic = FormatChecker()
    draft = Draft202012Validator.FORMAT_CHECKER

    metadata = importlib.metadata.distribution("jsonschema")
    files = metadata.files or []
    dist_file_hashes = {}
    for rel in files:
        candidate = Path(metadata.locate_file(rel))
        if candidate.is_file() and candidate.suffix == ".py":
            dist_file_hashes[str(rel)] = sha256(candidate)

    emit("protocol", "F2.2-runtime-provenance-v1")
    emit("python_version", platform.python_version())
    emit("python_executable", sys.executable)
    emit("python_implementation", platform.python_implementation())
    emit("jsonschema_version_imported", jsonschema.__version__)
    emit("jsonschema_version_distribution", metadata.version)
    emit("jsonschema_distribution_location", str(metadata.locate_file("")))
    emit("jsonschema_module_file", jsonschema.__file__)
    emit("jsonschema_format_module_file", __import__("jsonschema._format", fromlist=["*"]).__file__)
    emit("jsonschema_distribution_sha256s", dist_file_hashes)
    emit("schema_sha256", sha256(SCHEMA_PATH))
    emit("fixture_sha256", sha256(FIXTURE_PATH))
    emit("baseline_validator_sha256", sha256(BASELINE_VALIDATOR))
    emit("baseline_validator_expected_sha256", "5ba942980b63ed8f53dfd8f16e40e0f69349e98c")
    emit("baseline_validator_sha_match", sha256(BASELINE_VALIDATOR) == "5ba942980b63ed8f53dfd8f16e40e0f69349e98c")

    emit("formatchecker_generic", checker_info(generic))
    emit("formatchecker_draft202012", checker_info(draft))
    emit("primitive_generic", primitive(generic))
    emit("primitive_draft202012", primitive(draft))

    minimal = {
        "type": "object",
        "properties": {"created_at": {"type": "string", "format": "date-time"}},
        "required": ["created_at"],
        "additionalProperties": False,
    }
    instance = {"created_at": "not-a-date"}
    emit("minimal_generic", validate(Draft202012Validator(minimal, format_checker=generic), instance))
    emit("minimal_draft202012", validate(Draft202012Validator(minimal, format_checker=draft), instance))
    emit("actual_generic", validate(Draft202012Validator(schema, format_checker=generic), fixture))
    emit("actual_draft202012", validate(Draft202012Validator(schema, format_checker=draft), fixture))

    baseline_source = BASELINE_VALIDATOR.read_text(encoding="utf-8")
    emit("baseline_uses_generic_formatchecker", "FormatChecker()" in baseline_source and "format_checker=FormatChecker()" in baseline_source)
    emit("baseline_validator_class", "Draft202012Validator")
    emit("baseline_format_checker_wiring", "Draft202012Validator(schema, format_checker=FormatChecker())")

    draft_primitive_fail = primitive(draft)["result"] == "FAIL"
    draft_minimal_fail = validate(Draft202012Validator(minimal, format_checker=draft), instance)["result"] == "FAIL"
    draft_actual_fail = validate(Draft202012Validator(schema, format_checker=draft), fixture)["result"] == "FAIL"
    if not draft_primitive_fail:
        classification = "R1_RUNTIME_OR_INSTALLED_PACKAGE_BEHAVIOR"
    elif not draft_minimal_fail:
        classification = "R2_SCHEMA_FORMAT_APPLICATION_DISCREPANCY"
    elif not draft_actual_fail:
        classification = "R2_ACTUAL_SCHEMA_OR_FIXTURE_DISCREPANCY"
    else:
        classification = "R3_BASELINE_INTEGRATION_DISCREPANCY_OR_UNREPRODUCED"
    emit("classification", classification)
    emit("verdict", "INVESTIGATION_COMPLETE")


if __name__ == "__main__":
    main()
