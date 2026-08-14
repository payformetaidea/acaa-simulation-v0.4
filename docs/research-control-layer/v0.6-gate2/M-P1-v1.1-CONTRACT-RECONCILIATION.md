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

The raw O2 artifact `9147901382` contains 1,936 records and 1,936 unique IDs. All 1,936 IDs satisfy the O2 six-digit contract and zero satisfy the M-P1-v1.0 sixteen-hex-character contract.

Therefore M-P1-v1.0 cannot be treated as a valid consumer contract for this O2 artifact without changing either the artifact or the metric specification. Both actions are outside the current evidence boundary.

## 2. Canonical contract for the v1.1 draft

The v1.1 draft adopts the already-frozen O2 boundary directly. No translation layer is introduced.

| Element | v1.1 draft contract |
|---|---|
| Input root | O2 evidence artifact |
| Record container | `records[]` |
| Record identity | `records[].cau_id` |
| CAU ID format | `^CAU-[0-9]{6}$` |
| Aggregate cross-check | `aggregate.cau_records` |
| Aggregate type | integer count |
| Record/aggregate invariant | `aggregate.cau_records == len(records)` |
| Uniqueness | unique within execution artifact |
| Zero valid records | `VALID / ZERO_COUNT` |
| Missing/unusable record container | `DATA_INTEGRITY_FAIL` |
| Duplicate IDs | counted once after validation |
| Adapter/normalization | prohibited |
| Artifact mutation | prohibited |

## 3. Missing-field semantics

The v1.1 draft retains the required distinction:

```text
valid artifact + zero records
    -> M-P1 = 0
    -> VALID / ZERO_COUNT

missing or unusable records container
    -> DATA_INTEGRITY_FAIL
    -> M-P1 = null / no value
```

A consumer must fail closed on structurally unusable input. It must never turn a missing record container into an empty valid record set.

## 4. Provenance boundary

This document does **not** claim that the previously reported Python and JavaScript implementations are v1.1 implementations. Their exact source provenance remains unresolved.

Accordingly:

- no implementation source is silently reclassified as v1.1;
- no runtime behavior is promoted to specification evidence;
- no adapter is introduced;
- no raw artifact is modified;
- no Gate-2 execution is authorized by this document.

## 5. Required implementation contract

Once exact implementation provenance is recovered, both implementations must consume the same boundary:

```text
parse artifact
    |
    +-- require records[] to be an array
    +-- require each record.cau_id to match ^CAU-[0-9]{6}$
    +-- enforce aggregate.cau_records == len(records)
    +-- apply only the specified canonicalization
    +-- deduplicate by canonical cau_id
    +-- return DATA_INTEGRITY_FAIL for unusable input
    +-- return VALID / ZERO_COUNT for a valid empty record set
```

Python and JavaScript must implement the same state machine and return the same classification/value for the same bytes.

## 6. Gate disposition

`RPL-MP1-001` remains OPEN until exact consumer provenance is attached.

`RPL-MP1-002` remains OPEN until the exact Python/JavaScript sources are provenance-verified and corrected if necessary.

`RPL-MP1-003` is resolved at the contract-design level by this draft, but **not closed at the protocol level**. Closure requires formal review, version acceptance, and execution authorization.

### Current Gate state

```text
O2 canonical contract             PASS / VERIFIED
Raw artifact structure             PASS / VERIFIED
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
