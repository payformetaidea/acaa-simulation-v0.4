# Integrity Report v0.1

## Verdict

`CLEAN — self-consistent`

## Counts

- Claims: 10 — DEMONSTRATED 6, SUPPORTED 1, PROPOSED 3
- Limitations: 18 — Hypothesis-linked 16, Work Item 1, Constraint 1, Orphan 0
- Hypotheses: 16 — grounded 16, falsifiable 16, experiment-defined 16
- Traceability: 10 complete, 0 partial, 0 broken
- Findings in cross-reconciliation: 0

## Integrity constraints

The canonical ontology is `DEMONSTRATED / SUPPORTED / PROPOSED`. `BOUNDED` is a scope modifier, not a status.

Rule 5: Every bounded claim must carry its scope qualification wherever the claim is published or reused.

L-018 is a continuous Publication/Release Integrity Constraint. It prevents unsupported promotion, scope loss, and drift between evidence and public claims.

## Baseline-state warning

The repository currently contains two materially different statements: the root README describes v0.5.0 as a frozen baseline, while `docs/governance/ACAA_v0.5_BASELINE.md` still states `BASELINE CANDIDATE — FINAL CI REQUIRED`. The tag `v0.5.0` resolves to the candidate commit `de7d11ed...`.

This package does not silently resolve that governance discrepancy. It preserves the evidence boundary and therefore must not be cited as proof that the Freeze transition itself is complete.

## Release boundary

This package is additive documentation. It does not alter the v0.5 implementation, tag, or governance artifact.
