# H-AICR v0.3.5 — G0 Pre-Registration Manifest

**Status:** G0 CANDIDATE — execution lock pending final audit
**Date:** 2026-08-13
**Parent protocol:** H-AICR v0.3.4
**Parent ACAA baseline:** v0.5.0 (`de7d11ed9457ede84c1954aa70a59331bf07b72e`)
**Repository:** `payformetaidea/acaa-simulation-v0.4`

## 0. Purpose

This manifest closes the two unresolved protocol parameters identified in the v0.3.4 freeze audit and records them before execution:

1. H-AICR-003 weighted Graph Edit Distance operation costs.
2. H-AICR-007 operational incentive-compatibility criterion.

No primary test result may be inspected before this manifest is committed. After G0 lock, these parameters are immutable for the registered execution.

## 1. H-AICR-003 — Weighted Graph Edit Distance

### 1.1 Frozen operation weights

| Operation | Weight |
|---|---:|
| Node addition | 2.0 |
| Node deletion | 2.0 |
| Edge addition | 1.0 |
| Edge deletion | 1.0 |
| Attribute change | 0.5 |
| Type change | 0.5 |

The canonical ratio is **Node : Edge : Attribute = 4 : 2 : 1**.

### 1.2 Definition

`GED_weighted = 2.0 * NodeOps + 1.0 * EdgeOps + 0.5 * AttributeOps`

Type changes are encoded as attribute changes in the canonical implementation and therefore carry cost `0.5`. This avoids introducing an additional semantic hierarchy unsupported by the current protocol.

### 1.3 Double-counting control

A node deletion is one node operation. Incident edge deletions are not separately charged when they are mechanically implied by that node deletion. Explicit edge deletions receive edge cost only when they represent an independently evaluated relation change.

### 1.4 Interpretation boundary

The weights are **pre-registered design parameters**, not empirical estimates of semantic importance. They define the evaluation metric for this experiment and do not establish that node changes are universally more valuable than edge or attribute changes.

### 1.5 Sensitivity analysis

A secondary robustness analysis may report normalized GED under equal weights `(1,1,1)` and the frozen hierarchical weights `(2,1,0.5)`. The primary decision uses the frozen hierarchical metric. Sensitivity analysis cannot replace the primary metric or alter the gate decision.

## 2. H-AICR-007 — Incentive Compatibility

### 2.1 Operational criterion

The experimental incentive-compatibility index is:

`IC = mean_credit_honest / mean_credit_strategic`

where the two cohorts are matched on the pre-registered interaction opportunity/exposure schedule.

### 2.2 Primary acceptance criterion

`IC >= 1.25`

In addition, the bootstrap lower confidence bound for the ratio must be above `1.00` at the pre-registered confidence level. This prevents a point estimate from passing solely because of sampling noise.

### 2.3 Unstable denominator rule

If mean strategic credit is zero or numerically negligible relative to the registered credit scale, the ratio is treated as unstable rather than automatically successful. The result is reported as `DENOMINATOR_UNSTABLE` and the raw group distributions are evaluated separately.

### 2.4 Robustness statistics

Report, at minimum:
- mean credit by cohort;
- median credit by cohort;
- IC ratio;
- bootstrap confidence interval for IC;
- distributional concentration metrics already registered under H-AICR-007;
- sensitivity to reasonable strategic-policy perturbations.

### 2.5 Important scope limitation

This operational index is a **behavioral incentive-alignment criterion for the H-AICR experiment**. By itself it does not prove formal game-theoretic incentive compatibility, dominant-strategy truthfulness, or equilibrium existence. Any such claim requires a separate game-theoretic protocol.

## 3. Experimental cohort design

The harness uses controlled cohorts:

- G1 Pure Consumer
- G2 Low Producer
- G3 High Producer
- G4 Iterative Researcher
- G5 Adversarial Spam
- G6 Synthetic AI
- G7 Human Expert

Target: 20 interaction windows per cohort for the initial engineering run. This dataset is a **harness validation dataset**, not automatically a sufficient statistical sample for final scientific claims. Sample-size adequacy must be assessed before confirmatory execution.

## 4. Leakage controls

- user-disjoint train/validation/test manifests;
- locked test identifiers before model fitting;
- deterministic seed recorded;
- no test-derived normalization or feature selection;
- no economic reward during Phase A;
- independent validation artifacts stored separately.

## 5. Execution lock

G0 is considered PASS only when:

- this manifest is committed;
- protocol hash is recorded;
- model/dependency revisions are recorded;
- dataset generation seed is recorded;
- train/validation/test manifests exist;
- the two unresolved parameters above are unchanged;
- the G0 audit explicitly records PASS.

Until those conditions are met, H-AICR remains `PRE-FREEZE`.
