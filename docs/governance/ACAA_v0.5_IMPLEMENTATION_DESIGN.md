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
- Every run records seed, effective configuration fingerprint, scenario, engine hash, execution artifact hash, final metrics, and required trajectory-level metrics.
- Aggregate analysis is performed from preserved run artifacts rather than mutable in-memory state.

### 4.3 Configuration invariants

1. All runs use the same declared v0.4 scenario semantics.
2. All seed values are unique within the planned set.
3. The base configuration fingerprint is identical across runs.
4. Effective configuration fingerprints differ only through the intentional seed difference.
5. Engine hash is recorded for every run.
6. No run is silently substituted, omitted, or reconfigured.

### 4.4 Metrics

Preserve existing v0.4 metrics and derive, where appropriate:

- final CAU count;
- final and trajectory-level failure rate;
- gate efficiency;
- total artifacts;
- detection/isolation counts;
- equilibrium metrics;
- mean, standard deviation, variance, and coefficient of variation where meaningful;
- predefined outlier analysis.

Zero-mean and zero-variance cases must have explicit, reproducible handling rules.

### 4.5 Independent validation

The independent validator must verify from preserved artifacts:

- planned seed set equals executed seed set;
- no duplicate seeds;
- configuration identity consistency;
- required metrics and reproducible extraction;
- declared statistical formulas and edge-case handling;
- artifact hashes and provenance;
- v0.4 regression preservation.

### 4.6 Conclusion boundary

O1 may establish observed variability, distributional statistics, and experimental reproducibility. It must not convert those observations into a universal robustness claim. High variability is a valid outcome.

## 5. O2 — CAU Identity-Level Evidence Verification

### 5.1 Objective

Expose and independently validate CAU identity-level evidence while preserving v0.4 provenance and integrity contracts.

### 5.2 Identity contract

Before implementation, define:

- identifier format;
- uniqueness scope;
- lifecycle semantics;
- reuse policy;
- relation between `cau_id` and ledger record;
- provenance linkage;
- collision/duplicate behavior.

The current sequential `CAU-######` generation is an implementation observation, not yet a validated identity guarantee.

### 5.3 Evidence representation

Prefer an additive evidence structure that preserves the existing aggregate `cau_records` field while exposing a verifiable identity index or individual CAU records.

Minimum identity evidence should include `cau_id`, actor, action, verdict, timestamp, CAU level, provenance linkage, and a deterministic record representation suitable for integrity binding.

### 5.4 Independent validation

The validator must independently verify:

1. identifier format;
2. uniqueness within declared scope;
3. identity count equals aggregate CAU count;
4. each identity resolves to exactly one record;
5. lifecycle/provenance linkage;
6. duplicate/collision detection;
7. integrity coverage;
8. preservation of existing provenance and regression checks.

The validator must consume preserved evidence and must not reconstruct identity truth by executing the Engine.

### 5.5 Conclusion boundary

O2 establishes identity-level evidence integrity and verifiability. It does not establish behavioral correctness, causal validity, or semantic quality of the CAU.

## 6. Shared Architecture Rules

- Evidence changes should be additive where practical.
- Independent validation remains structurally separate from Engine execution.
- Every controlled run produces a preserved evidence package before interpretation.
- Derived statistics and identity checks must be reproducible from preserved artifacts.
- All new evidence must be included in the declared integrity/manifest boundary.

## 7. Controlled Implementation Sequence

### Phase 0 — Design freeze

- Freeze this specification.
- Define the O1 experiment protocol and O2 identity contract in machine-checkable terms.
- Define acceptance tests before implementation.

### Phase 1 — O1 implementation

Add v0.5 experiment/analysis capability in a controlled branch and produce a reproducible multi-seed evidence package without silently changing v0.4 semantics.

### Phase 2 — O2 implementation

Add identity evidence representation, extend independent validation, and preserve aggregate count and existing integrity/provenance checks.

### Phase 3 — Independent validation

Run O1/O2 validation independently, execute the full v0.4 regression suite, and execute targeted negative tests.

### Phase 4 — Evidence review

Freeze artifacts and record hashes, configuration fingerprints, seed set, validator version/hash, and execution metadata. Produce an evidence interpretation record separating established claims from non-claims.

### Phase 5 — Candidate baseline decision

Only after independent validation and integrity/regression gates pass may the result be considered for a candidate v0.5 baseline.

## 8. Required Negative Tests

### O1

- missing, duplicate, or unexpected seed;
- configuration fingerprint mismatch;
- altered or missing metric;
- malformed statistical input;
- zero-mean CV case;
- zero-variance case;
- altered run artifact hash.

### O2

- duplicate, missing, or malformed `cau_id`;
- aggregate/identity count mismatch;
- identity without provenance;
- provenance reference to nonexistent identity;
- post-manifest CAU alteration;
- collision/reuse violation;
- incomplete lifecycle record.

## 9. Explicit Non-Goals

This design does not authorize R2, R3, production deployment, broad generalizability claims, universal robustness claims, scientific validity claims beyond scope, CAU semantic redesign, or replacement of the frozen v0.4 baseline.

## 10. Implementation Authorization Boundary

This document authorizes planning and controlled design decomposition for O1 and O2. It does not authorize a code merge or a new baseline.

Before code modification, the following must exist:

- frozen implementation protocol;
- O1 experiment specification;
- O2 identity contract;
- acceptance-test specification;
- controlled implementation branch;
- objective-to-file traceability;
- rollback path to v0.4.

## 11. Decision Record

```text
O1 — Multi-Seed Behavioral Characterization
    APPROVED → Design specified → Code change pending controlled execution

O2 — CAU Identity-Level Evidence Verification
    APPROVED → Design specified → Code change pending controlled execution

R2 / R3
    REFINE / no implementation authorization

v0.4 baseline
    FROZEN / PRESERVED
```

**Next controlled artifact:** O1 experiment specification and O2 identity-contract/test specification, followed by implementation in a dedicated v0.5 branch.