def money_flow_analysis(client):
    if isinstance(client,dict) and '_error' in client:return {'status':'UNAVAILABLE'}
    return {'status':'OK','raw':client} if client else {'status':'UNAVAILABLE'}
