# Integrity Report v0.1

## Verdict

`CLEAN — self-consistent and governance-reconciled`

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

## Baseline-state reconciliation

The previously identified discrepancy between the root README and `docs/governance/ACAA_v0.5_BASELINE.md` has been resolved on the v0.5 governance branch. The baseline governance artifact now records `FROZEN`, with Final CI evidence and the unchanged `v0.5.0` tag target.

The validated release target remains `de7d11ed9457ede84c1954aa70a59331bf07b72e`. The governance transition was recorded by merge commit `94dbfe6da3c62a366c9423a6c785e4b1a74ce340` without rewriting or moving the tag.

## Finding F-001

`F-001 — Governance Freeze Incompleteness` is resolved by the completed Final CI → Governance Reconciliation → Freeze chain recorded in the repository history.

## Release boundary

This package is additive documentation. It does not alter the validated v0.5 implementation target or move the `v0.5.0` tag.
