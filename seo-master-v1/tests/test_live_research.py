import unittest,tempfile
from live_research import crawl,discover,keyword_rows,target
from workspace import Workspace
class ResearchTests(unittest.TestCase):
 def test_discovery(self):
  self.assertEqual(len(discover('test','https://own.test',lambda q:{'web':{'results':[{'url':'https://own.test'},{'url':'https://other.test/a'},{'url':'https://other.test/b'}]}})),1)
 def test_crawl(self):
  def fake(u):
   if u.endswith('robots.txt'):return 200,{},'User-agent: *\nDisallow: /private'
   return 200,{'content-type':'text/html'},'<title>Test</title><a href="/private">x</a><a href="/next">y</a>'
  r=crawl('https://example.com',3,fake);self.assertEqual(r[0]['title'],'Test');self.assertEqual(r[1]['status'],'robots blocked');self.assertEqual(len(r),3)
 def test_target(self):
  for u in ['http://example.com','https://user@example.com','https://example.com:99']:
   with self.assertRaises(ValueError):target(u)
 def test_keywords(self):
  r=keyword_rows('keyword,volume,difficulty\nBest shoes,100,20\nother,,','CA','en','fixture');self.assertEqual(r[0]['intent'],'commercial');self.assertIsNone(r[1]['volume'])
 def test_invalid_metric(self):
  with self.assertRaises(ValueError):keyword_rows('keyword,volume\nx,-1','CA','en','fixture')
