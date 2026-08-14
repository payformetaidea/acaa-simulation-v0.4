# G2-0.5 — Failure / Missing-Data Policy

**Status:** DRAFT / PRE-REGISTRATION
**Binding design:** `S=11`, `n=3`, `N_planned=33`

## 1. Core principle

> No failure is discarded. Each failure is classified, counted, preserved, and reported.

No replacement, imputation, or silent retry is permitted after an execution has been launched.

## 2. Binding denominators

```text
N_planned   = 33
N_attempted = executions actually launched
N_valid     = executions satisfying all validity rules
N_failed    = N_attempted - N_valid
N_invalid_seed = seeds with μ_s = 0

Success Rate = N_valid / N_planned
```

For the canonical design, execution authorization requires all 33 planned executions to be launched unless a predeclared infrastructure stop condition is formally invoked. A failed execution is never converted into a valid execution by retry.

## 3. Validity rules

An execution is `VALID` only if:

1. a parseable manifest exists;
2. all required identifiers pass the M-P1 extraction rules;
3. `M-P1 >= 0`;
4. the seed matches the frozen Seed Registry;
5. required provenance and execution metadata are present.

A seed with `μ_s = 0` is a successful execution state but is `ZERO_COUNT / INVALID_SEED` for seed-level statistical aggregation. Its executions remain in the overall valid-execution denominator and are never deleted.

## 4. Failure taxonomy

```text
F-parse:      output format mismatch; CAU identifiers cannot be extracted
F-crash:      engine terminates unexpectedly / non-zero exit
F-timeout:    execution exceeds the frozen time limit
F-malformed:  syntactically invalid output (e.g. JSON parse failure)
F-negative:   M-P1 < 0; DATA_INTEGRITY_FAIL
F-zero-seed:  μ_s = 0; statistically invalid seed, execution retained
F-protocol:   seed/configuration/procedure violates frozen protocol
F-infra:      network/resource/environment failure attributable to infrastructure
```

The most specific applicable class is recorded; multiple contributing causes may be preserved in provenance.

## 5. Evidence preservation

Every attempted execution must appear in:

- E-001 Execution Manifest;
- E-005 Execution Logs;
- E-009 Artifact Hashes where an artifact exists;
- E-010 Provenance Record.

Raw evidence is immutable after execution.

## 6. No replacement / no retry

A failed execution is not replaced with a new execution carrying the same seed. A retry may occur only if the frozen protocol explicitly defines a technical retry semantics before execution; otherwise a retry is prohibited. Any accidental retry is a new attempted execution and a protocol deviation.

## 7. Success-rate tiers

| Valid executions | Success rate | Tier |
|---:|---:|---|
| 32–33 / 33 | ≥ 0.9697 | PASS |
| 30–31 / 33 | 0.9091–0.9394 | MARGINAL |
| ≤29 / 33 | < 0.9091 | FAIL |

The Gate-2 acceptance matrix may impose a stricter hard criterion. These tiers are binding once the protocol is frozen.

## 8. Zero-count policy

```text
μ_s = 0 for one seed:
  ZERO_COUNT; seed-level aggregation excluded; review required.

μ_s = 0 for ≥2 seeds:
  ZERO_COUNT_SYSTEMATIC; formal investigation required.
  FALSIFIED only if the frozen theoretical expectation explicitly requires
  non-zero output for every tested seed.
  Otherwise → MARGINAL / NOT DEMONSTRATED.
```

Zero-count is never treated as proof that the underlying method is invalid unless such a theoretical expectation was frozen before execution.

## 9. Missing data

Missing observations are never imputed. Their absence is reported explicitly. Any analysis using fewer than the planned valid observations must state the exact denominator and reason.

## 10. Decision authority

A MARGINAL failure tier requires Formal Protocol Review. It does not automatically imply falsification. The review must document cause, impact, evidence integrity, and whether a protocol amendment is required.
