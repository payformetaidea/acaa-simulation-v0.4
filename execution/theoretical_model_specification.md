# H-AICR G0 Theoretical Agent Model Specification

## Status

`FROZEN_DESIGN_SPECIFICATION` — In-Silico Theoretical Evidence only.

This document defines the mathematical design of the agent-based simulation. Parameter values are **theoretical design parameters**, not empirical estimates of human behavior. No human-population inference is licensed from this simulation.

## 1. Common state and utility

Each independent analytical unit is an agent observed over a fixed study window. For interaction `t`, latent effort `e_t >= 0` produces substantive contribution according to:

`q(e_t) = 1 - exp(-e_t)`

The baseline agent utility is:

`U_t = b * q(e_t) - c_g * e_t`

where `b = 1.0` is the common theoretical benefit coefficient and `c_g` is the cohort-specific effort-cost parameter.

For `0 < c_g < b`, the deterministic utility-maximising effort is:

`e*_g = ln(b / c_g)`

For `c_g >= b`, `e*_g = 0`.

The simulation uses these closed-form optima rather than fitting parameters to observed human data.

## 2. Observable quantities

For each interaction:

- `contribution_score = 10 * q(e_t)` and is bounded to `[0,10]`.
- `credit = 10 * (q(e_t) + gaming_t)` clipped to `[0,10]`.
- `gaming_t` is cohort-specific and represents divergence between the observable reward metric and substantive contribution.
- `ground_truth_label` is generated from the frozen cohort rule and is not inferred from post-hoc clustering.

The simulation therefore distinguishes substantive contribution from an observable credit/reward signal.

## 3. Frozen cohort parameters

| Cohort | Model role | `c_g` | Base effort `e*` | Gaming rule | Operational boundary |
|---|---|---:|---:|---|---|
| G1 | Pure consumer | `1.25` | `0` | `0` | `e* = 0` and `q(e*) < 0.05` |
| G2 | Low producer | `0.75` | `ln(1/0.75)` | `0` | `0.05 <= q(e*) < 0.40` |
| G3 | High producer | `0.45` | `ln(1/0.45)` | `0` | `q(e*) >= 0.40` |
| G4 | Iterative researcher | `0.50` | `ln(1/0.50)` | `0` | at least 3 sequential revisions with non-decreasing `q(e)` across the first 4 qualifying interactions |
| G5 | Adversarial/spam | `0.90` | `ln(1/0.90)` | `gaming_t = min(0.60, 0.15 + 0.05*t)` | `credit_t - contribution_t >= 1.50` on at least 3 interactions and substantive `q(e) < 0.40` |
| G6 | Synthetic AI | `0.40` | `ln(1/0.40)` | `0` | provenance declares `agent_type = synthetic_ai` and `model_revision = deterministic_abm_v1` |
| G7 | Expert proxy | `0.35` | `ln(1/0.35)` | `0` | expertise proxy flag true and `q(e*) >= 0.50` |

For G4, the refinement trajectory is deterministic: for the first four qualifying interactions, effort multipliers are `[0.75, 0.90, 1.00, 1.10]` applied to `e*`, with later interactions repeating the final state. This is a theoretical trajectory rule, not an empirical estimate.

For G5, the agent optimises the observable credit signal rather than substantive contribution. The gaming term is deterministic and bounded, creating an explicit Goodhart-style divergence between reward and contribution.

## 4. Cohort exclusivity

Cohort assignment is made from the frozen generation mode and model parameters. Each analytical unit belongs to exactly one cohort. Cohort membership is assigned before any generated outcome is evaluated.

## 5. Determinism

All stochastic components, if introduced by the implementation, must use registered seed `42` and deterministic stream partitioning. UUIDs must be UUID5 values derived from the frozen namespace and canonical unit/interaction keys. No system clock, UUID4, or unseeded randomness is permitted.

## 6. Epistemic boundary

The generated dataset is `IN_SILICO_THEORETICAL_EVIDENCE`. It may test algorithmic behavior, implementation consistency, sensitivity, and internal validity of the simulation. It must not be presented as direct empirical evidence about human users.

## 7. Reproducibility rule

Any change to equations, cohort parameters, boundary rules, trajectory multipliers, or generation semantics constitutes a protocol change and requires a new preregistered revision before scientific generation.
