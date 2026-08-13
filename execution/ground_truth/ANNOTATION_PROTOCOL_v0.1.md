# H-AICR Ground Truth Annotation Protocol v0.1

**Status:** PRE-EXECUTION / BLIND ANNOTATION SPECIFICATION
**Parent protocol:** H-AICR v0.3.4
**Purpose:** Prepare independent ground-truth annotation without exposing H-AICR predictions or economic outputs.

## 1. Independence requirements

- Three annotators operate independently.
- Annotators receive only the interaction record and the frozen ontology/instructions.
- Annotators do not receive model predictions, H-AICR scores, cohort credit, or other annotator labels.
- Annotators do not communicate during the independent annotation phase.
- Original labels are immutable after submission.

## 2. Annotation targets

### Categorical role

Each interaction window receives one role label from the registered ontology:

- `Consumer`
- `Producer`
- `Mixed`
- `Unclear`

If the experimental protocol requires binary Consumer/Producer evaluation, the binary mapping must be explicitly registered before analysis; annotators must retain the original categorical label.

### Contribution value

Ordinal score on the frozen 1–10 scale.

- 1 = negligible contribution
- 10 = exceptionally substantive contribution

Annotators must apply the same rubric to every record and must not infer labels from system outputs.

## 3. Required provenance

Every annotation record must contain:

- `record_id`
- `annotator_id`
- `annotation_timestamp`
- `role_label`
- `contribution_score`
- `rationale_code` (predefined code, if enabled)
- `protocol_version`

## 4. Reliability phase

Reliability is calculated before adjudication:

- categorical: Fleiss' Kappa for multi-rater labels; pairwise Cohen's Kappa may be reported as secondary analysis;
- ordinal: two-way random-effects ICC with absolute agreement; Krippendorff's Alpha may be reported as secondary analysis.

Pre-registered interpretation threshold: >= 0.70 acceptable.

## 5. Adjudication

Adjudication begins only after reliability is calculated.

- Original independent labels remain immutable primary evidence.
- Adjudicated labels are stored as a separate artifact.
- The adjudication record documents disagreements and the resolution rationale.
- Both pre-adjudication and adjudicated labels remain available for sensitivity analysis.

## 6. Evidence boundary

Annotation preparation and annotation execution are distinct from scientific validation. Synthetic control records may validate the annotation tooling, but they are not human ground truth and must never be reported as such.
