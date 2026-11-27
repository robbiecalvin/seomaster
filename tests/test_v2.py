import json,tempfile,threading,unittest,urllib.request,re
from pathlib import Path
from dashboard import server
from workspace import Workspace
class V2Tests(unittest.TestCase):
    def test_wizard_http_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            w=Workspace(Path(d)/'db');s=server(w,0);t=threading.Thread(target=s.serve_forever);t.start();base=f'http://127.0.0.1:{s.server_port}'
            try:
                html=urllib.request.urlopen(base).read().decode();token=re.search('name="workspace-token" content="([^"]+)"',html)[1]
                p={'name':'Wizard project','website_type':'saas','mode':'discovery','domain':'https://example.com','markets':['CA'],'languages':['en'],'objectives':['Leads'],'description':'Software','audience':'Businesses','known_competitors':['example.org']}
                req=urllib.request.Request(base+'/api/projects',json.dumps(p).encode(),{'Content-Type':'application/json','X-Workspace-Token':token});key=json.load(urllib.request.urlopen(req))['id'];out=json.load(urllib.request.urlopen(base+'/api/export/'+key));self.assertEqual(out['project'],p);self.assertTrue(out['plan']['steps']);self.assertFalse(out['plan']['execution_authorized'])
            finally:s.shutdown();t.join();s.server_close()
