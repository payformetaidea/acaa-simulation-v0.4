# Gate 2 Seed and Sample Policy

**Status:** DRAFT / PRE-REGISTRATION

## Planned design

- 1 fixed reference seed.
- 10 non-reference seeds.
- 3 executions per seed.
- Planned total: 33 atomic executions.

The planned count is not evidence of completed execution.

## Seed registry requirements

Before the protocol is frozen, the exact seed values must be committed in a machine-readable registry. The registry must include:

- seed identifier;
- numeric/hex value;
- generation method;
- creation timestamp;
- registry hash.

After freeze, seed values cannot be changed without a versioned protocol amendment and a new freeze.

## Execution order

The execution order must be recorded. If randomized, the randomization algorithm, source seed, and resulting order must be committed before execution.

## Repeats

Each seed condition receives three planned repeats. Failed runs remain in the provenance record and may not be silently replaced.

## Outliers

The primary outlier flagging rule is IQR-based and must be applied without using the observed result to redefine the threshold. Outliers are retained in the primary dataset; exclusion, if ever permitted, is a separate sensitivity analysis with explicit justification.
