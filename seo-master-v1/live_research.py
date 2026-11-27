"""Bounded, opt-in public HTTPS research. No credentials sent to crawled sites."""
import csv, io, os, json, ipaddress, socket, ssl, http.client, time, re
from urllib.parse import urlsplit, urljoin, urlencode
from urllib.robotparser import RobotFileParser
from datetime import datetime, timezone
from technical import audit, Parser
from research import intent

def stamp(): return datetime.now(timezone.utc).isoformat()
def target(url):
    p=urlsplit(url)
    if p.scheme!='https' or not p.hostname or p.username or p.password or p.port not in (None,443): raise ValueError('Public HTTPS URLs only')
    return p

def fetch(url):
    p=target(url); addresses=socket.getaddrinfo(p.hostname,443,type=socket.SOCK_STREAM)
    ips=[a[4][0] for a in addresses]
    if not ips or any(not ipaddress.ip_address(i).is_global for i in ips): raise ValueError('Non-public destination blocked')
    # Pin the validated address while retaining TLS hostname verification.
    c=http.client.HTTPSConnection(p.hostname,timeout=8,context=ssl.create_default_context())
    c._create_connection=lambda address,timeout,source_address: socket.create_connection((ips[0],443),timeout,source_address)
    try:
        c.request('GET',(p.path or '/')+('?' + p.query if p.query else ''),headers={'User-Agent':'SEOMasterResearch/2.0','Accept-Encoding':'identity'})
        r=c.getresponse(); raw=r.read(1_000_001)
        if len(raw)>1_000_000: raise ValueError('Response too large')
        return r.status,dict((k.lower(),v) for k,v in r.getheaders()),raw.decode('utf-8','replace')
    finally:c.close()

def crawl(url,limit=5,transport=fetch):
    p=target(url); limit=int(limit)
    if not 1<=limit<=10: raise ValueError('Choose 1–10 pages')
    origin='https://'+p.netloc; code,_,robots=transport(origin+'/robots.txt'); rp=RobotFileParser();rp.parse(robots.splitlines() if code==200 else [])
    if code not in (200,404,410): raise ValueError('Robots policy unavailable; crawl stopped')
    delay=max(1,rp.crawl_delay('SEOMasterResearch') or rp.crawl_delay('*') or 1)
    if delay>30:raise ValueError('Crawl delay exceeds local interactive limit')
    queue=[url.split('#')[0]]; seen=set(); rows=[]
    while queue and len(seen)<limit:
        u=queue.pop(0)
        if u in seen:continue
        seen.add(u)
        if not rp.can_fetch('SEOMasterResearch',u):rows.append({'url':u,'status':'robots blocked'});continue
        if transport is fetch:time.sleep(delay)
        try: code,h,html=transport(u)
        except (OSError,ValueError,http.client.HTTPException):rows.append({'url':u,'status':'fetch failed'});continue
        row={'url':u,'status':code,'collected_at':stamp()};rows.append(row)
        if code!=200 or 'text/html' not in h.get('content-type',''):continue
        a=audit({'url':u,'html':html,'status':code,'x_robots_tag':h.get('x-robots-tag','')});row.update({'title':' | '.join(a['titles']),'description':' | '.join(a['descriptions']),'h1_count':a['h1_count'],'noindex':a['indexability']['noindex'],'canonical':', '.join(a['canonical']['targets'])})
        for link in Parser(html).attrs('a'):
            v=urljoin(u,link.get('href','')).split('#')[0]; q=urlsplit(v)
            if q.scheme=='https' and q.netloc==p.netloc and not q.query and v not in seen and v not in queue and len(queue)<100:queue.append(v)
    return rows

def discover(query,own='',transport=None):
    if not query.strip() or len(query)>300:raise ValueError('Enter a search query (max 300 characters)')
    if transport is None:
        import urllib.request
        key=os.environ.get('BRAVE_SEARCH_API_KEY')
        if not key:raise ValueError('Set BRAVE_SEARCH_API_KEY before using live discovery')
        def transport(q):
            from integrations import NoRedirect
            req=urllib.request.Request('https://api.search.brave.com/res/v1/web/search?'+urlencode({'q':q,'count':20}),headers={'X-Subscription-Token':key,'Accept':'application/json'})
            with urllib.request.build_opener(NoRedirect()).open(req,timeout=15) as r:
                raw=r.read(2_000_001)
                if len(raw)>2_000_000:raise ValueError('Search response too large')
                return json.loads(raw)
    data=transport(query); rows=[];seen=set(); own=urlsplit(own).hostname or ''
    for r in data.get('web',{}).get('results',[]):
        u=r.get('url',''); host=urlsplit(u).hostname
        if not host or host.removeprefix('www.')==own.removeprefix('www.') or host in seen:continue
        seen.add(host);rows.append({'domain':host,'url':u,'title':r.get('title',''),'query':query,'source':'Brave Search','collected_at':stamp(),'classification':'candidate — review required'})
    return rows

def keyword_rows(text,market,language,source):
    if not all(x.strip() for x in (market,language,source)):raise ValueError('Market, language and source required')
    reader=csv.DictReader(io.StringIO(text)); rows=[];seen=set()
    if not reader.fieldnames or 'keyword' not in reader.fieldnames:raise ValueError('CSV needs a keyword header')
    for r in reader:
        k=' '.join((r['keyword'] or '').casefold().split())
        if not k or k in seen:continue
        seen.add(k); v=r.get('volume',''); d=r.get('difficulty','')
        volume=int(v) if v else None; difficulty=float(d) if d else None
        if (volume is not None and volume<0) or (difficulty is not None and not 0<=difficulty<=100):raise ValueError('Invalid keyword metric')
        rows.append({'keyword':k,'market':market,'language':language,'volume':volume,'difficulty':difficulty,'intent':intent(k)['intent'],'source':source,'collected_at':stamp(),'classification':'supplied; intent heuristic'})
        if len(rows)>5000:raise ValueError('Maximum 5000 keywords per import')
    return rows
