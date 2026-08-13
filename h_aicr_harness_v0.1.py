"""H-AICR execution-engineering harness (stdlib-only scaffold).

This module provides deterministic building blocks for preregistered
engineering tests. It does not claim empirical validity.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median
from typing import Iterable, Mapping
import random

NODE_W = 2.0
EDGE_W = 1.0
ATTRIBUTE_W = 0.5
IC_THRESHOLD = 1.25
IC_LCB_THRESHOLD = 1.00

@dataclass(frozen=True)
class GraphDelta:
    node_add: int = 0
    node_delete: int = 0
    edge_add: int = 0
    edge_delete: int = 0
    attribute_change: int = 0

    def weighted_cost(self) -> float:
        return (
            NODE_W * (self.node_add + self.node_delete)
            + EDGE_W * (self.edge_add + self.edge_delete)
            + ATTRIBUTE_W * self.attribute_change
        )


def weighted_ged(delta: GraphDelta) -> float:
    """Return preregistered weighted GED cost for an evaluated delta."""
    return delta.weighted_cost()


def incentive_compatibility(
    honest_credit: Iterable[float], strategic_credit: Iterable[float]
) -> Mapping[str, float | str]:
    """Compute the preregistered behavioral IC index.

    A negligible strategic denominator is explicitly unstable rather than
    being treated as automatic success.
    """
    honest = list(honest_credit)
    strategic = list(strategic_credit)
    if not honest or not strategic:
        raise ValueError("Both cohorts require observations")
    h = mean(honest)
    s = mean(strategic)
    if s <= 1e-12:
        return {
            "status": "DENOMINATOR_UNSTABLE",
            "mean_honest": h,
            "mean_strategic": s,
        }
    return {
        "status": "OK",
        "mean_honest": h,
        "mean_strategic": s,
        "ic_ratio": h / s,
        "median_honest": median(honest),
        "median_strategic": median(strategic),
        "threshold": IC_THRESHOLD,
    }


def bootstrap_ratio_lcb(
    honest_credit: Iterable[float], strategic_credit: Iterable[float],
    seed: int = 20260813, resamples: int = 10000, alpha: float = 0.10,
) -> float:
    """Percentile bootstrap lower bound for the mean-credit ratio.

    The function is intentionally simple and deterministic. Production
    analysis should use the locked analysis environment and report its
    dependency versions in the execution manifest.
    """
    honest = list(honest_credit)
    strategic = list(strategic_credit)
    if not honest or not strategic:
        raise ValueError("Both cohorts require observations")
    if mean(strategic) <= 1e-12:
        raise ZeroDivisionError("Strategic-credit denominator is unstable")
    rng = random.Random(seed)
    ratios = []
    for _ in range(resamples):
        hs = [honest[rng.randrange(len(honest))] for _ in honest]
        ss = [strategic[rng.randrange(len(strategic))] for _ in strategic]
        denom = mean(ss)
        if denom > 1e-12:
            ratios.append(mean(hs) / denom)
    if not ratios:
        raise ZeroDivisionError("All bootstrap denominators were unstable")
    ratios.sort()
    index = max(0, min(len(ratios) - 1, int(alpha * len(ratios))))
    return ratios[index]


def generate_controlled_groups(seed: int = 20260813, n_per_group: int = 20):
    """Generate deterministic interaction metadata for harness testing.

    These are synthetic control records only. They are not human ground truth.
    """
    rng = random.Random(seed)
    groups = [
        "G1-Pure-Consumer", "G2-Low-Producer", "G3-High-Producer",
        "G4-Iterative-Researcher", "G5-Adversarial-Spam",
        "G6-Synthetic-AI", "G7-Human-Expert",
    ]
    return [
        {
            "user_id": f"{group}-{i:03d}",
            "group": group,
            "seed_feature": rng.random(),
        }
        for group in groups for i in range(n_per_group)
    ]


if __name__ == "__main__":
    delta = GraphDelta(node_add=2, edge_add=3, attribute_change=4)
    print({"weighted_ged": weighted_ged(delta)})
    groups = generate_controlled_groups()
    print({"synthetic_records": len(groups), "groups": 7})
