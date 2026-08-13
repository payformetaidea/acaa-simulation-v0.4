# Research Control Layer v0.1

## Purpose

The Research Control Layer records how ACAA research claims, evidence, limitations, hypotheses, reconciliation, and release controls are related.

This package is documentation-only. It does not modify the validated v0.5 implementation target at `de7d11ed9457ede84c1954aa70a59331bf07b72e`.

## Baseline reference

- Release/tag: `v0.5.0`
- Commit: `de7d11ed9457ede84c1954aa70a59331bf07b72e`
- Governance status: `FROZEN`
- Freeze governance merge: `94dbfe6da3c62a366c9423a6c785e4b1a74ce340`
- Final CI: O1 Run #58 / O2 Run #31 — PASS

The validated candidate commit remains the immutable v0.5 release target. The governance freeze was subsequently recorded by the governance merge without rewriting or moving the `v0.5.0` tag.

## Claim ontology

Canonical claim states are:

- `DEMONSTRATED`
- `SUPPORTED`
- `PROPOSED`

Scope is an independent modifier. A bounded claim must retain its scope qualification wherever published or reused.

**Rule 5:** Every bounded claim must carry its scope qualification wherever the claim is published or reused.

## Research Control Loop

`CLAIM → EVIDENCE STATUS → LIMITATION → HYPOTHESIS / WORK ITEM / CONSTRAINT → EXPERIMENT → EVIDENCE → REASSESSMENT → RELEASE GATE`

The package distinguishes the research program from the control layer used to govern the research itself.

## Integrity boundaries

The Cross-Reconciliation result is a self-consistency result, not independent ground-truth verification. Demonstrated claims remain bounded by the evidence paths and scopes recorded in the matrix and reconciliation map.

`L-018` is a continuous research-integrity constraint enforced by publication/release gating rather than a hypothesis.

`L-016` is a literature/research work item rather than a hypothesis.

## v0.6 doctrine

v0.6 is experiment-driven: it starts from measured limitations in v0.5, derives falsifiable hypotheses, executes controlled experiments, and reassesses claims before release.

> ACAA must not grow faster than its evidence.
