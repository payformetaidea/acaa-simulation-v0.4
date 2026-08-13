# H-AICR Scientific Sampling Frame v0.2

Status: SAMPLING-FRAME REVIEW CANDIDATE — SCIENTIFIC ACQUISITION NOT AUTHORIZED

## Analytical unit

Primary analytical unit: one unique user/agent identity observed over the preregistered study window. For G4, the unit is the complete iterative trajectory; interaction records are nested observations.

Secondary observational unit: one interaction record with one unit_id, record_uuid, UTC timestamp, and provenance record.

The frozen power plan specifies 97 independent analytical units per registered cohort, 7 cohorts, 679 planned analytical units total. Raw interaction-record count must not be substituted for independent-unit count.

## Cohorts

- G1-Pure-Consumer: information-consumption interactions with no substantive original contribution under the frozen codebook.
- G2-Low-Producer: limited original contribution satisfying the frozen low-production codebook.
- G3-High-Producer: substantive original contribution/synthesis satisfying the frozen high-production codebook.
- G4-Iterative-Researcher: a preregistered repeated research sequence with identifiable refinement over time.
- G5-Adversarial-Spam: behavior satisfying the preregistered adversarial/spam protocol; never assigned from outcome alone.
- G6-Synthetic-AI: declared AI/synthetic agent under a fixed, versioned generation protocol.
- G7-Human-Expert: human satisfying the preregistered expert-qualification rule independently of H-AICR outcomes.

No cohort assignment may use H-AICR output, credit, or any primary outcome.

## Independence

1. Each analytical unit belongs to exactly one cohort.
2. Each analytical unit has one stable privacy-preserving unit_id.
3. No unit_id may occur in more than one Train/Validation/Test split.
4. Repeated records from one unit are clustered and never treated as independent units.
5. G6 agent/model identity and model revision are provenance fields.
6. G7 expert qualification remains distinct from annotator identity wherever feasible.

## Inclusion

A scientific unit must originate from the declared source/protocol, have deterministic identity, valid UTC timing, auditable provenance, satisfy schema and cohort eligibility, complete required annotation, and have no unresolved integrity failure.

## Exclusion reason codes

MISSING_IDENTITY; DUPLICATE_UNIT; DUPLICATE_RECORD; INVALID_TIMESTAMP; INSUFFICIENT_PROVENANCE; COHORT_CRITERION_UNMET; G4_SEQUENCE_INCOMPLETE; G6_MODEL_PROVENANCE_MISSING; G7_QUALIFICATION_UNVERIFIED; ANNOTATION_INTEGRITY_FAILURE; DATA_LEAKAGE_DETECTED.

Exclusions must be logged before primary-outcome analysis and cannot be introduced because of observed outcomes.

## Temporal design

For temporal validation, Test observations must occur after the registered training cutoff. A single unit may not cross Train/Validation/Test.

## Acquisition prohibition

The existing controlled synthetic harness is prohibited as a source of scientific evidence and remains Level-A engineering validation only.

## Gate

This document does not authorize scientific generation. Authorization requires closure of analytical-unit definition, cohort thresholds/codebook, deterministic UUID specification, split algorithm, leakage checker, schema, and provenance plan.

Current status: SCIENTIFIC_GENERATION_BLOCKED
