# Gate 2 Outlier Analysis Policy

**Status:** DRAFT / PRE-REGISTRATION

## 1. Core principle

> Detect → Retain → Flag → Analyze → Sensitivity Analysis.

Detection is not exclusion. Primary analysis retains all valid observations.

## 2. Primary detection rule

For each seed `s`:

```text
Q1_s = 25th percentile
Q3_s = 75th percentile
IQR_s = Q3_s − Q1_s
lower = Q1_s − 1.5 × IQR_s
upper = Q3_s + 1.5 × IQR_s
```

A value outside `[lower, upper]` is flagged.

Because `n=3` per seed, IQR-based detection is low-resolution and is used only as a flagging mechanism.

## 3. Zero-IQR handling

If `IQR_s = 0`:

- `[47,47,47]` → all observations `NORMAL`; report `ZERO_VARIATION`.
- `[47,47,48]` → median = 47; any value different from the median is `FLAGGED`.

Flagging never removes the observation from the primary analysis.

## 4. Classification

### Random outlier
Single occurrence in one run/seed without cross-seed repetition.

### Structural outlier
Pattern repeats in ≥2 repeats of the same seed, or has a reproducible seed-specific pattern.

### Cross-seed/systematic outlier
The same directional pattern appears in ≥2 seeds with similar magnitude and cannot reasonably be explained by random variation. For F-3.5, the stronger falsification threshold is `≥3 seeds` OR `≥30% of runs`.

## 5. Primary action

Every flagged observation is:

- retained in primary analysis;
- recorded in E-007;
- discussed in E-008;
- included in sensitivity analysis where exclusion is permitted.

## 6. Exclusion rule

Exclusion is allowed only when all conditions hold:

1. the observation is structural/systematic, not merely random;
2. the cause is traced to infrastructure or a documented protocol violation;
3. root-cause evidence is preserved;
4. the decision is documented in `DECISION_LOG.md`;
5. sensitivity analysis with and without exclusion is reported.

No exclusion is allowed merely because it improves a result.

## 7. Decision authority

Only **Formal Protocol Review** may authorize exclusion. No individual researcher may unilaterally remove an observation.

The record must contain rationale, root-cause evidence, affected run IDs, hashes, and sensitivity results before final Gate decision.

## 8. Sensitivity interpretation

If primary and sensitivity conclusions agree → `ROBUST`.

If the Gate conclusion changes in either direction → `SENSITIVE`:

- report both analyses;
- H-003/H-004 remain `NOT DEMONSTRATED` pending review;
- no favorable sensitivity result may override an unfavorable primary result.

## 9. Provenance

Outlier flags, classification, investigation, and any authorized exclusion are part of E-007 and E-010. Primary raw artifacts remain immutable.
