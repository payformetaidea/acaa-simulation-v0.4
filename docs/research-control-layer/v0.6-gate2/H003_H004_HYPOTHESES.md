# H-003 / H-004 Hypotheses

## H-003 — Reproducibility Characterization

**Statement:** The frozen v0.5.0 method exhibits measurable repeatability under the declared execution conditions and its variability can be quantitatively characterized.

**Pre-run state:** `PROPOSED`

**Evidence required:** immutable execution evidence, preregistered metrics, independent validation, variance/uncertainty analysis, outlier review, and Gate review.

**Scope:** only the frozen method and declared Gate-2 conditions.

## H-004 — Atomic / Seed Variability Characterization

**Statement:** Execution-level variability, including seed-associated variability, can be identified and quantitatively characterized under the declared Gate-2 design.

**Pre-run state:** `PROPOSED`

**Ontology:** Direction-neutral with respect to the direction of seed effects. The variance-component alternative is one-sided at the boundary zero.

```text
H0: σ²_B = 0
H1: σ²_B > 0
```

The 11×3 design has no perturbation arm and therefore no natural signed contrast. A future perturbation-arm experiment may address directional/signed effects; that is outside the present Gate-2 hypothesis.

**Evidence required:** frozen seed registry, repeated executions, validated metric extraction, variance decomposition, permutation analysis, outlier analysis, and independent review.

## Epistemic state policy

`PROPOSED → SUPPORTED → DEMONSTRATED` is evidence-gated.

No transition occurs merely because an experiment was planned, executed, or documented.

For H-004 in Gate 2, a non-significant permutation result yields `NOT DEMONSTRATED`; it does not establish `σ²_B = 0`.

Historical Gate-1 states are unaffected.
