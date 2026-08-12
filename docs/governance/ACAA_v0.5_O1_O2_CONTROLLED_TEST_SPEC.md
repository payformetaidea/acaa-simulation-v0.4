# ACAA v0.5 — O1/O2 Controlled Test Specification

**Status:** Pre-Implementation Test Contract  
**Parent Design:** `ACAA_v0.5_IMPLEMENTATION_DESIGN.md`  
**Governance Source:** `ACAA_v0.5_EVOLUTION_GATE.md`  
**Approved Objectives:** O1, O2  
**Design Date:** 2026-08-12

## 1. Purpose

This document freezes the validation/test contract before implementation. It defines what must be measured, what the independent validator must verify, and which negative conditions must fail validation.

It does not modify the v0.4 Engine or Validator and does not define a scientific conclusion in advance.

## 2. O1 — Multi-Seed Behavioral Characterization

### 2.1 Experimental unit

One experimental unit is one complete baseline-scenario execution with:

- one unique seed;
- one immutable base configuration;
- one effective configuration fingerprint;
- one Engine hash;
- one preserved execution artifact.

### 2.2 Planned seed protocol

Initial target: **at least 12 unique seeds**.

The exact seed list must be frozen before execution and stored in the experiment manifest. Execution is valid only when the planned and observed seed sets are identical.

### 2.3 Configuration invariants

For all O1 runs:

```text
base_config_fingerprint: identical
scenario: identical
scenario_params: identical
engine_hash: identical
seed: unique per run
```

The effective configuration fingerprint must be reproducible from the recorded configuration and seed.

### 2.4 Required per-run evidence

Each run must preserve:

- seed;
- base/effective configuration fingerprints;
- scenario and scenario parameters;
- Engine hash;
- execution timestamp;
- final CAU count;
- final Gini;
- gate efficiency;
- failure rate;
- total artifacts;
- detected agents;
- isolated agents;
- equilibrium metrics;
- complete metric trajectory required by the experiment;
- artifact digest.

### 2.5 Required aggregate analysis

Before interpretation, compute:

- count of valid runs;
- mean;
- standard deviation;
- variance;
- coefficient of variation where defined;
- minimum/maximum;
- predefined outlier indicator;
- per-metric distribution summary.

For a zero mean, CV must be represented using the predefined edge-case rule rather than division by zero. For zero variance, the result must remain explicitly distinguishable from missing data.

### 2.6 O1 validation predicates

The independent validator must evaluate at minimum:

```text
O1-01 planned_seed_set == executed_seed_set
O1-02 seed_values_are_unique
O1-03 base_configuration_is_constant
O1-04 effective_fingerprints_reproduce
O1-05 engine_hash_is_consistent
O1-06 required_metrics_present_for_all_runs
O1-07 aggregate_statistics_reproduce_from_run_artifacts
O1-08 statistical_edge_cases_follow_declared_rules
O1-09 artifact_digests_validate
O1-10 v0.4_regression_suite_passes
```

### 2.7 O1 negative cases

Each case must be demonstrated to produce a validation failure:

```text
O1-N01 missing seed
O1-N02 duplicate seed
O1-N03 unexpected seed
O1-N04 configuration fingerprint mismatch
O1-N05 engine hash mismatch
O1-N06 missing metric
O1-N07 altered metric
O1-N08 malformed numeric metric
O1-N09 inconsistent aggregate statistic
O1-N10 altered artifact digest
```

### 2.8 O1 interpretation boundary

Passing O1 establishes that the defined multi-seed experiment was executed and independently validated according to contract. It does not, by itself, establish universal, population-level, or scientific robustness.

## 3. O2 — CAU Identity-Level Evidence Verification

### 3.1 Identity contract

The implementation must declare:

- identifier format: current candidate `CAU-######`;
- uniqueness scope: the declared execution artifact unless a broader scope is explicitly specified;
- lifecycle: creation through all exported lifecycle/provenance references;
- reuse policy: reuse prohibited within the declared uniqueness scope;
- collision policy: any duplicate identity is a validation failure.

The final identity contract must be frozen before implementation.

### 3.2 Required identity evidence

For every exported CAU, preserve at minimum:

- `cau_id`;
- `actor_id`;
- action;
- verdict;
- timestamp;
- level;
- provenance linkage;
- deterministic representation used for integrity binding.

The aggregate `cau_records` count remains mandatory as a cross-check.

### 3.3 O2 validation predicates

```text
O2-01 every_identity_matches_declared_format
O2-02 identities_are_unique_within_declared_scope
O2-03 identity_count == aggregate_cau_records
O2-04 every_identity_maps_to_one_record
O2-05 every_record_has_required_identity_fields
O2-06 lifecycle_links_resolve
O2-07 provenance_links_resolve
O2-08 duplicate_or_collision_is_detectable
O2-09 identity_evidence_is_integrity_bound
O2-10 v0.4_provenance_and_regression_checks_pass
```

### 3.4 O2 negative cases

Each case must produce a validation failure:

```text
O2-N01 duplicate cau_id
O2-N02 missing cau_id
O2-N03 malformed cau_id
O2-N04 aggregate/identity count mismatch
O2-N05 identity without provenance linkage
O2-N06 dangling provenance reference
O2-N07 lifecycle inconsistency
O2-N08 altered identity record after manifest creation
O2-N09 collision/reuse violation
O2-N10 identity evidence omitted from integrity boundary
```

### 3.5 O2 interpretation boundary

Passing O2 establishes identity-level evidence integrity and independent verifiability. It does not establish CAU behavioral correctness, quality, causality, or system-level effectiveness.

## 4. Cross-Objective Preservation Tests

Both objectives must preserve:

```text
P-01 v0.4 artifact contract
P-02 SHA-256 / manifest integrity
P-03 provenance invariant
P-04 independent validation architecture
P-05 existing regression suite
P-06 release/execution traceability
```

Any preservation failure blocks candidate-baseline consideration.

## 5. Execution Order

```text
Freeze Test Contract
        ↓
Implement O1
        ↓
Run O1 Negative + Positive Validation
        ↓
Freeze O1 Evidence
        ↓
Implement O2
        ↓
Run O2 Negative + Positive Validation
        ↓
Run Cross-Objective Preservation Tests
        ↓
Evidence Interpretation
        ↓
Candidate Baseline Gate
```

## 6. Stop Conditions

Implementation must stop and return to design review if:

- v0.4 semantics must be changed to satisfy an objective;
- required evidence cannot be preserved independently;
- validator independence is compromised;
- integrity/provenance contracts cannot be maintained;
- an acceptance predicate cannot be made reproducible;
- a new claim is required that exceeds the approved objective scope.

## 7. Authorization Boundary

This specification freezes the test contract for O1/O2. It authorizes implementation planning against these predicates. It does not authorize merging implementation code or declaring a v0.5 baseline.
