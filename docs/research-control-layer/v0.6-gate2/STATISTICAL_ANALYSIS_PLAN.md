# G2-0.4 — Statistical Analysis Plan

**Status:** DRAFT / PRE-REGISTRATION
**Design:** `S=11` seeds, `n=3` repeats, `N=33` planned executions

## 1. Notation

`y_sj = M-P1(run)`; `ȳ_s` = seed mean; `ȳ` = grand mean.

Balanced one-way random-effects model:

```text
y_sj = μ + α_s + ε_sj
α_s ~ (0, σ²_B)
ε_sj ~ (0, σ²_W)
```

The model is an estimative characterization tool. No causal interpretation is permitted.

## 2. Variance estimands

```text
MS_W = (1/(S(n−1))) ΣΣ (y_sj − ȳ_s)²       df_W = 22
MS_B = (n/(S−1)) Σ (ȳ_s − ȳ)²              df_B = 10

σ̂²_W = MS_W
σ̂²_B,raw = (MS_B − MS_W)/n
σ̂²_B,reported = max(0, σ̂²_B,raw)
σ̂²_total = σ̂²_W + σ̂²_B,reported
```

Both the raw signed estimator and the reported non-negative estimator are binding outputs. A negative raw estimate means `MS_B < MS_W`; it is not proof that the true between-seed variance is zero. The reported component obeys the parameter constraint `σ²_B ≥ 0`.

## 3. ICC

```text
ICC = σ̂²_B,reported / (σ̂²_B,reported + σ̂²_W)
```

Interpretation: proportion of **modeled** variance attributable to between-seed differences. If `σ̂²_B,reported = 0`, ICC is 0 and means no between-seed variance was detected above within-seed noise; it does not prove absence of an unobserved seed effect.

## 4. CV estimands

```text
CV_within  = sqrt(MS_W) / ȳ
CV_total   = sqrt(σ̂²_total) / ȳ
CV_between = SD(ȳ_s) / ȳ
```

If `ȳ = 0`, all CV quantities are `UNDEFINED / ZERO_DENOMINATOR` and no CV-based decision is permitted.

## 5. Uncertainty

For `σ²_W`, use the exact chi-square interval where the model assumptions are declared adequate:

```text
[df_W·MS_W / χ²_(1−α/2), df_W·MS_W / χ²_(α/2)]
```

For ICC, report the exact balanced one-way random-effects F-based interval where applicable. Confidence intervals must always be reported with the point estimate and assumptions.

Because `n=3` per seed, seed-level SD/CV estimates have low precision and potentially wide uncertainty. No population-level generalization beyond the declared seed set is allowed.

## 6. H-004 variance-component permutation test

H-004 is direction-neutral with respect to the direction of seed effects. Its variance-component alternative is one-sided at the boundary zero:

```text
H0: σ²_B = 0
H1: σ²_B > 0
```

Test statistic:

```text
T = σ̂²_B,reported / σ̂²_W
  = max(0, (MS_B − MS_W)/n) / MS_W
  = max(0, F − 1) / 3

where F = MS_B / MS_W and n = 3.
```

Permutation procedure:

1. preserve the 33 observed M-P1 values;
2. permute the observed values into 11 balanced seed groups of 3, preserving group size;
3. recompute `MS_B`, `MS_W`, `σ̂²_B,reported`, and `T` for each permutation using the same non-negativity constraint;
4. use `B=9999` permutations;
5. compute `p = (count(T_perm >= T_obs)+1)/(B+1)`;
6. compare with the frozen `α = 0.05` in `ACCEPTANCE_CRITERIA.md`.

A result with `p < 0.05` supports `σ²_B > 0` under the declared protocol and may yield `H-004 = DEMONSTRATED`, subject to all Gate criteria. A result with `p ≥ 0.05` yields `H-004 = NOT DEMONSTRATED`; it does not establish `σ²_B = 0`.

No signed-effect falsification rule is active in the current 11×3 design. A future perturbation-arm experiment may define a separate signed contrast, but that is outside this protocol.

## 7. Three-layer separation

```text
ESTIMATION      → point estimates + uncertainty
HYPOTHESIS TEST → permutation p-value for H-004
DECISION RULE   → frozen Acceptance Matrix
```

A p-value is not a Gate decision. A decision tier is not a p-value.

## 8. Outliers and sensitivity

Primary analysis retains all observations. Outlier detection follows `OUTLIER_ANALYSIS.md`. Any permitted exclusion is a separate sensitivity analysis and must preserve the primary result unchanged in the evidence record.

## 9. Diagnostics

Normality and variance diagnostics are descriptive checks. Failure of a diagnostic does not automatically falsify a hypothesis. Model suitability, robust alternatives, and limitations must be documented before any inferential conclusion.

## 10. Binding limitations

- `n=3` repeats per seed limits precision.
- `S=11` limits between-seed inference.
- `N=33` is exploratory characterization, not confirmatory population inference.
- Results apply only to the frozen v0.5.0 method and declared execution conditions.
- Evidence of `σ²_B > 0` does not establish causality, universal seed effects, or generalization beyond the registered seed set.
- Failure to demonstrate `σ²_B > 0` does not establish `σ²_B = 0`.
