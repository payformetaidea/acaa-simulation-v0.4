# M-P1-v1.1 Independent Verification

**Status:** PARTIAL PASS — semantic verification complete; raw baseline manifest replay pending

**Branch:** `research/gate2-mp1-v1.1-amendment`

**Baseline:** ACAA v0.5.0 (`de7d11ed9457ede84c1954aa70a59331bf07b72e`)

**Candidate metric:** `M-P1-v1.1`

## 1. Verification objective

Independently implement the candidate M-P1-v1.1 extraction rules twice, using different implementation languages, and verify that both implementations agree on schema validation, canonicalization boundary, unique-cardinality semantics, zero handling, integrity-failure handling, and deterministic behavior.

The verification must not modify the frozen baseline or the frozen `v0.6-gate2-protocol` artifact.

## 2. Independent implementations

### Implementation A — Python

```text
scripts/gate2_mp1_v1_1_independent_verifier_py.py
```

### Implementation B — JavaScript

```text
scripts/gate2_mp1_v1_1_independent_verifier_js.js
```

The implementations were written independently from the v1.1 specification and use separate language/runtime semantics. They do not import or call the Gate-2 runner.

## 3. Test matrix

| Test | Expected | Python | JavaScript |
|---|---|---|---|
| `CAU-000001`, `CAU-000002`, duplicate `CAU-000001` | `VALID`, M-P1=2 | PASS | PASS |
| surrounding whitespace | accepted after trim | PASS | PASS |
| lowercase prefix/letters | uppercase boundary applied, then schema validation | PASS | PASS |
| malformed identifier only | `DATA_INTEGRITY_FAIL` | PASS | PASS |
| empty valid CAU record list | `VALID`, M-P1=0, `ZERO_COUNT` interpretation | PASS | PASS |
| duplicate valid identifiers | counted once | PASS | PASS |
| negative M-P1 | impossible by construction | PASS | PASS |

The representative baseline-shaped input used for cross-implementation comparison was:

```json
{
  "cau_records": [
    {"cau_id": "CAU-000001"},
    {"cau_id": "CAU-000002"},
    {"cau_id": "CAU-000001"}
  ]
}
```

Both implementations returned:

```text
VALID / M-P1 = 2
```

## 4. Determinism

Repeated evaluation of the same input by both implementations produced the same classification and cardinality. No runtime entropy, timestamp, seed regeneration, or external state is used by either extractor.

## 5. Baseline compatibility assessment

The frozen baseline audit establishes that the authoritative identity field is `CAURecord.cau_id` and that the observed representation is:

```text
CAU-{cau_seq:06d}
```

Therefore a baseline value such as `CAU-000001` is accepted by the v1.1 schema without identifier rewriting.

This establishes specification-level compatibility with the observed baseline identity contract.

## 6. Raw baseline artifact replay — OPEN

A committed raw baseline manifest/output artifact containing serialized `CAURecord.cau_id` values was not identified in the accessible frozen repository tree during this verification pass.

Accordingly, the following stronger claim is deliberately **not** made:

> "M-P1-v1.1 has been replayed against an actual frozen v0.5.0 manifest artifact."

That claim remains pending until an exact baseline output artifact is identified and its immutable provenance is recorded.

## 7. Governance result

```text
Specification semantics                  PASS
Independent implementation A              PASS
Independent implementation B              PASS
Cross-implementation agreement           PASS
Observed baseline schema compatibility   PASS
Raw frozen-output replay                  PENDING
Amendment approval                        BLOCKED
New protocol freeze                      BLOCKED
Execution authorization                  BLOCKED
Gate-2 execution                         BLOCKED
Evidence generation                      BLOCKED
```

## 8. Conclusion

The candidate M-P1-v1.1 rules have passed independent semantic verification using two separate implementations and are consistent with the audited baseline CAU identity representation.

However, the verification gate is **not fully closed** because an exact raw baseline output artifact has not yet been replayed. No amendment freeze, authorization, execution, evidence generation, or hypothesis claim is permitted until that final evidence link is resolved.

**Principle:** evidence precedes claim.
