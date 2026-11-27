import unittest,tempfile,json
from pathlib import Path
from workspace import Workspace
from validation import validate
from install_skills import install
from offline import METHODS
class ReleaseTests(unittest.TestCase):
    def test_schema(self):
        p=json.loads(Path('examples/project.json').read_text());self.assertTrue(validate('project',p));p['unexpected']=1
        with self.assertRaises(ValueError):validate('project',p)
    def test_registry(self):
        r=json.loads(Path('registry.json').read_text())
        for s in r['skills']:
            self.assertTrue((Path('skills')/s['id']/'SKILL.md').is_file(),s['id'])
            if s.get('entrypoint'):self.assertIn(s['entrypoint'],METHODS)
    def test_install(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertGreater(install(d),0)
            with self.assertRaises(FileExistsError):install(d)
    def test_run_export(self):
        with tempfile.TemporaryDirectory() as d:
            w=Workspace(Path(d)/'db');k=w.create(json.loads(Path('examples/project.json').read_text()));e={'id':'fixture','source':'synthetic test','scope':'test','collected_at':'2026-01-01T00:00:00Z','classification':'assumption','confidence':1,'value':None};r=w.run(k,'release_checks',{'evidence':[e],'data':{'checks':[]}});self.assertFalse(r['result']['deployment_authorized']);self.assertEqual(Workspace(Path(d)/'db').export(k)['runs'],[r])
