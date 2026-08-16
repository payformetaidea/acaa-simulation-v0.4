import importlib.metadata
import json
import platform
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, FormatError

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "infrastructure" / "schemas" / "invariant-registry.schema.json"
FIXTURE_PATH = ROOT / "infrastructure" / "schema-conformance" / "invalid" / "invariant-registry.invalid-date-time.json"


def emit(label, value):
    print(f"{label}={value}")


def run_check(checker, value="not-a-date"):
    try:
        checker.check(value, "date-time")
        return False, "NO_EXCEPTION"
    except FormatError as exc:
        return True, type(exc).__name__


def main():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    generic_checker = FormatChecker()
    draft_checker = Draft202012Validator.FORMAT_CHECKER

    emit("python_version", platform.python_version())
    emit("python_executable", sys.executable)
    emit("jsonschema_version", importlib.metadata.version("jsonschema"))

    generic_registered = "date-time" in generic_checker.checkers
    draft_registered = "date-time" in draft_checker.checkers
    emit("generic_checker_date_time_registered", generic_registered)
    emit("draft202012_checker_date_time_registered", draft_registered)

    generic_rejects, generic_exception = run_check(generic_checker)
    draft_rejects, draft_exception = run_check(draft_checker)
    emit("generic_primitive_date_time", "EXPECTED_FAIL" if generic_rejects else "UNEXPECTED_PASS")
    emit("generic_primitive_exception", generic_exception)
    emit("draft202012_primitive_date_time", "EXPECTED_FAIL" if draft_rejects else "UNEXPECTED_PASS")
    emit("draft202012_primitive_exception", draft_exception)

    metadata = schema.get("properties", {}).get("metadata", {}).get("properties", {})
    created_at_schema = metadata.get("created_at", {})
    emit("schema_created_at_format", created_at_schema.get("format"))

    minimal_schema = {
        "type": "object",
        "properties": {"created_at": {"type": "string", "format": "date-time"}},
        "required": ["created_at"],
        "additionalProperties": False,
    }

    generic_validator = Draft202012Validator(minimal_schema, format_checker=generic_checker)
    draft_validator = Draft202012Validator(minimal_schema, format_checker=draft_checker)
    generic_minimal_errors = list(generic_validator.iter_errors({"created_at": "not-a-date"}))
    draft_minimal_errors = list(draft_validator.iter_errors({"created_at": "not-a-date"}))
    emit("minimal_generic_errors", len(generic_minimal_errors))
    emit("minimal_generic_result", "FAIL" if generic_minimal_errors else "PASS")
    emit("minimal_draft202012_errors", len(draft_minimal_errors))
    emit("minimal_draft202012_result", "FAIL" if draft_minimal_errors else "PASS")

    actual_generic_validator = Draft202012Validator(schema, format_checker=generic_checker)
    actual_draft_validator = Draft202012Validator(schema, format_checker=draft_checker)
    actual_generic_errors = list(actual_generic_validator.iter_errors(fixture))
    actual_draft_errors = list(actual_draft_validator.iter_errors(fixture))
    emit("actual_generic_errors", len(actual_generic_errors))
    emit("actual_generic_result", "FAIL" if actual_generic_errors else "PASS")
    emit("actual_draft202012_errors", len(actual_draft_errors))
    emit("actual_draft202012_result", "FAIL" if actual_draft_errors else "PASS")

    if actual_draft_errors:
        first = actual_draft_errors[0]
        emit("actual_draft_first_validator", first.validator)
        emit("actual_draft_first_path", list(first.absolute_path))
        emit("actual_draft_first_message", first.message)

    print("--- classification ---")
    if not draft_rejects or not draft_minimal_errors or not actual_draft_errors:
        emit("classification", "RUNTIME_OR_SCHEMA_FORMAT_DEFECT")
    elif not generic_minimal_errors and not actual_generic_errors:
        emit("classification", "GENERIC_FORMATCHECKER_WIRING_DEFECT")
    else:
        emit("classification", "NO_FORMATCHECKER_DISCREPANCY_REPRODUCED")


if __name__ == "__main__":
    main()
