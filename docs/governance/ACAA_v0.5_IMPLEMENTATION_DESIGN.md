# ACAA v0.5 — Controlled Implementation Design

**Status:** Design Specification — Pre-Implementation  
**Baseline:** ACAA v0.4 Frozen Validated Baseline  
**Source Governance:** `ACAA_v0.5_EVOLUTION_GATE.md`  
**Approved Objectives:** O1, O2  
**Implementation Branch:** `agent/v0.5-implementation-design`  
**Design Date:** 2026-08-12

## 1. Purpose

This document converts the approved v0.5 objectives into a bounded implementation design. It authorizes design-level decomposition only. It does **not** authorize modification of the v0.4 Engine or Validator and does not establish a v0.5 baseline.

The governing sequence is:

```text
Approved Objective
      ↓
Implementation Design
      ↓
Controlled Change
      ↓
Independent Validation
      ↓
Evidence Package
      ↓
Regression / Integrity Gate
      ↓
Candidate v0.5 Baseline
```

## 2. Baseline Protection

The following v0.4 anchors remain immutable reference points:

- Release anchor: `239fd30de9e9c22b8f3bab0303250cfa98774696`
- Validated execution anchor: `50892a3be4bf05b54283514ccc6fd4798703aa35`
- v0.4 Engine semantics and existing regression suite
- Existing artifact, SHA-256/manifest, provenance, independent-validation, and Gatekeeper contracts

Any implementation that requires changing v0.4 semantics must be re-evaluated as a separate design decision.

## 3. Current v0.4 Evidence Surface

Inspection of `value_flow_simulator_v0.4.py` confirms:

- `CAURecord` already contains `cau_id`, actor, action, verdict, timestamp, level, and provenance chain.
- `_make_cau()` creates sequential identifiers of the form `CAU-######` and appends records to `self.ledger`.
- `BaseConfig.get_fingerprint()` intentionally excludes the seed from the base fingerprint.
- `EffectiveConfig.get_fingerprint()` binds base fingerprint, seed, scenario, and scenario parameters.
- CLI multi-seed execution currently runs seeds `42`, `137`, and `256` and exports each run through `sim.export()`.
- `export()` currently exposes `cau_records` as an aggregate count rather than individual CAU identities.
- `export()` already exposes effective configuration fingerprint, seed, scenario, metrics, attack log, adaptive log, provenance-event count, engine hash, and configuration hash.

These observations constrain the v0.5 design: O1 should extend the existing multi-seed evidence pathway; O2 should expose the existing identity capability to the independent evidence boundary.

## 4. O1 — Multi-Seed Behavioral Characterization

### 4.1 Objective

Formalize and independently validate multi-seed behavioral characterization without treating seed coverage, CV values, or observed variability as a universal robustness claim.

### 4.2 Proposed change surface

Create a v0.5 experiment/runner layer rather than changing v0.4 semantics in place.

Preferred design:

- A dedicated v0.5 experiment runner invokes the existing Engine with an immutable baseline configuration.
- The seed set is explicit and preregistered in the experiment specification.
- Initial target: at least 12 distinct seeds.
- Every run records:
  - seed;
  - effective configuration fingerprint;
  - scenario and scenario parameters;
  - engine hash;
  - execution artifact hash;
  - final metrics;
  - trajectory-level metrics required by the O1 protocol.
- Aggregate analysis is performed from preserved run artifacts rather than from mutable in-memory state.

### 4.3 Configuration invariants

For a valid O1 run set:

1. All runs use the same declared v0.4 scenario semantics.
2. All seed values are unique within the planned set.
3. The base configuration fingerprint is identical across runs.
4. The effective configuration fingerprint differs only where the seed is intentionally different.
5. Engine hash is recorded for every run.
6. No run is silently substituted, omitted, or reconfigured.

### 4.4 Metrics

The experiment must preserve the metrics already emitted by v0.4 and add analysis derived from them where appropriate:

- final CAU count;
- final and trajectory-level failure rate;
- gate efficiency;
- total artifacts;
- detection/isolation counts;
- equilibrium metrics;
- mean, standard deviation, variance, and coefficient of variation where mathematically meaningful;
- outlier identification under a predefined rule.

The implementation must explicitly handle zero-mean and zero-variance cases and record the handling rule in the evidence package.

### 4.5 Independent validation requirements

The independent validator for O1 must verify from preserved artifacts:

- planned seed set equals executed seed set;
- no duplicate seeds exist;
- configuration identity is consistent;
- required metrics are present and numerically extractable;
- aggregation is reproducible from individual run artifacts;
- statistical formulas and edge-case handling conform to the declared protocol;
- artifact hashes and provenance remain valid;
- v0.4 regression checks remain green.

### 4.6 O1 conclusion boundary

The validator may establish facts such as observed variability, distributional statistics, and reproducibility of the experiment. It must not convert those observations into a universal robustness claim.

A high-variability outcome is valid evidence and does not constitute an O1 failure by itself.

## 5. O2 — CAU Identity-Level Evidence Verification

### 5.1 Objective

Expose and independently validate CAU identity-level evidence while preserving v0.4 provenance and integrity contracts.

### 5.2 Identity contract to define before implementation

The implementation must explicitly define:

- identifier format;
- uniqueness scope;
- lifecycle semantics;
- reuse policy;
- relation between `cau_id` and ledger record;
- provenance linkage;
- collision/duplicate detection behavior.

The current sequential `CAU-######` generation is an observed implementation detail. It must not be promoted to a stronger identity guarantee until the contract and validator requirements are defined.

### 5.3 Proposed evidence representation

Prefer an additive evidence structure that preserves the existing aggregate field while exposing a verifiable identity index or individual CAU records.

Minimum information required for independent validation:

- `cau_id`;
- actor identity;
- action;
- verdict;
- timestamp;
- CAU level;
- provenance linkage sufficient to trace the record;
- a deterministic record representation suitable for integrity binding.

The aggregate `cau_records` count should remain available as a cross-check rather than being removed.

### 5.4 Independent validation requirements

The validator must independently verify:

1. every exported CAU identity conforms to the declared format;
2. identities are unique within the declared scope;
3. identity count equals the aggregate CAU count;
4. every identity resolves to exactly one exported record within scope;
5. lifecycle/provenance linkage is valid;
6. duplicate or collision conditions are detectable;
7. identity evidence is covered by the artifact integrity mechanism;
8. existing provenance and regression checks remain valid.

The validator must consume preserved evidence and must not reconstruct identity truth by executing the Engine.

### 5.5 O2 conclusion boundary

Successful O2 validation establishes identity-level evidence integrity and verifiability. It does not establish behavioral correctness, causal validity, or semantic quality of the CAU itself.

## 6. Shared Architecture Rules

### 6.1 Additive evolution

Where possible, v0.5 evidence should extend existing export structures without invalidating v0.4 consumers or historical artifacts.

### 6.2 Independent validation

The validator must remain structurally independent from Engine execution. Shared constants or schemas may be used only where they do not cause the validator to derive expected truth from the Engine implementation itself.

### 6.3 Evidence-first execution

Every controlled implementation run must produce a preserved evidence package before interpretation.

### 6.4 Deterministic extraction

Derived statistics and identity checks must be reproducible from the preserved artifact without relying on runtime state that is absent from the artifact.

### 6.5 Integrity preservation

Every new evidence field or artifact must be included in the declared integrity/manifest boundary. Adding data outside the integrity boundary is a validation defect.

## 7. Controlled Implementation Sequence

### Phase 0 — Design freeze

- Freeze this design specification.
- Define O1 experiment protocol and O2 identity contract in machine-checkable terms.
- Define acceptance tests before implementation.

### Phase 1 — O1 implementation

- Add v0.5 experiment/analysis capability in a controlled branch.
- Avoid modifying v0.4 baseline semantics unless explicitly justified.
- Produce a reproducible multi-seed evidence package.

### Phase 2 — O2 implementation

- Add identity evidence representation.
- Extend independent validation.
- Preserve aggregate count and existing integrity/provenance checks.

### Phase 3 — Independent validation

- Run O1 and O2 validators independently.
- Execute the full v0.4 regression suite.
- Execute targeted negative tests for duplicate IDs, missing identities, mismatched counts, seed mismatch, configuration mismatch, malformed statistics, and integrity-boundary violations.

### Phase 4 — Evidence review

- Freeze the produced artifacts.
- Record hashes, configuration fingerprints, seed set, validator version/hash, and execution metadata.
- Produce an evidence interpretation record that separates established claims from non-claims.

### Phase 5 — Candidate baseline decision

Only after independent validation and integrity/regression gates pass may the result be considered for a candidate v0.5 baseline.

## 8. Required Negative Tests

At minimum, the controlled validation suite should include:

### O1

- missing planned seed;
- duplicate seed;
- unexpected seed;
- configuration fingerprint mismatch;
- altered metric value;
- missing metric;
- malformed statistical input;
- zero-mean CV case;
- zero-variance case;
- altered run artifact hash.

### O2

- duplicate `cau_id`;
- missing `cau_id`;
- malformed `cau_id`;
- aggregate/identity count mismatch;
- identity without provenance linkage;
- provenance reference to nonexistent identity;
- altered CAU record after manifest generation;
- collision/reuse violation;
- incomplete lifecycle record.

## 9. Explicit Non-Goals

This implementation design does not authorize:

- R2 adaptive-behavior implementation;
- R3 adversarial-effectiveness implementation;
- production deployment;
- broad generalizability claims;
- universal robustness claims;
- scientific validity claims beyond the defined evidence and validation scope;
- redesign of CAU semantics beyond the minimum identity contract;
- replacement of the frozen v0.4 baseline.

## 10. Implementation Authorization Boundary

This document authorizes **planning and controlled design decomposition for O1 and O2**. It does not by itself authorize a code merge or a new baseline.

Before code modification, the following must exist:

- frozen implementation protocol;
- O1 experiment specification;
- O2 identity contract;
- acceptance-test specification;
- controlled implementation branch;
- explicit traceability from objective to changed files;
- rollback path to the v0.4 baseline.

## 11. Decision Record

```text
O1 — Multi-Seed Behavioral Characterization
    APPROVED → Design specified → Code change pending controlled execution

O2 — CAU Identity-Level Evidence Verification
    APPROVED → Design specified → Code change pending controlled execution

R2 — Adaptive Behavior
    REFINE / no implementation authorization

R3 — Adversarial Effectiveness
    REFINE / no implementation authorization

v0.4 baseline
    FROZEN / PRESERVED
```

**Next controlled artifact:** O1 experiment specification and O2 identity-contract/test specification, followed by implementation in a dedicated v0.5 branch.
