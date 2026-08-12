#!/usr/bin/env python3
"""Independent O2 evidence validator.

This validator intentionally does not import or call O2 producer functions.
It validates a materialized evidence artifact against the frozen contract.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ID_RE = re.compile(r"^CAU-[0-9]{6}$")
REQUIRED = {"cau_id", "actor_id", "action", "verdict", "timestamp", "level", "provenance_linkage", "deterministic_record_representation"}


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def validate(data):
    failures = []
    records = data.get("records", [])
    aggregate = data.get("aggregate", {}).get("cau_records")
    if aggregate != len(records): failures.append("O2-03 aggregate count mismatch")
    ids = [r.get("cau_id") for r in records]
    if any(not isinstance(x, str) or not ID_RE.fullmatch(x) for x in ids): failures.append("O2-01 malformed identity")
    if len(ids) != len(set(ids)): failures.append("O2-02 duplicate identity")
    for r in records:
        if not REQUIRED.issubset(r): failures.append(f"O2-05 required field missing: {r.get('cau_id')}")
        if not r.get("provenance_linkage"): failures.append(f"O2-06 lifecycle/provenance empty: {r.get('cau_id')}")
        expected = canonical({k: r[k] for k in ["cau_id", "actor_id", "action", "verdict", "timestamp", "level"]})
        if r.get("deterministic_record_representation") != expected: failures.append(f"O2-09 canonical representation mismatch: {r.get('cau_id')}")
    hashes = [digest(json.loads(r["deterministic_record_representation"])) for r in records]
    if data.get("record_hashes") != hashes: failures.append("O2-09 record hash mismatch")
    manifest = data.get("manifest", {})
    if manifest.get("record_count") != len(records): failures.append("manifest record count mismatch")
    if manifest.get("record_hashes_digest") != digest(hashes): failures.append("manifest hash digest mismatch")
    supplied_manifest_digest = data.get("manifest_digest")
    if supplied_manifest_digest != digest(manifest): failures.append("O2-N10 manifest integrity failure")
    copy_for_digest = dict(data)
    copy_for_digest.pop("evidence_digest", None)
    # evidence_digest is defined over the evidence before that field is added.
    if data.get("evidence_digest") != digest(copy_for_digest): failures.append("evidence digest mismatch")
    return failures


def negative_cases(data):
    cases = {}
    base = json.loads(json.dumps(data))
    if base.get("records"):
        dup = json.loads(json.dumps(base)); dup["records"].append(json.loads(json.dumps(base["records"][0]))); dup["aggregate"]["cau_records"] += 1
        cases["O2-N01"] = dup
        missing = json.loads(json.dumps(base)); missing["records"][0].pop("cau_id", None)
        cases["O2-N02"] = missing
        malformed = json.loads(json.dumps(base)); malformed["records"][0]["cau_id"] = "BAD-ID"
        cases["O2-N03"] = malformed
        mismatch = json.loads(json.dumps(base)); mismatch["aggregate"]["cau_records"] += 1
        cases["O2-N04"] = mismatch
        prov = json.loads(json.dumps(base)); prov["records"][0]["provenance_linkage"] = []
        cases["O2-N05"] = prov
        post = json.loads(json.dumps(base)); post["records"][0]["actor_id"] = "MUTATED"
        cases["O2-N08"] = post
        reuse = json.loads(json.dumps(base)); reuse["records"][1]["cau_id"] = reuse["records"][0]["cau_id"]
        cases["O2-N09"] = reuse
        manifest = json.loads(json.dumps(base)); manifest["manifest"]["record_count"] += 1
        cases["O2-N10"] = manifest
    results = {}
    for cid, mutated in cases.items():
        results[cid] = bool(validate(mutated))
    return results


def main():
    p = argparse.ArgumentParser(); p.add_argument("artifact"); args = p.parse_args()
    data = json.loads(Path(args.artifact).read_text(encoding="utf-8"))
    failures = validate(data)
    negatives = negative_cases(data)
    print(f"O2 positive validation: {'PASS' if not failures else 'FAIL'}")
    for cid, ok in negatives.items(): print(f"{cid}: {'PASS' if ok else 'FAIL'}")
    if failures: print("Failures:", *failures, sep="\n- ")
    if failures or not negatives or not all(negatives.values()): raise SystemExit(1)


if __name__ == "__main__": main()
