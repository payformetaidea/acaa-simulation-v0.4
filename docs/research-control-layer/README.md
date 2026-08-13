# Research Control Layer v0.1

## Purpose

The Research Control Layer records how ACAA research claims, evidence, limitations, hypotheses, reconciliation, and release controls are related.

This package is documentation-only. It does not modify the candidate baseline implementation at `de7d11ed9457ede84c1954aa70a59331bf07b72e`.

## Baseline reference

- Release/tag: `v0.5.0`
- Commit: `de7d11ed9457ede84c1954aa70a59331bf07b72e`
- Governance status in the repository baseline artifact: `BASELINE CANDIDATE — FINAL CI REQUIRED`
- Important: the public README currently describes v0.5.0 as frozen. This package does not resolve that inconsistency; it records the evidence boundary and preserves the repository artifact as the authoritative governance record.

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
