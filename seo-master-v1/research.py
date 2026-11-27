from collections import Counter, defaultdict
import math

def keywords(rows):
    out=[]; seen=set()
    for row in rows:
        k=' '.join(row['keyword'].casefold().split()); key=(k,row['market'],row['language'])
        if not k or key in seen: raise ValueError('Empty or duplicate keyword: '+k)
        seen.add(key); out.append(dict(row,keyword=k))
    return out

def intent(query):
    q=query.casefold().split()
    for words,label in [({'buy','hire','book','order'},'transactional'),({'best','vs','review','compare','pricing'},'commercial'),({'how','what','why','guide'},'informational'),({'login','signin'},'navigational')]:
        if set(q)&words:return {'intent':label,'method':'heuristic','review_required':True}
    return {'intent':'unknown','review_required':True}

def competitors(data):
    own=set(data['own_keywords']); return [dict(r,shared_keywords=len(own & set(r['keywords']))) for r in data['competitors']]

def serp(rows):
    return {'types':dict(Counter(r['type'] for r in rows)), 'domains':dict(Counter(r['domain'] for r in rows)), 'sample_size':len(rows)}

def markets(rows):
    out=defaultdict(float)
    for r in keywords(rows):
        if r.get('volume') is not None: out[r['market']]+=r['volume']
    return dict(out)

def changes(data):
    if data['before_scope']!=data['after_scope']:raise ValueError('Incomparable snapshots')
    def index(rows):
        result={r['id']:r['value'] for r in rows}
        if len(result)!=len(rows):raise ValueError('Duplicate IDs')
        return result
    a,b=index(data['before']),index(data['after'])
    return [{'id':k,'before':a.get(k),'after':b.get(k),'delta':b[k]-a[k] if k in a and k in b and a[k] is not None and b[k] is not None else None} for k in sorted(a.keys()|b.keys())]

def gaps(data):
    own={(r['keyword'],r['market'],r['language']) for r in keywords(data['own'])}
    return [r for r in keywords(data['competitor']) if (r['keyword'],r['market'],r['language']) not in own]

def score(d):
    weights={'demand':.2,'difficulty':.2,'relevance':.25,'commercial':.15,'weakness':.1,'effort':.1}
    for k in weights:
        v=d[k]
        if isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v) or not 0<=v<=10:raise ValueError('Invalid factor '+k)
    return round(10*sum(w*(10-d[k] if k in ('difficulty','effort') else d[k]) for k,w in weights.items()),2)
