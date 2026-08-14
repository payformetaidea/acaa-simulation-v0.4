# Gate 2 M-P1 Metric Specification

**Status:** DRAFT / PRE-REGISTRATION
**Algorithm:** `M-P1-v1.0`
**Protocol:** `v0.6-gate2`

## Definition

```text
M-P1(r) = |{c ∈ CAU : c ∈ output(r)}|
```

M-P1 is the cardinality of the set of unique canonical CAU identifiers in a run's manifest.

## CAU_ID schema

```yaml
pattern: "^CAU-[0-9A-F]{16}$"
encoding: UTF-8
canonicalization: uppercase + trim whitespace
```

- empty/null ID → `FAILED`;
- malformed/non-matching ID → excluded and logged;
- duplicate ID → counted once;
- negative M-P1 → `DATA_INTEGRITY_FAIL`.

## Manifest validation boundary

A manifest is valid for M-P1 extraction only when its structure is parseable and its CAU records can be deterministically classified under the canonical CAU_ID schema.

```text
At least one valid canonical CAU_ID
    → normal M-P1 extraction

All entries malformed / non-matching
    → DATA_INTEGRITY_FAIL
    → do NOT record M-P1 = 0

Valid manifest structure with zero CAU records
    → M-P1 = 0
    → VALID execution + ZERO_COUNT
```

This distinction is binding: an empty valid output is a measured zero; an unusable manifest is an integrity failure.

## Boundary

M-P1 measures cardinality stability only. Equal cardinality does not establish set identity, output-content consistency, or semantic equivalence.

## Extraction

```text
parse(manifest) → canonicalize → validate → unique IDs → len(set)
```

Deterministic: same artifact + same algorithm version → same value.

## Aggregation

```text
n_s = number of valid runs for seed s
μ_s = mean(M-P1) within seed
σ_s = sample SD within seed
CV_s = σ_s / μ_s, if μ_s > 0
CV_s = UNDEFINED, if μ_s = 0

N_total = Σ n_s
μ_total = mean(M-P1) across valid runs
```

Frozen SAP definitions:

```text
CV_within  = sqrt(MS_W) / μ_total
CV_total   = sqrt(σ̂²_total) / μ_total
CV_between = SD(μ_s) / μ_total
```

If `μ_total = 0`: `ZERO_DENOMINATOR`; CVs undefined; no CV decision.

## Hashing

```text
artifact_sha256 = SHA256(manifest_file)
canonical_string =
  metric=M-P1\n
  version=M-P1-v1.0\n
  run_id={run_id}\n
  value={m_p1_value}\n
  artifact_sha256={manifest_sha256}\n
metric_hash = SHA256(canonical_string.encode("utf-8"))
```

Hashes are recorded in E-004 and E-009/E-010 as appropriate.

## Synthetic illustration — not evidence

`[47,48,47]` → mean `47.333`, sample SD approximately `0.577`.

## Immutability

After protocol freeze, schema, canonicalization, extraction, algorithm version, and serialization are immutable. Any change requires a new protocol version and re-authorization.
