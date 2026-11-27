import unittest
from section9 import *
class Governance(unittest.TestCase):
 def test_regression(self): self.assertEqual(regressions({'baseline':[{'url':'/a','title':'A'}],'candidate':[{'url':'/a','noindex':True}]})[0]['issues'],['lost title','new noindex'])
 def test_missing(self): self.assertFalse(release_checks({'checks':[]})['checklist_passed'])
 def test_pass(self):
  r=release_checks({'checks':[dict(id=k,status='pass',evidence_ids=['e1']) for k in REQUIRED]});self.assertTrue(r['checklist_passed']);self.assertFalse(r['deployment_authorized'])
 def test_duplicate(self): self.assertRaises(ValueError,release_checks,{'checks':[{'id':'a'},{'id':'a'}]})
