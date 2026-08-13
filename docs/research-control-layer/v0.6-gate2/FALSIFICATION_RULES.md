# Gate 2 Falsification Rules

**Status:** DRAFT / PRE-REGISTRATION

A falsification condition is evaluated against the frozen protocol, not against a threshold chosen after observing outcomes.

## Candidate conditions

1. Execution failure exceeds the predeclared analyzability limit.
2. Primary metric variability exceeds its frozen tolerance.
3. Evidence reveals structural rather than incidental outlier behavior that invalidates the declared model.
4. Variance-model assumptions are materially violated and no preregistered robust alternative is applicable.
5. A systematic toolchain/provenance defect compromises the affected evidence.
6. Required metric extraction is non-deterministic or cannot be independently reproduced.
7. A material protocol deviation occurs without a valid pre-execution amendment.

## Policy

Failure of one diagnostic test does not automatically falsify a hypothesis. Falsification requires application of the hypothesis-specific rule and documented reasoning.

Exact numerical thresholds must be frozen before execution.
