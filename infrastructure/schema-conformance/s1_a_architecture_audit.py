#!/usr/bin/env python3
"""Executable S1-A architecture audit; does not mutate the repository."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = "d1cef3768ccaa39525a0c23e1a9b94c3528a8995"
VALIDATOR = ROOT / "infrastructure/schema-conformance/validate_s1.py"
SCHEMA = ROOT / "infrastructure/schemas/invariant-registry.schema.json"
F2_4_FIXTURE = ROOT / "infrastructure/schema-conformance/annotation/invariant-registry.invalid-date-time.json"
SEMANTIC_A = ROOT / "infrastructure/schema-conformance/invalid/invariant-registry.duplicate-id.json"
SEMANTIC_B = ROOT / "infrastructure/schema-conformance/invalid/invariant-registry.cross-field-mismatch.json"
S1V_WORKFLOW = ROOT / ".github/workflows/s1-v-f2-4-revalidation.yml"
EXPECTED_VALIDATOR_SHA256 = "30b62555377e1eac569c2ea7d08d66b6376257d492227fee271e830c567b10dc"
EXPECTED_SCHEMA_SHA256 = "624a2f8fea39cfa20440b8f53d3b500af710a54f76f12840ae1bbe0796fb68a7"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_show(path):
    return subprocess.check_output(["git", "show", f"{TARGET}:{path.relative_to(ROOT).as_posix()}"], text=False)


def check(name, ok, detail):
    return {"control": name, "result": "PASS" if ok else "FAIL", "detail": detail}


def main():
    results = []
    workflow_text = S1V_WORKFLOW.read_text()
    validator_text = VALIDATOR.read_text()
    results.append(check("validator-baseline-identity", sha(VALIDATOR) == EXPECTED_VALIDATOR_SHA256, sha(VALIDATOR)))
    results.append(check("schema-baseline-identity", sha(SCHEMA) == EXPECTED_SCHEMA_SHA256, sha(SCHEMA)))
    results.append(check("validator-byte-identical-to-target", VALIDATOR.read_bytes() == git_show(VALIDATOR), "working tree vs target commit"))
    results.append(check("schema-byte-identical-to-target", SCHEMA.read_bytes() == git_show(SCHEMA), "working tree vs target commit"))
    results.append(check("layer-separation", "SEMANTIC_NEGATIVE_FIXTURES" in validator_text and "semantic_errors" in validator_text, "Layer 1 and Layer 2 paths are explicit"))
    results.append(check("semantic-fixture-taxonomy", '"invariant-registry.duplicate-id.json": "REG-C-001"' in validator_text and '"invariant-registry.cross-field-mismatch.json": "REG-C-002"' in validator_text, "semantic negatives are explicitly mapped"))
    results.append(check("format-annotation-lineage", F2_4_FIXTURE.exists() and not (ROOT / "infrastructure/schema-conformance/invalid/invariant-registry.invalid-date-time.json").exists(), "date-time fixture is outside structural-negative corpus"))
    results.append(check("evidence-on-failure", "if: always()" in workflow_text and "Upload S1-V evidence" in workflow_text, "evidence upload is unconditional"))
    results.append(check("deterministic-rerun", "Run validator twice" in workflow_text and "structured_identical" in workflow_text, "two-run comparison is explicit"))
    results.append(check("provenance-separation", "TARGET_COMMIT" in workflow_text and "validator_sha256" in workflow_text, "commit and file hashes are separately recorded"))
    results.append(check("semantic-fixtures-present", SEMANTIC_A.exists() and SEMANTIC_B.exists(), "semantic-negative fixtures remain present"))
    report = {"audit": "S1-A", "target_commit": TARGET, "controls": results}
    report["verdict"] = "PASS" if all(x["result"] == "PASS" for x in results) else "FAIL"
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
