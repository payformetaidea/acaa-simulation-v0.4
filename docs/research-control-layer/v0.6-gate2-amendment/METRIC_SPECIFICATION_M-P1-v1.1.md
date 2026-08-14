# M-P1 Metric Specification — v1.1

**Status:** DRAFT / AMENDMENT CANDIDATE — NOT FROZEN  
**Algorithm:** `M-P1-v1.1`  
**Supersedes for amendment review:** `M-P1-v1.0` only after successor freeze  
**Baseline:** ACAA v0.5.0 (`de7d11ed9457ede84c1954aa70a59331bf07b72e`)  
**Frozen protocol reference:** `v0.6-gate2-protocol`  
**Amendment branch:** `research/gate2-mp1-v1.1-amendment`

## 1. Purpose

M-P1-v1.1 preserves the measurement semantics of M-P1-v1.0 while correcting the CAU identifier schema so that raw identifiers emitted by the immutable ACAA v0.5.0 baseline can be evaluated without rewriting, normalization into another identifier, adapter substitution, or baseline modification.

This document is a successor **candidate specification**. It is not a new protocol freeze and does not authorize execution.

## 2. Source of the Identifier Contract

The identifier contract is derived from:

`docs/research-control-layer/v0.6-gate2-amendment/BASELINE_IDENTITY_CONTRACT_AUDIT.md`

The audit establishes the following observed baseline facts:

```text
Identity field:      CAURecord.cau_id
Generation source:   simulator-local cau_seq
Representation:      CAU-{cau_seq:06d}
Identifier class:    sequential string identifier
Observed width:      6 decimal digits after `CAU-`
```

No transformation of the baseline identifier is part of M-P1-v1.1.

## 3. Definition

```text
M-P1(r) = |{c ∈ CAU : c ∈ output(r)}|
```

M-P1 is the cardinality of the set of unique canonical CAU identifiers present in a run's manifest.

The measurement answers only the cardinality question. Equal cardinality does not establish set identity, output-content consistency, or semantic equivalence.

## 4. CAU_ID Schema

The successor schema is derived directly from the observed baseline representation:

```yaml
pattern: "^CAU-[0-9]{6}$"
encoding: UTF-8
canonicalization: trim whitespace, then uppercase
```

### 4.1 Raw baseline preservation

The value extracted from the baseline manifest is the source value. M-P1 does not rewrite a valid baseline identifier into a different identifier representation.

For example:

```text
CAU-000001  → accepted as CAU-000001
```

The following is **not** performed:

```text
CAU-000001  → CAU-0000000000000001
CAU-000001  → hexadecimal conversion
CAU-000001  → hash-derived identifier
```

### 4.2 Canonicalization boundary

Canonicalization is limited to the metric's textual parsing boundary:

```text
raw field value
    ↓
trim surrounding whitespace
    ↓
uppercase
    ↓
validate against ^CAU-[0-9]{6}$
```

Because the baseline representation is already uppercase and decimal, canonicalization does not alter a normally serialized baseline `cau_id`.

It is not permitted to change digits, pad digits, remove digits, replace prefixes, or derive a new identifier.

## 5. Extraction Algorithm

The extraction boundary is the serialized CAU record's `cau_id` field.

```text
parse(manifest)
    ↓
locate CAU records
    ↓
read record.cau_id
    ↓
trim surrounding whitespace
    ↓
uppercase
    ↓
validate against ^CAU-[0-9]{6}$
    ↓
collect valid canonical values
    ↓
unique(set)
    ↓
len(set)
```

No filename, execution ID, seed, timestamp, array position, wrapper ID, or alternate identifier may substitute for `record.cau_id`.

## 6. Validation Boundary

A manifest is valid for M-P1 extraction only when its structure is parseable and CAU records can be deterministically classified under the v1.1 schema.

Rules:

```text
empty/null ID
    → FAILED

malformed/non-matching ID
    → excluded and logged

duplicate valid ID
    → counted once

valid manifest structure with zero CAU records
    → M-P1 = 0
    → VALID execution + ZERO_COUNT

all CAU entries malformed/non-matching
    → DATA_INTEGRITY_FAIL
    → do NOT record M-P1 = 0

negative M-P1
    → DATA_INTEGRITY_FAIL
```

The distinction between a valid measured zero and an unusable manifest is binding for v1.1.

## 7. Determinism

For the same manifest artifact and the same M-P1-v1.1 algorithm implementation, extraction MUST produce the same metric value and the same validation classification.

No runtime entropy, wall-clock time, seed regeneration, or external state may influence M-P1 extraction.

## 8. Aggregation

The existing Gate-2 statistical definitions are preserved unless formally amended elsewhere:

```text
n_s = number of valid runs for seed s
μ_s = mean(M-P1) within seed
σ_s = sample SD within seed
CV_s = σ_s / μ_s, if μ_s > 0
CV_s = UNDEFINED, if μ_s = 0

N_total = Σ n_s
μ_total = mean(M-P1) across valid runs
```

Frozen SAP definitions retained for amendment review:

```text
CV_within  = sqrt(MS_W) / μ_total
CV_total   = sqrt(σ̂²_total) / μ_total
CV_between = SD(μ_s) / μ_total
```

If `μ_total = 0`, return `ZERO_DENOMINATOR`; CVs are undefined and no CV decision is made.

## 9. Hashing and Provenance

The artifact hash remains the SHA-256 digest of the exact manifest file bytes:

```text
artifact_sha256 = SHA256(manifest_file)
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

The use of `M-P1-v1.1` in the canonical hash string prevents a v1.0 and v1.1 metric record from being represented as the same algorithm-versioned provenance object.

Hashes are to be recorded in the applicable evidence artifacts only after the successor protocol has passed verification and received a new freeze.

## 10. Compatibility Statement

M-P1-v1.1 is designed to be compatible with the observed raw baseline identifier contract:

| Requirement | v0.5.0 baseline | M-P1-v1.1 | Result |
|---|---|---|---|
| Identity field | `CAURecord.cau_id` | `CAURecord.cau_id` | PASS |
| Representation | `CAU-{cau_seq:06d}` | `^CAU-[0-9]{6}$` | PASS |
| Identifier transformation | none | none | PASS |
| Baseline mutation | none | none | PASS |
| 16-hex requirement | absent | not required | PASS |

This is a **specification-level compatibility statement**, not an independent verification result. Independent verification remains mandatory.

## 11. Non-Claims

This specification does not claim:

- that M-P1-v1.1 has been independently verified;
- that the amendment has been approved;
- that a new protocol freeze exists;
- that execution is authorized;
- that any Gate-2 evidence exists;
- that H-003 or H-004 is supported or falsified.

## 12. Required Verification Sequence

```text
Baseline Identity Contract Audit       PASS
        ↓
M-P1-v1.1 Specification                DRAFT
        ↓
Independent Implementation #1
Independent Implementation #2
        ↓
Compatibility + deterministic verification
        ↓
Amendment Review
        ↓
New Protocol Freeze
        ↓
New Execution Authorization
        ↓
33 Runs
```

Until those gates are completed, execution and evidence generation remain prohibited.
