import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
EXEC = ROOT / "execution"
GENERATOR = EXEC / "scientific_generator.py"
SCHEMA = EXEC / "analytical_unit_schema.json"
CODEBOOK = EXEC / "cohort_codebook.json"
OUT1 = EXEC / ".determinism_run_1.json"
OUT2 = EXEC / ".determinism_run_2.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(output, seed=42, expect_success=True):
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(output), "--seed", str(seed)],
        capture_output=True,
        text=True,
    )
    if expect_success and result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    if not expect_success and result.returncode == 0:
        raise AssertionError("UNREGISTERED_SEED_ACCEPTED")


def validate_schema(data):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    errors = []
    for index, unit in enumerate(data):
        errors.extend((index, error.message) for error in validator.iter_errors(unit))
    if errors:
        raise AssertionError(f"SCHEMA_VALIDATION_FAILURE: {errors[:5]}")


def validate_codebook_boundaries(data):
    codebook = json.loads(CODEBOOK.read_text(encoding="utf-8"))
    expected_groups = set(codebook["groups"])
    observed_groups = {unit["group"] for unit in data}
    if observed_groups != expected_groups:
        raise AssertionError("COHORT_SET_VIOLATION")

    for unit in data:
        spec = codebook["groups"][unit["group"]]
        cost = float(spec["parameters"]["effort_cost_c"])
        expected_q = 1.0 - math.exp(-max(0.0, math.log(1.0 / cost) if cost < 1.0 else 0.0))
        records = unit["interaction_records"]
        if len(records) != 4:
            raise AssertionError("NESTED_INTERACTION_COUNT_VIOLATION")

        if unit["group"] == "G4_Iterative_Researcher":
            qs = [record["contribution_score"] / 10.0 for record in records]
            if any(qs[i] > qs[i + 1] for i in range(3)):
                raise AssertionError("G4_TRAJECTORY_VIOLATION")
        elif unit["group"] in {"G1_Pure_Consumer", "G2_Low_Producer", "G3_High_Producer", "G7_Human_Expert"}:
            if abs((records[0]["contribution_score"] / 10.0) - expected_q) > 1e-7:
                raise AssertionError("MODEL_PARAMETER_VIOLATION")

        if unit["group"] == "G5_Adversarial_Spam":
            divergences = [r["credit"] - r["contribution_score"] for r in records]
            if sum(value >= 1.5 for value in divergences) < 3:
                raise AssertionError("G5_GAMING_BOUNDARY_VIOLATION")


def main():
    try:
        run(OUT1)
        run(OUT2)
        if digest(OUT1) != digest(OUT2):
            raise AssertionError("DETERMINISM_VIOLATION")

        data = json.loads(OUT1.read_text(encoding="utf-8"))
        if len(data) != 679:
            raise AssertionError("UNIT_COUNT_VIOLATION")
        if len({u["unit_uuid"] for u in data}) != 679:
            raise AssertionError("UNIT_UUID_DUPLICATION")

        record_ids = [r["record_uuid"] for u in data for r in u["interaction_records"]]
        if len(record_ids) != 2716 or len(set(record_ids)) != 2716:
            raise AssertionError("RECORD_UUID_VIOLATION")

        counts = {}
        for unit in data:
            counts[unit["group"]] = counts.get(unit["group"], 0) + 1
            if unit["window_end"] < unit["window_start"]:
                raise AssertionError("WINDOW_ORDER_VIOLATION")
            for record in unit["interaction_records"]:
                if record["provenance"]["seed"] != 42:
                    raise AssertionError("PROVENANCE_SEED_VIOLATION")
                if record["provenance"]["model_revision"] != "deterministic_abm_v1":
                    raise AssertionError("MODEL_REVISION_VIOLATION")

        expected_counts = {name: 97 for name in [
            "G1_Pure_Consumer", "G2_Low_Producer", "G3_High_Producer",
            "G4_Iterative_Researcher", "G5_Adversarial_Spam",
            "G6_Synthetic_AI", "G7_Human_Expert",
        ]}
        if counts != expected_counts:
            raise AssertionError("COHORT_ALLOCATION_VIOLATION")

        validate_schema(data)
        validate_codebook_boundaries(data)
        run(OUT2, seed=43, expect_success=False)
        print(json.dumps({"status": "PASS", "units": 679, "records": 2716, "sha256": digest(OUT1)}, sort_keys=True))
        return 0
    finally:
        for path in (OUT1, OUT2):
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
