# ACAA v0.5 — O1 Independent Evidence Validation Record

**Gate status: PASS**

## Execution record

- PR: #13 — Controlled O1 Implementation
- O1 implementation HEAD: `6618e3d305d0819a6eea39e4f559e21d929045b3`
- PR merge-test commit validated by CI: `879a829284d3d307c4fe469bb36622bc0d6e67af`
- Controlled CI workflow: `ACAA v0.5 — O1 Controlled Implementation`
- Run: **#27**
- Workflow run ID: `31578088577`
- Result: **SUCCESS**
- Evidence artifact ID: `9134026903`
- Evidence artifact SHA-256: `c0a905da4c375082f73350b9689fd81a596ad811332eba7d0e01606cb0d66307`

## Independent validation predicates

| Predicate | Result |
|---|---|
| O1-01 — planned seed set equals executed seed set | PASS |
| O1-02 — seed values are unique | PASS |
| O1-03 — base configuration identity is constant / scenario preserved | PASS |
| O1-04 — effective fingerprints independently reproduce | PASS |
| O1-05 — engine hash is consistent | PASS |
| O1-06 — required metrics and trajectories are valid | PASS |
| O1-07 — aggregate statistics reproduce from run artifacts | PASS |
| O1-08 — statistical edge-case rules are respected | PASS |
| O1-09 — artifact/evidence integrity verifies | PASS |
| O1-10 — regression and controlled execution evidence passes | PASS |

## Negative-case coverage

O1-N01 through O1-N10: **PASS**.

The validator independently exercises rejection paths for seed mutation, duplicate/unexpected seeds, configuration mutation, engine-hash mutation, metric removal/alteration, malformed numeric values, aggregate mutation, and artifact-digest mutation.

## Root-cause correction

The preceding validation attempt (Run #23) failed because the validator treated the pre-run `o1_base_config_fingerprint` as if it had to reproduce from the post-run `params`. Adaptive governance may mutate the post-run BaseConfig; therefore these identities have distinct roles.

The corrected boundary is:

```text
Pre-run BaseConfig fingerprint
        │
        ├── must remain constant across all 12 runs
        │
        ▼
Raw run artifact
        │
        ▼
Post-run effective configuration
        │
        └── effective fingerprint independently recomputed
```

No v0.4 engine or independent validator semantics were changed to resolve this issue.

## Interpretation boundary

This PASS establishes that the defined 12-seed O1 experiment and its evidence contract have passed independent contract, integrity, provenance, and distributional-statistics validation.

It does not establish universal robustness, population-level robustness, or scientific validity beyond O1 scope.

## Scope boundary

- v0.4 engine: unchanged
- v0.4 independent validator: unchanged
- O2: not implemented
- R2/R3: excluded
- v0.5 baseline: not yet established

**Decision: O1 PASSES the Independent Evidence Validation Gate and is eligible for the next Gatekeeper decision.**
