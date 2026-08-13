# Gate 2 Protocol — Reproducibility and Atomic Variability Characterization

**Status:** DRAFT / PRE-REGISTRATION
**Gate:** 2
**Phase:** G2-0 Planning
**Baseline:** `v0.5.0` / `de7d11ed9457ede84c1954aa70a59331bf07b72e`
**Execution permitted:** NO

## 1. Governing principle

**Principle Zero:** ACAA must not grow faster than its evidence.

Gate 2 is an evidence-generating experiment. No Gate-2 result, hypothesis promotion, execution count, or PASS status is established by this document alone.

The v0.5.0 baseline is immutable. Gate 2 may observe, execute, and analyze the declared method; it may not modify the baseline implementation, tag, or historical Gate-1 evidence.

## 2. Research question

Can the declared v0.5.0 method be characterized for repeatability and seed-associated variability under a preregistered, multi-seed, repeated-execution design, with all acceptance and falsification rules fixed before execution?

### Subquestions

- S1: What is the within-condition variability under repeated executions?
- S2: What component of observed variability is associated with seed/condition differences?
- S3: Are observed distributions and outliers compatible with the preregistered model assumptions?
- S4: Are the primary metrics sufficiently defined and measured to support the stated characterization?

## 3. Hypotheses

### H-003 — Reproducibility Characterization

The v0.5.0 method exhibits measurable repeatability under the declared execution conditions, and its variability can be quantified with preregistered metrics and uncertainty estimates.

**Epistemic state before execution:** `PROPOSED`.

### H-004 — Atomic Variability Characterization

Variability attributable to execution-level conditions, including seed, can be identified and statistically characterized without changing the frozen method.

**Epistemic state before execution:** `PROPOSED`.

Neither hypothesis may become `SUPPORTED` or `DEMONSTRATED` until the corresponding evidence exists and the Gate-2 decision is independently reviewed.

## 4. Experimental unit and design

The atomic experimental unit is one complete execution of the frozen v0.5.0 method under one declared seed and one declared execution condition.

The proposed design is:

- 11 seed conditions total: 1 fixed reference seed + 10 pre-registered non-reference seeds.
- 3 repeated executions per seed condition.
- Planned total: 33 atomic executions.

The number 33 is a **planned sample size**, not evidence that 33 executions have occurred.

### Randomization

Seed values must be frozen before execution. No seed may be added, removed, or replaced after seeing outcome data. Execution order must be recorded. If execution order is randomized, the randomization procedure and resulting order must be committed before the first run.

## 5. Controlled variables

- Frozen baseline commit/tag.
- Input dataset and input hashes.
- Container/image identity and digest.
- Runtime/toolchain versions.
- Protocol version.
- Seed registry.
- Execution configuration.

Any deviation must be recorded before interpreting affected results.

## 6. Primary and secondary metrics

Metrics must be machine-readable and derived from immutable raw outputs/logs.

### Primary metric

`M-P1` shall be the principal declared output-consistency metric. Its exact formula, units, valid range, and extraction procedure must be fixed in `METRIC_SPECIFICATION.md` before execution.

### Secondary metrics

- `M-001`: time-to-completion.
- `M-002`: peak memory usage.
- `M-003`: output consistency.
- `M-004`: step-level variability.
- `M-005`: protocol-defined quality score, only if a deterministic scoring rule is available before execution.

No metric may be retroactively selected as primary because it produces a favorable result.

## 7. Statistical analysis plan

The primary analysis is descriptive and variance-decomposition oriented. Inferential tests are secondary and must not substitute for direct reporting of effect sizes and uncertainty.

Planned analyses include:

- within-seed repeatability;
- between-seed variability;
- total variability;
- confidence intervals where assumptions permit;
- hierarchical/mixed-effects variance decomposition where identifiable;
- outlier analysis under the predeclared rule;
- sensitivity analysis with and without retained outliers.

Normality tests such as Shapiro-Wilk are diagnostic, not proof of normality. Levene/Brown-Forsythe-type variance tests are diagnostic. ANOVA/Friedman or other inferential tests may be used only where their assumptions and pairing structure are appropriate and must not be treated as automatic acceptance criteria.

## 8. Acceptance framework

Acceptance thresholds are frozen in `ACCEPTANCE_CRITERIA.md` before execution.

The protocol distinguishes:

- **Hard criteria:** required for a Gate-PASS decision.
- **Diagnostic/soft criteria:** informative and reported separately; failure does not automatically equal Gate failure unless explicitly designated as a hard criterion before execution.

A Gate-PASS cannot be inferred from an aggregate score or from a subset of favorable metrics.

## 9. Falsification

Falsification conditions are frozen in `FALSIFICATION_RULES.md` before execution. At minimum, the analysis must address:

- excessive execution failure;
- excessive primary-metric variability;
- structural/non-random outliers;
- material variance-model violations;
- unexplained systematic variation;
- toolchain or provenance failures.

Falsification is evaluated against the hypothesis-specific rule, not by post-hoc threshold selection.

## 10. Evidence contract

Required evidence classes are defined in `EVIDENCE_CONTRACT.md`.

The evidence chain must preserve:

`Protocol → Inputs → Seed Registry → Execution Manifest → Raw Outputs/Logs → Derived Metrics → Validation → Analysis → Report → Decision`

Raw evidence is immutable after execution. Derived documents may be generated post-run only under explicit provenance and versioning rules.

## 11. Reconciliation policy

Post-run reconciliation is allowed for documentation and derivation only when:

1. the underlying raw evidence remains preserved;
2. the change is traceable;
3. the original artifact is not overwritten;
4. the reason for reconciliation is recorded;
5. the reconciliation does not change a pre-registered criterion or threshold;
6. any protocol ambiguity discovered before execution is resolved by a versioned protocol amendment and a new freeze before execution.

Reconciliation cannot convert absent raw evidence into observed evidence and cannot retroactively change the experimental design.

## 12. Independent validation

Execution, validation, and Gate evaluation are logically separate roles. If one person performs more than one role, the overlap and timing must be disclosed.

Validation must independently verify:

- protocol/baseline identity;
- seed registry;
- artifact completeness;
- metric derivation;
- statistical calculations;
- provenance integrity.

## 13. Freeze rule

This protocol is not executable until:

- all referenced specifications exist;
- seed policy is complete;
- acceptance and falsification rules are complete;
- evidence contract is complete;
- a formal review is recorded;
- the final protocol commit is identified;
- a Gate-2 protocol tag is created.

After freeze, changes require an explicit versioned amendment. No silent edits are permitted.

## 14. Scope boundary

A successful Gate 2 would support a bounded characterization of the declared v0.5.0 method under the tested conditions. It would not establish universal reproducibility, scientific generalizability, or robustness outside the declared protocol scope.

## 15. Current decision

**G2-0:** `IN PROGRESS`

**Execution:** `PROHIBITED`

**H-003:** `PROPOSED`

**H-004:** `PROPOSED`
