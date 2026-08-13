# H-AICR v0.3.5 — G0 Audit Record

**Audit status:** PASS — parameter closure
**Date:** 2026-08-13
**Scope:** Closure of the two blockers recorded against H-AICR v0.3.4

## H-AICR-003

Frozen weighted Graph Edit Distance:

- node addition = `2.0`
- node deletion = `2.0`
- edge addition = `1.0`
- edge deletion = `1.0`
- attribute change = `0.5`
- type change = `0.5`

Primary formula: `GED_weighted = 2.0*NodeOps + 1.0*EdgeOps + 0.5*AttributeOps`.
Mechanically implied incident-edge deletion is not charged twice.

## H-AICR-007

Operational index: `IC = mean_credit_honest / mean_credit_strategic`.
Primary threshold: `IC >= 1.25`.
The bootstrap lower confidence bound must exceed `1.00`. A zero or negligible denominator is reported as unstable rather than automatic success.

This is a behavioral experimental criterion. It does not constitute a formal proof of game-theoretic incentive compatibility.

## Gate disposition

The two previously open G0 parameter blockers are closed by `H-AICR_v0.3.5_G0_PREREGISTRATION.md`.

Empirical validity remains untested until execution and independent validation.
