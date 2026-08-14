# Gate 2 Evidence Contract

**Status:** DRAFT / PRE-REGISTRATION

## Canonical evidence IDs

| ID | Artifact | Production point | Mutability | Required |
|---|---|---|---|---|
| E-001 | Execution Manifest | pre-run / run registration | immutable after freeze | Yes |
| E-002 | Frozen Seed Registry | pre-run | immutable after freeze | Yes |
| E-003 | Raw Outputs | run-time | immutable | Yes |
| E-004 | Machine-readable Metrics | post-run derivation | versioned, traceable | Yes |
| E-005 | Execution Logs | run-time | immutable | Yes |
| E-006 | Independent Validation Output | post-run validation | immutable | Yes |
| E-007 | Variability / Outlier Analysis | post-validation | versioned | Yes |
| E-008 | Human-readable Report | post-validation | versioned | Yes |
| E-009 | Artifact Hashes | throughout | append-only | Yes |
| E-010 | Provenance / Decision Record | throughout | append-only/versioned | Yes |

## Evidence chain

```text
Protocol
  → Seed Registry
  → Execution Manifest
  → Raw Outputs + Logs
  → Machine-readable Metrics
  → Independent Validation
  → Variability/Outlier Analysis
  → Report
  → Hashes + Provenance
  → Gate Decision
```

## Integrity rules

1. Raw evidence cannot be reconstructed after the fact.
2. No raw artifact may be overwritten.
3. Any replacement artifact preserves the previous artifact and records the reason.
4. Derived metrics must reference exact input artifacts and algorithm versions.
5. Reconciliation may repair packaging/documentation only; it may not fabricate missing raw evidence.
6. Frozen thresholds may not be changed after outcome observation.

## Required run-level provenance

Each run record must contain at minimum:

- run ID;
- seed ID/value;
- protocol version and frozen commit;
- baseline version/commit;
- input artifact hashes;
- runtime/container identity;
- start/end timestamps;
- execution status;
- output artifact hashes;
- metric algorithm version;
- failure class if failed.

## Evidence integrity states

- `VALID`
- `INCOMPLETE`
- `CORRUPTED`
- `MISSING`
- `DATA_INTEGRITY_FAIL`

Material integrity failure blocks hypothesis evaluation and yields `NOT EVALUATED` rather than falsification.
