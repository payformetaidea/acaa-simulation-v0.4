# Gate 2 Acceptance Criteria

**Status:** DRAFT / PRE-REGISTRATION
**Binding only after protocol freeze**

## AC-001 — Execution analyzability

`Success Rate = N_valid / N_planned`, with `N_planned = 33`.

| Tier | Valid runs | Rate | Interpretation |
|---|---:|---:|---|
| PASS | 32–33 | ≥ 0.9697 | analyzable execution set |
| MARGINAL | 30–31 | 0.9091–0.9394 | review required; H-003 not demonstrated |
| FAIL | ≤29 | < 0.9091 | insufficient analyzable execution set |

For hypothesis falsification, F-3.3 is triggered only when `Success Rate < 0.90`. The distinction between the hard Gate tier and the falsification threshold is intentional.

## AC-002 — Total variability

`CV_total ≤ 0.10` → PASS.

`CV_total > 0.10` → H-003 FALSIFIED under F-3.1, subject to evidence integrity and sensitivity rules.

## AC-003 — Within-seed variability

`CV_within ≤ 0.10` → PASS.

`CV_within > 0.10` → H-003 FALSIFIED under F-3.2, subject to evidence integrity and sensitivity rules.

## AC-004 — Between-seed characterization

`CV_between` is reported as a descriptive estimand. `CV_between > 0.10` is a diagnostic threshold for material seed-associated variability; it is **not itself a falsification condition for H-004** under the non-directional Gate-2 ontology.

H-004 is evaluated primarily through the preregistered variance decomposition and permutation test in the SAP.

### H-004 permutation test — frozen parameters

```text
H0: σ²_B = 0
H1: σ²_B ≠ 0
T = MS_B / MS_W
B = 9999 permutations
α = 0.05 (frozen)
p = (count(T_perm ≥ T_obs) + 1) / (B + 1)
```

Decision for the hypothesis test:

- `p < 0.05` → statistically significant evidence against H0; H-004 is **DEMONSTRATED**, subject to all other Gate conditions.
- `p ≥ 0.05` → H-004 is **NOT DEMONSTRATED**; this is never treated as falsification.

The Gate-2 H-004 ontology is non-directional. Directional falsification is deferred to a future perturbation-arm experiment.

## AC-005 — Zero-count

- `μ_s = 0` for one seed → `ZERO_COUNT`, review required.
- `μ_s = 0` for ≥2 seeds → `ZERO_COUNT_SYSTEMATIC`, formal investigation.
- Falsification is possible only if the frozen theoretical expectation explicitly requires non-zero output for every tested seed.
- Otherwise the state is MARGINAL / NOT DEMONSTRATED.

## AC-006 — Evidence integrity

PASS requires complete and traceable E-001 through E-010 evidence appropriate to the execution stage, with no material provenance break.

A material evidence-integrity failure means the affected hypothesis is `NOT EVALUATED`, not falsified.

## AC-007 — Metric determinism

M-P1 extraction must be deterministic and independently reproducible from the immutable manifest using `M-P1-v1.0`. Failure is an evidence/measurement-integrity problem and blocks evaluation.

## AC-008 — Outlier robustness

Primary analysis retains all observations. If a preregistered exclusion is permitted and sensitivity analysis changes the Gate conclusion, the conclusion is `SENSITIVE` and H-003/H-004 remain `NOT DEMONSTRATED` pending further review.

## Gate decision rule

Gate 2 PASS requires all hard acceptance criteria to pass, evidence integrity to pass, independent validation to pass, and both H-003 and H-004 to be evaluable.

For the current Gate-2 characterization:

- `H-003 = DEMONSTRATED` or `FALSIFIED` → H-003 is evaluable; Gate decision follows the frozen hypothesis-specific rules.
- `H-003 = NOT DEMONSTRATED` → H-003 remains evaluable but unsupported; Gate 2 cannot claim H-003 demonstration.
- `H-004 = DEMONSTRATED` → H-004 characterization requirement is satisfied, subject to all other hard criteria.
- `H-004 = NOT DEMONSTRATED` → Gate-2 characterization is incomplete; Gate 2 = `NOT PASS`. H-003 may still be evaluated independently and must retain its own status.
- `H-004 = NOT EVALUATED` → Gate 2 = `NOT PASS` because the required characterization cannot be completed.
- `H-004 = FALSIFIED` → applicable only if a future frozen Gate-2 rule explicitly permits a falsification condition; under the current non-directional ontology no Gate-2 falsification rule exists.

MARGINAL or sensitive results cannot be silently converted to PASS. No aggregate score may compensate for a failed hard criterion.

## Interpretation classes

- `PASS` = criterion satisfied.
- `MARGINAL` = intermediate state requiring Formal Protocol Review.
- `FAIL` = hard criterion not satisfied.
- `NOT PASS` = Gate-level closure condition not satisfied.
- `NOT EVALUATED` = evidence integrity or identifiability prevents valid judgment.
- `NOT DEMONSTRATED` = evidence was evaluable but insufficient to support the hypothesis.
- `FALSIFIED` = frozen hypothesis-specific condition actively contradicts the hypothesis.
