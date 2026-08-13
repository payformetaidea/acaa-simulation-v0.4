import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "execution" / "scientific_generator.py"
OUT1 = ROOT / "execution" / ".determinism_run_1.json"
OUT2 = ROOT / "execution" / ".determinism_run_2.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(output: Path) -> None:
    subprocess.run([sys.executable, str(GENERATOR), "--output", str(output), "--seed", "42"], check=True)


def main() -> int:
    try:
        run(OUT1)
        run(OUT2)
        d1, d2 = digest(OUT1), digest(OUT2)
        if d1 != d2:
            raise AssertionError("DETERMINISM_VIOLATION")
        data = json.loads(OUT1.read_text(encoding="utf-8"))
        if len(data) != 679:
            raise AssertionError("UNIT_COUNT_VIOLATION")
        if len({u["unit_uuid"] for u in data}) != 679:
            raise AssertionError("UNIT_UUID_DUPLICATION")
        print(json.dumps({"status": "PASS", "units": 679, "sha256": d1}, sort_keys=True))
        return 0
    finally:
        for path in (OUT1, OUT2):
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
