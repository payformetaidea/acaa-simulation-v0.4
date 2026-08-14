# Baseline Identity Contract Audit

## ACAA Gate 2 Amendment Track

**Audit status:** COMPLETE — OBSERVATION ONLY  
**Amendment branch:** `research/gate2-mp1-v1.1-amendment`  
**Frozen protocol reference:** `v0.6-gate2-protocol`  
**Frozen protocol commit:** `e5fde0b298e5bff9fd00196bd718a62934f09060`  
**Baseline:** ACAA v0.5.0 (`de7d11ed9457ede84c1954aa70a59331bf07b72e`)  

> This document records the observed identity contract of the frozen baseline. It does not modify the baseline, normalize identifiers, rewrite identifiers, or define M-P1-v1.1.

## 1. Scope and Governance Boundary

This audit exists solely to establish the factual CAU identity contract implemented by the frozen baseline before any successor metric is specified.

The following are explicitly out of scope:

- changing the frozen baseline;
- changing `cau_id` values;
- introducing an adapter or normalization layer;
- defining a successor metric schema;
- executing Gate-2 runs;
- generating Gate-2 evidence;
- modifying the frozen protocol tag.

The amendment branch starts from the frozen protocol commit so that all post-freeze work remains provenance-linked to the immutable reference.

## 2. Source Evidence

### 2.1 Frozen engine source

Observed source: `value_flow_simulator_v0.4.py` at the frozen baseline lineage.

The source defines:

```python
@dataclass
class CAURecord:
    cau_id: str
    ...
```

The simulator initializes an internal CAU sequence counter as:

```python
self.cau_seq: int = 0
```

The frozen engine therefore has an explicit sequence state associated with CAU creation, and CAU records carry the resulting identifier in the `cau_id` field.

### 2.2 Baseline identity format

The observed baseline implementation uses the six-decimal sequence representation:

```text
CAU-{cau_seq:06d}
```

The corresponding observed form is therefore:

```text
CAU-000001
CAU-000002
CAU-000003
...
```

This is materially different from the frozen M-P1-v1.0 requirement:

```text
^CAU-[0-9A-F]{16}$
```

The incompatibility finding is therefore reproducible at the schema boundary without changing either artifact.

## 3. Generation Contract

### Observed facts

1. `cau_seq` is initialized to integer zero when the simulator instance is created.
2. CAU records contain a dedicated `cau_id` string field.
3. The baseline identifier is generated from the sequence representation rather than from a 16-character hexadecimal identifier.
4. The sequence is execution-local state of the simulator instance.

### Audit interpretation

The baseline CAU identifier is a **sequential simulator-generated identifier**. The identifier itself is not observed to encode a cryptographic digest, seed, timestamp, actor identity, or other composite provenance value.

This statement is limited to the identifier-generation mechanism observed in the baseline source. Other provenance is carried by separate CAURecord fields and provenance structures.

## 4. Serialization Contract

The CAU object model contains `cau_id` as a first-class field of `CAURecord`.

The audit boundary for M-P1 extraction is therefore the serialized CAU record's `cau_id` field. No transformation is authorized between the baseline record and metric extraction.

Where a manifest or output wrapper contains CAU records, the audit treats the value associated with the record's `cau_id` field as the authoritative baseline identifier. A wrapper-level identifier must not be substituted for it without explicit evidence from the frozen baseline.

**Important:** this audit does not infer a different identifier from filenames, execution IDs, seeds, timestamps, or array positions.

## 5. Identity Contract

The observed baseline identity contract is:

```text
Identity field:      CAURecord.cau_id
Generation source:   simulator-local cau_seq
Representation:      CAU-{cau_seq:06d}
Identifier class:    sequential string identifier
Observed width:      6 decimal digits after `CAU-`
16-hex requirement:  absent from baseline generation
```

The identifier is therefore **not** a canonical 16-hexadecimal CAU identifier under the frozen M-P1-v1.0 schema.

## 6. Extraction Boundary

For any successor metric derived from the baseline, the extraction boundary is:

```text
serialized baseline CAU record
        ↓
`cau_id` field
        ↓
raw baseline identifier
```

The following operations are explicitly excluded from this audit and must remain excluded unless a future protocol amendment explicitly authorizes them:

```text
CAU-000001 → CAU-0000000000000001   [NOT performed]
CAU-000001 → hexadecimal conversion  [NOT performed]
CAU-000001 → hash-derived ID         [NOT performed]
CAU-000001 → normalized replacement   [NOT performed]
```

## 7. Compatibility Finding

| Requirement | Frozen baseline | Result |
|---|---|---|
| CAU field exists | `CAURecord.cau_id` | PASS |
| Sequential source exists | `cau_seq` | PASS |
| Baseline ID representation | `CAU-{cau_seq:06d}` | OBSERVED |
| M-P1-v1.0 schema | `^CAU-[0-9A-F]{16}$` | OBSERVED |
| Raw baseline satisfies M-P1-v1.0 schema | No | **FAIL** |
| Transformation required to force compatibility | Yes | **PROHIBITED** |

## 8. Audit Conclusion

**Baseline Identity Contract: ESTABLISHED for the generation and identity layers.**

The frozen baseline produces CAU identifiers using a six-digit decimal sequence representation. The raw identifier is carried by `CAURecord.cau_id`. This directly explains the incompatibility with M-P1-v1.0's 16-hexadecimal schema.

No modification to the frozen baseline is required or permitted.

## 9. Gate Decision

```text
Baseline Identity Contract Audit     PASS
Baseline mutation                    NONE
ID transformation                    NONE
M-P1-v1.0 compatibility              FAIL
M-P1-v1.1 design                     NOT YET AUTHORIZED BY THIS AUDIT
Gate-2 execution                     BLOCKED
Execution authorization              BLOCKED
```

## 10. Required Next Artifact

The next artifact may define **M-P1-v1.1**, but only by deriving its identifier schema and extraction rules from this observed baseline contract and by subjecting the successor specification to independent verification.

The required sequence remains:

```text
Baseline Identity Contract Audit
        ↓
M-P1-v1.1 Specification
        ↓
Independent Implementations (2x)
        ↓
Compatibility Verification
        ↓
Amendment Review
        ↓
New Protocol Freeze
        ↓
New Execution Authorization
        ↓
33 Runs
```

## 11. Non-Claims

This audit does **not** claim that Gate 2 has executed, that any hypothesis has been supported or falsified, or that M-P1-v1.1 is already valid. Those determinations require the subsequent formal amendment and verification gates.
