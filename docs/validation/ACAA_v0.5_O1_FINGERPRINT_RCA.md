# ACAA v0.5 — O1 Fingerprint Reproduction RCA

## Status

Controlled correction applied on `agent/v0.5-controlled-implementation-o1`.
Independent Evidence Validation remains **PENDING** until the corrected commit passes CI and a fresh evidence run.

## Observed Failure

The independent validator rejected an O1 run with an `effective fingerprint not reproducible` condition.

## Root Cause

`EffectiveConfig.get_fingerprint()` in the frozen v0.4 engine is defined from:

- the **pre-run BaseConfig fingerprint**,
- the seed,
- the scenario,
- the scenario parameters.

The O1 runner correctly captured that immutable pre-run fingerprint as `o1_base_config_fingerprint` before simulation execution.

The independent validator incorrectly attempted to reconstruct the same value from the exported `params` object. That object is serialized after execution and may reflect adaptive governance changes. Consequently, the validator was comparing the engine's pre-run identity against a post-run configuration projection.

This is an **evidence-boundary reconstruction error**, not evidence that the engine fingerprint itself is unstable.

## Controlled Correction

`independent_o1_validator_v0_5.py` now reconstructs the EffectiveConfig fingerprint from the immutable `o1_base_config_fingerprint` captured before execution.

A regression test suite was added to prove that:

1. the independent reconstruction matches the engine's fingerprint formula;
2. post-run adaptive mutations of exported `params` do not change the reconstructed fingerprint;
3. absence of the immutable pre-run fingerprint is rejected.

## Integrity Boundary

- v0.4 engine: unchanged
- v0.4 independent validator: unchanged
- O1 implementation scope: unchanged
- O2: excluded
- v0.4 baseline: preserved

## Validation Rule

The correction itself does not establish O1 validation. A fresh CI execution and independent evidence validation are required before the O1 Gate can be evaluated again.
