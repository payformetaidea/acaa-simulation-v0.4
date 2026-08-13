"""Hard invariants for ACAA v0.6 E1 records."""
PROTOCOL = "ACAA-v0.6-E1"
CONTROL_TAG = "v0.5.0"
CONTROL_COMMIT = "de7d11ed9457ede84c1954aa70a59331bf07b72e"

def check(record: dict) -> list[str]:
    errors = []
    if record.get("protocol") != PROTOCOL:
        errors.append("protocol mismatch")
    target = record.get("control_target", {})
    if target.get("tag") != CONTROL_TAG:
        errors.append("control tag mismatch")
    if target.get("commit") != CONTROL_COMMIT:
        errors.append("frozen control commit mismatch")
    if not isinstance(record.get("seed"), int):
        errors.append("seed is not an integer")
    provenance = record.get("provenance", {})
    for key in ("runner", "input_sha256", "artifact_sha256"):
        if not provenance.get(key):
            errors.append("missing provenance: " + key)
    return errors
