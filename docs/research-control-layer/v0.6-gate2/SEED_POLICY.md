# Gate 2 Seed and Sample Policy

**Status:** DRAFT / PRE-REGISTRATION

## Planned design

- 11 seed conditions: 1 fixed reference + 10 non-reference.
- 3 repeats per seed.
- Planned total: 33 atomic executions.

The planned count is not evidence of completed execution.

## Frozen registry

Before protocol freeze, the exact seed values must be committed in a machine-readable registry containing:

- seed ID;
- numeric/hex value;
- generation method;
- creation timestamp;
- registry hash.

After freeze, values cannot change without a versioned amendment and new freeze.

## Execution order

Execution order must be recorded. If randomized, the randomization algorithm, source seed, and resulting order must be committed before the first execution.

## Repeats

Exactly three planned repeats are assigned to each seed. Failed runs are retained and are not silently replaced.

## Seed validity

A run with a seed not present in the frozen registry is `F-PROTOCOL` and is excluded from valid statistical analysis while remaining in provenance.

## Outliers

Outlier detection follows `OUTLIER_ANALYSIS.md`; flagged observations remain in primary analysis.
