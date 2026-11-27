import unittest,tempfile,json,threading,urllib.request
from pathlib import Path
from workspace import Workspace
from dashboard import server
class WorkspaceTests(unittest.TestCase):
    def test_persistence(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'db';w=Workspace(p);key=w.create(json.loads(Path('examples/project.json').read_text()));self.assertEqual(Workspace(p).export(key)['project']['name'],'Example project')
            with self.assertRaises(ValueError):w.run(key,'intent',{'evidence':[],'data':{}})
    def test_http(self):
        with tempfile.TemporaryDirectory() as d:
            s=server(Workspace(Path(d)/'db'),0);t=threading.Thread(target=s.serve_forever);t.start()
            try:
                with urllib.request.urlopen(f'http://127.0.0.1:{s.server_port}/') as r:self.assertIn(b'SEO MASTER',r.read())
            finally:s.shutdown();t.join();s.server_close()
