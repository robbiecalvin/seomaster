import unittest
import section4
class SectionTests(unittest.TestCase):
 def test_coverage(self):
  self.assertEqual(section4.coverage({'required': ['a', 'b'], 'covered': ['a']}), ['b'])
 def test_metadata(self):
  self.assertEqual(section4.metadata([{'url': 'a', 'title': 'X'}, {'url': 'b', 'title': 'x'}]), [{'url': 'a', 'missing': ['description'], 'duplicate_title': True}, {'url': 'b', 'missing': ['description'], 'duplicate_title': True}])
 def test_cannibalization(self):
  self.assertEqual(section4.cannibalization([{'keyword': 'x', 'market': 'CA', 'language': 'en', 'url': 'a'}, {'keyword': 'x', 'market': 'CA', 'language': 'en', 'url': 'b'}]), [{'keyword': 'x', 'market': 'CA', 'language': 'en', 'urls': ['a', 'b']}])
 def test_refresh(self):
  self.assertEqual(section4.refresh([{'url': 'a', 'current': 1, 'previous': 0}]), [{'url': 'a', 'change': None}])
