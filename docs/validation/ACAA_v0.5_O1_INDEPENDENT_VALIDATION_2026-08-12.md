# ACAA v0.5 — O1 Independent Evidence Validation Record

**Gate status: PASS**

## Execution record

- PR: #13 — Controlled O1 Implementation
- O1 implementation HEAD: `76c9d1d51bf01e88056092b87fc4204831eac4f8`
- PR merge-test commit validated by CI: `547166a9c527a13e74ba08f74f69d6a30907f13f`
- Controlled CI workflow: `ACAA v0.5 — O1 Controlled Implementation`
- Run: **#43**
- Workflow run ID: `31578812539`
- Result: **SUCCESS**
- Evidence artifact ID: `9134308412`
- Evidence artifact SHA-256: `51b7b94e066caea1c23e17d8da003b632259c3b0da4548d97e1026473a89ffcb`

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
Post-run BaseConfig / effective configuration
        │
        └── effective fingerprint independently recomputed
```

The validation contract now explicitly distinguishes cross-run baseline identity from the post-run effective configuration identity used by the engine's serialized `EffectiveConfig` fingerprint.

No v0.4 engine semantics were changed to resolve this issue.

## Interpretation boundary

This PASS establishes that the defined 12-seed O1 experiment and its evidence contract have passed independent contract, integrity, provenance, and distributional-statistics validation.

It does not establish universal robustness, population-level robustness, or scientific validity beyond O1 scope.

## Scope boundary

- v0.4 engine: unchanged
- v0.4 independent validator: validation-only changes in the O1 branch
- O2: not implemented
- R2/R3: excluded
- v0.5 baseline: not yet established

**Decision: O1 PASSES the Independent Evidence Validation Gate and is eligible for the next Gatekeeper decision.**
