# ACAA v0.5 — O1 Independent Evidence Validation

## Purpose

This artifact defines the validation boundary between the controlled O1 implementation and any claim that O1 has passed its validation gate.

The validator is independent of `o1_robustness_v0_5.py`. It consumes the generated run artifacts, recomputes integrity and distributional statistics, reproduces effective-configuration fingerprints from the recorded post-run configuration, and emits a normalized evidence package.

## Validation sequence

```text
O1 Controlled Implementation
        |
        v
Fresh 12-seed execution
        |
        v
Raw run artifacts
        |
        v
Independent Validator
  |-- seed protocol
  |-- configuration integrity
  |-- effective fingerprint reproduction
  |-- engine hash consistency
  |-- required metric integrity
  |-- artifact digest verification
  |-- aggregate-statistic reproduction
  |-- declared statistical edge cases
        |
        v
Independent Evidence Package
        |
        v
O1 Gate Decision
```

## Independence boundary

The independent validator does not import the O1 implementation module or reuse its validation functions. The v0.4 engine is treated as an execution dependency and its SHA-256 is independently compared against every run artifact.

The validator derives `scenario_params`, `metric_trajectory`, and `equilibrium_metrics` from the raw run artifacts at the evidence boundary. These are validation-envelope fields; they do not modify v0.4 engine semantics.

## Gate predicates

| Predicate | Requirement |
|---|---|
| O1-01 | Planned seed set equals executed seed set |
| O1-02 | Seed values are unique |
| O1-03 | Base configuration fingerprint is constant; baseline scenario remains fixed |
| O1-04 | Effective configuration fingerprints are independently reproducible |
| O1-05 | Engine hash is consistent across all runs |
| O1-06 | Required metrics and trajectories are structurally valid |
| O1-07 | Aggregate statistics reproduce from run artifacts |
| O1-08 | Declared zero-mean / zero-variance rules are respected |
| O1-09 | Individual artifact digests verify |
| O1-10 | v0.4 regression / controlled execution succeeds before independent validation |

## Interpretation boundary

A PASS establishes that the defined O1 experiment has been independently checked at the evidence and contract level and that the observed distributional statistics are reproducible from the preserved artifacts.

A PASS does not establish universal robustness, population-level robustness, or scientific validity beyond the approved O1 scope.

## Integrity boundary

- v0.4 engine remains unchanged.
- v0.4 validator remains unchanged.
- O2 remains excluded.
- R2/R3 remain excluded.
- No v0.5 baseline is established by this artifact alone.

## Gate status

**PENDING FRESH CI EXECUTION.**

The gate is considered PASS only when the dedicated `o1_independent_validation.yml` workflow completes successfully and its generated evidence artifact reports all O1-01 through O1-10 as `PASS`.
