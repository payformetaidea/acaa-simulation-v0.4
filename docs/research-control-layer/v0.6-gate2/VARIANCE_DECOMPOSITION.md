# Gate 2 Variance Decomposition

**Status:** TEMPLATE / NO RESULTS

No Gate-2 execution result is present in this document.

## Design

`S=11` seeds × `n=3` repeats; response `y_sj = M-P1(run)`.

## Estimators

```text
MS_W = (1/(S(n−1))) ΣΣ (y_sj − ȳ_s)²
MS_B = (n/(S−1)) Σ (ȳ_s − ȳ)²

df_W = 22
df_B = 10

σ̂²_W = MS_W
σ̂²_B,raw = (MS_B − MS_W)/n
σ̂²_B,reported = max(0, σ̂²_B,raw)
σ̂²_total = σ̂²_W + σ̂²_B,reported

ICC = σ̂²_B,reported / (σ̂²_B,reported + σ̂²_W)
```

The signed raw estimator must always be preserved. A negative raw estimate indicates `MS_B < MS_W`; it is not proof of zero true variance.

## CV outputs

```text
CV_within  = sqrt(MS_W) / ȳ
CV_total   = sqrt(σ̂²_total) / ȳ
CV_between = SD(ȳ_s) / ȳ
```

If `ȳ = 0`, CVs are undefined and no CV-based decision is permitted.

## H-004 permutation analysis

```text
T = MS_B / MS_W
B = 9999
p = (#{T_perm >= T_obs}+1)/(B+1)
```

Seed labels are permuted while preserving 11 labels × 3 observations. H-004 is non-directional in Gate 2.

## Uncertainty

Report point estimates and confidence intervals where model assumptions permit. With `n=3`, uncertainty is expected to be wide. No population-level generalization beyond the declared seed set is allowed.

## Required output table

| Quantity | Result |
|---|---|
| MS_W | NOT AVAILABLE |
| MS_B | NOT AVAILABLE |
| σ̂²_W | NOT AVAILABLE |
| σ̂²_B,raw | NOT AVAILABLE |
| σ̂²_B,reported | NOT AVAILABLE |
| σ̂²_total | NOT AVAILABLE |
| ICC | NOT AVAILABLE |
| CV_within | NOT AVAILABLE |
| CV_between | NOT AVAILABLE |
| CV_total | NOT AVAILABLE |
| Permutation p | NOT AVAILABLE |

## Decision

`NOT EVALUATED — NO GATE-2 RESULTS VERIFIED`
