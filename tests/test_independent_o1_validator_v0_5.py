#!/usr/bin/env python3
"""Regression tests for independent O1 evidence validation boundaries."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "independent_o1_validator_v0_5.py"
SPEC = importlib.util.spec_from_file_location("independent_o1_validator", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class IndependentFingerprintTests(unittest.TestCase):
    def test_effective_fingerprint_uses_immutable_pre_run_base(self):
        base_keys = VALIDATOR.BASE_KEYS
        pre_run_params = {key: 1 for key in base_keys}
        pre_run_base = VALIDATOR.base_fp(pre_run_params)

        run = {
            "o1_base_config_fingerprint": pre_run_base,
            "params": dict(pre_run_params),
            "effective_config": {
                "seed": 42,
                "scenario": "baseline",
                "scenario_params": {},
            },
        }
        expected = VALIDATOR.hashlib.sha256(
            json.dumps({
                "base_fingerprint": pre_run_base,
                "seed": 42,
                "scenario": "baseline",
                "scenario_params": {},
            }, sort_keys=True).encode()
        ).hexdigest()

        self.assertEqual(VALIDATOR.effective_fp(run), expected)

    def test_post_run_adaptive_params_do_not_change_effective_fingerprint(self):
        base_params = {key: 1 for key in VALIDATOR.BASE_KEYS}
        pre_run_base = VALIDATOR.base_fp(base_params)
        run = {
            "o1_base_config_fingerprint": pre_run_base,
            "params": dict(base_params),
            "effective_config": {
                "seed": 137,
                "scenario": "baseline",
                "scenario_params": {},
            },
        }

        before = VALIDATOR.effective_fp(run)
        run["params"]["noise"] = 999
        run["params"]["periods"] = 9999
        run["params"]["equilibrium_variance_threshold"] = 999

        self.assertEqual(VALIDATOR.effective_fp(run), before)

    def test_missing_pre_run_fingerprint_is_rejected(self):
        run = {
            "params": {key: 1 for key in VALIDATOR.BASE_KEYS},
            "effective_config": {
                "seed": 42,
                "scenario": "baseline",
                "scenario_params": {},
            },
        }
        with self.assertRaises(VALIDATOR.ValidationError):
            VALIDATOR.effective_fp(run)


if __name__ == "__main__":
    unittest.main()
