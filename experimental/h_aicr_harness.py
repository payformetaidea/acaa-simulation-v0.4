#!/usr/bin/env python3
"""H-AICR execution-engineering scaffold.

Generates controlled synthetic interaction records and enforces the
user-disjoint split required by the frozen protocol. This module makes no
empirical validity claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path

SEED = 20260813
GROUPS = [
    "G1-Pure-Consumer", "G2-Low-Producer", "G3-High-Producer",
    "G4-Iterative-Researcher", "G5-Adversarial-Spam",
    "G6-Synthetic-AI", "G7-Human-Expert",
]

@dataclass(frozen=True)
class Interaction:
    interaction_id: str
    user_id: str
    group: str
    role: str
    text: str
    correction_count: int
    artifact_count: int


def stable_id(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


def generate_interactions(per_group: int = 20, seed: int = SEED) -> list[Interaction]:
    rng = random.Random(seed)
    rows = []
    for group in GROUPS:
        for i in range(per_group):
            user = stable_id(group, str(i))
            if group == "G1-Pure-Consumer":
                role, c, a = "Consumer", 0, 0
            elif group == "G2-Low-Producer":
                role, c, a = "Producer", rng.randint(0, 1), rng.randint(0, 1)
            elif group == "G3-High-Producer":
                role, c, a = "Producer", rng.randint(1, 3), rng.randint(1, 3)
            elif group == "G4-Iterative-Researcher":
                role, c, a = "Producer", rng.randint(2, 5), rng.randint(1, 4)
            elif group == "G5-Adversarial-Spam":
                role, c, a = "Producer", rng.randint(0, 1), rng.randint(4, 8)
            elif group == "G6-Synthetic-AI":
                role, c, a = "Producer", rng.randint(1, 2), rng.randint(1, 3)
            else:
                role, c, a = "Producer", rng.randint(2, 4), rng.randint(1, 4)
            text = f"{group} interaction {i}: structured contribution."
            rows.append(Interaction(stable_id(user, str(i)), user, group, role, text, c, a))
    return rows


def user_disjoint_split(rows: list[Interaction], test_fraction: float = 0.20, seed: int = SEED):
    users = sorted({r.user_id for r in rows})
    rng = random.Random(seed)
    rng.shuffle(users)
    cut = max(1, round(len(users) * test_fraction))
    test_users = set(users[:cut])
    train = [r for r in rows if r.user_id not in test_users]
    test = [r for r in rows if r.user_id in test_users]
    if {r.user_id for r in train} & {r.user_id for r in test}:
        raise AssertionError("user leakage detected")
    return train, test


def write_jsonl(path: Path, rows: list[Interaction]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(asdict(r), ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="artifacts/h-aicr")
    p.add_argument("--per-group", type=int, default=20)
    args = p.parse_args()
    rows = generate_interactions(args.per_group)
    train, test = user_disjoint_split(rows)
    out = Path(args.output)
    write_jsonl(out / "interactions.jsonl", rows)
    write_jsonl(out / "train.jsonl", train)
    write_jsonl(out / "test.jsonl", test)
    manifest = {"seed": SEED, "groups": GROUPS, "rows": len(rows), "train": len(train), "test": len(test), "user_disjoint": True, "status": "SCAFFOLD_ONLY"}
    (out / "generation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
