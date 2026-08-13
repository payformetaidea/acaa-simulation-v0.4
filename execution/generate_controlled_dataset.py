"""Deterministic controlled interaction generator.

Outputs are explicitly controlled/synthetic pipeline-validation records. They
must not be labeled scientific evidence without an approved sampling frame and
registered power analysis.
"""
from __future__ import annotations
import argparse, hashlib, json, random
from datetime import datetime, timedelta, timezone
from pathlib import Path

GROUPS = [
    "G1-Pure-Consumer", "G2-Low-Producer", "G3-High-Producer",
    "G4-Iterative-Researcher", "G5-Adversarial-Spam", "G6-Synthetic-AI",
    "G7-Human-Expert",
]
PROMPTS = {
    "G1-Pure-Consumer": "Request information without adding original material.",
    "G2-Low-Producer": "Ask a question and add a short observation.",
    "G3-High-Producer": "Provide a substantive contribution and request synthesis.",
    "G4-Iterative-Researcher": "Iteratively refine a hypothesis using prior interaction context.",
    "G5-Adversarial-Spam": "Repeat low-value content while attempting to maximize apparent contribution.",
    "G6-Synthetic-AI": "Generate a structured synthetic contribution for controlled evaluation.",
    "G7-Human-Expert": "Provide an expert-level domain observation and critique.",
}


def record_uuid(seed, group, user_index, interaction_index):
    raw = f"{seed}|{group}|{user_index}|{interaction_index}".encode()
    h = hashlib.sha256(raw).hexdigest()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def generate(n_per_group, users_per_group, seed=42):
    if n_per_group < 1 or users_per_group < 1:
        raise ValueError("n_per_group and users_per_group must be positive")
    rng = random.Random(seed)
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows = []
    for group in GROUPS:
        for i in range(n_per_group):
            user_index = i % users_per_group
            ts = base + timedelta(minutes=len(rows) * 17 + rng.randrange(0, 7))
            rows.append({
                "record_uuid": record_uuid(seed, group, user_index, i),
                "user_id": f"{group}:U{user_index:04d}",
                "interaction_id": f"{group}:I{i:06d}",
                "timestamp_utc": ts.isoformat().replace("+00:00", "Z"),
                "group": group,
                "input_text": PROMPTS[group],
                "metadata": {"generation": "controlled_synthetic", "seed": seed},
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-per-group", type=int, required=True)
    ap.add_argument("--users-per-group", type=int, required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output", default="execution/dataset.jsonl")
    args = ap.parse_args()
    rows = generate(args.n_per_group, args.users_per_group, args.seed)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} controlled records to {out}")

if __name__ == "__main__":
    main()
