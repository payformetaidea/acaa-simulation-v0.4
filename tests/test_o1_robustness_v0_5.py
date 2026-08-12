#!/usr/bin/env python3
"""Machine-checkable tests for the frozen O1 contract."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "o1_robustness_v0_5.py"
SPEC = importlib.util.spec_from_file_location("o1_runner", MODULE_PATH)
assert SPEC and SPEC.loader
O1 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(O1)


class O1ContractTests(unittest.TestCase):
    def record(self, seed: int, base: str = "base", engine: str = "engine"):
        return {
            "seed": seed,
            "base_config_fingerprint": base,
            "effective_config_fingerprint": f"effective-{seed}",
            "engine_hash": engine,
            "execution_timestamp": "2026-08-12T00:00:00+00:00",
            "final_cau_count": 1000 + seed,
            "final_gini": 0.02,
            "gate_efficiency": 0.2,
            "failure_rate": 0.1,
            "total_artifacts": 100,
            "detected_agents": 0,
            "isolated_agents": 0,
            "artifact_digest": "a" * 64,
        }

    def valid_records(self):
        return [self.record(seed) for seed in O1.PLANNED_SEEDS]

    def assert_contract_failure(self, records):
        with self.assertRaises(O1.O1ContractError):
            O1.validate_protocol(records)

    def test_o1_01_planned_equals_executed(self):
        records = self.valid_records()
        O1.validate_protocol(records)
        records.pop(0)
        self.assert_contract_failure(records)

    def test_o1_02_duplicate_seed_rejected(self):
        records = self.valid_records()
        records[1]["seed"] = records[0]["seed"]
        self.assert_contract_failure(records)

    def test_o1_03_configuration_change_rejected(self):
        records = self.valid_records()
        records[3]["base_config_fingerprint"] = "mutated"
        self.assert_contract_failure(records)

    def test_o1_05_engine_hash_change_rejected(self):
        records = self.valid_records()
        records[5]["engine_hash"] = "mutated"
        self.assert_contract_failure(records)

    def test_o1_06_required_evidence_field_rejected(self):
        records = self.valid_records()
        del records[0]["final_gini"]
        self.assert_contract_failure(records)

    def test_summary_statistics(self):
        result = O1.summarize([1.0, 2.0, 3.0, 4.0])
        self.assertEqual(result["mean"], 2.5)
        self.assertAlmostEqual(result["variance"], 1.25)
        self.assertAlmostEqual(result["standard_deviation"], 1.118033988749895)
        self.assertAlmostEqual(result["coefficient_of_variation"], 0.447213595499958)

    def test_zero_mean_cv_rule(self):
        result = O1.summarize([-1.0, 1.0])
        self.assertIsNone(result["coefficient_of_variation"])
        self.assertEqual(result["cv_reason"], "zero_mean")

    def test_tukey_rule(self):
        result = O1.tukey_outliers([1.0, 1.0, 1.0, 1.0, 10.0])
        self.assertIn(4, result["indices"])

    def test_artifact_negative_cases(self):
        artifact = {
            "params": {},
            "periods_executed": 1,
            "cau_records": 1,
            "agents": {},
            "metrics": [{
                "period": 1,
                "gini_coefficient": 0.01,
                "gate_efficiency": 0.2,
                "failure_rate": 0.1,
                "total_artifacts": 1,
            }],
            "attack_log": [],
            "adaptive_log": [],
            "provenance_events": 1,
            "engine_hash": "engine",
            "config_hash": "config",
            "effective_config": {"seed": 42},
            "execution_timestamp": "2026-08-12T00:00:00+00:00",
            "scenario": "baseline",
            "random_seed": 42,
        }
        O1.validate_artifact(artifact, 42)

        for mutation in (
            lambda x: x.pop("random_seed"),
            lambda x: x.update(random_seed=137),
            lambda x: x["metrics"][0].pop("gate_efficiency"),
            lambda x: x["metrics"][0].update(gate_efficiency="malformed"),
            lambda x: x.update(scenario="sybil"),
        ):
            mutated = copy.deepcopy(artifact)
            mutation(mutated)
            with self.assertRaises(O1.O1ContractError):
                O1.validate_artifact(mutated, 42)


if __name__ == "__main__":
    unittest.main()
