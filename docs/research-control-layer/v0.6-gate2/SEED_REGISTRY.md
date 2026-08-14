# Gate 2 Seed Registry

**Status:** DRAFT / PRE-FREEZE
**Rule:** Rule B — CANONICAL / PRE-REGISTERED
**Domain:** `ACAA-G2-v0.6-SEED-REGISTRY-v1`
**Generation:** SHA-256(`domain | NONREF | index | counter`)
**Output:** unsigned 32-bit integer
**Rejected values:** `0`, `1`, duplicates

## Registry

| Index | Seed ID | Role | Counter | Value |
|---:|---|---|---:|---:|
| 0 | REF-01 | REFERENCE | 0 | 2168776509 |
| 1 | NONREF-01 | NON_REFERENCE | 0 | 3977867781 |
| 2 | NONREF-02 | NON_REFERENCE | 0 | 5319100 |
| 3 | NONREF-03 | NON_REFERENCE | 0 | 1223121603 |
| 4 | NONREF-04 | NON_REFERENCE | 0 | 1164549617 |
| 5 | NONREF-05 | NON_REFERENCE | 0 | 208381252 |
| 6 | NONREF-06 | NON_REFERENCE | 0 | 1440089971 |
| 7 | NONREF-07 | NON_REFERENCE | 0 | 3991924077 |
| 8 | NONREF-08 | NON_REFERENCE | 0 | 2787646547 |
| 9 | NONREF-09 | NON_REFERENCE | 0 | 1045378760 |
| 10 | NONREF-10 | NON_REFERENCE | 0 | 2035830628 |

## Generation provenance

- `created_at`: `2026-08-14T16:25:39Z`
- Timestamp is provenance metadata only and was not used as a generator input.
- No OS entropy, runtime RNG, or execution-dependent input was used.
- All candidates were accepted at `counter = 0`.
- The v0.5.0 baseline commit is provenance only and is not an input to this generator.

## Independent verification

Two independent implementations were executed against the canonical rule:

1. Python `hashlib.sha256` implementation.
2. Node.js `crypto.createHash('sha256')` implementation using `readUInt32BE(0)`.

Both implementations produced the identical 11-value registry, with no rejected candidates and no duplicates.

## Registry hash

SHA-256 of the exact UTF-8 bytes of `SEED_REGISTRY.json`:

```text
4a856e4777a64d4e59ddc8fab4e66967e7232fd4e9132aff7b916d31a912a18e
```

The sidecar `SEED_REGISTRY.sha256` records the same digest.

## Freeze state

This registry is **generated and independently verified**, but the Gate-2 protocol remains **NOT FROZEN** and execution remains **PROHIBITED** pending the final seven-invariant cross-document review and atomic protocol freeze.
