#!/usr/bin/env python3
"""Regression tests for independent O1 evidence validation boundaries."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "independent_o1_validator", ROOT / "independent_o1_validator_v0_5.py"
)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class IndependentFingerprintTests(unittest.TestCase):
    def make_run(self):
        return {
            "params": {key: 1 for key in VALIDATOR.BASE_KEYS},
            "effective_config": {
                "seed": 42,
                "scenario": "baseline",
                "scenario_params": {},
            },
            "o1_base_config_fingerprint": "b" * 64,
        }

    def test_effective_fingerprint_reproduces_from_post_run_base_config(self):
        run = self.make_run()
        expected = VALIDATOR.effective_fp(run)
        self.assertEqual(len(expected), 64)
        self.assertEqual(run["effective_config"].get("scenario"), "baseline")

    def test_post_run_configuration_changes_effective_identity(self):
        run = self.make_run()
        before = VALIDATOR.effective_fp(run)
        run["params"]["noise"] = 999
        run["params"]["periods"] = 9999
        self.assertNotEqual(VALIDATOR.effective_fp(run), before)

    def test_missing_post_run_configuration_is_rejected(self):
        run = self.make_run()
        del run["params"]
        with self.assertRaises(VALIDATOR.ValidationError):
            VALIDATOR.effective_fp(run)

    def test_prerun_identity_is_separate_from_effective_identity(self):
        run = self.make_run()
        prerun = run["o1_base_config_fingerprint"]
        self.assertEqual(len(prerun), 64)
        effective_before = VALIDATOR.effective_fp(run)
        run["params"]["noise"] = 999
        self.assertEqual(run["o1_base_config_fingerprint"], prerun)
        self.assertNotEqual(VALIDATOR.effective_fp(run), effective_before)


if __name__ == "__main__":
    unittest.main()
