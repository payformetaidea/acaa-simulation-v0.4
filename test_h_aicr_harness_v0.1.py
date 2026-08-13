import importlib.util
from pathlib import Path
import unittest


_MODULE_PATH = Path(__file__).with_name("h_aicr_harness_v0.1.py")
_SPEC = importlib.util.spec_from_file_location("h_aicr_harness_v0_1", _MODULE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Unable to load harness module: {_MODULE_PATH}")
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

GraphDelta = _MODULE.GraphDelta
weighted_ged = _MODULE.weighted_ged
incentive_compatibility = _MODULE.incentive_compatibility
bootstrap_ratio_lcb = _MODULE.bootstrap_ratio_lcb
generate_controlled_groups = _MODULE.generate_controlled_groups


class TestHACAAHarness(unittest.TestCase):
    def test_weighted_ged(self):
        delta = GraphDelta(node_add=1, edge_add=2, attribute_change=2)
        self.assertEqual(weighted_ged(delta), 4.0)

    def test_incentive_ratio(self):
        result = incentive_compatibility([125, 150, 175], [100, 100, 100])
        self.assertEqual(result["status"], "OK")
        self.assertAlmostEqual(result["ic_ratio"], 1.5)
        self.assertEqual(result["threshold"], 1.25)

    def test_unstable_denominator(self):
        result = incentive_compatibility([10, 20], [0, 0])
        self.assertEqual(result["status"], "DENOMINATOR_UNSTABLE")

    def test_bootstrap_lcb_is_deterministic(self):
        values = ([125, 150, 175], [100, 100, 100])
        first = bootstrap_ratio_lcb(*values, seed=20260813, resamples=2000, alpha=0.10)
        second = bootstrap_ratio_lcb(*values, seed=20260813, resamples=2000, alpha=0.10)
        self.assertEqual(first, second)
        self.assertGreater(first, 1.00)

    def test_controlled_groups_are_deterministic_and_balanced(self):
        first = generate_controlled_groups(seed=20260813, n_per_group=20)
        second = generate_controlled_groups(seed=20260813, n_per_group=20)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 140)
        counts = {}
        for row in first:
            counts[row["group"]] = counts.get(row["group"], 0) + 1
        self.assertEqual(len(counts), 7)
        self.assertTrue(all(count == 20 for count in counts.values()))


if __name__ == "__main__":
    unittest.main()
