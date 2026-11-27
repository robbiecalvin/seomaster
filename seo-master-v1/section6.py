def backlinks(d):
 from urllib.parse import urlsplit
 domains=set(); targets={}
 for x in d:
  host=urlsplit(x['source']).hostname
  if not host: raise ValueError('Absolute source URL required')
  domains.add(host.lower()); targets.setdefault(x['target'],set()).add(host.lower())
 return {'unique_hosts':len(domains),'target_hosts':{k:len(v) for k,v in targets.items()}}
def listings(d):
 return [{'source':x['source'],'differences':[k for k,v in d['canonical'].items() if x.get(k)!=v]} for x in d['listings']]
def prospects(d):
 return [x['url'] for x in d if x.get('editorial_relevance') is True and x.get('paid_link') is False and x.get('spam') is False]
