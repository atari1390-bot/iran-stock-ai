import pandas as pd, numpy as np
def technical_analysis(history):
    rows=history.get('closingPriceDaily') if isinstance(history,dict) else history
    if not rows:return {'status':'INSUFFICIENT_DATA'}
    df=pd.DataFrame(rows); cc=next((c for c in df.columns if c.lower() in ('pclosing','price','close','pclosingprice')),None)
    vc=next((c for c in df.columns if 'volume' in c.lower()),None)
    if not cc:return {'status':'INSUFFICIENT_DATA'}
    df['close']=pd.to_numeric(df[cc],errors='coerce'); df['volume']=pd.to_numeric(df[vc],errors='coerce') if vc else 0; df=df.dropna(subset=['close'])
    if len(df)<20:return {'status':'INSUFFICIENT_DATA'}
    c=df.close; d=c.diff(); g=d.clip(lower=0).rolling(14).mean(); l=(-d.clip(upper=0)).rolling(14).mean(); rsi=100-100/(1+g/l.replace(0,np.nan)); e12=c.ewm(span=12,adjust=False).mean(); e26=c.ewm(span=26,adjust=False).mean(); macd=e12-e26; sig=macd.ewm(span=9,adjust=False).mean()
    o={'status':'OK','last':float(c.iloc[-1]),'rsi':float(rsi.iloc[-1]) if pd.notna(rsi.iloc[-1]) else None,'macd':float(macd.iloc[-1]),'macd_signal':float(sig.iloc[-1]),'support20':float(c.tail(20).min()),'resistance20':float(c.tail(20).max()),'sma20':float(c.rolling(20).mean().iloc[-1]),'volume_last':float(df.volume.iloc[-1]),'volume_avg20':float(df.volume.rolling(20).mean().iloc[-1])}
    for n in (50,100,200):o[f'sma{n}']=float(c.rolling(n).mean().iloc[-1]) if len(c)>=n else None
    return o
