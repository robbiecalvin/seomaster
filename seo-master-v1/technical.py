from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit
import json,xml.etree.ElementTree as ET
class Parser(HTMLParser):
    def __init__(self,html):
        super().__init__();self.tags=[];self.title=[];self.jsonld=[];self.active=None;self.feed(html);self.close()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append((tag,a))
        if tag=='title':self.active='title';self.title.append('')
        if tag=='script' and a.get('type','').lower()=='application/ld+json':self.active='jsonld';self.jsonld.append('')
    def handle_endtag(self,tag):
        if tag in ('title','script'):self.active=None
    def handle_data(self,data):
        if self.active:getattr(self,self.active)[-1]+=data
    def attrs(self,tag):return [a for t,a in self.tags if t==tag]
    def meta(self,name):return [a.get('content','') for a in self.attrs('meta') if a.get('name','').lower()==name]
def parse(d):return Parser(d['html'])
def audit(d):
    p=parse(d);return {'titles':p.title,'descriptions':p.meta('description'),'h1_count':len(p.attrs('h1')),'indexability':indexability(d),'canonical':canonical(d),'mobile':mobile(d)}
def indexability(d):
    p=parse(d); directives=p.meta('robots')+p.meta('googlebot')+[d.get('x_robots_tag','')]; tokens={x.strip().lower() for v in directives for x in v.split(',')};return {'status':d.get('status'),'noindex':bool(tokens & {'noindex','none'}),'directives':directives,'indexing_confirmed':False}
def canonical(d):
    p=parse(d);targets=[urljoin(d['url'],a['href']) for a in p.attrs('link') if 'canonical' in a.get('rel','').lower().split() and a.get('href')];return {'targets':targets,'count':len(targets),'self_referencing':targets==[d['url']]}
def mobile(d):return {'viewport':parse(d).meta('viewport')}
def schema(d):
    out=[]
    for raw in parse(d).jsonld:
        try:out.append({'valid_json':True,'value':json.loads(raw)})
        except ValueError as e:out.append({'valid_json':False,'error':str(e)})
    return out
def graph(rows):
    urls={r['url'] for r in rows};incoming={u:set() for u in urls};external=[]
    for r in rows:
        for a in parse(r).attrs('a'):
            if not a.get('href'):continue
            u=urljoin(r['url'],a['href']).split('#')[0]
            if u in urls and u!=r['url']:incoming[u].add(r['url'])
            elif u not in urls:external.append(u)
    return {'pages':[{'url':u,'inbound':len(incoming[u]),'depth':len([x for x in urlsplit(u).path.split('/') if x])} for u in sorted(urls)],'orphan_candidates':sorted(u for u in urls if not incoming[u]),'out_of_inventory':sorted(set(external))}
def performance(d):
    thresholds={'lcp_ms':2500,'inp_ms':200,'cls':.1};return {k:('unknown' if d.get(k) is None else 'good' if 0<=d[k]<=v else 'invalid' if d[k]<0 else 'above_good_threshold') for k,v in thresholds.items()}
def rendering(d):return {'before':audit(dict(d,html=d['before_html'])),'after':audit(dict(d,html=d['after_html']))}
def sitemap(xml):
    root=ET.fromstring(xml);kind=root.tag.split('}')[-1];urls=[e.text.strip() for e in root.iter() if e.tag.split('}')[-1]=='loc' and e.text];return {'kind':kind,'urls':urls,'duplicates':sorted({u for u in urls if urls.count(u)>1}),'invalid_urls':[u for u in urls if urlsplit(u).scheme not in ('http','https') or not urlsplit(u).netloc]}
def redirects(mapping):
    out=[]
    for start in sorted(mapping):
        path=[start];u=start
        while u in mapping:
            u=mapping[u];path.append(u)
            if u in path[:-1]:break
        out.append({'start':start,'path':path,'loop':u in path[:-1],'hops':len(path)-1})
    return out
def hreflang(rows):
    by={r['url']:r['alternates'] for r in rows};return [{'source':u,'language':lang,'target':v,'reciprocal':u in by.get(v,{}).values()} for u,a in by.items() for lang,v in a.items()]
def migration(d):
    new=set(d['new']);mapping=d['mapping'];return {'unmapped':[u for u in d['old'] if u not in mapping and u not in new],'missing_targets':[u for u,v in mapping.items() if v not in new],'redirects':redirects(mapping)}
