import sqlite3,json,uuid
from pathlib import Path
from seo_master import plan,validate_evidence,ROOT
from offline import METHODS
from validation import validate
class Workspace:
    def __init__(self,path):
        self.path=path
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, data TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, project TEXT REFERENCES projects(id), data TEXT NOT NULL)')
            db.execute("CREATE TABLE IF NOT EXISTS research_records (id TEXT PRIMARY KEY, project TEXT REFERENCES projects(id), kind TEXT, data TEXT NOT NULL)")
    def records(self,key,kind):
        with self.connect() as db:return [json.loads(r[0]) for r in db.execute("SELECT data FROM research_records WHERE project=? AND kind=? ORDER BY rowid",(key,kind))]
    def save_records(self,key,kind,rows):
        self.export(key)
        with self.connect() as db:db.executemany("INSERT INTO research_records VALUES (?,?,?,?)",[(uuid.uuid4().hex,key,kind,json.dumps(r,allow_nan=False)) for r in rows])
        return self.records(key,kind)
    def connect(self):
        db=sqlite3.connect(self.path);db.execute('PRAGMA foreign_keys=ON');return db
    def create(self,data):
        validate("project",data)
        plan(data,json.loads((ROOT/'registry.json').read_text())); key=uuid.uuid4().hex
        with self.connect() as db: db.execute('INSERT INTO projects VALUES (?,?)',(key,json.dumps(data,allow_nan=False)))
        return key
    def projects(self):
        with self.connect() as db:return [{'id':k,'project':json.loads(v)} for k,v in db.execute('SELECT id,data FROM projects ORDER BY rowid DESC')]
    def export(self,key):
        with self.connect() as db:
            row=db.execute('SELECT data FROM projects WHERE id=?',(key,)).fetchone()
            if not row:raise ValueError('Unknown project')
            project=json.loads(row[0]); runs=[json.loads(r[0]) for r in db.execute('SELECT data FROM runs WHERE project=? ORDER BY rowid',(key,))]
        return {'project':project,'plan':plan(project,json.loads((ROOT/'registry.json').read_text())),'runs':runs,'research':{k:self.records(key,k) for k in ('competitors','crawl','keywords','content_map','ai_observations','backlinks','provider_runs','task_runs','architecture','opportunities')}}
    def run(self,key,method,payload):
        self.export(key); evidence=payload['evidence']
        if not evidence:raise ValueError('Evidence required')
        for e in evidence:validate("evidence",e);validate_evidence(e)
        if len({e['id'] for e in evidence})!=len(evidence):raise ValueError('Duplicate evidence ID')
        result={'method':method,'evidence':evidence,'result':METHODS[method](payload['data']),'limitations':'Supplied data, not independently verified'}
        with self.connect() as db:db.execute('INSERT INTO runs VALUES (?,?,?)',(uuid.uuid4().hex,key,json.dumps(result,allow_nan=False)))
        return result
