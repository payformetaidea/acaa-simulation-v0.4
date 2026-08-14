# Gate 2 Seed Generation — Independent Verification Record

**Rule:** Rule B
**Domain:** `ACAA-G2-v0.6-SEED-REGISTRY-v1`
**Date:** 2026-08-14

## Implementations

### Implementation A — Python

- SHA-256: `hashlib.sha256`
- Input: UTF-8 encoded `domain|NONREF|index|counter`
- Candidate: first 4 digest bytes, unsigned big-endian

### Implementation B — Node.js

- SHA-256: `crypto.createHash('sha256')`
- Input: UTF-8 encoded `domain|NONREF|index|counter`
- Candidate: `readUInt32BE(0)`

## Result

Both independent implementations returned the same ordered registry:

```text
0  0  2168776509
1  0  3977867781
2  0  5319100
3  0  1223121603
4  0  1164549617
5  0  208381252
6  0  1440089971
7  0  3991924077
8  0  2787646547
9  0  1045378760
10 0  2035830628
```

Checks passed:

- exactly 11 values: PASS
- index range `0..10`: PASS
- index `0` assigned to `REF-01`: PASS
- all values unsigned 32-bit: PASS
- no value `0`: PASS
- no value `1`: PASS
- no duplicates: PASS
- deterministic reproduction across implementations: PASS
- counter behavior: PASS; all accepted at counter `0`
- registry ordering: PASS

## Conclusion

**Independent seed-generation verification: PASS.**

No execution authorization is implied by this verification.
