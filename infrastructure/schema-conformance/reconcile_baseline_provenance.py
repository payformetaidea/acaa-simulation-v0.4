#!/usr/bin/env python3
"""F2.3 Baseline Provenance Reconciliation.

Investigation-only. This protocol does not modify the frozen S1 validator.
It reconciles commit -> tree -> blob -> working-tree provenance for the
validator, schema, and controlled fixture set.
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = "d1cef3768ccaa39525a0c23e1a9b94c3528a8995"
EXPECTED_VALIDATOR_SHA256 = "5ba942980b63ed8f53dfd8f16e40e0f69349e98c"
FILES = [
    "infrastructure/schema-conformance/validate_s1.py",
    "infrastructure/schemas/invariant-registry.schema.json",
    "infrastructure/schema-conformance/invalid/invariant-registry.cross-field-mismatch.json",
]


def run(*args):
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    return {"returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(path.read_bytes())


def git_blob_sha(path):
    r = run("git", "hash-object", str(path))
    return r["stdout"] if r["returncode"] == 0 else None


def target_blob_sha(path):
    r = run("git", "rev-parse", f"{TARGET}:{path}")
    return r["stdout"] if r["returncode"] == 0 else None


def target_file_sha256(path):
    r = run("git", "show", f"{TARGET}:{path}")
    if r["returncode"] != 0:
        return None
    return sha256_bytes(r["stdout"].encode())


def main():
    report = {
        "protocol": "F2.3-baseline-provenance-reconciliation-v1",
        "target_commit": TARGET,
        "head": run("git", "rev-parse", "HEAD")["stdout"],
        "branch": run("git", "branch", "--show-current")["stdout"],
        "status_porcelain": run("git", "status", "--porcelain")["stdout"],
        "target_commit_exists": run("git", "cat-file", "-e", f"{TARGET}^{{commit}}")["returncode"] == 0,
        "files": {},
    }

    for path in FILES:
        p = ROOT / path
        target_sha = target_file_sha256(path)
        current_sha = sha256_file(p)
        target_blob = target_blob_sha(path)
        current_blob = git_blob_sha(path)
        report["files"][path] = {
            "target_commit_sha256": target_sha,
            "working_tree_sha256": current_sha,
            "sha256_match": target_sha == current_sha,
            "target_git_blob_sha1": target_blob,
            "working_tree_git_blob_sha1": current_blob,
            "git_blob_match": target_blob == current_blob,
            "exists_in_target_commit": target_sha is not None,
        }

    v = report["files"][FILES[0]]
    report["validator_expected_sha256"] = EXPECTED_VALIDATOR_SHA256
    report["validator_expected_sha_match"] = v["target_commit_sha256"] == EXPECTED_VALIDATOR_SHA256
    report["validator_commit_to_worktree_match"] = v["sha256_match"]
    report["validator_blob_match"] = v["git_blob_match"]

    if not report["target_commit_exists"]:
        classification = "TARGET_COMMIT_UNAVAILABLE"
    elif not v["sha256_match"] or not v["git_blob_match"]:
        classification = "CHECKOUT_OR_WORKTREE_INTEGRITY_DEFECT"
    elif not report["validator_expected_sha_match"]:
        classification = "PROVENANCE_RECORD_EXPECTED_SHA_DEFECT"
    else:
        classification = "BASELINE_PROVENANCE_RECONCILED"

    report["classification"] = classification
    report["verdict"] = "PASS" if classification == "BASELINE_PROVENANCE_RECONCILED" else "FAIL"
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
