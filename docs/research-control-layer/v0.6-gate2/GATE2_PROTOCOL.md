# Gate 2 Protocol — Reproducibility and Atomic Variability Characterization

**Status:** DRAFT / PRE-REGISTRATION
**Gate:** 2
**Phase:** G2-0 Planning
**Baseline:** `v0.5.0` / `de7d11ed9457ede84c1954aa70a59331bf07b72e`
**Execution permitted:** NO

## 1. Governing principle

**Principle Zero:** ACAA must not grow faster than its evidence.

Gate 2 is an evidence-generating experiment. No Gate-2 result, hypothesis promotion, execution count, or PASS status is established by this document alone.

The v0.5.0 baseline and historical Gate-1 evidence remain immutable.

## 2. Research question

Can the declared v0.5.0 method be characterized for repeatability and seed-associated variability under a preregistered repeated-execution design, with acceptance, falsification, failure, and evidence rules fixed before execution?

## 3. Hypotheses

### H-003 — Reproducibility Characterization

The frozen v0.5.0 method exhibits measurable repeatability under the declared execution conditions and its variability can be quantitatively characterized.

Pre-run state: `PROPOSED`.

### H-004 — Atomic / Seed Variability Characterization

Execution-level variability, including seed-associated variability, can be identified and quantitatively characterized under the declared design.

Pre-run state: `PROPOSED`.

H-004 is **direction-neutral with respect to the direction of seed effects**. Its variance-component alternative is one-sided at the boundary zero:

```text
H0: σ²_B = 0
H1: σ²_B > 0
```

The current design has no perturbation arm and therefore no preregistered signed contrast.

## 4. Experimental design

- 11 seeds: 1 fixed reference + 10 pre-registered non-reference seeds.
- 3 repeats per seed.
- Planned total: 33 atomic executions.
- Atomic unit: one complete execution under one frozen seed/configuration.

`33` is a planned sample size, not evidence of completed execution.

## 5. Controlled variables

- v0.5.0 baseline commit/tag;
- input dataset and hashes;
- runtime/toolchain/container identity;
- protocol version;
- frozen seed registry;
- execution configuration.

Any deviation must be recorded and cannot be silently repaired.

## 6. Metrics

Primary metric: `M-P1`, defined immutably in `METRIC_SPECIFICATION.md` as Atomic CAU Count, algorithm `M-P1-v1.0`.

Secondary metrics may include time-to-completion, peak memory, output consistency, and step-level variability only when their deterministic extraction rules are preregistered.

## 7. Statistical analysis

The binding SAP is `STATISTICAL_ANALYSIS_PLAN.md`.

It defines:

- within-seed and between-seed estimands;
- total variability;
- signed and reported variance estimators;
- ICC;
- CV definitions;
- confidence intervals;
- the H-004 variance-component permutation test with `H0: σ²_B = 0`, `H1: σ²_B > 0`, and `B=9999`;
- diagnostic/model limitations;
- outlier and sensitivity analysis.

Estimation, hypothesis testing, and Gate decision rules are separate layers.

## 8. Acceptance

Binding thresholds are defined in `ACCEPTANCE_CRITERIA.md` and remain frozen before execution.

Hard criteria include execution analyzability, M-P1 variability, evidence integrity, metric determinism, and outlier robustness where applicable.

## 9. Falsification

Hypothesis-specific rules are defined in `FALSIFICATION_RULES.md`.

H-003 has active falsification conditions for excessive variability and severe failure.

H-004 has no active signed-effect falsification pathway in Gate 2. A non-significant result is `NOT DEMONSTRATED`; evidence-integrity failure is `NOT EVALUATED`.

## 10. Failure policy

`FAILURE_POLICY.md` is binding for denominator arithmetic, failure classification, no replacement, no imputation, no silent retry, and zero-count handling.

## 11. Outlier policy

`OUTLIER_ANALYSIS.md` is binding. Detection does not equal exclusion. Primary analysis retains all observations. Any authorized exclusion requires Formal Protocol Review and sensitivity analysis.

## 12. Evidence contract

The canonical evidence IDs are E-001 through E-010 in `EVIDENCE_CONTRACT.md`.

Raw evidence outranks derived summaries. Derived summaries must remain traceable to exact raw artifacts.

## 13. Independent validation

Validation must independently verify:

- baseline/protocol identity;
- seed registry;
- artifact completeness and hashes;
- M-P1 derivation;
- statistical calculations;
- provenance.

Execution, validation, and Gate evaluation are logically separate roles; overlaps must be disclosed.

## 14. Freeze rule

Execution is prohibited until all of the following are satisfied:

1. every referenced specification exists;
2. cross-document consistency check passes;
3. seed registry is complete and frozen;
4. formal review is recorded;
5. final protocol commit is identified;
6. atomic protocol tag is created.

After freeze, no silent edit is permitted. Any binding change requires a versioned amendment and a new freeze before affected execution.

## 15. Atomic freeze package

The package must contain at minimum:

```text
docs/research-control-layer/v0.6-gate2/
├── GATE2_PROTOCOL.md
├── H003_H004_HYPOTHESES.md
├── METRIC_SPECIFICATION.md
├── ACCEPTANCE_CRITERIA.md
├── FALSIFICATION_RULES.md
├── EVIDENCE_CONTRACT.md
├── DECISION_LOG.md
├── SEED_POLICY.md
├── FAILURE_POLICY.md
├── STATISTICAL_ANALYSIS_PLAN.md
├── VARIANCE_DECOMPOSITION.md
├── OUTLIER_ANALYSIS.md
└── FINAL_REPORT.md
```

Atomic tag format:

```text
v0.6-gate2-protocol
```

The tag is created only after formal review and final reconciliation. This document itself does not create the tag.

## 16. Current decision

`G2-0 = IN PROGRESS`

`Protocol Freeze = NO`

`Execution Authorization = NO`

`Gate-2 Evidence = NONE VERIFIED`

`H-003 = PROPOSED`

`H-004 = PROPOSED`
