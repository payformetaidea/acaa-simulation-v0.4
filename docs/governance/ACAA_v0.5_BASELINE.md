# ACAA v0.5 Baseline

**Status:** FROZEN
**Date:** 2026-08-12
**Baseline branch:** `agent/v0.5-integration-ci-gate`
**Validated finalization predecessor:** `de7d11ed9457ede84c1954aa70a59331bf07b72e`
**Final CI predecessor:** Run #58 / `31612771156` — PASS

## Formation Basis

The v0.5 baseline consists of the approved O1 and O2 controlled implementations integrated in the mandated order O1 → O2.

- O1: APPROVED / VALIDATED
- O2: APPROVED / VALIDATED
- Evolution Gate: APPROVED FOR INTEGRATION
- Combined Integration CI: PASS — Run #56 / `31612056935`
- Evidence Reconciliation: COMPLETE
- Final CI predecessor: PASS — Run #58 / `31612771156`
- v0.4 Frozen Baseline: PRESERVED

## Integrated Baseline

- O1 merge: `50a9999f...` (recorded integration state)
- O2 merge: `889efee0...` (recorded integration state)
- Baseline candidate commit: `de7d11ed9457ede84c1954aa70a59331bf07b72e`

## Finalization

The candidate passed Final CI on the exact candidate commit. This governance document records the transition to **FROZEN**. The finalization commit itself is documentation-only and does not alter O1/O2 implementation semantics.

Required release action:

1. Preserve the validated candidate commit as the immutable release target.
2. Create tag `v0.5.0` pointing to `de7d11ed9457ede84c1954aa70a59331bf07b72e`.
3. Keep v0.4 provenance and implementation unchanged.

## Scope Boundary

v0.5 validity is limited to the validated O1 and O2 specifications, controlled executions, independent evidence packages, and integrated CI contract. No universal robustness, CAU behavioral correctness, or system-level effectiveness claim is established.

## Baseline Doctrine

`Specification → Controlled Implementation → Independent Validation → Integration CI → Evidence Reconciliation → Final CI → Tag → Freeze`
