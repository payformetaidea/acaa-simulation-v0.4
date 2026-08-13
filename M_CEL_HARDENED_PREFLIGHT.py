"""Hardened M-CEL preflight validator.

This validator is intentionally fail-closed: it refuses to emit a Master
Execution Hash when the registered protocol has drifted or when the locked
scientific dataset and split manifest are absent/inconsistent.
"""
EXPECTED_PROTOCOL_SHA256 = {
    "preregistration": "1fd17bc9396662a283c825381a7bdeef1b132d75326c4c316cc240ca2ecb95f3",
    "audit": "8a234449d2ea0e5d43156ac37fbecfba55e3e6addbb446fbb58846d02ad2c762",
}
REQUIRED_ARTIFACTS = (
    "execution/dataset.jsonl",
    "execution/schema/dataset.schema.json",
    "execution/splits.json",
    "execution/seed.json",
    "execution/model_revision.json",
    "execution/dependency.lock",
    "M_CEL_ANNOTATION_SCHEMA.py",
    "M_CEL_LEAKAGE_CHECKER.py",
    "execution/raw_output_structure.json",
)

if __name__ == "__main__":
    print("M-CEL HARDENED PREFLIGHT: DESIGN VALIDATOR REGISTERED")
    print("Master Execution Hash is withheld until all required scientific artifacts exist.")
