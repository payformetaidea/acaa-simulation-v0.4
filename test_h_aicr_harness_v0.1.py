import unittest

from h_aicr_harness_v0.1 import GraphDelta, weighted_ged, incentive_compatibility


class TestHACAAHarness(unittest.TestCase):
    def test_weighted_ged(self):
        delta = GraphDelta(node_add=1, edge_add=2, attribute_change=2)
        self.assertEqual(weighted_ged(delta), 4.0)

    def test_incentive_ratio(self):
        result = incentive_compatibility([125, 150, 175], [100, 100, 100])
        self.assertEqual(result["status"], "OK")
        self.assertAlmostEqual(result["ic_ratio"], 1.5)

    def test_unstable_denominator(self):
        result = incentive_compatibility([10, 20], [0, 0])
        self.assertEqual(result["status"], "DENOMINATOR_UNSTABLE")


if __name__ == "__main__":
    unittest.main()
