"""Explicit, bounded read-only provider requests. No automatic network access."""
import os,json,time,urllib.request,urllib.parse,urllib.error
from datetime import datetime,timezone
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
class ProviderClient:
    def __init__(self, authorized=False, transport=None):
        self.authorized=authorized; self.transport=transport or self._send; self.last=0
    def _send(self,request):
        with urllib.request.build_opener(NoRedirect()).open(request,timeout=20) as response:
            raw=response.read(5_000_001)
            if len(raw)>5_000_000: raise ValueError('Response exceeds limit')
            return json.loads(raw)
    def fetch(self,provider,params):
        if not self.authorized: raise PermissionError('Explicit network authorization required')
        headers={'Accept':'application/json'}; body=None
        if provider=='pagespeed':
            target=urllib.parse.urlsplit(params['url'])
            if target.scheme not in ('http','https') or not target.hostname or target.username: raise ValueError('Invalid target URL')
            url='https://www.googleapis.com/pagespeedonline/v5/runPagespeed?'+urllib.parse.urlencode({'url':params['url'],'strategy':params.get('strategy','mobile'),'key':os.environ['PAGESPEED_API_KEY']})
        elif provider=='search-console':
            url='https://www.googleapis.com/webmasters/v3/sites/'+urllib.parse.quote(params['site'],safe='')+'/searchAnalytics/query'
            headers['Authorization']='Bearer '+os.environ['GOOGLE_ACCESS_TOKEN']; body={k:params[k] for k in ('startDate','endDate','dimensions')}; body['rowLimit']=min(25000,int(params.get('rowLimit',1000)))
        elif provider=='analytics':
            prop=str(params['property']);
            if not prop.isdigit(): raise ValueError('Numeric property required')
            url=f'https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport'; headers['Authorization']='Bearer '+os.environ['GOOGLE_ACCESS_TOKEN']; body={k:params[k] for k in ('dateRanges','metrics','dimensions')}; body['limit']=min(10000,int(params.get('limit',1000)))
        else: raise ValueError('Unsupported live provider; import exported evidence instead')
        if body is not None: headers['Content-Type']='application/json'
        request=urllib.request.Request(url,data=json.dumps(body).encode() if body is not None else None,headers=headers)
        time.sleep(max(0,1-(time.monotonic()-self.last))); self.last=time.monotonic()
        try: result=self.transport(request)
        except urllib.error.HTTPError as e: raise RuntimeError(f'Provider HTTP {e.code}; no automatic retry') from None
        except (urllib.error.URLError,OSError): raise RuntimeError('Provider connection failed') from None
        return {'provider':provider,'collected_at':datetime.now(timezone.utc).isoformat(),'response':result,'classification':'observation','limitations':'Raw provider response; check sampling, pagination and metric definitions'}
