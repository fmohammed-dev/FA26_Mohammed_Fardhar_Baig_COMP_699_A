import unittest
from run_step3_cutoff import metrics

class CutoffTests(unittest.TestCase):
    def test_perfect(self):
        self.assertEqual(metrics([2,1,0],2),(1,1,1))
    def test_recall(self):
        self.assertEqual(metrics([1,0,1],1)[1],0.5)
    def test_empty_relevance(self):
        self.assertEqual(metrics([0,0],1),(0,0,0))
    def test_order(self):
        self.assertLess(metrics([1,2],1)[2],metrics([2,1],1)[2])
    def test_invalid(self):
        with self.assertRaises(ValueError): metrics([1],2)
