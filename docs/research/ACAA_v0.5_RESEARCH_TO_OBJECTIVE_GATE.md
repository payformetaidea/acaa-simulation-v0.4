# ACAA v0.5 — Research → Objective Gate

**Status:** Governance Artifact — Draft for Review  
**Baseline:** ACAA v0.4 Frozen Validated Baseline  
**Repository:** `payformetaidea/acaa-simulation-v0.4`  
**Baseline Release Commit:** `239fd30de9e9c22b8f3bab0303250cfa98774696`  
**Validated Execution Commit:** `50892a3be4bf05b54283514ccc6fd4798703aa35`  
**Gatekeeper Decision:** PASS — 2026-08-11  

## 1. Purpose

This document defines the decision boundary between the v0.4 **Knowledge Domain** and the v0.5 **Design Domain**.

A Research Opportunity becomes an Objective Candidate only when its evidence lineage, research question, experimental design, measurements, acceptance criteria, and validation relevance are sufficiently specified.

This artifact authorizes **no implementation**.

## 2. Decision Model

```text
v0.4 Frozen Validated Baseline
        ↓
Evidence
        ↓
Interpretation
        ↓
Knowledge Gap
        ↓
Research Opportunity
        ↓
Research Definition
        ↓
RESEARCH → OBJECTIVE GATE
        ↓
 ┌──────────┬──────────┬──────────┐
 │ ACCEPT   │ REFINE   │ DEFER    │
 └────┬─────┴────┬─────┴────┬─────┘
      ↓          ↓          ↓
 Objective    Research    Research
 Candidate     Track       Backlog
      ↓
 v0.5 Evolution Gate
      ↓
 Approved Objective
      ↓
 Controlled Implementation
```

## 3. Epistemic Boundary

```text
Research Opportunity
        ≠
Research Experiment
        ≠
Objective Candidate
        ≠
Approved Objective
        ≠
Implementation Task
```

`ACCEPT` at this Gate means **Objective Candidate**, not approved implementation scope. Final approval remains with `ACAA_v0.5_EVOLUTION_GATE.md`.

## 4. Gate Entry Requirements

A candidate must document:

1. exact v0.4 evidence source;
2. established claim;
3. non-claim;
4. knowledge gap;
5. testable research question;
6. required evidence;
7. reproducible experimental design;
8. measurement plan;
9. predefined acceptance criteria;
10. expected Engine / Validator / Evidence Contract / documentation impact;
11. independent validation path;
12. preservation requirements for the v0.4 integrity chain.

Missing material requirements result in `REFINE`.

## 5. Repository Evidence Used for the Decision

The analysis was performed against the frozen v0.4 Engine, independent validator, Gatekeeper record, and preserved independent execution artifact.

The independent execution artifact is from run `31516580718`, with digest:

`sha256:6d8916c386b569a930f436a85065955123bb669e34c1e9d83ada16a65bbd99bb`

The validator is explicitly independent of Engine execution: it validates the artifact set without importing or executing the Engine.

The v0.4 validator checks artifact presence, manifest integrity, schema, sensitivity structure, multi-seed record presence, regression summary, equilibrium, attack-response event existence, provenance count equality, an architecture-level CAU criterion, and adaptive-event existence.

## 6. R1 — Robustness Characterization

### v0.4 evidence

V7 contains three baseline seed executions: `42`, `137`, and `256`. The Engine also contains multi-seed execution and configured candidate CV thresholds (`cv_cau_threshold=0.05`, `cv_gini_threshold=0.01`). The validator only verifies that the three required seed records are present.

The preserved artifact shows the following final outcomes:

| Metric | Seed 42 | Seed 137 | Seed 256 |
|---|---:|---:|---:|
| CAU records | 1936 | 2466 | 1685 |
| Gini | 0.0 | 0.0 | 0.0 |
| Gate efficiency | 0.142420 | 0.299367 | 0.125586 |
| Failure rate | 0.291667 | 0.327059 | 0.380000 |
| Total artifacts | 1200 | 1700 | 1000 |
| Detected agents | 87 | 82 | 88 |

The observed CV of final CAU count across these three seeds is approximately `0.16045`. This establishes measurable seed-dependent variation. It does not establish a scientifically validated robustness threshold.

### Decision

**ACCEPT → Objective Candidate**

### Objective Candidate

**Formalize and independently validate multi-seed behavioral characterization without equating seed coverage with robustness.**

### Experimental design

- Freeze the v0.4 configuration and scenario.
- Use a preregistered seed set larger than the existing three-seed smoke check; initial target: at least 12 independent seeds.
- Verify identical configuration fingerprints across runs.
- Record final and trajectory-level CAU count, failure rate, gate efficiency, total artifacts, detection/isolation counts, equilibrium, variance, and outliers.
- Report mean, standard deviation, CV where mathematically meaningful, and run-level distributions.
- Preserve every run as a reproducible evidence package.
- Treat the existing Engine CV thresholds as hypotheses requiring justification, not as established scientific truth.

### Acceptance criteria

The objective succeeds when an independent validator can verify seed coverage, configuration identity, reproducible metric extraction, distributional statistics, explicit zero-mean/zero-variance handling, and a bounded conclusion distinguishing observed variability from a robustness claim.

A finding of high variability is a valid outcome. The objective is characterization, not forced confirmation of robustness.

## 7. R2 — Adaptive Behavior Characterization

### v0.4 evidence

V6 verifies adaptive-event existence. The Gatekeeper reports 91 adaptive events. The Engine records trigger metrics and adjustments, including `avg_failure`, `avg_efficiency`, `gini`, and parameter changes such as `alpha_threshold`.

### Non-claim

Event occurrence does not establish that adaptation caused improvement, degradation, recovery, or any other behavioral effect.

### Decision

**REFINE**

### Required refinement

Define a matched ablation design with adaptation enabled versus disabled under the same seed, scenario, and configuration conditions. Define the causal estimand before execution and specify which behavioral metrics constitute an effect.

R2 remains a Research Opportunity until the counterfactual/ablation contract and acceptance criteria are fixed.

## 8. R3 — Adversarial Effectiveness

### v0.4 evidence

V2 reports 2,589 attack-response events under the validator's event-counting rule. The Engine contains explicit attack injection functions and an observable-only detection layer. Attack events already record fields such as period, type, action, score, threshold, and observable features.

### Non-claim

Event existence does not establish detection recall, false-negative rate, detection latency, response latency, recovery time, false-positive behavior, or systemic impact.

### Decision

**REFINE**

### Required refinement

Define an attack-instance ground-truth contract linking every controlled injected attack to its detection and response outcome. At minimum: attack ID, type, injection time, target, detection time, response time, final state, and TP/FP/FN/TN classification where applicable.

Acceptance thresholds must be attack-class-specific and predefined. Event volume alone cannot become the effectiveness criterion.

## 9. R4 — CAU Identity-Level Verification

### v0.4 evidence

The Engine already creates individual CAU identifiers in `CAURecord` using a sequence such as `CAU-000001`, and the collusion detector operates on individual CAU IDs. The export contract, however, exposes only `cau_records: len(self.ledger)` rather than the individual records or IDs. The independent validator therefore cannot verify identity-level uniqueness from the preserved export.

This is an evidence-boundary gap: identity exists internally and is used by Engine logic, while the exported evidence collapses identity to an aggregate count.

### Decision

**ACCEPT → Objective Candidate**

### Objective Candidate

**Expose and independently validate CAU identity-level evidence while preserving the v0.4 provenance and integrity contract.**

### Experimental / validation design

1. Define the CAU identity contract: format, uniqueness scope, lifecycle, and reuse semantics.
2. Export individual CAU records or a cryptographically bound identity index sufficient for independent verification.
3. Validate identifier format and uniqueness.
4. Validate identity count against `cau_records`.
5. Validate lifecycle, actor/action/timestamp linkage, and provenance linkage.
6. Test unintended duplication or collision.
7. Preserve SHA-256 manifest integrity and existing provenance invariants.
8. Keep the validator independent from Engine execution.

### Acceptance criteria

An independent validator must be able to demonstrate from the preserved artifact alone that every exported CAU identity is unique within the declared scope, traceable to its relevant metadata and provenance chain, and consistent with the aggregate CAU count.

Adding IDs without independent verification is insufficient.

## 10. Cross-Track Decision Matrix

| Track | Decision | Evidence basis | v0.5 role |
|---|---|---|---|
| R1 Robustness | **ACCEPT** | Existing multi-seed execution already exposes measurable variability; missing layer is formal characterization and independent validation. | Objective Candidate |
| R2 Adaptive | **REFINE** | Temporal adaptive evidence exists; causal attribution remains unspecified. | Research Track |
| R3 Adversarial | **REFINE** | Attack injection and detection evidence exist; formal attack-instance outcome linkage is missing. | Research Track |
| R4 CAU Identity | **ACCEPT** | Individual IDs exist internally but are lost at the export/evidence boundary. | Objective Candidate |

## 11. Preserve Requirements

Any v0.5 candidate must preserve:

- artifact contract and required artifact coverage;
- SHA-256 / manifest integrity;
- provenance integrity;
- independent validation architecture;
- existing regression protection;
- bounded Gatekeeper interpretation;
- release and baseline traceability.

## 12. Out-of-Scope Boundary

The following remain outside this Gate unless separately justified by new evidence and governance:

- production deployment;
- broad generalizability claims;
- large-scale real-world deployment;
- scientific validity claims beyond the defined validation scope;
- feature expansion without an evidence trail;
- modification of the frozen v0.4 baseline.

## 13. No-Code Rule

```text
v0.4 source code          FROZEN
v0.4 evidence             PRESERVED
v0.5 implementation       NOT STARTED
v0.5 approved objective   NONE
Objective candidates      R1, R4
```

R1 and R4 are **Objective Candidates only**. They are not approved v0.5 implementation scope.

## 14. Relationship to v0.5 Evolution Gate

Only Objective Candidates that pass this boundary may be evaluated by `ACAA_v0.5_EVOLUTION_GATE.md`.

```text
R1 ACCEPT ─┐
           ├──→ v0.5 Evolution Gate → Approved Scope → Implementation
R4 ACCEPT ─┘

R2 REFINE ─→ Research Track
R3 REFINE ─→ Research Track
```

## 15. Decision Record — 2026-08-12

**Decision boundary:** ACTIVE  
**R1:** ACCEPT → Objective Candidate  
**R2:** REFINE  
**R3:** REFINE  
**R4:** ACCEPT → Objective Candidate  
**Approved v0.5 Objectives:** NONE  
**Code changes authorized by this Gate:** NONE  
**Next governance artifact:** `ACAA_v0.5_EVOLUTION_GATE.md`

This decision supersedes the earlier provisional `4 × REFINE` state in this document and is based on the deeper inspection of the actual v0.4 Engine and preserved execution artifact.

---

**ACAA — Adaptive Cognitive Architecture**  
**v0.5 Governance — Research → Objective Boundary**
