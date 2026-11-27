import unittest
import section6
class SectionTests(unittest.TestCase):
 def test_backlinks(self):
  self.assertEqual(section6.backlinks([{'source': 'https://a.test/x', 'target': 'b'}, {'source': 'https://a.test/y', 'target': 'b'}]), {'unique_hosts': 1, 'target_hosts': {'b': 1}})
 def test_listings(self):
  self.assertEqual(section6.listings({'canonical': {'name': 'A'}, 'listings': [{'source': 'x', 'name': 'B'}]}), [{'source': 'x', 'differences': ['name']}])
 def test_prospects(self):
  self.assertEqual(section6.prospects([{'url': 'a', 'editorial_relevance': True, 'paid_link': True, 'spam': False}]), [])
