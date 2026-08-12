# O1 Gate Retry Note

The independent validator test contract was aligned with the observed v0.4 identity model: the pre-run BaseConfig fingerprint is the constant cross-run identity, while the effective fingerprint is reproducible from the serialized post-run configuration.

This note intentionally changes no engine semantics and exists only to force a fresh PR-specific CI evaluation after the test-contract correction.
