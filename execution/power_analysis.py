"""Registered power-analysis guard for H-AICR-007.

The 25% IC ratio alone does not determine sample size. A dispersion/CV
assumption is therefore required before confirmatory dataset generation.
"""
from __future__ import annotations
import math
from statistics import NormalDist

TARGET_RATIO = 1.25
ALPHA = 0.05
POWER = 0.80


def required_n_per_group(cv: float, ratio: float = TARGET_RATIO,
                         alpha: float = ALPHA, power: float = POWER) -> int:
    if cv <= 0 or ratio <= 1:
        raise ValueError("cv must be > 0 and ratio must be > 1")
    sigma_log = math.sqrt(math.log1p(cv * cv))
    effect = math.log(ratio) / sigma_log
    z_alpha = NormalDist().inv_cdf(1 - alpha / 2)
    z_power = NormalDist().inv_cdf(power)
    return math.ceil(2 * ((z_alpha + z_power) / effect) ** 2)


def sensitivity_table():
    return {cv: required_n_per_group(cv) for cv in (0.30, 0.40, 0.50, 0.60)}


if __name__ == "__main__":
    for cv, n in sensitivity_table().items():
        print(f"CV={cv:.2f} n/group={n}")
    print("STATUS=PARAMETER_REQUIRED")
