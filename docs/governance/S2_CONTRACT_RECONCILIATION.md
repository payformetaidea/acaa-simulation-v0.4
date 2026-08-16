# S2 Contract Reconciliation

**Control:** R-S2-001  
**Gate:** S2 Readiness  
**Status:** BLOCKED — no S2 execution authorization  
**Branch:** `research/s2-readiness-gate`

## 1. Purpose

Establish the exact, versioned S2 normative contract before an oracle, execution harness, or execution authorization is treated as valid.

This document is a reconciliation record, not an invented S2 specification. Unknown or unsupported contract elements remain `UNRESOLVED`.

## 2. Governing rule

No S2 assertion may be promoted to normative status solely because it appears in code, a fixture, a workflow, a historical note, or an investigator assumption.

The authoritative source must be identified by:

- document/path or external specification identifier;
- version;
- commit or immutable reference;
- applicable section(s);
- provenance evidence.

## 3. Required contract inventory

| ID | Contract element | Required classification | Current state | Evidence required |
|---|---|---|---|---|
| S2-C-001 | S2 input contract | normative | UNRESOLVED | authoritative specification |
| S2-C-002 | S2 output contract | normative | UNRESOLVED | authoritative specification |
| S2-C-003 | schema assertions | Layer 1 | UNRESOLVED | schema + specification mapping |
| S2-C-004 | semantic invariants | Layer 2 | UNRESOLVED | invariant registry/oracle |
| S2-C-005 | architectural assertions | architecture audit | UNRESOLVED | architecture specification |
| S2-C-006 | positive fixtures | conformance evidence | UNRESOLVED | fixture lineage |
| S2-C-007 | negative fixtures | conformance evidence | UNRESOLVED | fixture + intended failure layer |
| S2-C-008 | expected outcomes | oracle input | UNRESOLVED | versioned oracle |
| S2-C-009 | contract version | provenance | UNRESOLVED | immutable version identifier |
| S2-C-010 | contract source | provenance | UNRESOLVED | authoritative source reference |

## 4. Fixture lineage rule

Every negative fixture must have an explicit tuple:

`fixture_id → source contract requirement → intended assertion layer → expected oracle result → provenance`

A fixture must not be reclassified merely to obtain a PASS result.

## 5. Assertion-layer model

The reconciliation must distinguish at least:

1. **Layer 1 — Schema conformance**: structural/schema-validity assertions.
2. **Layer 2 — Semantic conformance**: registry, invariant, cross-field, identity, and semantic assertions.
3. **Layer 3 — Architectural audit**: claims about system architecture or research methodology that are not reducible to schema/semantic validation.

An assertion whose layer cannot be established from authoritative evidence remains `UNRESOLVED`.

## 6. Reconciliation procedure

1. Identify the authoritative S2 specification.
2. Pin its immutable version/reference.
3. Extract every normative requirement.
4. Assign a stable requirement ID.
5. Map each requirement to its assertion layer.
6. Map each requirement to implementation, fixture, and oracle where applicable.
7. Identify contradictions between specification, schema, code, fixtures, and existing governance records.
8. Classify every contradiction using the established failure taxonomy.
9. Produce the versioned S2 contract record.
10. Obtain independent validation of the reconciliation.

## 7. Current evidence

The S2 Readiness Gate and Issue #31 establish that R-S2-001 requires an exact S2 normative contract, separation of schema/semantic/architectural assertions, and explicit negative-fixture classification. They do **not** themselves constitute the missing S2 normative contract.

Therefore R-S2-001 remains `BLOCKED` until the authoritative S2 specification and its immutable provenance are identified and reconciled.

## 8. Authorization impact

While this control is `BLOCKED`:

- S2 execution: **NOT AUTHORIZED**
- Gate-2 execution: **NOT AUTHORIZED**
- 33-run campaign: **NOT AUTHORIZED**
- Freeze: **NOT AUTHORIZED**
- Merge: **NOT AUTHORIZED**

## 9. Evolution requirement

Once reconciled, this procedure becomes reusable readiness infrastructure. The resulting contract map must be suitable for reuse by later gates without silently inheriting S2-specific assumptions.
