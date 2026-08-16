# M-P1 Metric Specification — v1.1

**Status:** DRAFT / AMENDMENT CANDIDATE — NOT FROZEN  
**Algorithm:** `M-P1-v1.1`  
**Supersedes for amendment review:** `M-P1-v1.0` only after successor freeze  
**Baseline:** ACAA v0.5.0 (`de7d11ed9457ede84c1954aa70a59331bf07b72e`)  
**Frozen protocol reference:** `v0.6-gate2-protocol`  
**Amendment branch:** `research/mp1-v1.1-amendment`

## 1. Purpose

M-P1-v1.1 preserves the measurement semantics of M-P1-v1.0 while correcting the CAU identifier schema and input boundary so that the raw O2 artifact emitted by the immutable ACAA v0.5.0 baseline can be evaluated directly.

No adapter, alternate identity source, identifier rewriting, hexadecimal conversion, or baseline modification is permitted.

This is a successor candidate specification. It is not a protocol freeze and does not authorize execution.

## 2. Canonical O2 input boundary

M-P1-v1.1 consumes the canonical O2 evidence artifact directly:

```text
artifact root
├── records[]
│   └── cau_id
└── aggregate.cau_records
```

The authoritative identity field is `records[].cau_id`.

The canonical O2 contract is:

```text
records[].cau_id      = ^CAU-[0-9]{6}$
aggregate.cau_records = integer count
aggregate.cau_records = len(records)
```

The retained baseline artifact is `9147901382` and its exact JSON bytes are provenance-verified separately.

## 3. Definition

```text
M-P1(r) = |{ c ∈ CAU : c ∈ records(r) }|
```

M-P1 is the cardinality of the set of unique canonical CAU identifiers present in a valid O2 run artifact.

Equal cardinality does not establish set identity, output-content consistency, or semantic equivalence.

## 4. Canonicalization

Canonicalization is limited to the textual parsing boundary:

```text
raw cau_id
    ↓
trim surrounding whitespace
    ↓
uppercase
    ↓
validate against ^CAU-[0-9]{6}$
```

No digits may be changed, padded, removed, converted to hexadecimal, hashed, or replaced by another identifier.

For normally serialized baseline data, canonicalization is a no-op.

## 5. Structural validation

The O2 artifact is usable for M-P1 extraction only when all of the following hold:

```text
artifact root is an object
records exists and is an array
aggregate exists and is an object
aggregate.cau_records is an integer, excluding booleans
aggregate.cau_records == len(records)
```

Missing or unusable `records` is `DATA_INTEGRITY_FAIL`.

Missing or unusable `aggregate` is `DATA_INTEGRITY_FAIL`.

An aggregate/record cardinality mismatch is `DATA_INTEGRITY_FAIL`.

A malformed JSON artifact is `DATA_INTEGRITY_FAIL`.

## 6. Record validation and metric semantics

For every raw record:

- a non-object record is invalid;
- a missing, null, empty, or non-string `cau_id` is invalid;
- a non-matching identifier is invalid and excluded from the valid identifier set;
- a valid identifier is canonicalized and collected;
- duplicate valid canonical identifiers are counted once, because M-P1 is a unique-cardinality metric.

The following states are binding:

```text
valid records + zero records
    -> VALID / ZERO_COUNT
    -> M-P1 = 0

some valid identifiers + some invalid records
    -> VALID
    -> M-P1 = number of unique valid canonical identifiers

all records invalid
    -> DATA_INTEGRITY_FAIL
    -> M-P1 = null

missing/unusable records container
    -> DATA_INTEGRITY_FAIL
    -> M-P1 = null
```

Deduplication is a metric operation over valid canonical identifiers; it must never be used to repair a malformed record container or bypass structural validation.

## 7. Independent implementation requirement

Python and JavaScript implementations must independently consume the same serialized O2 artifact boundary and produce identical classification and metric value for identical bytes.

They must not import or call the Gate-2 runner and must not share runtime state.

## 8. Determinism

For the same verified artifact bytes and the same M-P1-v1.1 algorithm, extraction MUST produce the same classification and metric value.

No runtime entropy, wall-clock time, seed regeneration, or external state may influence extraction.

## 9. Provenance and hashing

The artifact hash is the SHA-256 digest of the exact O2 manifest file bytes:

```text
artifact_sha256 = SHA256(manifest_file_bytes)
```

The metric provenance hash uses the successor algorithm version explicitly:

```text
canonical_string =
  metric=M-P1\n
  version=M-P1-v1.1\n
  run_id={run_id}\n
  value={m_p1_value}\n
  artifact_sha256={manifest_sha256}\n
metric_hash = SHA256(canonical_string.encode("utf-8"))
```

Hashes are recorded in applicable evidence artifacts only after the successor protocol passes verification and receives a new freeze.

## 10. Compatibility statement

| Requirement | v0.5.0 O2 baseline | M-P1-v1.1 | Result |
|---|---|---|---|
| Identity field | `records[].cau_id` | `records[].cau_id` | PASS |
| Representation | `CAU-{cau_seq:06d}` | `^CAU-[0-9]{6}$` | PASS |
| Input root | O2 artifact | O2 artifact | PASS |
| Identifier transformation | none | none beyond parse-boundary canonicalization | PASS |
| 16-hex requirement | absent | not required | PASS |
| Aggregate invariant | `aggregate.cau_records == len(records)` | required | PASS |

This is a specification-level compatibility statement. Independent verification remains mandatory.

## 11. Non-claims

This specification does not claim:

- that M-P1-v1.1 is frozen;
- that Gate-2 execution is authorized;
- that any Gate-2 experimental evidence exists;
- that H-003 or H-004 is supported or falsified.

## 12. Required verification sequence

```text
Baseline Identity Contract Audit
        ↓
Canonical O2 artifact provenance
        ↓
M-P1-v1.1 Specification
        ↓
Independent Python implementation
Independent JavaScript implementation
        ↓
Cross-runtime parity
        ↓
Exact raw O2 artifact replay
        ↓
Amendment Review
        ↓
Post-Mutation Audit
        ↓
New Protocol Freeze
        ↓
New Execution Authorization
        ↓
33 Runs
```

Until all preceding gates are complete, execution and evidence generation remain prohibited.
