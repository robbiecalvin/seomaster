"""Explicit provider requests and evidence-bound local task execution."""
import os, uuid
from datetime import datetime, timezone, date
from integrations import ProviderClient
import strategy, live_research

def stamp(): return datetime.now(timezone.utc).isoformat()
PROVIDERS={'brave':'BRAVE_SEARCH_API_KEY','pagespeed':'PAGESPEED_API_KEY','search-console':'GOOGLE_ACCESS_TOKEN','analytics':'GOOGLE_ACCESS_TOKEN'}
def provider_status():
    return [{'provider':p,'credential_variable':k,'configured':bool(os.environ.get(k)),'verified':False} for p,k in PROVIDERS.items()]
def collect(workspace,key,d,client=None):
    project=workspace.export(key)['project']; p=d['provider']
    if p not in PROVIDERS: raise ValueError('Unknown provider')
    if d.get('authorized') is not True: raise ValueError('Explicit network authorization required')
    if not os.environ.get(PROVIDERS[p]) and client is None: raise ValueError('Configure '+PROVIDERS[p]+' before starting the server')
    if p=='brave':
        rows=live_research.discover(d['target'],project.get('domain','')); workspace.save_records(key,'competitors',rows); result={'response':rows,'provider':p,'collected_at':stamp()}
    else:
        if p=='pagespeed': params={'url':d['target'],'strategy':d.get('strategy','mobile')}; live_research.target(params['url'])
        else:
            start=date.fromisoformat(d['start']); end=date.fromisoformat(d['end'])
            if start>end: raise ValueError('Start date must precede end date')
            if p=='search-console': params={'site':d['target'],'startDate':str(start),'endDate':str(end),'dimensions':['query'],'rowLimit':100}
            else: params={'property':d['target'],'dateRanges':[{'startDate':str(start),'endDate':str(end)}],'metrics':[{'name':'sessions'},{'name':'engagedSessions'}],'dimensions':[{'name':'sessionDefaultChannelGroup'}],'limit':100}
        result=(client or ProviderClient(authorized=True)).fetch(p,params)
    result['target']=d['target']; result['limitations']='Provider response; limited sample, not independently verified.'
    workspace.save_records(key,'provider_runs',[result]); return result
TASKS={'technical':('crawl',),'content':('keywords',),'visibility':('ai_observations',),'authority':('backlinks',)}
def execute(workspace,key,selected):
    if not isinstance(selected,list) or not selected or any(x not in TASKS for x in selected): raise ValueError('Select supported tasks')
    r=workspace.export(key)['research']; batch=uuid.uuid4().hex; out=[]
    funcs={'technical':lambda:strategy.technical(r['crawl']),'content':lambda:strategy.content(r['keywords'],r['content_map']),'visibility':lambda:strategy.visibility(r['ai_observations']),'authority':lambda:strategy.backlinks(r['backlinks'])}
    for task in dict.fromkeys(selected):
        row={'batch':batch,'task':task,'started_at':stamp(),'inputs':{k:len(r[k]) for k in TASKS[task]}}
        try:
            if not all(r[k] for k in TASKS[task]): row.update(status='blocked',reason='Missing saved evidence')
            else: row.update(status='completed',result=funcs[task]())
        except (ValueError,KeyError,TypeError,ArithmeticError): row.update(status='failed',reason='Invalid saved evidence')
        row['finished_at']=stamp(); out.append(row)
    workspace.save_records(key,'task_runs',out); return out
