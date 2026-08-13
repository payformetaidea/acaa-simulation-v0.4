# H-AICR v0.3.4 — Final Methodological Protocol

**Status:** FROZEN FOR EXECUTION DESIGN
**Date:** 2026-08-13
**Parent baseline:** ACAA v0.5.0 (`de7d11ed9457ede84c1954aa70a59331bf07b72e`)
**Epistemic status:** PROPOSED RESEARCH EXTENSION

## 0. Scope and non-claim rule

H-AICR is a research extension to the frozen ACAA v0.5.0 baseline. Nothing in this protocol upgrades ACAA capabilities or establishes empirical validity before execution and independent validation.

The protocol follows the evidence progression:

`measure contribution → validate measurement → recognize contribution → evaluate incentives → tokenize → evaluate economic value`

Each transition requires its own evidence gate.

## 1. Epistemic status ontology

| Status | Meaning |
|---|---|
| PROPOSED_CONSTRUCT | Conceptual construct defined for research design |
| HYPOTHESIS | Operational, falsifiable prediction |
| OBSERVED | Directly measured execution data |
| VALIDATED | Independently and reproducibly verified result |
| CLAIMED | System capability assertion; cannot be treated as validated without evidence |

Constructs and hypotheses never inherit `VALIDATED` status from the ACAA baseline.

## 2. Relationship to ACAA v0.5.0

- ACAA v0.5.0 is the frozen control baseline.
- H-AICR consumes the baseline as a controlled research substrate.
- H-AICR does not modify O1/O2 semantics in the baseline.
- Any H-AICR implementation that changes baseline behavior is a separate experimental condition and must be versioned independently.
- Baseline provenance must remain reconstructable from the frozen release target.

## 3. Ground Truth Protocol

### Phase A — Independent annotation

- Minimum 3 independent annotators.
- No access to model predictions, other annotations, or study outcomes.
- Annotators receive a frozen ontology and calibration examples.
- Original labels are immutable.

### Phase B — Reliability estimation

Categorical role labels:
- Fleiss' Kappa for multi-rater agreement.
- Pairwise Cohen's Kappa may be reported as a diagnostic.
- Pre-registered acceptable threshold: `κ ≥ 0.70`.

Ordinal contribution scores:
- ICC, two-way random effects, absolute agreement.
- Krippendorff's Alpha (ordinal) as robustness analysis.
- Pre-registered acceptable threshold: `ICC ≥ 0.70`.

Reliability is reported before adjudication.

### Phase C — Adjudication

- Conducted only after reliability is calculated.
- Original annotations remain immutable.
- Consensus/adjudicated labels are stored as separate artifacts.
- Primary analyses use pre-adjudication labels where the protocol specifies independent agreement; sensitivity analyses may use adjudicated labels.

## 4. H-AICR-001 — Role Recognition

**Question:** Can interaction trajectory support reproducible Consumer/Producer classification?

Primary metric: Macro-F1.
Secondary metrics: per-class precision/recall and balanced accuracy.

Baselines:
1. majority class;
2. stratified random;
3. predefined simple heuristic;
4. predefined external/standard benchmark classifier, if available.

Pre-registered target:
- Macro-F1 `≥ 0.70`;
- per-class precision `≥ 0.60`;
- per-class recall `≥ 0.60`.

Evaluation:
- user-disjoint held-out test set;
- 20% test allocation unless sample-size feasibility requires a documented alternative before lock;
- paired bootstrap, 10,000 resamples;
- 95% CI for performance estimates;
- family-wise error control across baseline comparisons (Holm correction, α=0.05).

Falsification:
- Macro-F1 below 0.70;
- failure to outperform the strongest baseline after multiplicity correction;
- any class precision or recall below 0.50.

## 5. H-AICR-002 — Data Field Reconstruction

### Atomic unit

The atomic unit is the smallest unit defined by the frozen annotation ontology that can be independently identified, attributed, and evaluated.

Types: Fact, Claim, Evidence, Relation, Correction, Artifact, Problem, Hypothesis.

### Matching policy

Matching is deterministic and one-to-one within an evaluation window. Candidate matches are evaluated in the following priority order:

1. exact text + context + type;
2. normalized text + context + type;
3. semantic similarity ≥ 0.85 + same type;
4. predefined partial-match rule + same type.

A candidate may receive only one final match. If multiple candidates qualify, the highest-priority rule wins; ties are resolved deterministically by the frozen identifier ordering.

Primary metrics: precision, recall, F1, plus component-wise scores by atomic-unit type.

Falsification threshold: overall reconstruction F1 `< 0.70`.

The ontology and matching policy are frozen before execution.

## 6. H-AICR-003 — Knowledge Delta Attribution

Canonical representation: versioned Knowledge Graph, Neo4j/Cypher-compatible schema.
Secondary representation: semantic embeddings.
Tertiary representation: versioned fact store.

Embedding model: `sentence-transformers/all-MiniLM-L6-v2`, dimension 384. The exact model revision/hash and library versions must be captured in the pre-registration manifest before execution.

Delta components:
- additions;
- removals;
- modifications;
- relation changes;
- confidence changes.

Attribution classes:
- User-originated;
- AI-originated;
- Joint synthesis;
- External evidence.

Primary comparison: weighted graph edit distance. The graph operation weights must be explicitly frozen in the pre-registration manifest.
Secondary comparison: cosine similarity.
Tertiary comparison: fact-overlap ratio.

Falsification:
- overall attribution accuracy `< 0.60`, or
- any attribution category `< 0.50`.

## 7. H-AICR-004 — Content Assay Validation

The assay must use atomic, pre-registered dimensions:
- novelty;
- accuracy;
- evidence support;
- relevance;
- reusability;
- contribution type/value dimensions defined in the annotation ontology.

Human assessment is independent of the system score.

Primary validity criterion: pre-registered association between assay output and independent human assessment. Pearson correlation is insufficient as the sole validity statistic; Spearman correlation and calibration/error analysis must also be reported where scale assumptions require them.

Falsification: primary association `< 0.30` together with failure of the pre-registered robustness criteria.

## 8. H-AICR-005 — Payment/Access Measurement Invariance

Framework: equivalence / non-inferiority.

Equivalence margin: `δ = 0.15` on the normalized contribution-measurement scale.

The margin is a design criterion, not an empirical fact. It must be justified in the calibration record before outcome inspection and cannot be revised after seeing the main results.

Primary analysis:
- TOST at α=0.05;
- covariate adjustment for interaction quality and exposure;
- group weighting specified before analysis.

Important statistical convention: a TOST conducted at α=0.05 corresponds to a 90% confidence interval for equivalence. A 95% CI is reported separately as a descriptive robustness interval and is not substituted for the TOST decision rule.

Success:
- TOST rejects both non-equivalence nulls;
- estimated difference is within ±0.15;
- robustness analysis does not reveal material systematic distortion.

Falsification:
- equivalence not established;
- or predefined sensitivity analysis identifies systematic bias beyond δ.

## 9. H-AICR-006 — Adversarial Robustness

Threat dimensions:

Compute multiplier: 1x, 5x, 10x, 25x.
Sybil identities: 10, 50, 100, 500.
Attacker budget: low (2 h/day × 1 week), medium (8 h/day × 2 weeks), high (24/7 automation × 1 month).

This is a 4 × 4 × 3 sensitivity matrix.

Attack surfaces:
1. Data Field injection;
2. Knowledge Delta manipulation;
3. Value Assay gaming;
4. token allocation exploitation;
5. downstream accumulation.

Success metrics:
- attack success rate;
- excess credit obtained relative to honest users;
- false-positive rate against honest users;
- defense degradation relative to undefended and baseline-defense conditions.

Pre-registered target:
- attack success `< 10%` at baseline threat level;
- false-positive rate `≤ 5%` for honest users.

Falsification:
- attack success `> 20%` at any moderate threat level;
- defended condition performs worse than the predefined defense baseline;
- false-positive rate `> 5%`.

All threat parameters are recorded as a robustness curve rather than reduced to a single point estimate.

## 10. H-AICR-007 — Token Mapping Feasibility

Tokenization is downstream of validated measurement. Token eligibility is therefore evaluated against independent economic/design criteria and not against the same metric used to generate the token score.

Criteria:
- Gini coefficient `≤ 0.40` as a design criterion;
- top-10% contribution share `< 40%` as a design criterion;
- token allocation change `< 15%` under ±20% metric perturbation;
- incentive-compatibility analysis reported separately from descriptive fairness metrics.

The first three thresholds are design criteria, not empirical facts. Any change requires pre-registration before execution.

Falsification:
- circular validation;
- Gini `> 0.60`;
- top-10% share `≥ 40%`;
- allocation sensitivity `> 20%` under the predefined perturbation;
- or failure of the pre-registered incentive-compatibility criterion.

The incentive-compatibility criterion must be operationalized in the execution preregistration before H-AICR-007 is run.

## 11. H-AICR-008 — Deferred Economic Extension

Status: `ECONOMIC_EXTENSION_DEFERRED`.

No economic-value claim is permitted in the H-AICR core protocol.

Prerequisites:
- H-AICR-002 validated;
- H-AICR-004 validated;
- H-AICR-006 validated;
- H-AICR-007 independently evaluated.

A separate economic protocol is required before any Data Dividend experiment or economic-value claim.

## 12. Leakage and contamination control

- User-level train/test separation is mandatory.
- Temporal separation is used where applicable.
- Test-set lock occurs before model selection.
- Feature extraction and normalization parameters are learned from training data only.
- Economic rewards are disabled during Phase A measurement validation.
- Phase B uses a fresh cohort.
- Phase B outcomes cannot validate Phase A.

A machine-checkable leakage report is mandatory before the primary analysis.

## 13. No retroactive metric selection

Metrics, thresholds, aggregation functions, matching rules, statistical tests, exclusion rules, and decision gates are frozen before observing primary test results.

Exploratory analyses are allowed only on designated validation data and must be labeled exploratory.

## 14. Evidence Contract

Evidence independence is defined by provenance, not file count.

Critical hypotheses require at least Level-3 evidence:
- independent execution or replication;
- independent annotation where applicable;
- independent validation path;
- immutable provenance and hashes.

Three artifacts from one execution pipeline do not constitute independent evidence.

## 15. Claim → Evidence → Artifact → Decision

Every H-AICR claim must trace through:

`Claim → Hypothesis → Evidence → Artifact → Independent Validation → Gate Decision`.

Missing links block promotion to `VALIDATED`.

## 16. Gate model

### Gate G0 — Protocol Freeze
All definitions, thresholds, models, splits, statistical tests, threat parameters, and decision rules are locked.

### Gate G1 — Measurement Validity
H-001 through H-004 must satisfy their pre-registered criteria before recognition is used as an evidence-backed system function.

### Gate G2 — Recognition/Incentive Safety
H-005 and H-006 must pass before economic recognition is enabled in an experimental environment.

### Gate G3 — Tokenization
H-007 must pass independently before token mapping is treated as a validated design.

### Gate G4 — Economic Extension
H-008 requires a separate protocol and separate evidence gate.

## 17. Failure policy

A failed hypothesis is recorded as `FAILED` with its evidence and scope. Failure does not permit threshold relaxation or retroactive protocol changes.

Any protocol deviation creates a new versioned protocol state and cannot overwrite the frozen protocol.

## 18. Reproducibility manifest

The execution package must record:
- repository commit SHA;
- ACAA baseline release/tag;
- protocol hash;
- dataset identifiers and hashes;
- model identifiers and revisions;
- dependency lockfile/hash;
- random seeds;
- train/validation/test manifests;
- annotation artifacts;
- execution logs;
- analysis scripts;
- result artifacts;
- independent-validation artifacts.

## 19. Final status

This document is the v0.3.4 methodological hardening target. It becomes an execution protocol only after the repository records the pre-registration manifest and the G0 freeze decision.
