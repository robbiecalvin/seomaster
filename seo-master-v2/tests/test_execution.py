import unittest,tempfile, json
from pathlib import Path
from workspace import Workspace
from execution import execute,collect,provider_status
class ExecutionTests(unittest.TestCase):
 def setUp(self):
    self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.w=Workspace(Path(self.tmp.name)/'db'); self.key=self.w.create(json.loads(Path('examples/project.json').read_text()))
 def test_blocked(self):
    self.assertEqual(execute(self.w,self.key,['technical'])[0]['status'],'blocked')
 def test_completed(self):
    self.w.save_records(self.key,'crawl',[{'url':'https://example.com','status':200,'title':''}]); self.assertEqual(execute(self.w,self.key,['technical'])[0]['status'],'completed'); self.assertEqual(len(self.w.export(self.key)['research']['task_runs']),1)
 def test_authorization(self):
    with self.assertRaises(ValueError):collect(self.w,self.key,{'provider':'pagespeed'})
 def test_provider(self):
    class Fake:
      def fetch(self,p,params):return {'provider':p,'response':{'ok':True},'collected_at':'2026-01-01T00:00:00Z'}
    collect(self.w,self.key,{'provider':'pagespeed','target':'https://example.com','authorized':True},Fake());self.assertEqual(len(self.w.export(self.key)['research']['provider_runs']),1)
 def test_status(self):self.assertTrue(all('verified' in r and not r['verified'] for r in provider_status()))
