# Gate 2 Execution Architecture

## Purpose

Define the execution infrastructure required before Gate-2 authorization. This artifact is post-freeze infrastructure and does not alter the frozen protocol.

## Architecture

Frozen Protocol
→ Execution Manifest
→ Dedicated Gate-2 Runner
→ 11 seeds × 3 repeats
→ Per-run provenance record
→ Immutable raw output
→ Evidence packaging
→ Independent validation
→ Authorization-controlled release

## Binding Inputs

1. Frozen protocol tag `v0.6-gate2-protocol`
2. Frozen commit `e5fde0b298e5bff9fd00196bd718a62934f09060`
3. Canonical seed registry and recorded SHA-256
4. Execution manifest
5. Frozen metric, statistical, failure, outlier, and evidence specifications

## Prohibited Shortcuts

- Do not use the legacy v0.4 independent-execution workflow for Gate-2 evidence.
- Do not substitute runtime RNG, timestamps, or environment-dependent seed inputs.
- Do not silently retry, replace, impute, or reorder a failed execution.
- Do not generate evidence before explicit authorization.
- Do not modify the frozen protocol artifacts.

## Required Runner Properties

The dedicated runner must:

- verify the frozen protocol reference;
- verify the seed-registry hash before execution;
- consume the exact 11 registered seed values;
- execute exactly three repeats per seed in deterministic manifest order;
- capture runtime identity and configuration;
- preserve raw output before analysis;
- compute hashes for raw evidence and manifests;
- assign stable run identifiers;
- fail closed on invariant violations;
- expose no execution path that bypasses authorization.

## Current State

**NOT READY FOR EXECUTION.** The architecture is specified; implementation and independent validation remain required.
