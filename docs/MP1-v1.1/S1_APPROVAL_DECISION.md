# S1 Approval Decision

## Evidence basis

S1-V and S1-A have both completed with independent execution evidence on the controlled F2.4 lineage.

### S1-V

- Run: `31961151357`
- Artifact: `9267271632`
- Target validator commit: `d1cef3768ccaa39525a0c23e1a9b94c3528a8995`
- Validator SHA-256: `30b62555377e1eac569c2ea7d08d66b6376257d492227fee271e830c567b10dc`
- Schema SHA-256: `624a2f8fea39cfa20440b8f53d3b500af710a54f76f12840ae1bbe0796fb68a7`
- Run 1: exit `0`, verdict `PASS`
- Run 2: exit `0`, verdict `PASS`
- Byte-identical: `TRUE`
- Structured-identical: `TRUE`

### S1-A

- Run: `31961261640`
- Artifact: `9267297048`
- Audit verdict: `PASS`
- All 11 architecture controls: `PASS`

## Decision

**S1 = APPROVED.**

The approval is bounded to the controlled S1 contract, validator, fixtures, evidence workflow, and architecture controls audited above. It does not retroactively approve unrelated research claims.

## Transition

- S1-R2: COMPLETED
- F1: VALIDATED
- F2.1–F2.4: COMPLETED / RECONCILED
- S1-V: PASS
- S1-A: PASS
- S1: APPROVED
- S2: UNBLOCKED FOR CONTROLLED READINESS WORK
- Gate-2 execution: NOT AUTHORIZED by this decision
- 33-run execution: NOT AUTHORIZED by this decision
- Freeze/merge: NOT AUTHORIZED by this decision

## Evolution rule

S2 must begin with protocol/readiness reconciliation and evidence-contract review. No experimental execution is permitted until its own prerequisites are frozen and explicitly authorized.
