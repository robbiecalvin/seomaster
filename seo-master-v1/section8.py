import math

def number(x):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<0: raise ValueError('Expected nonnegative finite number')
    return x

def metrics(data):
    totals={k:sum(number(x[k]) for x in data) for k in ('clicks','impressions','sessions','conversions')}
    if totals['clicks']>totals['impressions']: raise ValueError('Clicks exceed impressions')
    return dict(totals,ctr=totals['clicks']/totals['impressions'] if totals['impressions'] else None,conversion_rate=totals['conversions']/totals['sessions'] if totals['sessions'] else None)

def compare_metrics(data):
    a,b=metrics(data['baseline']),metrics(data['current'])
    return {k:{'baseline':a[k],'current':b[k],'relative_change':(b[k]-a[k])/a[k] if a[k] not in (0,None) and b[k] is not None else None} for k in a}

def forecast(data):
    out=[]
    for x in data:
        traffic=number(x['sessions']);rate=number(x['conversion_rate']);value=number(x['value_per_conversion'])
        if rate>1: raise ValueError('Rate exceeds 1')
        out.append({'name':x['name'],'conversions':traffic*rate,'value':traffic*rate*value})
    return out
