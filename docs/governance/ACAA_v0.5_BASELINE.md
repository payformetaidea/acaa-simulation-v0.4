# ACAA v0.5 Baseline

**Status:** BASELINE CANDIDATE — FINAL CI REQUIRED
**Date:** 2026-08-12
**Candidate branch:** `agent/v0.5-integration-ci-gate`
**Integration HEAD before this artifact:** `65ec8cd8741c37de30c03e1b4e8257cf593b6fd6`

## Formation Basis

The v0.5 candidate consists of the approved O1 and O2 controlled implementations integrated in the mandated order O1 → O2.

- O1: APPROVED / VALIDATED
- O2: APPROVED / VALIDATED
- Evolution Gate: APPROVED FOR INTEGRATION
- Combined Integration CI: PASS — Run #56 / `31612056935`
- Evidence Reconciliation: COMPLETE
- v0.4 Frozen Baseline: PRESERVED

## Integrated Candidate

- O1 merge: `50a9999f...` (recorded integration state)
- O2 merge: `889efee0...` (recorded integration state)
- Integration gate HEAD: `65ec8cd8741c37de30c03e1b4e8257cf593b6fd6`

## Required Finalization Gate

This artifact intentionally remains a **Candidate** until CI passes on the exact commit containing this document. After that pass, the repository may be tagged `v0.5.0` and the baseline status may be changed to **FROZEN**.

Required final checks:

1. CI PASS on the exact baseline commit.
2. v0.4 integrity/provenance remains preserved.
3. Evidence reconciliation remains unchanged.
4. Tag `v0.5.0` is created from the validated baseline commit.
5. Baseline status is changed from `CANDIDATE` to `FROZEN` only after the preceding checks.

## Scope Boundary

v0.5 validity is limited to the validated O1 and O2 specifications, controlled executions, independent evidence packages, and integrated CI contract. No universal robustness, CAU behavioral correctness, or system-level effectiveness claim is established.

## Baseline Doctrine

`Specification → Controlled Implementation → Independent Validation → Integration CI → Evidence Reconciliation → Final CI → Tag → Freeze`
