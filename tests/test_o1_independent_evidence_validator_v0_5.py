import copy
import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('independent_validator',ROOT/'o1_independent_evidence_validator_v0_5.py')
assert SPEC and SPEC.loader
V=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(V)

class IndependentO1Tests(unittest.TestCase):
    def test_effective_fingerprint_reproduction(self):
        run={'params':{'a':1,'seed':42},'effective_config':{'seed':42,'scenario':'baseline','scenario_params':{},'fingerprint':''}}
        run['effective_config']['fingerprint']=V.effective_fp(run)
        self.assertEqual(run['effective_config']['fingerprint'],V.effective_fp(run))

    def test_tukey_and_summary(self):
        s=V.summarize([1.0,1.0,1.0,1.0,10.0])
        self.assertIn(4,s['outliers']['indices'])
        self.assertAlmostEqual(s['mean'],2.8)

    def test_missing_run_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'o1_evidence.json').write_text(json.dumps({'objective':'O1','protocol':{'planned_seed_set':V.SEEDS,'executed_seed_set':V.SEEDS,'seed_count':12}}))
            with self.assertRaises(AssertionError): V.validate(root,Path('/dev/null'))

    def test_mutation_of_digest_is_detectable(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'run.json'; p.write_text('{"x":1}')
            original=V.sha256_file(p); p.write_text('{"x":2}')
            self.assertNotEqual(original,V.sha256_file(p))

if __name__=='__main__': unittest.main()
