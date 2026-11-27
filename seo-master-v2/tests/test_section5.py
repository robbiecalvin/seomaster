import unittest
import section5
class SectionTests(unittest.TestCase):
 def test_visibility(self):
  self.assertEqual(section5.visibility([{'engine': 'test', 'mentioned': True, 'cited': False}]), {'test': {'samples': 1, 'mention_rate': 1.0, 'citation_rate': 0.0}})
 def test_claim_sources(self):
  self.assertEqual(section5.claim_sources([{'id': 'a', 'source_ids': []}]), ['a'])
 def test_graph_references(self):
  self.assertEqual(section5.graph_references({'entities': ['a'], 'triples': [{'subject': 'a', 'object': 'b'}]}), [{'subject': 'a', 'object': 'b'}])
