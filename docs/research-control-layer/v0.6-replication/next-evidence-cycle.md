# ACAA v0.6 — Next Evidence Cycle

## Status

**Active research cycle — post-Gate-1**

Gate 1 has passed within the bounded v0.6-D1/O1 replication scope. This document defines the next evidence cycle without modifying the frozen v0.5.0 baseline.

## Evidence boundary

The next cycle must preserve the distinction between:

- demonstrated claims;
- supported procedural observations;
- open hypotheses;
- proposed/general claims.

No result from this cycle should be promoted beyond its demonstrated scope without a new gate decision.

## Research objectives

1. Test whether the observed O1 replication result is stable under additional preregistered conditions.
2. Expand evidence beyond the initial 12-seed replication without changing the frozen control target.
3. Stress the documentation/provenance pathway identified during Gate 1 reconciliation.
4. Determine whether any new observations justify a broader reproducibility claim.
5. Preserve all raw outputs and hashes before post-run curation.

## Controls

- Frozen control target: `v0.5.0` / `de7d11ed9457ede84c1954aa70a59331bf07b72e`
- No modification to the frozen implementation.
- New execution harnesses remain on v0.6 research branches.
- Inputs, seeds, environment records, outputs, and artifact digests must be retained.
- Any post-run curation must remain distinguishable from raw experimental output.

## Proposed sequence

### E1 — Expanded controlled replication

Run a preregistered expansion of the O1 procedure using additional independent seeds while preserving the exact frozen control target.

### E2 — Provenance integrity challenge

Verify that each execution can be mapped deterministically to:

`run → environment → control commit → inputs → outputs → artifact digest → final evidence package`

### E3 — Report/package integrity check

Repeat the evidence-package reconciliation process and determine whether the Gate 1 report-completeness issue can be eliminated at source rather than repaired post-run.

### E4 — Evidence classification

Update the claim/evidence matrix only from observed results. Do not broaden H-001/H-002 beyond their declared scope.

### E5 — Gate decision

A new gate is required before any claim is promoted, any new baseline is frozen, or v0.7 is proposed as a validated successor.

## Stop conditions

Stop and reconcile before continuing if any of the following occur:

- frozen target mismatch;
- undocumented dependency;
- missing run-specific hash;
- missing raw artifact;
- unexplained regression failure;
- provenance ambiguity;
- evidence/report inconsistency;
- deviation from preregistered procedure.

## Principle Zero

> **ACAA must not grow faster than its evidence.**
