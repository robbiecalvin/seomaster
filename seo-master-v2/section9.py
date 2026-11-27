def regressions(data):
    def index(rows):
        result={x['url']:x for x in rows}
        if len(result)!=len(rows): raise ValueError('Duplicate URL')
        return result
    a,b=index(data['baseline']),index(data['candidate']);out=[]
    for url,old in sorted(a.items()):
        new=b.get(url);issues=[]
        if new is None: issues.append('missing URL')
        else:
            if old.get('title') and not new.get('title'): issues.append('lost title')
            if not old.get('noindex') and new.get('noindex'): issues.append('new noindex')
            if old.get('canonical')!=new.get('canonical'): issues.append('canonical changed')
        if issues:out.append({'url':url,'issues':issues})
    return out

REQUIRED={'technical','content','evidence','regression','approval'}
def release_checks(data):
    checks=data['checks']; by_id={x['id']:x for x in checks}
    if len(by_id)!=len(checks):raise ValueError('Duplicate check')
    blocked=sorted(k for k in REQUIRED if k not in by_id or by_id[k].get('status')!='pass' or not by_id[k].get('evidence_ids'))
    blocked+=sorted(k for k,x in by_id.items() if k not in REQUIRED and x.get('status')!='pass')
    return {'checklist_passed':not blocked,'blocked':blocked,'deployment_authorized':False}
