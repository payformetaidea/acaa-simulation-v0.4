import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / '_smoke_record.json'

subprocess.run([sys.executable, str(HERE / 'e1_runner.py'), '--seed', '1001', '--out', str(OUT)], check=True)
record = json.loads(OUT.read_text(encoding='utf-8'))
assert record['status'] == 'SMOKE_ONLY'
assert record['control_target']['tag'] == 'v0.5.0'
assert record['control_target']['commit'] == 'de7d11ed9457ede84c1954aa70a59331bf07b72e'
subprocess.run([sys.executable, str(HERE / 'e1_validator.py'), str(OUT)], check=True)
OUT.unlink()
print('E1 harness smoke test: PASS')
