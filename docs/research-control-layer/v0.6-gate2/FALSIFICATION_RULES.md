# Gate 2 Falsification Rules

**Status:** DRAFT / PRE-REGISTRATION

## Governing distinction

`FALSIFIED ≠ NOT DEMONSTRATED ≠ NOT EVALUATED`.

- **FALSIFIED:** frozen evidence actively contradicts the hypothesis-specific rule.
- **NOT DEMONSTRATED:** evidence is valid but insufficient to support the hypothesis.
- **NOT EVALUATED:** evidence integrity, identifiability, or execution validity prevents a defensible judgment.

## H-003 — Reproducibility Characterization

### F-3.1 — Excessive total variability

```text
CV_total > 0.10
```

under the frozen SAP definition, with valid evidence and no material integrity break → `H-003 = FALSIFIED`.

### F-3.2 — Excessive within-seed variability

```text
CV_within > 0.10
```

under the frozen SAP definition, with valid evidence → `H-003 = FALSIFIED`.

### F-3.3 — Severe execution failure

```text
Success Rate < 0.90
```

→ `H-003 = FALSIFIED`, provided the failure evidence is attributable to the declared execution process rather than an external infrastructure event that invalidates the experiment. Infrastructure invalidation instead yields `NOT EVALUATED` / protocol review.

### F-3.4 — Systematic zero-count

`≥2` seeds with `μ_s = 0` → `ZERO_COUNT_SYSTEMATIC`.

Falsification occurs only if the frozen theoretical expectation explicitly requires non-zero output for every seed. Without such a preregistered expectation → `NOT DEMONSTRATED`.

### F-3.5 — Structural/systematic outlier pattern

Falsification requires all of:

1. a pre-specified structural/systematic pattern under `OUTLIER_ANALYSIS.md`;
2. threshold met: `≥3 seeds` OR `≥30% of runs`;
3. attribution to the method rather than infrastructure;
4. sensitivity analysis materially changes the Gate conclusion.

If infrastructure-attributable → failure/provenance pathway, not falsification.
If sensitivity is robust → report as a methodological note; do not falsify H-003.

## H-004 — Atomic / Seed Variability Characterization

H-004 is direction-neutral with respect to the direction of seed effects. Its variance-component alternative is one-sided at the boundary zero:

```text
H0: σ²_B = 0
H1: σ²_B > 0
```

### F-4.1

No active falsification condition is defined for the variance-component hypothesis in Gate 2. Non-identifiability or model failure is `NOT DEMONSTRATED` or `NOT EVALUATED`, depending on evidence integrity.

### F-4.2

`CV_between > 0.10` is a **diagnostic materiality threshold**, not a falsification rule. A high between-seed CV is evidence of larger seed-associated differences and therefore does not logically contradict the H-004 characterization hypothesis.

### F-4.3

No signed-effect falsification pathway is active in Gate 2. A future perturbation-arm experiment may preregister a signed contrast such as:

```text
Δ = variability(perturbed) − variability(baseline)
```

with a pre-registered minimum effect. Such a rule is outside the current 11×3 design.

## H-004 decision rule in Gate 2

- `p < 0.05` from the preregistered variance-component permutation test → evidence supports `σ²_B > 0`; H-004 may be `DEMONSTRATED`, subject to all Gate criteria.
- `p ≥ 0.05` → `NOT DEMONSTRATED`; this does not establish `σ²_B = 0`.
- Model non-identifiability → `NOT DEMONSTRATED` or `NOT EVALUATED` as specified above.
- The current Gate-2 design contains no active signed-effect falsification pathway for H-004.

## Evidence-integrity override

If raw evidence, provenance, metric extraction, or protocol identity is materially compromised, no hypothesis is falsified on that basis. The appropriate state is `NOT EVALUATED` pending reconciliation.
