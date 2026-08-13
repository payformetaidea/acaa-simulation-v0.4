# v0.6-D1 — Clean Environment Setup

## Reference environment

The reference runtime is the environment declared by the frozen repository workflow:

- Linux environment equivalent to the GitHub Actions Ubuntu runner
- Python 3.10
- Git

## Clean setup

1. Create a fresh working directory.
2. Clone the repository.
3. Check out the exact frozen target:

```bash
git clone https://github.com/payformetaidea/acaa-simulation-v0.4.git
cd acaa-simulation-v0.4
git checkout de7d11ed9457ede84c1954aa70a59331bf07b72e
```

4. Verify the immutable control point:

```bash
git rev-parse HEAD
git describe --tags --exact-match
```

Expected values:

```text
de7d11ed9457ede84c1954aa70a59331bf07b72e
v0.5.0
```

5. Record the host operating system and Python runtime:

```bash
uname -a
python3 --version
python3 -m pip --version
```

6. Confirm that the dependency manifest declares no third-party packages. Do not install unrecorded packages merely to make the run succeed.

7. If a command fails because of a missing package, runtime feature, OS facility, or undocumented environment assumption, stop the baseline replication at that point and record the observation under H-002 / F-R3 before remediation.

## File-integrity precheck

Before execution, record SHA-256 values for all required input files listed in `artifact-manifest.json`:

```bash
sha256sum \
  value_flow_simulator_v0.4.py \
  o1_robustness_v0_5.py \
  independent_o1_validator_v0_5.py \
  prepare_o1_independent_evidence_v0_5.py \
  tests/test_o1_robustness_v0_5.py \
  tests/test_independent_o1_validator_v0_5.py
```

Do not edit tracked files during the replication run.
