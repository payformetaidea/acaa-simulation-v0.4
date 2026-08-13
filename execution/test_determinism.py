import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXEC = ROOT / "execution"
GENERATOR = EXEC / "scientific_generator.py"
OUT1 = EXEC / ".determinism_run_1.json"
OUT2 = EXEC / ".determinism_run_2.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(output, seed=42, expect_success=True):
    result = subprocess.run([sys.executable, str(GENERATOR), "--output", str(output), "--seed", str(seed)], capture_output=True, text=True)
    if expect_success and result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    if not expect_success and result.returncode == 0:
        raise AssertionError("UNREGISTERED_SEED_ACCEPTED")


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
        if counts != {name: 97 for name in [
            "G1_Pure_Consumer", "G2_Low_Producer", "G3_High_Producer",
            "G4_Iterative_Researcher", "G5_Adversarial_Spam", "G6_Synthetic_AI", "G7_Human_Expert"]}:
            raise AssertionError("COHORT_ALLOCATION_VIOLATION")
        run(OUT2, seed=43, expect_success=False)
        print(json.dumps({"status": "PASS", "units": 679, "sha256": digest(OUT1)}, sort_keys=True))
        return 0
    finally:
        for path in (OUT1, OUT2):
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
