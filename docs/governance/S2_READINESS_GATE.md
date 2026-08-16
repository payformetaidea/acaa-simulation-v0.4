# S2 Readiness Gate

**Status:** IN PROGRESS — S2 execution NOT AUTHORIZED

**Parent gate:** S1 APPROVED

**Branch:** `research/s2-readiness-gate`

## 1. Purpose

S2 must not be treated as an execution target until its contract, oracle, evidence, provenance, determinism, failure taxonomy, harness, and independent-validation requirements are explicit and testable.

This gate is a reusable control layer. A readiness PASS authorizes only the execution scope explicitly named by the authorization record.

## 2. Fail-closed rule

Any control with status `BLOCKED`, `UNKNOWN`, `UNPROVEN`, or `FAIL` prevents S2 execution authorization.

No inferred PASS is permitted.

## 3. Controls

| ID | Control | Required output | Initial status |
|---|---|---|---|
| R-S2-001 | Contract reconciliation | Versioned S2 normative contract and assertion-layer map | BLOCKED |
| R-S2-002 | Oracle definition | Machine-checkable oracle for every S2 assertion | BLOCKED |
| R-S2-003 | Evidence contract | PASS/FAIL artifact schema and retention requirements | DEFINED |
| R-S2-004 | Provenance contract | Commit/tree/blob/file/runtime identity record | DEFINED |
| R-S2-005 | Determinism | Repeated-execution equivalence definition and comparator | DEFINED |
| R-S2-006 | Failure taxonomy | Closed classification vocabulary and escalation rule | DEFINED |
| R-S2-007 | Harness integrity | Non-masking execution/evidence behavior | DEFINED |
| R-S2-008 | Independent validation | Independent verifier and target-binding procedure | BLOCKED |

## 4. Contract requirements

S2 contract reconciliation must explicitly identify:

- normative requirements;
- schema assertions;
- semantic invariants;
- architectural assertions;
- positive fixtures;
- negative fixtures;
- expected failure layer for each negative fixture;
- version and provenance of the governing specification.

A fixture cannot be reclassified merely to make an execution pass.

## 5. Evidence requirements

Every execution must preserve, at minimum:

- target commit SHA;
- HEAD SHA;
- working-tree status;
- validator/schema/fixture SHA-256 values;
- Git blob identities where required for lineage;
- Python executable and version;
- dependency distribution versions and import paths;
- stdout;
- stderr;
- exit code;
- structured validator result;
- run/job identifiers;
- artifact manifest;
- artifact checksums.

Evidence generation must continue after a non-zero validator exit so that failures remain diagnosable.

## 6. Determinism

Readiness requires a defined comparator for:

1. structured validation results;
2. exit status;
3. artifact contents;
4. provenance fields whose values are expected to vary by run.

Expected run identifiers and timestamps must not be treated as semantic differences. Any unexplained semantic or byte-level difference is a readiness failure until classified.

## 7. Failure taxonomy

Every failure must resolve to exactly one primary class:

- validator defect;
- schema defect;
- fixture/oracle defect;
- contract defect;
- runtime/dependency defect;
- workflow/evidence defect;
- provenance/integrity defect;
- architectural-audit defect.

`UNKNOWN` is a blocker, not a PASS.

## 8. Authorization boundary

S2 execution remains prohibited until:

- R-S2-001 through R-S2-008 are PASS;
- readiness evidence is produced;
- independent validation confirms the readiness result;
- an explicit authorization record names the exact target commit, oracle version, runtime envelope, workflow/command, and artifact contract.

Until then, Gate-2, the 33-run campaign, freeze, and merge remain prohibited.

## 9. Evolution requirement

Any control discovered during S2 that improves diagnosis, provenance, evidence, reproducibility, or governance must be promoted into the reusable readiness framework rather than implemented as a one-off workaround.
