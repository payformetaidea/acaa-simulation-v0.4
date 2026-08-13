# Artifact 4 — v0.6 Hypothesis Register Draft 0.1

Control baseline for experiments: v0.5.0 candidate reference `de7d11ed9457ede84c1954aa70a59331bf07b72e`.

| H-ID | Derived limitation | Hypothesis / testable prediction | Independent variable | Dependent variable | Falsification condition | Target | Priority |
|---|---|---|---|---|---|---|---|
| H-001 | L-001 | An independent party can reconstruct the declared baseline procedure | replication operator/procedure | reconstruction success | required outputs cannot be reconstructed | v0.5.x/v0.6 | HIGH |
| H-002 | L-001 | Documentation contains sufficient information for independent reproduction | documentation completeness | reproduction sufficiency | independent reproduction fails due to missing information | v0.6 | MEDIUM |
| H-003 | L-002 | preregistered multi-seed characterization produces stable estimates within predefined criteria | seed set | variability estimates | criteria fail | v0.6 | HIGH |
| H-004 | L-003 | atomic variability metrics provide a reproducible characterization before any robustness claim | metric definition | metric stability | metrics cannot distinguish predefined conditions | v0.6 | HIGH |
| H-005 | L-004 | identity provenance can support semantic and behavioral validation within the O2 contract | validation protocol | identity agreement | identity checks fail under controlled perturbation | v0.6/v0.7 | HIGH |
| H-006 | L-005 | an independently implemented validator reproduces the declared result | validator implementation | agreement with reference | independent validator disagrees under identical inputs | v0.6 | HIGH |
| H-007 | L-006 | a machine-readable epistemic-state model can enforce valid transitions | state/transition rules | accepted/rejected transitions | invalid transition is accepted or valid transition rejected | v0.6 | CRITICAL |
| H-008 | L-007/L-011 | versioned thesis lifecycle transitions can remain evidence-bound and reconstructable | lifecycle transition | lineage completeness | any transition lacks reconstructable evidence lineage | v0.6 | CRITICAL |
| H-009 | L-008 | atomic evidence-quality metrics can be operationally validated | metric definitions | validity/reliability | atomic metric fails predefined validity test | v0.6 | CRITICAL |
| H-010 | L-010 | controlled evolution can preserve immutable provenance under declared change rules | controlled change | provenance integrity | provenance cannot reconstruct change history | v0.7+ | CRITICAL |
| H-011 | L-009 | a composite metric is useful only after atomic metrics are validated | composite construction | incremental validated information | composite adds no validated information or violates atomic validity | v0.7+ | MEDIUM |
| H-012 | L-012 | machine-verifiable self-uncertainty can be represented and audited | uncertainty state model | verifiability | uncertainty cannot be independently verified | v0.7 | HIGH |
| H-013 | L-013 | organizational memory can preserve provenance across reconstruction | memory representation | provenance preservation | reconstructed memory loses provenance | v0.7+ | MEDIUM |
| H-014 | L-014 | external replication and peer critique can reproduce and challenge declared findings | external replication protocol | agreement/critique outcomes | external replication fails without explainable scope difference | v0.6 | HIGH |
| H-015 | L-015 | the validated architecture generalizes across predefined diverse domains | domain set | cross-domain performance | predefined domain criteria fail | v0.7+ | HIGH |
| H-016 | L-017 | explicit mapping to external governance frameworks reveals actionable coverage gaps | framework mapping | mapping completeness | mapping cannot produce reproducible gap analysis | v0.7+ | MEDIUM |

## Non-hypothesis items

- L-016 → Technical Paper v1.0 related-work work item.
- L-018 → continuous Publication/Release Integrity Constraint.

No hypothesis is promoted to evidence merely by appearing in this register.
