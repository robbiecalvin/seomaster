def coverage(d):
 return sorted(set(d['required'])-set(d['covered']))
def metadata(d):
 from collections import Counter
 counts=Counter(x['title'].strip().casefold() for x in d if x.get('title','').strip())
 return [{'url':x['url'],'missing':[k for k in ('title','description') if not x.get(k,'').strip()],'duplicate_title':counts[x.get('title','').strip().casefold()]>1} for x in d]
def cannibalization(d):
 groups={}
 for x in d: groups.setdefault((x['keyword'].casefold().strip(),x['market'],x['language']),set()).add(x['url'])
 return [{'keyword':k[0],'market':k[1],'language':k[2],'urls':sorted(v)} for k,v in sorted(groups.items()) if len(v)>1]
def refresh(d):
 return [{'url':x['url'],'change':(x['current']-x['previous'])/x['previous'] if x['previous']>0 else None} for x in d]
