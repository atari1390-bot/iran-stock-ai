def validate_snapshot(s):
    checks=[]
    for k in ('closing','orderbook','client_type','history'):
        v=s.get(k); ok=isinstance(v,(dict,list)) and not (isinstance(v,dict) and '_error' in v); checks.append({'field':k,'ok':ok})
    n=sum(x['ok'] for x in checks); status='OK' if n>=3 else 'NEEDS_REVIEW'
    return {'score':round(100*n/4),'status':status,'checks':checks}
