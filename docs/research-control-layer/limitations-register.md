# Artifact 3 — Research Limitations Register Draft 0.1

Severity taxonomy: `CRITICAL — Integrity`, `HIGH — Scientific`, `MEDIUM`, `LOW`.

| ID | Derived from | Limitation | Severity | Mitigation / target | Verification criterion |
|---|---|---|---|---|---|
| L-001 | C-001/C-002 | Reproducibility is bounded by defined procedures and artifacts | MEDIUM | independent mini-replication; v0.5.x/v0.6 | independent party reconstructs baseline |
| L-002 | C-004 | Variability characterization is bounded by the declared O1 experiment | HIGH — Scientific | larger preregistered seed set; v0.6 | predefined statistical criteria pass |
| L-003 | C-004 | No scientifically validated robustness threshold is established | HIGH — Scientific | atomic variability metrics; v0.6 | threshold is preregistered and tested |
| L-004 | C-005 | Identity evidence remains bounded to the declared O2 contract | HIGH — Scientific | semantic/behavioral validation; v0.6/v0.7 | identity preservation is independently validated |
| L-005 | C-006 | Independent validation scope is limited to declared evidence contracts | HIGH — Scientific | independent validator experiment; v0.6 | independent implementation reproduces result |
| L-006 | C-007 | No general machine-readable epistemic-state model is demonstrated | HIGH — Scientific | explicit state model; v0.6 | invalid transitions rejected and provenance preserved |
| L-007 | C-008 | Thesis lifecycle is not demonstrated as an implemented general mechanism | HIGH — Scientific | versioned lifecycle experiment; v0.6 | transitions reconstructable |
| L-008 | C-009 | Evidence-quality measures require atomic operational definitions | HIGH — Scientific | validate atomic metrics first; v0.6 | atomic metrics meet predefined validity criteria |
| L-009 | C-009 | Composite evidence-quality validity is unestablished | HIGH — Scientific | defer composite metric; v0.7+ | composite adds validated information beyond atomic metrics |
| L-010 | C-010 | Controlled self-evolution is not demonstrated | CRITICAL — Scientific | provenance-preserving evolution experiment; v0.7+ | controlled changes remain auditable |
| L-011 | C-008 | Evidence-bound thesis transitions require explicit lifecycle semantics | HIGH — Scientific | H-008; v0.6 | all state transitions have evidence lineage |
| L-012 | C-010 | Machine-verifiable self-uncertainty/reflexivity is unvalidated | HIGH — Scientific | H-012; v0.7 | system exposes verifiable uncertainty state |
| L-013 | C-010 | Provenance-preserving organizational memory is unvalidated | MEDIUM | H-013; v0.7+ | memory reconstruction preserves provenance |
| L-014 | C-006 / external validation | External replication and peer critique protocol is absent | HIGH — Scientific | H-014; v0.6 | external replication/critique completed |
| L-015 | C-003/C-004 | Domain-diverse generalization is unvalidated | HIGH — Scientific | H-015; v0.7+ | predefined domain-diverse benchmark succeeds |
| L-016 | research program | Related-work and governance comparison remains a literature work item | MEDIUM | Technical Paper v1.0 | comparison and gap analysis complete |
| L-017 | governance claims | Mapping to external governance frameworks is incomplete | MEDIUM | H-016; v0.7+ | explicit mapping and gap analysis |
| L-018 | all claims | Risk of demonstrated/proposed status drift and overclaiming | CRITICAL — Integrity | Publication Gate + Release Gate; continuous | no ungrounded promotion or scope loss |

L-016 is a Work Item, not a hypothesis. L-018 is a permanent Integrity Constraint, not a hypothesis.
