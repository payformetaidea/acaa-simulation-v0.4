# G0 Scientific Generator — Determinism Review

Status: `INDEPENDENTLY_VERIFIED — CI NOT YET EXECUTED`

## Scope

This review covers the committed `scientific_generator.py`, `generation_configuration.json`, `cohort_codebook.json`, and executable Draft-07 analytical-unit schema. It is an implementation verification artifact only and does not constitute empirical evidence.

## Independent verification results

- Independent analytical units: **679**
- Units per cohort: **97 x 7**
- Unique `unit_uuid`: **679/679**
- Unique nested `record_uuid`: **2716/2716**
- Nested interactions per unit: **4**
- Schema validation: **0 validation errors** across all 679 units and nested records
- Same-seed canonical output equality: **PASS**
- Canonical SHA-256 of generated unit payload: `91e023318a8dcde347fbefc2f0e542bee5f427815cf4715ba2788e21a4b77f5f`
- Unregistered seed behavior: **FAIL-CLOSED** (`seed != 42` rejected)
- Evidence classification: `IN_SILICO_THEORETICAL_EVIDENCE`
- Model revision: `deterministic_abm_v1`

## Boundary checks

The frozen model yields the following substantive contribution proportions at the closed-form optimum:

| Cohort | `q(e*)` |
|---|---:|
| G1_Pure_Consumer | 0.00 |
| G2_Low_Producer | 0.25 |
| G3_High_Producer | 0.55 |
| G4_Iterative_Researcher | 0.50 |
| G5_Adversarial_Spam | 0.10 |
| G6_Synthetic_AI | 0.60 |
| G7_Human_Expert | 0.65 |

For G4, the registered multipliers `[0.75, 0.90, 1.00, 1.10]` produce a non-decreasing refinement trajectory. For G5, the registered gaming term produces the required credit/contribution divergence without using H-AICR outcomes for cohort assignment.

## Important limitation

The verification above was executed independently against the committed generator logic. No GitHub Actions run was available on the execution branch at review time. Therefore this artifact must **not** be interpreted as a CI-generated execution log.

`DATASET_GENERATION` remains blocked until the repository-level determinism test is executed and recorded as a reproducible run artifact.
