import unittest,tempfile,zipfile,io,json
from pathlib import Path
from workspace import Workspace
from delivery import save_page,save_opportunity,build,package
class DeliveryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.w=Workspace(Path(self.tmp.name)/'db');self.key=self.w.create(json.loads(Path('examples/project.json').read_text()))
 def page(self,p='/',parent=None):return save_page(self.w,self.key,dict(path=p,parent=parent,title='Test',brief='Useful page',source='Planning assumption'))
 def test_tree(self):
  self.page();self.page('/child','/');self.assertEqual(len(build(self.w.export(self.key))['pages']),2)
  with self.assertRaises(ValueError):self.page('/','/child')
 def test_update(self):
  self.page();self.page();self.assertEqual(len(build(self.w.export(self.key))['pages']),1)
 def test_invalid(self):
  with self.assertRaises(ValueError):self.page('//evil')
 def test_score(self):
  self.page();save_opportunity(self.w,self.key,dict(path='/',description='Improve',source='Assumption',demand=10,difficulty=0,relevance=10,commercial=10,weakness=10,effort=0));self.assertEqual(build(self.w.export(self.key))['opportunities'][0]['score'],100)
 def test_package(self):
  self.page();z=zipfile.ZipFile(io.BytesIO(package(self.w.export(self.key))));self.assertEqual(len(z.namelist()),18);self.assertIsNone(z.testzip());self.assertEqual(json.loads(z.read('SEO_ARCHITECTURE.json'))['pages'][0]['path'],'/');self.assertEqual(len(z.read('KEYWORD_GAPS.csv').splitlines()),1)
