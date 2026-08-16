# S2 Readiness Evidence Matrix

**Gate state:** NOT READY

This matrix is intentionally conservative. `DEFINED` means the reusable control exists; it does not mean the S2 gate has passed.

| Control | State | Evidence required to promote to PASS |
|---|---|---|
| R-S2-001 Contract reconciliation | 🔴 BLOCKED | Exact S2 specification/version, normative assertion inventory, layer classification, fixture lineage |
| R-S2-002 Oracle definition | 🔴 BLOCKED | Versioned oracle with deterministic expected outcomes for every S2 assertion |
| R-S2-003 Evidence contract | 🟡 DEFINED | Executable artifact-schema validation and one controlled readiness artifact |
| R-S2-004 Provenance contract | 🟡 DEFINED | Executable provenance collector and verified target-binding evidence |
| R-S2-005 Determinism | 🟡 DEFINED | Two readiness executions plus comparator output and classification of permitted run-specific fields |
| R-S2-006 Failure taxonomy | 🟡 DEFINED | Machine-checkable taxonomy and unknown-failure fail-closed behavior |
| R-S2-007 Harness integrity | 🟡 DEFINED | Harness self-test proving non-zero validator exits still produce complete evidence |
| R-S2-008 Independent validation | 🔴 BLOCKED | Independent verifier executed against the declared readiness target and evidence |

## Current blockers

1. The exact S2 normative contract has not yet been reconciled in this readiness branch.
2. Consequently, an S2 oracle cannot yet be declared complete.
3. Independent validation cannot pass before the target contract and oracle are fixed and versioned.

## Authorization rule

No S2 execution may start while any row is `BLOCKED` or while readiness evidence is incomplete.

## Evolution rule

When a blocked control is resolved, preserve the resulting procedure as reusable infrastructure. Do not encode a one-time workaround into the S2 execution path.
