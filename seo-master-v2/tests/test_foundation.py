import unittest,json
from seo_master import plan,validate_evidence,ROOT
class Foundation(unittest.TestCase):
 def setUp(self):
  self.p=json.loads((ROOT/'examples/project.json').read_text()); self.r=json.loads((ROOT/'registry.json').read_text())
 def test_order(self):
  x=plan(self.p,self.r); ids=[s['id'] for s in x['steps']]; self.assertLess(ids.index('keyword-intelligence'),ids.index('architecture')); self.assertFalse(x['execution_authorized'])
 def test_cycle(self):
  self.r['skills'][0]['dependencies']=['keyword-intelligence']; self.assertRaises(ValueError,plan,self.p,self.r)
 def test_missing(self):
  self.r['skills'][0]['dependencies']=['missing']; self.assertRaises(ValueError,plan,self.p,self.r)
 def test_mode(self):
  self.p['mode']='bad'; self.assertRaises(ValueError,plan,self.p,self.r)
 def test_evidence(self):
  e=dict(id='e1',source='example',scope='CA',collected_at='2026-01-01T00:00:00Z',classification='unavailable',confidence=0,value=None); self.assertTrue(validate_evidence(e)); e['value']=12; self.assertRaises(ValueError,validate_evidence,e)
