# S1-V F1 — Fixture / Contract Reconciliation

## Status

**F1 correction applied — pending controlled execution.**

The validator baseline remains frozen at `d1cef3768ccaa39525a0c23e1a9b94c3528a8995`.

## Finding

The `cross-field-mismatch` semantic-negative fixture was previously rejected by JSON Schema because its `introduced_in.contract_id` value was `OTHER`, which does not satisfy the schema contract-id pattern.

That made the fixture structurally invalid rather than schema-valid / semantically-invalid, violating the intended Layer-1 / Layer-2 separation.

## Contract Evidence

The normative valid fixture defines `MP1-C-002` as:

> Each invariant introduction MUST match the registry contract identity.

The corresponding conformance vector is `MP1-V-002`.

Therefore the negative vector must preserve schema validity while violating the cross-field identity relation.

## Correction

Changed:

```text
introduced_in.contract_id
OTHER
```

to:

```text
introduced_in.contract_id
OTHER-CONTRACT
```

`OTHER-CONTRACT` satisfies the schema's contract-id pattern while remaining semantically different from the root `M-P1` contract identity.

Also corrected the fixture's conformance vector from `MP1-V-001` to `MP1-V-002` so the vector is aligned with the cross-field invariant under test.

## Controlled Branch

`research/mp1-v1.1-s1v-f1-fixture-reconciliation`

Base includes the previously approved evidence-harness correction. No change was made to the validator baseline.

F1 commits:

- `a3187a37faf1e23a93e6ac4f73c50caea52b5a84` — schema-valid semantic mismatch
- `a2e6121f076a2c8b6efad4ae4be495271ae2a0f7` — align conformance vector with `MP1-V-002`

## Acceptance Conditions

F1 is not considered validated until a controlled execution demonstrates:

1. Layer 1 accepts the fixture (`PASS`).
2. Layer 2 rejects it through `REG-C-002` (`FAIL`).
3. The result is deterministic across the required rerun.
4. No validator modification is present in the correction branch.

## Governance

This correction does **not** authorize S1 approval, S1-A, S2, merge, freeze, replayability approval, or Gate-2.

The validator baseline and schema remain frozen pending F2/F3 completion and controlled re-execution.
