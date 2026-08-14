# Gate 2 Decision Log

| ID | Decision | State | Evidence / Authority |
|---|---|---|---|
| D2-001 | Gate 2 begins at G2-0 planning | ACTIVE | Research Control Layer |
| D2-002 | v0.5.0 remains immutable | ACTIVE | frozen baseline `de7d11ed9457ede84c1954aa70a59331bf07b72e` |
| D2-003 | H-003 remains PROPOSED until evidence | ACTIVE | Hypothesis policy |
| D2-004 | H-004 remains PROPOSED until evidence | ACTIVE | Hypothesis policy |
| D2-005 | Design = 11 seeds × 3 repeats = 33 | PLANNED | Seed Policy |
| D2-006 | No execution before protocol freeze | ACTIVE | Gate 2 Protocol |
| D2-007 | Missing raw evidence cannot be reconstructed | ACTIVE | Evidence Contract |
| D2-008 | H-004 is direction-neutral with respect to the direction of seed effects; variance-component alternative is `H1: σ²_B > 0` | ACTIVE | SAP / Falsification Rules |
| D2-009 | Canonical evidence IDs E-001…E-010 reconciled | ACTIVE | Evidence Contract |
| D2-010 | G2-0.6 outlier policy uses detection/retention/exclusion separation | ACTIVE | Outlier Policy |
| D2-011 | F-3.5 requires method attribution + threshold + sensitivity impact | ACTIVE | Falsification Rules |
| D2-012 | Atomic freeze package requires cross-document consistency review | ACTIVE | G2-0.7 |
| D2-013 | R4.6 H-004 statistical alignment passed; `H0: σ²_B = 0`, `H1: σ²_B > 0`, non-negative variance estimator, `B=9999`, `α=0.05`, and +1 permutation correction are binding | CLOSED | R4.6 cross-document invariant review |
| D2-014 | R4 prospective design review closed; retain 11 seeds × 3 repeats as bounded characterization with explicit limitations | CLOSED | R4.1–R4.6 review |
| D2-015 | Seed-generation rule is deterministic, prospective, and frozen before value generation: fixed reference seed `1`; ten non-reference values derived by SHA-256 domain-separated generation with deterministic rejection of `0`, `1`, and duplicates | ACTIVE / PRE-REGISTRATION | R4 closure / Seed Policy |

## Amendment rule

Any binding change after freeze requires a new protocol version, explicit rationale, impact assessment, and new freeze before affected execution.

## Current state

`G2-0 / SEED GENERATION RULE DEFINED / EXECUTION PROHIBITED`

`R4 = CLOSED`

`Protocol Freeze = NO`

`Execution Authorization = NO`
