# H-AICR v0.3.5 — G0 Execution Preregistration

**Status:** G0 CANDIDATE — BLOCKERS RESOLVED FOR FREEZE REVIEW  
**Date:** 2026-08-13  
**Parent protocol:** H-AICR v0.3.4  
**Parent baseline:** ACAA v0.5.0 (`de7d11ed9457ede84c1954aa70a59331bf07b72e`)

## 1. Scope

This manifest closes the two explicit G0 blockers identified in the v0.3.4 freeze audit:

1. H-AICR-003 Graph Edit Distance operation weights.
2. H-AICR-007 Incentive Compatibility operational criterion.

It does not alter the frozen ACAA v0.5.0 semantics. It also does not constitute empirical validation of any H-AICR hypothesis.

## 2. H-AICR-003 — Graph Edit Distance Costs

### 2.1 Primary cost model

Because the literature defines GED as a minimum-cost edit path and permits operation-specific costs, but does not provide a universal domain-independent weighting scheme, the primary H-AICR cost model uses **unit costs**. This avoids introducing unsupported semantic importance weights into the primary endpoint. citeturn0search0turn0search1

| Operation | Frozen primary cost |
|---|---:|
| node_addition | 1.0 |
| node_deletion | 1.0 |
| edge_addition | 1.0 |
| edge_deletion | 1.0 |
| attribute_change | 1.0 |
| type_change | 1.0 |

Costs are symmetric for corresponding insertion/deletion operations.

### 2.2 Rationale

- Classical GED formulations permit operation-specific costs but do not prescribe a universal set of values.
- Unit costs provide the most transparent and reproducible primary specification when no validated H-AICR domain calibration exists.
- Domain-specific weighting is therefore excluded from the primary endpoint rather than presented as an empirical fact.

### 2.3 Sensitivity analysis

A secondary sensitivity analysis will evaluate the following pre-specified alternatives without changing the primary endpoint:

- `S1_EQUAL`: all costs = 1.0.
- `S2_STRUCTURAL`: node add/delete = 2.0; edge add/delete = 1.0; attribute change = 0.5; type change = 1.5.
- `S3_ATTRIBUTE_HEAVY`: node add/delete = 1.0; edge add/delete = 1.0; attribute change = 1.5; type change = 1.5.

Sensitivity results are reported separately. No alternative weighting may replace the primary unit-cost result after outcome inspection.

### 2.4 Implementation constraint

The execution engine must store the complete edit operation sequence and the cost contribution of every operation. A scalar GED value without its operation-level provenance is insufficient evidence for H-AICR-003.

## 3. H-AICR-007 — Incentive Compatibility

### 3.1 Operational definition

For this experiment, incentive compatibility is defined as **strategy-proofness with respect to the pre-registered manipulation action space**: an honest contribution strategy must weakly maximize the participant's experimental utility against every admissible strategic alternative.

This follows the standard mechanism-design notion that truthful behavior is a dominant strategy when no alternative report/action can improve the agent's utility, holding other agents' behavior fixed. citeturn0search36turn0search37

### 3.2 Experimental utility

For participant `i` and strategy `s`:

`U_i(s) = normalized_token_value_i(s) - normalized_action_cost_i(s)`

The token-value conversion and action-cost normalization are fixed before the experiment and are external to the H-AICR measurement score.

### 3.3 Strategy space

The execution harness will enumerate the pre-registered manipulation classes:

1. honest contribution;
2. redundant contribution inflation;
3. low-value high-volume spam;
4. strategic correction inflation;
5. provenance manipulation;
6. Sybil-assisted contribution splitting, where the threat condition permits it.

The honest strategy is compared against every admissible strategic alternative under matched task conditions.

### 3.4 Primary IC estimand

For each participant/task condition:

`regret_i = max_s U_i(s) - U_i(honest)`

where `s` ranges over admissible strategic alternatives.

Two complementary measures are reported:

- **IC violation rate:** proportion of participant/task cases where `regret_i > ε`.
- **Maximum normalized regret:** `max(regret_i)` over the evaluation set.

### 3.5 Frozen tolerance and decision rule

`ε = 0.05` normalized utility units.

**PASS:**
- IC violation rate `≤ 5%`, and
- maximum normalized regret `≤ 0.05`.

**FAIL:**
- IC violation rate `> 5%`, or
- maximum normalized regret `> 0.05`.

These are **pre-registered design criteria**, not empirical facts or literature-derived universal thresholds.

### 3.6 Independence constraint

The IC decision must be evaluated independently from the metric used to generate token eligibility. Fairness, concentration, and noise-sensitivity metrics remain separate endpoints.

### 3.7 Falsification and interpretation

A failure establishes that the tested mapping is not incentive-compatible under the tested action space and utility specification. It does not establish that every possible token mapping is incentive-incompatible.

## 4. G0 freeze conditions

G0 may be marked PASS only if:

- this manifest is committed before primary execution;
- H-AICR-003 primary costs are unchanged after outcome inspection;
- H-AICR-007 strategy space, utility, epsilon, estimands, and thresholds are unchanged after outcome inspection;
- dataset split, model revision, dependencies, random seeds, and statistical tests are locked;
- the machine-checkable harness preregistration passes;
- the ACAA v0.5.0 baseline remains untouched.

## 5. Evidence status

This document establishes **design decisions**, not empirical evidence. H-AICR-003 and H-AICR-007 remain `HYPOTHESIS`/`PROPOSED_CONSTRUCT` until execution and independent validation are completed.
