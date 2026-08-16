#!/usr/bin/env python3
"""F2.3-R1 baseline provenance reconciliation.

Investigation-only. The frozen S1 validator is never modified.
This revision explicitly distinguishes cryptographic file SHA-256 from
Git blob SHA-1 and treats a later-branch working tree as a separate state
from the frozen target commit.
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = "d1cef3768ccaa39525a0c23e1a9b94c3528a8995"
# Historical record under investigation: this value is 40 hex chars and
# therefore has SHA-1 length. It is retained as evidence, not relabeled.
EXPECTED_VALIDATOR_PROVENANCE = "5ba942980b63ed8f53dfd8f16e40e0f69349e98c"
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


def target_bytes(path):
    p = subprocess.run(("git", "show", f"{TARGET}:{path}"), cwd=ROOT, capture_output=True)
    return p.stdout if p.returncode == 0 else None


def git_blob_sha(path):
    r = run("git", "hash-object", str(ROOT / path))
    return r["stdout"] if r["returncode"] == 0 else None


def target_blob_sha(path):
    r = run("git", "rev-parse", f"{TARGET}:{path}")
    return r["stdout"] if r["returncode"] == 0 else None


def main():
    report = {
        "protocol": "F2.3-baseline-provenance-reconciliation-v2",
        "target_commit": TARGET,
        "head": run("git", "rev-parse", "HEAD")["stdout"],
        "branch": run("git", "branch", "--show-current")["stdout"],
        "status_porcelain": run("git", "status", "--porcelain")["stdout"],
        "target_commit_exists": run("git", "cat-file", "-e", f"{TARGET}^{{commit}}")["returncode"] == 0,
        "files": {},
    }

    for path in FILES:
        target = target_bytes(path)
        current = (ROOT / path).read_bytes() if (ROOT / path).exists() else None
        target_sha256 = sha256_bytes(target) if target is not None else None
        current_sha256 = sha256_bytes(current) if current is not None else None
        target_blob = target_blob_sha(path)
        current_blob = git_blob_sha(path) if current is not None else None
        report["files"][path] = {
            "exists_in_target_commit": target is not None,
            "target_commit_file_sha256": target_sha256,
            "working_tree_file_sha256": current_sha256,
            "file_sha256_match": target_sha256 == current_sha256,
            "target_git_blob_sha1": target_blob,
            "working_tree_git_blob_sha1": current_blob,
            "git_blob_match": target_blob == current_blob,
        }

    v = report["files"][FILES[0]]
    expected = EXPECTED_VALIDATOR_PROVENANCE
    report["historical_expected_validator_value"] = expected
    report["historical_expected_value_length"] = len(expected)
    report["historical_expected_value_matches_target_git_blob_sha1"] = expected == v["target_git_blob_sha1"]
    report["historical_expected_value_matches_target_file_sha256"] = expected == v["target_commit_file_sha256"]

    # Baseline integrity is established by commit->blob identity. A later
    # branch may legitimately differ in fixtures; that is branch drift, not
    # evidence that the frozen validator changed.
    if not report["target_commit_exists"]:
        classification = "TARGET_COMMIT_UNAVAILABLE"
    elif not v["git_blob_match"]:
        classification = "FROZEN_VALIDATOR_WORKTREE_MISMATCH"
    elif expected == v["target_git_blob_sha1"] and len(expected) == 40:
        classification = "PROVENANCE_LABEL_DEFECT_EXPECTED_VALUE_IS_GIT_BLOB_SHA1"
    elif not v["file_sha256_match"]:
        classification = "LATER_BRANCH_WORKTREE_DRIFT_NON_VALIDATOR"
    else:
        classification = "BASELINE_VALIDATOR_PROVENANCE_RECONCILED"

    report["classification"] = classification
    report["validator_baseline_integrity"] = "PASS" if v["git_blob_match"] else "FAIL"
    report["verdict"] = "PASS" if report["validator_baseline_integrity"] == "PASS" else "FAIL"
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
