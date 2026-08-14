# M-P1-v1.1 Contract Reconciliation — Draft

**Status:** DRAFT / NOT FROZEN / EXECUTION BLOCKED  
**Parent protocol:** `v0.6-gate2`  
**Baseline contract:** `acaa.v0.5.o2.identity-contract@1.0`  
**Baseline commit:** `de7d11ed9457ede84c1954aa70a59331bf07b72e`  
**O2 contract SHA:** `7b020332a3000f2b46c37bea08d27e070cacdf815`  
**M-P1-v1.0 source:** `e5fde0b298e5bff9fd00196bd718a62934f09060`  
**M-P1-v1.0 spec SHA:** `f136a09e3899c7b8d910ac11ee5de77e836bf70e`

## 1. Root architectural finding

The frozen O2 contract and the Gate-2 M-P1-v1.0 specification describe different CAU identifier contracts.

### O2 canonical boundary

```text
artifact root
├── records[]                  = CAURecord[]
│   └── cau_id                 = ^CAU-[0-9]{6}$
└── aggregate.cau_records      = integer count
```

### M-P1-v1.0 boundary

```text
manifest
└── CAU records
    └── cau_id                  = ^CAU-[0-9A-F]{16}$
```

The retained O2 artifact is identified as `9147901382`. The previously established inspection reported 1,936 raw records, 1,936 unique IDs, all IDs matching the O2 six-digit contract, zero matching the M-P1-v1.0 sixteen-hex-character contract, and `aggregate.cau_records = 1936`.

Therefore M-P1-v1.0 cannot be treated as a valid consumer contract for this O2 artifact without changing either the artifact or the metric specification. Both actions are outside the current evidence boundary.

## 2. Canonical contract for the v1.1 draft

The v1.1 draft consumes the canonical O2 boundary directly. No translation layer, normalization bridge, artifact mutation, or silent reclassification is introduced.

| Element | v1.1 draft contract |
|---|---|
| Input root | O2 evidence artifact |
| Artifact identity | `9147901382` plus independently verified SHA-256 |
| Record container | `records[]` |
| Record identity | `records[].cau_id` |
| CAU ID format | `^CAU-[0-9]{6}$` |
| Aggregate cross-check | `aggregate.cau_records` |
| Aggregate type | integer count, excluding booleans |
| Record/aggregate invariant | `aggregate.cau_records == len(records)` |
| Uniqueness | every `cau_id` must be unique in the raw validated record set |
| Duplicate IDs | `DATA_INTEGRITY_FAIL` |
| Zero valid records | `VALID / ZERO_COUNT` |
| Missing/unusable record container | `DATA_INTEGRITY_FAIL` |
| Deduplication | prohibited as validation or recovery behavior |
| Adapter/normalization | prohibited |
| Artifact mutation | prohibited |

## 3. Validation ordering and fail-closed semantics

Validation is ordered so that invalid input can never be repaired into a valid result.

```text
raw artifact bytes
      |
      +-- verify artifact identity
      |
      +-- verify SHA-256
      |
      +-- parse JSON
      |
      +-- require records[] to be an array
      |
      +-- require aggregate.cau_records to be an integer count
      |
      +-- require aggregate.cau_records == len(records)
      |
      +-- validate every record and every cau_id
      |
      +-- reject duplicate cau_id
      |
      +-- classify valid empty set as VALID / ZERO_COUNT
      |
      +-- otherwise VALID with the validated record cardinality
```

**No deduplication occurs at any point in this pipeline.** A duplicate identity is evidence of an integrity violation and terminates validation with `DATA_INTEGRITY_FAIL`.

The required distinction remains:

```text
valid artifact + zero records
    -> M-P1 = 0
    -> VALID / ZERO_COUNT

missing or unusable records container
    -> DATA_INTEGRITY_FAIL
    -> M-P1 = null / no value
```

A consumer must fail closed on structurally unusable input. It must never turn a missing record container into an empty valid record set.

## 4. Real-artifact verification boundary

Synthetic contract tests and real-artifact verification are separate gates.

### Synthetic Contract Gate

The regression suite proves contract semantics including:

- O2 identifier schema;
- aggregate typing;
- aggregate/record cardinality invariant;
- legacy M-P1-v1.0 incompatibility;
- missing-field fail-closed behavior;
- zero-count semantics;
- duplicate rejection;
- no-deduplication recovery behavior.

### Real Artifact Gate

CI must independently verify the retained artifact before the Contract Gate can pass. Verification must establish all of the following from the actual artifact bytes:

```text
artifact ID = 9147901382
SHA-256     = expected canonical SHA-256
records     = 1936
unique IDs  = 1936
O2 schema   = PASS
aggregate   = 1936
```

The expected SHA-256 and the artifact bytes must come from the canonical evidence source. They must never be reconstructed, generated, normalized, or inferred from the synthetic tests.

If the artifact or its expected SHA-256 is unavailable to CI, the Real Artifact Gate is **FAIL/BLOCKED**, not PASS.

## 5. Provenance boundary

This document does **not** claim that the previously reported Python and JavaScript implementations are v1.1 implementations. Their exact source provenance remains unresolved.

Accordingly:

- no implementation source is silently reclassified as v1.1;
- no runtime behavior is promoted to specification evidence;
- no adapter is introduced;
- no raw artifact is modified;
- no Gate-2 execution is authorized by this document.

## 6. Required implementation state machine

Once exact implementation provenance is recovered, Python and JavaScript consumers must implement the same state machine:

```text
INPUT
  |
  +-- artifact identity / SHA mismatch -> DATA_INTEGRITY_FAIL
  |
  +-- malformed JSON                  -> DATA_INTEGRITY_FAIL
  |
  +-- records[] unusable              -> DATA_INTEGRITY_FAIL
  |
  +-- aggregate invalid/mismatched    -> DATA_INTEGRITY_FAIL
  |
  +-- invalid cau_id                  -> DATA_INTEGRITY_FAIL
  |
  +-- duplicate cau_id                -> DATA_INTEGRITY_FAIL
  |
  +-- zero records                    -> VALID / ZERO_COUNT
  |
  `-- otherwise                       -> VALID
```

The implementations must return the same classification/value for the same verified bytes. No implementation may perform deduplication to obtain a successful classification.

## 7. Gate disposition

`RPL-MP1-001` remains OPEN until exact consumer provenance is attached.

`RPL-MP1-002` remains OPEN until the exact Python/JavaScript sources are provenance-verified and corrected if necessary.

`RPL-MP1-003` is resolved at the contract-design level by this draft, but **not closed at the protocol level**. Closure requires formal review, version acceptance, and execution authorization.

### Current Gate state

```text
O2 canonical contract             PASS / VERIFIED
Synthetic contract semantics       PASS / VERIFIED
Raw artifact verification          BLOCKED until CI has canonical bytes + SHA
M-P1-v1.0 compatibility            FAIL / DEMONSTRATED MISMATCH
M-P1-v1.1 draft contract            DEFINED / NOT FROZEN
Implementation provenance          OPEN
Strict replay                      BLOCKED
Amendment review                   BLOCKED
Protocol freeze                    BLOCKED
Execution authorization            BLOCKED
33-run execution                   BLOCKED
```

**Principle Zero: ACAA must not grow faster than its evidence.**
