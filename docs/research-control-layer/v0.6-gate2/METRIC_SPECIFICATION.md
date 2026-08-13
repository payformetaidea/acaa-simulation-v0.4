# Gate 2 Metric Specification

**Status:** DRAFT / PRE-REGISTRATION

## Rule

No metric becomes an acceptance metric merely because it is convenient to compute. Every metric must have a fixed definition, unit, extraction rule, validity rule, and provenance path before execution.

## Metrics

| ID | Metric | Status | Required definition before freeze |
|---|---|---|---|
| M-P1 | Primary output-consistency metric | REQUIRED | exact formula, denominator, tolerance, units, valid range |
| M-001 | Time-to-completion | REQUIRED | start/stop events, clock source, units |
| M-002 | Peak memory | REQUIRED if observable | sampling method, units, process scope |
| M-003 | Output consistency | REQUIRED | deterministic comparison rule |
| M-004 | Step variability | REQUIRED if step logs exist | event definition and aggregation |
| M-005 | Quality score | OPTIONAL | deterministic scoring rubric fixed pre-run |

## Derived variability statistics

For each quantitative metric where meaningful:

- mean;
- median;
- standard deviation;
- coefficient of variation (CV), with denominator explicitly stated;
- range;
- IQR;
- confidence interval where justified;
- within-seed and between-seed components where identifiable.

## Important restriction

Thresholds such as `CV <= 5%` are not valid acceptance criteria until frozen in `ACCEPTANCE_CRITERIA.md`. Diagnostic values must not be silently promoted to acceptance criteria after observing data.

## Data-quality rules

Missing, undefined, infinite, or non-comparable metric values must be reported explicitly. They may not be silently dropped.
