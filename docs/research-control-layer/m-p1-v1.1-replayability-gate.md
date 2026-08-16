# M-P1 v1.1 Replayability Gate

## Status

**CONTROLLED SPECIFICATION — NOT YET PASSED**

This gate defines the minimum evidence required before M-P1 v1.1 can proceed from contract verification to scaled execution. It does not itself authorize S1 approval, Gate-2, freeze, merge, or the 33-run campaign.

## Principle

Artifact integrity, replayability, implementation agreement, and scientific validity are distinct properties.

```text
Artifact integrity
    != Replayability
    != Cross-implementation agreement
    != Scientific validity
```

## Gate inputs

A replayability assessment must identify, at minimum:

1. Exact metric/specification version.
2. Exact input contract and missing-field semantics.
3. Exact raw evidence artifact and SHA-256.
4. Exact implementation commit(s).
5. Exact runtime/environment versions.
6. Exact execution command.
7. Exact output artifact(s) and SHA-256.

## Replayability condition

For a fixed specification, contract, raw evidence set, implementation, and runtime:

```text
same specification
+ same contract
+ same raw evidence
+ same implementation
+ same runtime
        => same result
```

Any divergence must be classified before statistical scaling. It must not be normalized away, patched by an execution-specific workaround, or resolved by adding more runs.

## Required checks

### RPL-01 — Provenance

The execution evidence must cryptographically bind the execution to the declared implementation commit and input artifact.

**PASS:** exact identifiers and SHA-256 values are present and internally consistent.

### RPL-02 — Contract closure

All input semantics relevant to computation must be explicit, including missing-field behavior, nullability, type interpretation, and aggregation rules.

**PASS:** no unresolved semantic ambiguity affects the replay.

### RPL-03 — Single-implementation replay

The same implementation must reproduce the same canonical result from the same evidence and environment.

**PASS:** canonical structured outputs are identical across independent executions.

### RPL-04 — Cross-implementation agreement

Where multiple implementations exist, they must consume the same contract and produce the same result, or every divergence must be explicitly reconciled.

**PASS:** agreement or documented, adjudicated divergence.

### RPL-05 — Statistical scaling lock

Gate-2 / 33-run execution remains blocked until RPL-01 through RPL-04 pass.

## Independence rule

A validator must not be treated as an independent oracle merely because it is deterministic. Where practical, expected behavior should be represented independently from the implementation under test.

For S1-V, the current controlled validator remains frozen at commit `d1cef3768ccaa39525a0c23e1a9b94c3528a8995`. Oracle-independence is therefore a **next-revision control requirement**, not a reason to modify the frozen S1-V target retroactively.

## Evidence chain

The preferred lineage is:

```text
Claim
  ↓
Specification / Contract
  ↓
Oracle
  ↓
Implementation
  ↓
Execution
  ↓
Environment + Raw Evidence
  ↓
Output Artifact
  ↓
Reconciliation
  ↓
Gate Decision
```

Every release-level claim must be traceable through this chain.

## Prohibited shortcuts

- No statistical campaign to resolve specification ambiguity.
- No execution-specific normalization of divergent results.
- No PASS inferred from source inspection alone.
- No replay claim without raw-evidence identity.
- No Gate-2 advancement while replayability is unresolved.

## Current decision

S1-V remains pending until a real execution artifact is produced and independently checked. This document records the forward control architecture; it does not constitute execution evidence.
