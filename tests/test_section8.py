import unittest
from section8 import *
class Analytics(unittest.TestCase):
 def test_zero(self): self.assertIsNone(metrics([])['ctr'])
 def test_metrics(self): self.assertEqual(metrics([dict(clicks=2,impressions=10,sessions=4,conversions=1)])['conversion_rate'],.25)
 def test_compare(self): self.assertIsNone(compare_metrics(dict(baseline=[],current=[]))['clicks']['relative_change'])
 def test_forecast(self): self.assertEqual(forecast([dict(name='a',sessions=100,conversion_rate=.1,value_per_conversion=5)])[0]['value'],50)
 def test_invalid(self): self.assertRaises(ValueError,number,float('nan'))
