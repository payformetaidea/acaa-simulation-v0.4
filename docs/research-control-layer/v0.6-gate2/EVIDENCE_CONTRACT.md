# Gate 2 Evidence Contract

**Status:** DRAFT / PRE-REGISTRATION

## Required evidence classes

| ID | Artifact | Production point | Mutability | Requirement |
|---|---|---|---|---|
| E-001 | Protocol manifest | pre-run | immutable after freeze | required |
| E-002 | Seed registry | pre-run | immutable after freeze | required |
| E-003 | Input manifest/hashes | pre-run | immutable | required |
| E-004 | Raw outputs | run-time | immutable | required |
| E-005 | Execution logs | run-time | immutable | required |
| E-006 | Machine-readable metrics | post-run derivation | versioned | required |
| E-007 | Independent validation output | post-validation | immutable | required |
| E-008 | Variability analysis | post-validation | versioned | required |
| E-009 | Human-readable report | post-validation | versioned | required |
| E-010 | Provenance/decision record | throughout | append-only/versioned | required |

## Hash policy

Hashes must identify the exact artifact used in analysis. Replacing an artifact requires preserving the prior version and documenting the reason.

## Reconciliation policy

Reconciliation may repair packaging, derive missing presentation metadata, or clarify documentation. It may not fabricate missing raw evidence, alter historical run outputs, or rewrite pre-registered thresholds after outcome observation.

## Evidence hierarchy

Raw execution evidence outranks derived summaries. Derived summaries must remain traceable to raw evidence. A report is an interpretation layer, not a substitute for missing execution artifacts.
