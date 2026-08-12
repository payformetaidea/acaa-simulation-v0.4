#!/usr/bin/env python3
"""Regression tests for independent O1 evidence validation boundaries."""
from __future__ import annotations
import importlib.util, json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('independent_o1_validator',ROOT/'independent_o1_validator_v0_5.py')
assert SPEC and SPEC.loader
VALIDATOR=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(VALIDATOR)

class IndependentFingerprintTests(unittest.TestCase):
    def make_run(self):
        params={key:1 for key in VALIDATOR.BASE_KEYS}
        return {'params':params,'effective_config':{'seed':42,'scenario':'baseline','scenario_params':{}}}

    def test_effective_fingerprint_reproduces_from_post_run_configuration(self):
        run=self.make_run()
        expected=VALIDATOR.effective_fp(run)
        self.assertEqual(len(expected),64)
        self.assertEqual(run['effective_config'].get('scenario'), 'baseline')

    def test_post_run_configuration_is_part_of_effective_identity(self):
        run=self.make_run()
        before=VALIDATOR.effective_fp(run)
        run['params']['noise']=999
        run['params']['periods']=9999
        self.assertNotEqual(VALIDATOR.effective_fp(run),before)

    def test_missing_base_configuration_fields_are_rejected(self):
        run=self.make_run()
        del run['params']['noise']
        with self.assertRaises(KeyError):
            VALIDATOR.effective_fp(run)

if __name__=='__main__': unittest.main()
