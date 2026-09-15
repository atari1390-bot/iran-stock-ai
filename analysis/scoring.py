def score_stock(t,b,f,v):
    s=50
    if v.get('status')!='OK':s-=15
    if t.get('status')=='OK':
        if t['last']>t['sma20']:s+=10
        if t.get('rsi') is not None and 45<=t['rsi']<=65:s+=10
        if t['macd']>t['macd_signal']:s+=10
        if t.get('volume_avg20',0)>0 and t['volume_last']>t['volume_avg20']:s+=5
    if b.get('status')=='OK':s+=3
    if f.get('status')=='OK':s+=2
    return max(0,min(100,s))
