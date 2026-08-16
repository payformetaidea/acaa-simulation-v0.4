# F2 — FormatChecker Runtime Investigation

Status: EXECUTION AUTHORIZED / EVIDENCE PENDING

## Frozen target

- Validator target: `d1cef3768ccaa39525a0c23e1a9b94c3528a8995`
- Validator file: `infrastructure/schema-conformance/validate_s1.py`
- Runtime target: Ubuntu 24.04 / Python 3.12.3 / jsonschema 4.23.0

## Investigation ladder

1. Primitive `FormatChecker` registration and `date-time` rejection.
2. Minimal Draft 2020-12 schema using `format: date-time`.
3. Actual invariant-registry schema against the invalid-date-time fixture.
4. Compare the isolated result with the validator execution evidence.

## Classification rules

- Primitive fails: runtime/dependency defect.
- Primitive passes, minimal schema passes: validator wiring defect.
- Primitive + minimal pass, actual schema accepts: schema/fixture discrepancy.
- All isolated checks reject: discrepancy is not reproduced; inspect execution integration/evidence next.

No validator patch is authorized by this document.
