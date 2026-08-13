#!/usr/bin/env python3
"""M-CEL: fail-closed machine-checkable H-AICR G0 execution lock."""
from __future__ import annotations
import argparse, hashlib, json, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROTOCOLS = [ROOT / "docs/research/H-AICR_v0.3.5_G0_PREREGISTRATION.md", ROOT / "docs/research/H-AICR_v0.3.5_G0_AUDIT.md"]
ARTIFACTS = {
    "dataset_schema": ROOT / "execution/schema/dataset.schema.json",
    "split_manifest": ROOT / "execution/splits.json",
    "seed_manifest": ROOT / "execution/seed.json",
    "model_revision": ROOT / "execution/model_revision.json",
    "dependency_lock": ROOT / "execution/dependency.lock",
    "annotation_schema": ROOT / "execution/annotation_schema.py",
    "leakage_checker": ROOT / "execution/leakage_checker.py",
    "raw_output_structure": ROOT / "execution/raw_output_structure.json",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def json_hash(value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def load(path: Path, code: str):
    if not path.is_file():
        raise RuntimeError(f"{code}: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"{code}: {e}") from e


def validate() -> dict:
    for p in PROTOCOLS:
        if not p.is_file():
            raise RuntimeError(f"PROTOCOL_MISSING: {p.relative_to(ROOT)}")

    schema = load(ARTIFACTS["dataset_schema"], "DATASET_SCHEMA_INVALID")
    if schema.get("$schema") != "http://json-schema.org/draft-07/schema#":
        raise RuntimeError("DATASET_SCHEMA_INVALID: Draft-07 declaration required")

    splits = load(ARTIFACTS["split_manifest"], "SPLIT_MANIFEST_INVALID")
    if set(splits) != {"train", "validation", "test"}:
        raise RuntimeError("SPLIT_MANIFEST_INVALID: train/validation/test required")
    ids = [x for k in splits for x in splits[k]]
    if len(ids) != len(set(ids)):
        raise RuntimeError("DATA_LEAKAGE_DETECTED: Record_UUID appears in multiple splits")

    seed = load(ARTIFACTS["seed_manifest"], "SEED_INVALID")
    if seed.get("seed") != 42:
        raise RuntimeError("SEED_INVALID: registered seed must be 42")
    rng = random.Random(42)
    probe = [rng.random() for _ in range(5)]
    if seed.get("dummy_process_sha256") != json_hash(probe):
        raise RuntimeError("SEED_REPRODUCIBILITY_FAILED: dummy probe mismatch")

    model = load(ARTIFACTS["model_revision"], "MODEL_REVISION_INVALID")
    if model.get("floating_tag"):
        raise RuntimeError("MODEL_REVISION_INVALID: floating tags forbidden")
    if not any(model.get(k) for k in ("commit_sha", "image_digest", "implementation_sha256")):
        raise RuntimeError("MODEL_REVISION_INVALID: immutable revision required")

    dep = ARTIFACTS["dependency_lock"]
    if not dep.is_file() or not dep.read_text(encoding="utf-8").strip():
        raise RuntimeError(f"DEPENDENCY_LOCK_MISSING: {dep.relative_to(ROOT)}")

    for key in ("annotation_schema", "leakage_checker"):
        if not ARTIFACTS[key].is_file():
            raise RuntimeError(f"{key.upper()}_MISSING: {ARTIFACTS[key].relative_to(ROOT)}")

    raw = load(ARTIFACTS["raw_output_structure"], "RAW_OUTPUT_STRUCTURE_INVALID")
    if raw.get("write_once") is not True:
        raise RuntimeError("IMMUTABILITY_POLICY_INVALID: write_once=true required")

    hashes = {p.name: sha256(p) for p in PROTOCOLS}
    hashes.update({k: sha256(p) for k, p in ARTIFACTS.items()})
    master = json_hash(dict(sorted(hashes.items())))
    return {"schema_version":"M-CEL-1.0","status":"PASS","protocol":"H-AICR-v0.3.5","repository":"payformetaidea/acaa-simulation-v0.4","branch":"execution-engineering/h-aicr-g0-v2","hash_algorithm":"SHA-256","hashes":dict(sorted(hashes.items())),"master_execution_hash":master,"scientific_outcomes_inspected":False}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="execution_lock.json")
    args = ap.parse_args()
    try:
        result = validate()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 2
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result["master_execution_hash"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
