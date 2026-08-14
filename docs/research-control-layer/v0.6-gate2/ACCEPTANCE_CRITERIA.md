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

Gate 2 PASS requires all hard criteria to pass, evidence integrity to pass, and independent validation to pass. MARGINAL or sensitive results cannot be silently converted to PASS. No aggregate score may compensate for a failed hard criterion.

## Interpretation classes

- `PASS` = criterion satisfied.
- `MARGINAL` = intermediate state requiring Formal Protocol Review.
- `FAIL` = hard criterion not satisfied.
- `NOT EVALUATED` = evidence integrity or identifiability prevents valid judgment.
- `NOT DEMONSTRATED` = evidence was evaluable but insufficient to support the hypothesis.
- `FALSIFIED` = frozen hypothesis-specific condition actively contradicts the hypothesis.
