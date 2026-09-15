import requests
BASE='https://cdn.tsetmc.com/api'
class TSETMC:
    def __init__(self,timeout=15): self.timeout=timeout
    def _get(self,path):
        r=requests.get(BASE+path,headers={'User-Agent':'Mozilla/5.0'},timeout=self.timeout); r.raise_for_status(); return r.json()
    def search(self,symbol):
        d=self._get(f'/Instrument/GetInstrumentSearch/{symbol}')
        return d[0] if isinstance(d,list) and d else d
    def _safe(self,path):
        try:return self._get(path)
        except Exception as e:return {'_error':str(e)}
    def snapshot(self,symbol):
        item=self.search(symbol); ins=item.get('insCode') or item.get('InsCode') if isinstance(item,dict) else None
        if not ins: raise ValueError(f'Instrument not found: {symbol}')
        return {'symbol':symbol,'inscode':ins,'search':item,'closing':self._safe(f'/ClosingPrice/GetClosingPriceInfo/{ins}'),'orderbook':self._safe(f'/BestLimits/{ins}'),'client_type':self._safe(f'/ClientType/GetClientType/{ins}/1/0'),'history':self._safe(f'/ClosingPrice/GetClosingPriceDailyList/{ins}/0')}
