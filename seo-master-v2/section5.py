def visibility(d):
 groups={}
 for x in d:
  if type(x['mentioned']) is not bool or type(x['cited']) is not bool: raise ValueError('Boolean observations required')
  g=groups.setdefault(x['engine'],[0,0,0]); g[0]+=1; g[1]+=x['mentioned']; g[2]+=x['cited']
 return {k:{'samples':v[0],'mention_rate':v[1]/v[0],'citation_rate':v[2]/v[0]} for k,v in groups.items()}
def claim_sources(d):
 return [x['id'] for x in d if not x.get('source_ids')]
def graph_references(d):
 ids=set(d['entities']); return [x for x in d['triples'] if x['subject'] not in ids or x['object'] not in ids]
