def build_signal(snap,t,b,f,score):
    if t.get('status')!='OK':return {'status':'NEEDS_REVIEW','score':score,'decision':'داده ناکافی'}
    last=t['last']; sup=t['support20']; res=t['resistance20']; risk=max(last-sup,last*.05); stop=sup-max(risk*.25,last*.01)
    return {'status':'OK','score':score,'decision':'خرید پله‌ای' if score>=75 else ('صبر' if score>=55 else 'عدم ورود'),'entry_1':round(last,2),'entry_2':round(sup+.35*(last-sup),2),'stop':round(stop,2),'target_1':round(res,2),'target_2':round(last+2*(last-stop),2),'support':round(sup,2),'resistance':round(res,2)}
