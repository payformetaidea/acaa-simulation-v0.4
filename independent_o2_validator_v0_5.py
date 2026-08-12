#!/usr/bin/env python3
"""Independent O2 evidence validator.

The validator does not import the O2 producer or modify the v0.4 engine.
It validates only the materialized evidence artifact.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ID_RE = re.compile(r"^CAU-[0-9]{6}$")
REQUIRED = {"cau_id", "actor_id", "action", "verdict", "timestamp", "level", "provenance_linkage", "deterministic_record_representation"}
FIELDS = ["cau_id", "actor_id", "action", "verdict", "timestamp", "level"]


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def evidence_core(data):
    return {k: data[k] for k in ("schema", "objective", "execution", "aggregate", "records", "record_hashes")}


def validate(data):
    failures = []
    records = data.get("records", [])
    aggregate = data.get("aggregate", {}).get("cau_records")
    if aggregate != len(records): failures.append("O2-03 aggregate count mismatch")
    ids = [r.get("cau_id") for r in records]
    if any(not isinstance(x, str) or not ID_RE.fullmatch(x) for x in ids): failures.append("O2-01 malformed identity")
    if len(ids) != len(set(ids)): failures.append("O2-02 duplicate identity")
    valid_records = []
    for r in records:
        cid = r.get("cau_id")
        if not REQUIRED.issubset(r):
            failures.append(f"O2-05 required field missing: {cid}")
            continue
        if not r.get("provenance_linkage"): failures.append(f"O2-06 provenance empty: {cid}")
        try:
            expected = canonical({k: r[k] for k in FIELDS})
            if r.get("deterministic_record_representation") != expected:
                failures.append(f"O2-09 canonical representation mismatch: {cid}")
            else:
                valid_records.append(r)
        except KeyError:
            failures.append(f"O2-05 required field missing: {cid}")
    hashes = [digest(json.loads(r["deterministic_record_representation"])) for r in valid_records]
    if data.get("record_hashes") != hashes: failures.append("O2-09 record hash mismatch")
    manifest = data.get("manifest", {})
    if manifest.get("record_count") != len(records): failures.append("manifest record count mismatch")
    if manifest.get("record_hashes_digest") != digest(hashes): failures.append("manifest hash digest mismatch")
    if data.get("manifest_digest") != digest(manifest): failures.append("O2-N10 manifest integrity failure")
    if data.get("evidence_digest") != digest(evidence_core(data)): failures.append("evidence digest mismatch")
    return failures


def negative_cases(data):
    cases = {}
    base = json.loads(json.dumps(data))
    if len(base.get("records", [])) >= 2:
        dup = json.loads(json.dumps(base)); dup["records"].append(json.loads(json.dumps(base["records"][0]))); dup["aggregate"]["cau_records"] += 1
        cases["O2-N01"] = dup
        missing = json.loads(json.dumps(base)); missing["records"][0].pop("cau_id", None); cases["O2-N02"] = missing
        malformed = json.loads(json.dumps(base)); malformed["records"][0]["cau_id"] = "BAD-ID"; cases["O2-N03"] = malformed
        mismatch = json.loads(json.dumps(base)); mismatch["aggregate"]["cau_records"] += 1; cases["O2-N04"] = mismatch
        prov = json.loads(json.dumps(base)); prov["records"][0]["provenance_linkage"] = []; cases["O2-N05"] = prov
        post = json.loads(json.dumps(base)); post["records"][0]["actor_id"] = "MUTATED"; cases["O2-N08"] = post
        reuse = json.loads(json.dumps(base)); reuse["records"][1]["cau_id"] = reuse["records"][0]["cau_id"]; cases["O2-N09"] = reuse
        manifest = json.loads(json.dumps(base)); manifest["manifest"]["record_count"] += 1; cases["O2-N10"] = manifest
    return {cid: bool(validate(mutated)) for cid, mutated in cases.items()}


def main():
    p = argparse.ArgumentParser(); p.add_argument("artifact"); args = p.parse_args()
    data = json.loads(Path(args.artifact).read_text(encoding="utf-8"))
    failures = validate(data); negatives = negative_cases(data)
    print(f"O2 positive validation: {'PASS' if not failures else 'FAIL'}")
    for cid, ok in negatives.items(): print(f"{cid}: {'PASS' if ok else 'FAIL'}")
    if failures: print("Failures:", *failures, sep="\n- ")
    if failures or not negatives or not all(negatives.values()): raise SystemExit(1)

if __name__ == "__main__": main()
