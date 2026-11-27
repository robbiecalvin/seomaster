"""Evidence-bound workspace analyses; no network calls."""
import csv,io
from collections import Counter
from urllib.parse import urlsplit,urljoin
from datetime import datetime,timezone
from section5 import visibility
from section6 import backlinks

def technical(rows):
    latest={r['url']:r for r in rows}; counts=Counter(r.get('title','').strip().casefold() for r in latest.values() if r.get('title','').strip()); out=[]
    for u,r in latest.items():
        def issue(severity,problem,fix):out.append(dict(url=u,severity=severity,issue=problem,recommendation=fix,collected_at=r.get('collected_at')))
        if r['status']!=200:
            issue('Review','HTTP / crawl status: '+str(r['status']),'Check intended accessibility and response; do not override robots policy.');continue
        if 'title' not in r:continue
        if not r['title'].strip():issue('High','Missing title','Add a unique descriptive title.')
        elif counts[r['title'].strip().casefold()]>1:issue('Medium','Duplicate title','Review intent and differentiate titles where appropriate.')
        if not r.get('description','').strip():issue('Medium','Missing description','Write a useful page summary.')
        if r.get('h1_count')!=1:issue('Review','Heading count differs from one','Review heading structure and accessibility.')
        if r.get('noindex'):issue('Review','Noindex present','Confirm whether exclusion is intentional.')
        if r.get('canonical') and urljoin(u,r['canonical'])!=u:issue('Review','Non-self canonical','Verify intended canonical destination.')
    return out

def content(keywords,mappings):
    mapped={(r['keyword'].casefold().strip(),r['market'],r['language']) for r in mappings}
    return [dict(keyword=r['keyword'],market=r['market'],language=r['language'],intent=r['intent'],volume=r.get('volume'),status='Mapped' if (r['keyword'],r['market'],r['language']) in mapped else 'Unmapped — review opportunity') for r in { (x['keyword'],x['market'],x['language']):x for x in keywords}.values()]

def records(kind,d):
    def required(k):
        v=d.get(k,'').strip()
        if not v:raise ValueError(k+' is required')
        return v
    def url(k):
        v=required(k);p=urlsplit(v)
        if p.scheme not in ('http','https') or not p.hostname or p.username or p.password:raise ValueError('Enter absolute public-style URL')
        return v
    source=required('source'); row={'source':source,'collected_at':datetime.now(timezone.utc).isoformat()}
    if kind=='content_map':row.update(keyword=required('keyword').casefold(),market=required('market'),language=required('language'),topic=required('topic'),url=url('url'),brief=required('brief'))
    elif kind=='ai_observations':
        if d.get('mentioned') not in ('yes','no') or d.get('cited') not in ('yes','no'):raise ValueError('Select observation outcomes')
        row.update(engine=required('engine'),query=required('query'),mentioned=d['mentioned']=='yes',cited=d['cited']=='yes',observation_date=required('observation_date'))
        if row['cited']:row['citation_url']=url('citation_url')
    elif kind=='backlinks':row.update(source=url('link_url'),target=url('target'),evidence_source=source,anchor=d.get('anchor','').strip())
    else:raise ValueError('Unknown record type')
    return [row]
