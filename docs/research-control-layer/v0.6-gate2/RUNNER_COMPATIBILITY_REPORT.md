# Gate 2 Runner Compatibility Report

## Status

**BLOCKED — COMPATIBILITY FAILURE; NO EXECUTION PERFORMED**

## Binding References

- Protocol: `v0.6-gate2-protocol`
- Frozen commit: `e5fde0b298e5bff9fd00196bd718a62934f09060`
- Baseline: `v0.5.0` / `de7d11ed9457ede84c1954aa70a59331bf07b72e`
- Metric: `M-P1-v1.0`

## Finding

The frozen M-P1 specification defines canonical CAU identifiers as:

```text
^CAU-[0-9A-F]{16}$
```

The frozen baseline engine currently constructs CAU identifiers using the form:

```text
CAU-{six decimal digits}
```

Example implementation form:

```text
CAU-{self.cau_seq:06d}
```

Therefore baseline engine output does not satisfy the frozen M-P1 canonical identifier schema.

## Consequence

The Gate-2 runner cannot truthfully execute the baseline engine and then claim a valid M-P1 measurement under the frozen metric contract. Transforming or renaming IDs in a wrapper would change the measured artifact and would violate the frozen extraction boundary.

## Required Governance Action

This is a **binding compatibility blocker**, not an implementation detail. No Gate-2 execution authorization may be issued until one of the following is formally adopted through the protocol amendment process:

1. a new frozen metric specification compatible with the baseline artifact schema; or
2. a versioned baseline/engine change that emits the frozen canonical CAU_ID schema, followed by a new protocol freeze.

A silent adapter, ID rewriting, post-hoc normalization, or execution-time substitution is prohibited.

## Current Gate

```text
Dedicated runner architecture       DEFINED
Manifest                             DEFINED
Preflight                            DEFINED
Baseline engine                      AVAILABLE
M-P1 schema compatibility             FAIL
Execution Authorization               BLOCKED
33 executions                         BLOCKED
Evidence generation                   BLOCKED
```

## Principle

The runner must fail closed when the frozen measurement contract cannot be satisfied. No evidence is generated from an incompatible execution path.
