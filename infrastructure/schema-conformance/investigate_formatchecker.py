import json
import platform
import sys
from pathlib import Path

import jsonschema
from jsonschema import Draft202012Validator, FormatChecker, FormatError

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "infrastructure" / "schemas" / "invariant-registry.schema.json"
FIXTURE_PATH = ROOT / "infrastructure" / "schema-conformance" / "invalid" / "invariant-registry.invalid-date-time.json"


def emit(label, value):
    print(f"{label}={value}")


def main():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    checker = FormatChecker()

    emit("python_version", platform.python_version())
    emit("python_executable", sys.executable)
    emit("jsonschema_version", jsonschema.__version__)
    emit("format_checker_date_time_registered", "date-time" in checker.checkers)

    try:
        checker.check("not-a-date", "date-time")
        emit("primitive_date_time", "UNEXPECTED_PASS")
        primitive_ok = False
    except FormatError as exc:
        emit("primitive_date_time", "EXPECTED_FAIL")
        emit("primitive_exception", type(exc).__name__)
        primitive_ok = True

    metadata = schema.get("properties", {}).get("metadata", {}).get("properties", {})
    created_at_schema = metadata.get("created_at", {})
    emit("schema_created_at_format", created_at_schema.get("format"))

    minimal_schema = {
        "type": "object",
        "properties": {"created_at": {"type": "string", "format": "date-time"}},
        "required": ["created_at"],
        "additionalProperties": False,
    }
    minimal_validator = Draft202012Validator(minimal_schema, format_checker=checker)
    minimal_errors = list(minimal_validator.iter_errors({"created_at": "not-a-date"}))
    emit("minimal_schema_errors", len(minimal_errors))
    emit("minimal_schema_result", "FAIL" if minimal_errors else "PASS")
    if minimal_errors:
        emit("minimal_exception_validator", minimal_errors[0].validator)
        emit("minimal_exception_type", type(minimal_errors[0]).__name__)

    actual_validator = Draft202012Validator(schema, format_checker=checker)
    actual_errors = list(actual_validator.iter_errors(fixture))
    emit("actual_schema_errors", len(actual_errors))
    emit("actual_schema_result", "FAIL" if actual_errors else "PASS")
    for i, error in enumerate(actual_errors[:10], start=1):
        emit(f"actual_error_{i}_validator", error.validator)
        emit(f"actual_error_{i}_path", list(error.absolute_path))
        emit(f"actual_error_{i}_schema_path", list(error.absolute_schema_path))
        emit(f"actual_error_{i}_type", type(error).__name__)
        emit(f"actual_error_{i}_message", error.message)

    print("--- classification ---")
    if not primitive_ok:
        emit("classification", "RUNTIME_FORMATCHECKER_DEFECT")
    elif not minimal_errors:
        emit("classification", "VALIDATOR_FORMAT_WIRING_DEFECT")
    elif not actual_errors:
        emit("classification", "ACTUAL_SCHEMA_OR_FIXTURE_DISCREPANCY")
    else:
        emit("classification", "NO_FORMATCHECKER_DISCREPANCY_REPRODUCED")


if __name__ == "__main__":
    main()
