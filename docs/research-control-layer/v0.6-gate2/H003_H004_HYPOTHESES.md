# H-003 / H-004 Hypotheses

## H-003 — Reproducibility Characterization

**Statement:** The declared v0.5.0 method has measurable repeatability under fixed execution conditions, and the resulting variability can be quantitatively characterized.

**Pre-registration state:** `PROPOSED`

**Evidence required for promotion:** immutable execution evidence, preregistered metrics, independent validation, variance/uncertainty analysis, and Gate review.

**Scope:** only the frozen method and conditions declared by Gate 2.

## H-004 — Atomic Variability Characterization

**Statement:** Execution-level variability, including seed-associated variability, can be identified and quantitatively decomposed under the declared Gate-2 design.

**Pre-registration state:** `PROPOSED`

**Evidence required for promotion:** frozen seed registry, repeated atomic executions, validated metric extraction, variance decomposition, outlier analysis, and independent review.

**Scope:** only the tested seed and execution conditions.

## Epistemic-state policy

`PROPOSED → SUPPORTED → DEMONSTRATED` is evidence-gated. No transition may be made solely because an experiment was planned, executed, or documented.

`PROPOSED → REJECTED` is permitted when a preregistered falsification condition is satisfied and independently reviewed.

Historical Gate-1 states are unaffected by Gate 2.
