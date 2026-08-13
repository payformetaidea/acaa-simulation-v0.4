# H-AICR v0.3.4 — Final Freeze Audit

**Target:** H-AICR methodological hardening
**Parent:** ACAA v0.5.0 frozen baseline
**Status:** AUDIT CHECKLIST

## G0 — Protocol integrity

- [ ] Epistemic statuses are explicit and no proposed construct is represented as validated capability.
- [ ] ACAA v0.5.0 baseline remains immutable and unchanged in semantics.
- [ ] Ontology is frozen before execution.
- [ ] Matching policy is frozen before execution.
- [ ] Dataset split and leakage controls are frozen.
- [ ] Statistical tests and multiplicity correction are frozen.
- [ ] Model revision and dependency versions are frozen.
- [ ] Graph edit-distance weights are frozen.
- [ ] Threat matrix is frozen.
- [ ] H-AICR-007 incentive-compatibility criterion is operationalized before execution.

## G1 — Measurement validity

- [ ] H-001 target and baselines are pre-registered.
- [ ] H-002 one-to-one matching is deterministic.
- [ ] H-003 canonical knowledge representation is versioned.
- [ ] H-004 independent human assessment is defined.
- [ ] Ground-truth reliability is measured before adjudication.

## G2 — Recognition and safety

- [ ] H-005 uses TOST with the correct 90% equivalence CI convention at alpha=0.05.
- [ ] H-005 reports a separate 95% descriptive robustness interval.
- [ ] H-006 reports the full 4 x 4 x 3 threat sensitivity matrix.
- [ ] Honest-user false-positive rate is measured.
- [ ] Economic rewards remain disabled during Phase A.

## G3 — Tokenization

- [ ] H-007 evaluation is independent of the metric used to generate token scores.
- [ ] Fairness and concentration thresholds are labeled design criteria.
- [ ] Noise sensitivity is pre-registered.
- [ ] Incentive-compatibility criterion is independently specified.

## G4 — Economic extension

- [ ] H-008 remains deferred.
- [ ] No Data Dividend or economic-value claim is promoted into the core validated scope.
- [ ] A separate economic protocol is created before economic experimentation.

## Evidence and provenance

- [ ] Claim → Hypothesis → Evidence → Artifact → Independent Validation → Decision is complete.
- [ ] Critical hypotheses meet minimum Level-3 evidence.
- [ ] Raw logs and hashes are immutable.
- [ ] Independent validation is blind to primary outcomes where applicable.
- [ ] Deviations create a new protocol version and never overwrite the frozen protocol.

## Decision

`PASS` only when all mandatory G0 controls are complete and no critical integrity defect remains.

`REVISION REQUIRED` when any mandatory control is incomplete.

A PASS authorizes execution preparation. It does not constitute empirical validation of H-AICR.
