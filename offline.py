import argparse,json,research,technical
from pathlib import Path
from seo_master import validate_evidence
METHODS={k:getattr(research,k) for k in ('keywords','intent','competitors','serp','markets','changes','gaps','score')}
METHODS.update({k:getattr(technical,k) for k in ('audit','indexability','graph','schema','performance','rendering','canonical','sitemap','redirects','hreflang','mobile','migration')})
import section4
METHODS.update({k:getattr(section4,k) for k in ('cannibalization', 'coverage', 'metadata', 'refresh')})
import section5
METHODS.update({k:getattr(section5,k) for k in ('claim_sources', 'graph_references', 'visibility')})
import section6
METHODS.update({k:getattr(section6,k) for k in ('backlinks', 'listings', 'prospects')})
import section7
METHODS.update({k:getattr(section7,k) for k in ('catalog_checks', 'media_checks')})
import section8
METHODS.update({k:getattr(section8,k) for k in ('metrics', 'compare_metrics', 'forecast')})
import section9
METHODS.update({k:getattr(section9,k) for k in ('regressions', 'release_checks')})
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('method',choices=METHODS);parser.add_argument('input',type=Path);a=parser.parse_args()
    try:
        d=json.loads(a.input.read_text()); evidence=d['evidence'];
        if not evidence:raise ValueError('Evidence required')
        for e in evidence:validate_evidence(e)
        print(json.dumps({'method':a.method,'evidence_ids':[e['id'] for e in evidence],'result':METHODS[a.method](d['data']),'limitations':'Offline supplied data; not independently verified'},indent=2,allow_nan=False))
    except (ValueError,KeyError,TypeError,OSError) as e:parser.exit(1,str(e)+'\n')
