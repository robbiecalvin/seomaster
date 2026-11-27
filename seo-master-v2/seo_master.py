import argparse, json
from pathlib import Path
from datetime import datetime
ROOT = Path(__file__).resolve().parent
MODES = {'discovery','audit','architect','implement','monitor'}
def plan(project, registry):
    if not isinstance(project.get('name'), str) or not project['name'].strip() or project.get('mode') not in MODES:
        raise ValueError('Invalid project name or mode')
    for key in ('markets','languages','objectives'):
        if not isinstance(project.get(key), list) or not all(isinstance(x,str) for x in project[key]):
            raise ValueError('Invalid '+key)
    if not isinstance(project.get('website_type'),str): raise ValueError('Missing website type')
    skills = {s['id']:s for s in registry['skills']}
    if len(skills)!=len(registry['skills']): raise ValueError('Duplicate skill ID')
    visiting, done, ordered = set(), set(), []
    def visit(k):
        if k in visiting: raise ValueError('Dependency cycle: '+k)
        if k in done: return
        if k not in skills: raise ValueError('Unknown dependency: '+k)
        visiting.add(k)
        for d in skills[k]['dependencies']: visit(d)
        visiting.remove(k); done.add(k); ordered.append(k)
    for k in skills: visit(k)
    done.clear(); ordered.clear()
    for k,s in skills.items():
        if project['mode'] in s['modes'] and (not s.get('website_types') or project['website_type'].lower() in s['website_types']): visit(k)
    return {'project':project['name'],'mode':project['mode'],'execution_authorized':False,'steps':[{'id':k,'status':skills[k]['status'],'action':'offline analysis available' if skills[k]['status']=='offline' else 'manual reference review' if skills[k]['status']=='reference' else 'blocked: skill not implemented'} for k in ordered]}
def validate_evidence(e):
    for k in ('id','source','scope','collected_at'):
        if not isinstance(e.get(k),str) or not e[k].strip(): raise ValueError('Missing '+k)
    dt=datetime.fromisoformat(e['collected_at'].replace('Z','+00:00'))
    if dt.tzinfo is None: raise ValueError('Timezone required')
    if e.get('classification') not in {'measured','estimate','observation','assumption','unavailable'}: raise ValueError('Invalid classification')
    c=e.get('confidence')
    if isinstance(c,bool) or not isinstance(c,(int,float)) or not 0<=c<=1: raise ValueError('Invalid confidence')
    if 'value' not in e or (e['classification']=='unavailable' and e['value'] is not None): raise ValueError('Invalid value')
    return True
if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('command',choices=['plan','validate-evidence']); parser.add_argument('file',type=Path); a=parser.parse_args()
    try:
        data=json.loads(a.file.read_text()); result=plan(data,json.loads((ROOT/'registry.json').read_text())) if a.command=='plan' else validate_evidence(data); print(json.dumps(result,indent=2))
    except (ValueError,KeyError,TypeError,OSError) as e: parser.exit(1,str(e)+'\n')
