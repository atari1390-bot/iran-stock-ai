def orderbook_analysis(book):
    if isinstance(book,dict) and '_error' in book:return {'status':'UNAVAILABLE'}
    rows=book if isinstance(book,list) else (book.get('bestLimits') if isinstance(book,dict) else None)
    return {'status':'OK','levels':rows} if rows else {'status':'UNAVAILABLE'}
