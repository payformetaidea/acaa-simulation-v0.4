# ACAA v0.5 — Research Definition for R1–R4

**Status:** Governance / Analytical Artifact — Draft for Review  
**Baseline:** ACAA v0.4 Frozen Validated Baseline  
**Repository:** `payformetaidea/acaa-simulation-v0.4`  
**Source branch:** `agent/research-to-objective-gate`  

## Purpose

This document records the deeper R1–R4 analysis required by the Research → Objective Gate. It is derived from the frozen v0.4 Engine, independent validator, Gatekeeper decision, and the preserved independent execution artifact.

It does not authorize implementation or modify the v0.4 baseline.

## Evidence examined

- `value_flow_simulator_v0.4.py`
- `independent_validator_v0.4.py`
- `docs/validation/ACAA_v0.4_GATEKEEPER_DECISION_2026-08-11.md`
- Independent execution artifact from run `31516580718`
- Artifact digest: `sha256:6d8916c386b569a930f436a85065955123bb669e34c1e9d83ada16a65bbd99bb`

## R1 — Robustness Characterization

### New evidence interpretation

The v0.4 Engine already defines multi-seed execution for seeds `42`, `137`, and `256`, and the Engine contains candidate CV thresholds (`cv_cau_threshold=0.05`, `cv_gini_threshold=0.01`). The v0.4 validator, however, checks only that the three seed records exist.

The preserved execution artifact shows materially different final outcomes across the three seeds:

| Metric | Seed 42 | Seed 137 | Seed 256 |
|---|---:|---:|---:|
| CAU records | 1936 | 2466 | 1685 |
| Final Gini | 0.0 | 0.0 | 0.0 |
| Gate efficiency | 0.142420 | 0.299367 | 0.125586 |
| Failure rate | 0.291667 | 0.327059 | 0.380000 |
| Total artifacts | 1200 | 1700 | 1000 |
| Detected agents | 87 | 82 | 88 |

The observed coefficient of variation for final CAU count across these three seeds is approximately `0.16045`, while the Engine's configured candidate CAU CV threshold is `0.05`. This is evidence of a measurable robustness question; it is not evidence that the system fails a scientifically established robustness standard, because the threshold has not been validated as a research acceptance criterion.

### Decision

**ACCEPT → Objective Candidate**

### Objective Candidate

**Formalize and independently validate multi-seed behavioral characterization without equating seed coverage with robustness.**

### Experimental design

1. Freeze the v0.4 configuration and scenario definition.
2. Define a preregistered seed set larger than the existing three-seed smoke check; the initial v0.5 experiment should use at least 12 independent seeds.
3. Record the same seed-independent configuration fingerprint for every run.
4. Measure, before interpretation:
   - final CAU count and CV;
   - final and trajectory-level failure rate;
   - gate efficiency;
   - total artifacts;
   - detection/isolation counts;
   - equilibrium metrics;
   - per-period variance and outlier behavior.
5. Report distribution, mean, standard deviation, CV where mathematically meaningful, and run-level outliers.
6. Preserve every run as a reproducible evidence package.
7. Treat the existing `0.05` and `0.01` CV thresholds as hypotheses requiring justification, not as pre-established scientific truth.

### Acceptance criteria

The objective succeeds if the v0.5 validation package can independently establish:

- the exact seed set and configuration identity;
- complete execution coverage for every planned seed;
- reproducible metric extraction;
- predefined distributional and variance statistics;
- explicit handling of zero-variance / zero-mean metrics;
- a bounded conclusion distinguishing observed variability from a robustness claim;
- regression and integrity preservation relative to v0.4.

A result showing high variability remains a valid research outcome. The objective is characterization and validation of the evidence, not forced confirmation of robustness.

## R2 — Adaptive Behavior Characterization

### New evidence interpretation

The Engine records adaptive events with the triggering metrics and parameter adjustments. The preserved baseline artifact contains 91 adaptive events across the v0.4 scenario set. Example events record `avg_failure`, `avg_efficiency`, `gini`, and adjustments such as `alpha_threshold`.

The Engine also records period-level metrics before and after adaptation. This makes temporal analysis possible. It does not provide a counterfactual run in which the same trajectory occurs without adaptation.

### Decision

**REFINE**

### Required refinement

Define a controlled ablation design with adaptation enabled versus disabled under matched seeds, scenarios, and configuration fingerprints. Specify the causal estimand before execution, for example change in failure rate, gate efficiency, or recovery trajectory attributable to adaptation.

Until the counterfactual/ablation design and acceptance criteria are fixed, event counts remain descriptive evidence only.

## R3 — Adversarial Effectiveness

### New evidence interpretation

The Engine contains explicit attack injection functions and an observable-only detection layer. Attack events record useful operational fields such as period, attack type, action, score, threshold, and observable features. The v0.4 artifact contains 2,589 non-rollback attack-response events under the validator's V2 counting rule.

The current evidence still does not establish detection recall, false-negative rate, detection latency, response latency, recovery time, or systemic impact. The event log also does not yet provide a formal attack-instance identifier linking every injected ground-truth attack to its corresponding detection outcome.

### Decision

**REFINE**

### Required refinement

Define an attack-instance ground-truth contract and outcome linkage before implementation. At minimum, each controlled attack instance should have an identifier, injection timestamp, expected target/type, detection timestamp if detected, response timestamp, final state, and explicit classification as TP/FP/FN/TN where applicable.

Acceptance thresholds must be attack-class-specific and defined before execution. Event volume alone must not become the effectiveness criterion.

## R4 — CAU Identity-Level Verification

### New evidence interpretation

The v0.4 Engine already creates individual CAU identifiers in `_make_cau()` using the form `CAU-000001`, `CAU-000002`, etc., and stores them in `CAURecord`. The collusion detector also operates on individual CAU IDs. However, the exported evidence contract exposes only `cau_records: len(self.ledger)` rather than the individual CAU records or their identifiers. The independent validator therefore cannot verify identity-level uniqueness from the preserved export.

This is a stronger and more concrete gap than a request to invent identifiers: the identity capability exists internally while the evidence boundary collapses it to a count.

### Decision

**ACCEPT → Objective Candidate**

### Objective Candidate

**Expose and independently validate CAU identity-level evidence while preserving the v0.4 provenance and integrity contract.**

### Required design

1. Define a CAU identity contract: format, uniqueness domain, lifecycle, and allowed reuse semantics.
2. Export either individual CAU records or a cryptographically bound identity index sufficient for independent verification.
3. Validate:
   - identifier format;
   - uniqueness within the declared scope;
   - identity count equals CAU record count;
   - lifecycle traceability;
   - provenance linkage;
   - absence of unintended duplication/collision.
4. Preserve SHA-256 manifest integrity and existing provenance invariants.
5. Keep validation independent from Engine execution.

### Acceptance criteria

A v0.5 candidate implementation is acceptable only if an independent validator can demonstrate, from the preserved artifact alone, that every exported CAU identity is unique within the declared scope, traceable to its actor/action/timestamp and provenance chain, and consistent with the aggregate CAU count.

Adding an ID field without independent verification does not satisfy this objective.

## Cross-track prioritization

| Track | Decision | Rationale |
|---|---|---|
| R1 Robustness | **ACCEPT** | Existing multi-seed evidence already shows measurable variability and the Engine contains a multi-seed pathway; the missing layer is formal characterization and independent validation. |
| R2 Adaptive | **REFINE** | Temporal evidence exists, but attribution requires matched ablation/counterfactual design. |
| R3 Adversarial | **REFINE** | Detection events and injection mechanisms exist, but attack-instance ground truth and effectiveness metrics are not yet contractually linked. |
| R4 CAU Identity | **ACCEPT** | Individual CAU identity already exists inside the Engine but is lost at the evidence/export boundary; the gap is directly actionable in the validation architecture. |

## Governance conclusion

The deeper repository inspection changes the previous provisional state from `4 × REFINE` to:

```text
R1 Robustness Characterization        ACCEPT → Objective Candidate
R2 Adaptive Behavior Characterization REFINE
R3 Adversarial Effectiveness          REFINE
R4 CAU Identity-Level Verification   ACCEPT → Objective Candidate
```

These are **Objective Candidates**, not yet approved v0.5 Objectives. Approval remains the responsibility of `ACAA_v0.5_EVOLUTION_GATE.md`.

## No-code boundary

No Engine, Validator, v0.4 artifact, release tag, or frozen baseline was changed as part of this analysis.

The next action is to carry only R1 and R4 into the v0.5 Evolution Gate for formal scope approval. R2 and R3 remain in the research-definition track until their experimental controls and acceptance contracts are sufficiently specified.
