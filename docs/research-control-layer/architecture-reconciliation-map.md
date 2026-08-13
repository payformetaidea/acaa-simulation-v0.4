# Artifact 2 — Architecture Reconciliation Map Draft 0.1

## Demonstrated v0.5 research-control architecture

The repository evidence supports the following bounded research-control pattern:

`Specification → Controlled Implementation → Independent Validator → Positive/Negative Tests → Evidence Artifact → CI → Reconciliation → Freeze/Release Gate`

This pattern is reported as a demonstrated, bounded v0.5 research-control architecture used to govern the project evidence. It is not claimed as a general ACAA capability.

## Claim → repository evidence chain

| Claim | Repository object class | Reconciliation requirement |
|---|---|---|
| C-001 | baseline / provenance | canonical commit and evidence record |
| C-002 | traceability / governance records | claim-to-artifact lineage remains reconstructable |
| C-003 | `docs/specs/` + O1 implementation/validator/tests/workflow | controlled O1 path is identifiable |
| C-004 | O1 experiments and variability evidence | scope remains O1/v0.5.0 |
| C-005 | O2 identity/evidence contract artifacts | scope remains O2 identity contract/v0.5.0 |
| C-006 | independent validator and evidence contracts | independence claim remains bounded to declared contracts |
| C-007 | governance and reconciliation records | supported architecture, not general implementation |
| C-008 | future thesis lifecycle design | proposed; no present evidence upgrade |
| C-009 | future evidence-quality metrics | proposed; atomic metrics precede composites |
| C-010 | future controlled evolution | proposed; requires new experiments |

## Ground-truth boundary

The repository baseline artifact currently states `BASELINE CANDIDATE — FINAL CI REQUIRED`, while the public README describes the release as frozen. This package deliberately records that discrepancy rather than silently resolving it.

The tag `v0.5.0` resolves to `de7d11ed9457ede84c1954aa70a59331bf07b72e`. The existence of the tag does not, by itself, establish completion of every governance transition declared by the baseline artifact.
