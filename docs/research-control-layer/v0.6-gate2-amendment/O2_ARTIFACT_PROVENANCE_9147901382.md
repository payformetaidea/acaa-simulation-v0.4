# O2 Artifact Provenance — 9147901382

**Status:** VERIFIED / RETAINED ARTIFACT IDENTIFIED

## Source artifact

| Field | Value |
|---|---|
| GitHub Actions artifact ID | `9147901382` |
| Artifact name | `acaa-v0.5-o2-independent-evidence` |
| Workflow run | `31612771142` |
| Source branch | `agent/v0.5-integration-ci-gate` |
| Source commit | `de7d11ed9457ede84c1954aa70a59331bf07b72e` |
| Archive size | `106770` bytes |
| GitHub artifact archive digest | `sha256:8d923bb951e60764ad9604e708c03bafdc30053da9b766c5ede6ceea7a929d81` |
| Artifact expiration | `2026-11-10T15:31:32Z` |

## Exact retained file

The artifact archive contains exactly one file:

`o2_identity_evidence.json`

The SHA-256 of the extracted JSON file bytes is:

```text
7649e45f6484dd0a6121fe5cbe995c4d3a195a6a6f4259462af8e1e6b02d10c9
```

This digest is distinct from the GitHub Actions artifact archive digest above. Both values are retained deliberately.

## Content verification

Direct inspection of the exact extracted JSON established:

```text
schema                  = acaa.v0.5.o2.identity-contract@1.0
records                 = 1936
unique cau_id           = 1936
O2 pattern matches      = 1936 / 1936
aggregate.cau_records   = 1936
```

The observed first identifiers are `CAU-000001`, `CAU-000002`, `CAU-000003`, `CAU-000004`, `CAU-000005`.

The artifact metadata also records:

```text
evidence_digest         = 65ea4526d155405731a634ec4baea214853406944b0bd015abb4cd28cc37c866
record_hashes_digest    = 1aeaeac6864309c875394732d9e6f20492946d1e4505d4d13b3af5fc1913ff8a
manifest_digest          = 84b31d3590423f203ca5ee320719a9c9c16766b407b5b3d7681d57559530c8ee
```

## Governance boundary

This record does not alter the frozen artifact or baseline. It records provenance and exact-byte verification so the artifact can be consumed by a later Real Artifact Gate without reconstruction or silent substitution.

The artifact remains historical evidence from the frozen v0.5.0 baseline. It is not Gate-2 experimental evidence and does not authorize execution.
