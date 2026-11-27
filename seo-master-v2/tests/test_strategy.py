import unittest
import strategy
class StrategyTests(unittest.TestCase):
 def test_latest(self):
  self.assertEqual(strategy.technical([{'url':'https://x.test','status':404},{'url':'https://x.test','status':200,'title':'Good','description':'Good','h1_count':1}]),[])
 def test_missing(self):
  self.assertEqual(len(strategy.technical([{'url':'https://x.test','status':200,'title':'','description':'','h1_count':1}])),2)
 def test_content(self):
  k=dict(keyword='test',market='CA',language='en',intent='unknown');self.assertEqual(strategy.content([k],[k])[0]['status'],'Mapped')
 def test_ai(self):
  with self.assertRaises(ValueError):strategy.records('ai_observations',{'source':'test','mentioned':'yes','cited':'yes','engine':'test','query':'test','observation_date':'2026-01-01','citation_url':''})
 def test_backlink(self):
  r=strategy.records('backlinks',{'source':'manual','link_url':'https://a.test','target':'https://b.test'});self.assertEqual(strategy.backlinks(r)['unique_hosts'],1)
