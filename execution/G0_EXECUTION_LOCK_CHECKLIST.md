# H-AICR G0 Execution Lock Checklist

**Branch:** execution/h-aicr-v0.3.4
**Protocol:** H-AICR v0.3.4
**Protocol blob SHA:** b68d58b7e879b350267632617c9a0cb58375249d
**Parent baseline:** ACAA v0.5.0 / de7d11ed9457ede84c1954aa70a59331bf07b72e

## Lock prerequisites

- [x] H-AICR-003 weights registered: node 2.0, edge 1.0, attribute 0.5
- [x] H-AICR-007 primary criterion registered: IC >= 1.25
- [x] H-AICR-007 bootstrap lower-bound requirement registered: > 1.00
- [x] Ground-truth annotation protocol prepared for three independent annotators
- [x] Leakage checker implementation added
- [ ] Dataset schema and split manifest committed
- [ ] Dataset generation seed committed
- [ ] Model revision hash committed
- [ ] Dependency lock committed
- [ ] Raw output structure committed
- [ ] Final G0 audit records PASS

## Execution rule

No confirmatory scientific run may begin while any unchecked prerequisite remains. Engineering smoke tests may run only when explicitly labelled as non-evidence.

## Evidence boundary

Synthetic control data are harness-validation artifacts only. Human ground truth requires independent annotation and remains separate from system predictions.
