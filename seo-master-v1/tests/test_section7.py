import unittest,json
from section7 import *
from seo_master import plan,ROOT
class Specialized(unittest.TestCase):
 def test_catalog(self): self.assertEqual(catalog_checks([{'url':'/a','item_count':0}])[0]['issues'],['missing title','empty listing'])
 def test_media(self): self.assertEqual(media_checks([{'url':'/a','type':'image','decorative':True}])[0]['issues'],[])
 def test_routing(self):
  p=json.loads((ROOT/'examples/project.json').read_text());r=json.loads((ROOT/'registry.json').read_text()); ids=[x['id'] for x in plan(p,r)['steps']];self.assertIn('saas-seo',ids);self.assertNotIn('ecommerce-seo',ids)
