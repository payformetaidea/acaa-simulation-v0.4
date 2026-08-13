import argparse
import json
from pathlib import Path
from e1_invariants import check

p = argparse.ArgumentParser()
p.add_argument('record', type=Path)
a = p.parse_args()
try:
    record = json.loads(a.record.read_text(encoding='utf-8'))
except Exception as exc:
    print('INVALID JSON:', exc)
    raise SystemExit(2)
errors = check(record)
for error in errors:
    print('ERROR:', error)
print('VALID' if not errors else 'INVALID')
raise SystemExit(0 if not errors else 1)
