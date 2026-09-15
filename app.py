import streamlit as st
from data.tsetmc import TSETMC
from data.validator import validate_snapshot
from analysis.technical import technical_analysis
from analysis.orderbook import orderbook_analysis
from analysis.money_flow import money_flow_analysis
from analysis.scoring import score_stock
from analysis.signal import build_signal

st.set_page_config(page_title='Iran Stock AI', page_icon='📈', layout='wide')
st.title('Iran Stock AI Agent')
st.caption('TSETMC محور | تحلیل تکنیکال، تابلو، جریان پول و اعتبارسنجی داده')
symbols = st.text_input('نمادها را با فاصله وارد کنید', 'فولاد وبملت فزر فملی وپاسار')
if st.button('تحلیل نمادها'):
    api=TSETMC(); results=[]
    for symbol in symbols.replace(',', ' ').split():
        try:
            snap=api.snapshot(symbol)
            validation=validate_snapshot(snap)
            tech=technical_analysis(snap.get('history'))
            book=orderbook_analysis(snap.get('orderbook'))
            flow=money_flow_analysis(snap.get('client_type'))
            score=score_stock(tech,book,flow,validation)
            signal=build_signal(snap,tech,book,flow,score)
            results.append({'symbol':symbol,**signal,'validation':validation})
        except Exception as e: results.append({'symbol':symbol,'status':'DATA_ERROR','error':str(e)})
    st.dataframe(results,use_container_width=True)
    for r in results:
        if r.get('status')!='DATA_ERROR':
            st.subheader(r['symbol']); a,b,c,d=st.columns(4)
            a.metric('امتیاز',r.get('score','-')); b.metric('وضعیت',r.get('decision','-')); c.metric('ورود اول',r.get('entry_1','-')); d.metric('حد ضرر',r.get('stop','-'))
            st.json(r)
