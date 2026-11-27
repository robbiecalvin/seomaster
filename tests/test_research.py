import unittest,research as r
class Research(unittest.TestCase):
 def test_score(self):
  d=dict(demand=10,difficulty=0,relevance=10,commercial=10,weakness=10,effort=0);self.assertEqual(r.score(d),100);d['effort']=11;self.assertRaises(ValueError,r.score,d)
 def test_keywords(self):
  a=dict(keyword='  SEO  ',market='CA',language='en');self.assertEqual(r.keywords([a])[0]['keyword'],'seo');self.assertRaises(ValueError,r.keywords,[a,a])
 def test_intent(self):self.assertEqual(r.intent('how to build')['intent'],'informational')
 def test_changes(self):self.assertRaises(ValueError,r.changes,dict(before_scope='CA',after_scope='US'))
 def test_gaps(self):
  a=dict(keyword='seo',market='CA',language='en');self.assertEqual(r.gaps(dict(own=[a],competitor=[a])),[])
 def test_serp(self):self.assertEqual(r.serp([dict(domain='a',type='guide')])['sample_size'],1)
 def test_market(self):self.assertEqual(r.markets([dict(keyword='seo',market='CA',language='en',volume=3)]),{'CA':3})
 def test_competitors(self):self.assertEqual(r.competitors(dict(own_keywords=['a'],competitors=[dict(keywords=['a','b'])]))[0]['shared_keywords'],1)
